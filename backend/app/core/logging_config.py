# backend/app/core/logging_config.py
import logging
import sys
import structlog

# OpenTelemetry Imports
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
# from opentelemetry.sdk.resources import Resource
# --- ADD INSTRUMENTOR IMPORTS ---
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.instrumentation.celery import CeleryInstrumentor
# --- END INSTRUMENTOR IMPORTS ---


def configure_logging():
    """Configures standard logging, Structlog, and OpenTelemetry."""

    # OpenTelemetry Setup
    # resource = Resource(attributes={"service.name": "health-ai-backend"})
    # provider = TracerProvider(resource=resource)
    # exporter = ConsoleSpanExporter()
    # processor = BatchSpanProcessor(exporter)
    # provider.add_span_processor(processor)
    # trace.set_tracer_provider(provider)
    # print("OpenTelemetry configured with ConsoleSpanExporter.")

    # --- ENABLE INSTRUMENTATIONS ---
    # Instrument the 'requests' library
    # RequestsInstrumentor().instrument()
    # print("RequestsInstrumentor enabled.")

    # Instrument Celery
    # CeleryInstrumentor().instrument()
    # print("CeleryInstrumentor enabled.")
    # --- END ENABLE INSTRUMENTATIONS ---

    # Structlog configuration (Keep existing)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    print("Structlog configured.")


# ... (get_logger and get_tracer functions remain the same) ...
def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


# def get_tracer(name: str):
# return trace.get_tracer(name)
