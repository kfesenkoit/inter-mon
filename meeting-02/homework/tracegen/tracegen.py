import os
import random
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode


def build_tracer():
    endpoint = os.getenv("OTLP_ENDPOINT", "alloy:4317")
    service_name = os.getenv("OTEL_SERVICE_NAME", "checkout-simulator")

    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": service_name,
                "service.version": "1.0.0",
                "deployment.environment": "homework",
            }
        )
    )
    exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)


def main():
    tracer = build_tracer()

    while True:
        is_error = random.random() < 0.2
        route = "/checkout" if random.random() < 0.7 else "/cart"
        status_code = 500 if is_error else 200

        with tracer.start_as_current_span("HTTP " + route) as span:
            span.set_attribute("http.method", "GET")
            span.set_attribute("http.route", route)
            span.set_attribute("http.status_code", status_code)
            span.set_attribute("span.kind", "server")

            if is_error:
                span.set_status(Status(StatusCode.ERROR, "simulated failure"))
            else:
                span.set_status(Status(StatusCode.OK))

            # Variable latency for RED duration signals.
            time.sleep(random.uniform(0.03, 0.4))

        time.sleep(0.1)


if __name__ == "__main__":
    main()
