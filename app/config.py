import os
import sys


class ConfigurationError(Exception):
    """Raised when required configuration is missing."""

    pass


def get_required_env(var_name: str, config_name: str = "Config") -> str:
    """
    Get required environment variable or raise ConfigurationError.

    Args:
        var_name: Name of the environment variable
        config_name: Name of the configuration class (for error messages)

    Returns:
        str: Value of the environment variable

    Raises:
        ConfigurationError: If environment variable is not set
    """
    value = os.environ.get(var_name)
    if not value:
        raise ConfigurationError(
            f"{config_name} requires {var_name} environment variable to be set. "
            f"Please add {var_name} to your .env file or environment."
        )
    return value


class Config(object):
    """Default configuration options."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    BCRYPT_LOG_ROUNDS = 15

    # SECRET_KEY must be set via environment variable
    # This is critical for session security and CSRF protection
    _secret_key = os.environ.get("SECRET_KEY")
    if not _secret_key:
        # Allow insecure default only in development/testing
        # Production will override and validate
        SECRET_KEY = "INSECURE-DEV-KEY-CHANGE-THIS"
        print(
            "WARNING: Using insecure default SECRET_KEY. "
            "Set SECRET_KEY environment variable for production!",
            file=sys.stderr,
        )
    else:
        SECRET_KEY = _secret_key

    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_USER = os.environ.get("DB_ENV_USER", "postgres")
    POSTGRES_PASS = os.environ.get("DB_ENV_PASS", "postgres")
    POSTGRES_DB = "postgres"

    # Use SQLite for local development when PostgreSQL is not available
    use_sqlite = os.environ.get(
        "USE_SQLITE", ""
    ).lower() == "true" or not os.path.exists("/var/run/postgresql")
    if use_sqlite:
        SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    else:
        uri = (
            f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@"
            f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )
        SQLALCHEMY_DATABASE_URI = uri

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Mail credentials - insecure defaults only for development
    # Production must set these via environment variables
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or "dev-mail-username"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or "dev-mail-password"
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or "dev@example.com"

    if not os.environ.get("MAIL_USERNAME"):
        print(
            "WARNING: MAIL_USERNAME not set. Email sending will fail in production!",
            file=sys.stderr,
        )
    if not os.environ.get("MAIL_PASSWORD"):
        print(
            "WARNING: MAIL_PASSWORD not set. Email sending will fail in production!",
            file=sys.stderr,
        )

    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    RQ_REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    RQ_ASYNC = True
    RQ_SCHEDULER_INTERVAL = 10


class ProductionConfig(Config):
    """Production configuration options."""

    DEBUG = False

    # Production MUST have all critical environment variables set
    # Fail fast if any are missing
    def __init__(self):
        """Validate required environment variables for production."""
        super().__init__()

        # Validate critical secrets
        self.SECRET_KEY = get_required_env("SECRET_KEY", "ProductionConfig")
        self.MAIL_USERNAME = get_required_env("MAIL_USERNAME", "ProductionConfig")
        self.MAIL_PASSWORD = get_required_env("MAIL_PASSWORD", "ProductionConfig")
        self.MAIL_DEFAULT_SENDER = get_required_env(
            "MAIL_DEFAULT_SENDER", "ProductionConfig"
        )

    @classmethod
    def validate(cls) -> None:
        """
        Validate production configuration.

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        required_vars = [
            "SECRET_KEY",
            "MAIL_USERNAME",
            "MAIL_PASSWORD",
            "MAIL_DEFAULT_SENDER",
        ]

        missing = []
        for var in required_vars:
            if not os.environ.get(var):
                missing.append(var)

        if missing:
            missing_vars = ", ".join(missing)
            raise ConfigurationError(
                f"ProductionConfig missing required environment variables: "
                f"{missing_vars}. Please set these in your .env file or "
                f"environment before deploying to production."
            )


class StagingConfig(Config):
    """Staging configuration options."""

    DEVELOPMENT = True
    DEBUG = True

    @classmethod
    def validate(cls) -> None:
        """
        Validate staging configuration.

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        # Staging should also validate critical variables
        required_vars = ["SECRET_KEY", "MAIL_USERNAME", "MAIL_PASSWORD"]

        missing = []
        for var in required_vars:
            if not os.environ.get(var):
                missing.append(var)

        if missing:
            print(
                f"WARNING: StagingConfig missing: {', '.join(missing)}. "
                f"Some features may not work correctly.",
                file=sys.stderr,
            )


class DevelopmentConfig(Config):
    """Development configuration options."""

    DEVELOPMENT = True
    DEBUG = True
    # Keep CSRF enabled even in development for consistency
    # Tests can disable it via TestingConfig
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    RQ_SCHEDULER_INTERVAL = 1

    @classmethod
    def validate(cls) -> None:
        """Validate development configuration - only warnings, no failures."""
        if not os.environ.get("SECRET_KEY"):
            print(
                "INFO: Using default SECRET_KEY for development. "
                "This is OK for local development but NEVER for production.",
                file=sys.stderr,
            )


class TestingConfig(Config):
    """TESTING configuration options."""

    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False  # Disable for easier testing
    CSRF_ENABLED = False  # Disable for easier testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RQ_ASYNC = False

    # Override with test-specific values
    SECRET_KEY = "test-secret-key-for-testing-only"
    MAIL_USERNAME = "test@example.com"
    MAIL_PASSWORD = "test-password"
    MAIL_DEFAULT_SENDER = "test@example.com"

    @classmethod
    def validate(cls) -> None:
        """Testing config doesn't need validation."""
        pass
