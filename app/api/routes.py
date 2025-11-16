"""Endpoints for the Mail Scheduler API.

This module provides RESTful API endpoints
for scheduling emails and checking API health.
"""

import logging
from datetime import UTC, datetime, timedelta

from flask import request
from flask_restx import Namespace, Resource, fields
from pytz import timezone

from app.event.jobs import add_event

# Get logger for this module
logger = logging.getLogger(__name__)

# from app.services.event_service import EventService  # Import service layer

# Create namespace
ns = Namespace("Event", description="Email scheduling API endpoints", path="/")

"""Serializer for swagger documentation.
As example using Singapore Standart Timezone (SST).
List of recipients mail address separated by comma(s).
"""
sst = timezone("Asia/Singapore")
local_now = (datetime.now(UTC) + timedelta(minutes=1)).astimezone(sst)
mail_event = ns.model(
    "SubmitEvent",
    {
        "subject": fields.String(
            required=True, description="Mail subject", example="Email subject"
        ),
        "content": fields.String(
            required=True,
            description="Mail body content",
            example="Email body",
        ),
        "timestamp": fields.DateTime(
            required=True,
            dt_format="iso8601",
            description="Time mail to sent, format dd mm YYYY HH:MM\n\
                  Assume as server timezone when timezone not provided.",
            example=local_now.strftime("%d %b %Y %H:%M %Z"),
        ),
        "recipients": fields.String(
            required=True,
            description="Mail recipients separated by comma(s)",
            pattern=r"\w+@\w+\.\w+(,\s*\w+@\w+\.\w+)*",
            example="retphern@gmail.com, vedafarm.id@gmail.com",
        ),
    },
)

# Response model for listing events
event_model = ns.model(
    "Event",
    {
        "id": fields.Integer(description="Event ID"),
        "email_subject": fields.String(description="Email subject"),
        "email_content": fields.String(description="Email content"),
        "timestamp": fields.DateTime(description="Scheduled time for sending"),
        "created_at": fields.DateTime(description="Event creation time"),
        "is_done": fields.Boolean(description="Whether the email has been sent"),
        "done_at": fields.DateTime(
            description="Time when the email was sent", required=False
        ),
    },
)


@ns.route("/health")
class HealthCheck(Resource):
    """API health check endpoint for monitoring and status verification."""

    @ns.doc(
        description="Returns the current status of the API.",
        responses={
            200: "API is healthy and operational",
            500: "API is experiencing issues",
        },
    )
    def get(self):
        """
        Return API health status.

        This endpoint can be used by monitoring tools to verify service
        availability. Returns a simple JSON response with status and current
        timestamp.
        """
        return (
            {"status": "ok", "timestamp": datetime.now(UTC).isoformat()},
            200,
        )


@ns.route("/save_emails")
class EventApi(Resource):
    """
    Email scheduling endpoint.

    This resource allows clients to schedule emails to be sent at a specific
    time by creating an event in the system. The emails will be sent
    asynchronously using the background task queue.
    """

    @ns.expect(mail_event, validate=True)
    @ns.doc(
        description="Schedule a new email to be sent at a specific time",
        responses={
            201: "Email successfully scheduled",
            400: "Invalid request data",
            500: "Server error occurred",
        },
    )
    def post(self):
        """
        Submit a new email event for scheduling.

        Creates a new scheduled email event with the provided subject, content,
        timestamp, and recipients. The email will be sent at the specified time
        to all recipients.

        Returns:
            tuple: A tuple containing a JSON response and HTTP status code.
                  The JSON includes a success message and the ID of the created
                  event.

        Raises:
            Exception: If the event cannot be created due to validation errors
                       or database issues.
        """
        try:
            if request.json is None:
                return {"message": "No JSON data provided"}, 400
            event_id = add_event(request.json)
            return {
                "message": "Event successfully saved to scheduler",
                "id": event_id,
            }, 201
        except ValueError as e:
            # Handle validation errors (missing required fields, invalid data)
            logger.warning(f"Validation error in save_emails: {str(e)}")
            return {"message": f"Validation error: {str(e)}"}, 400
        except (KeyError, TypeError) as e:
            # Handle malformed request data
            logger.warning(f"Malformed request data: {str(e)}")
            return {"message": f"Invalid request data: {str(e)}"}, 400
        except Exception as e:
            # Log unexpected errors for investigation
            logger.error(f"Unexpected error in save_emails: {str(e)}", exc_info=True)
            return {"message": f"An unexpected error occurred: {str(e)}"}, 500


@ns.route("/events/<int:event_id>")
class EventDetailApi(Resource):
    """
    Event detail endpoint.

    This resource allows clients to retrieve, update,
    or delete a specific scheduled email event by its ID.
    """

    @ns.doc(
        description="Get details of a specific scheduled email",
        params={"event_id": "The ID of the event to retrieve"},
        responses={
            200: "Event details retrieved successfully",
            404: "Event not found",
            500: "Server error occurred",
        },
    )
    @ns.marshal_with(event_model)
    def get(self, event_id):
        """
        Retrieve a specific email event by ID.

        Returns detailed information about the requested email event,
        including subject, content, scheduled time, and status.

        Args:
            event_id (int): The ID of the event to retrieve

        Returns:
            dict: The event details if found

        Raises:
            404: If the event with the specified ID does not exist
        """
        try:
            # Use our service layer to get the specific event
            from app.services.event_service import EventService

            event = EventService.get_by_id(event_id)

            if not event:
                ns.abort(404, f"Event with ID {event_id} not found")

            return event, 200
        except ValueError as e:
            # Handle invalid event ID or data validation errors
            logger.warning(f"Invalid event ID {event_id}: {str(e)}")
            ns.abort(400, f"Invalid request: {str(e)}")
        except Exception as e:
            # Log unexpected database or system errors
            logger.error(
                f"Unexpected error retrieving event {event_id}: {str(e)}", exc_info=True
            )
            ns.abort(500, "An unexpected error occurred while retrieving the event")
