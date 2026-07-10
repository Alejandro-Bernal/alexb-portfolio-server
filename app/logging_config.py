import logging
import sys
import structlog


def setup_logging():
    """
    Configure structured logging for the application.
    """
    # These are the processors that will enrich the log records.
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # Configure the standard library logging to be structlog-aware.
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Define the formatter for our logs. We want JSON output.
    formatter = structlog.stdlib.ProcessorFormatter(
        # These processors will be applied only to the log records before formatting.
        processor=structlog.processors.JSONRenderer(),
        # These are the processors that will be applied to the log records before being passed to the formatter.
        foreign_pre_chain=shared_processors,
    )

    # Get the root handler and attach our new formatter.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO) # Set the default log level to INFO

    # Silence overly verbose logs from other libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
