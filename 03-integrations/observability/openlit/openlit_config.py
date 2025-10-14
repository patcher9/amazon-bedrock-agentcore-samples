import os
import openlit


def read_secret(secret: str):
    """Read secret from file system or environment variable."""
    try:
        with open(f"/etc/secrets/{secret}", "r") as f:
            return f.read().rstrip()
    except Exception as e:
        print("No token was provided as secret, checking environment variable")
        return os.environ.get("OPENLIT_API_KEY", "")


def init():
    """Initialize OpenLIT instrumentation for AgentCore."""

    # Read OpenLIT API key from secrets or environment
    api_key = read_secret("openlit_api_key")

    # Get OTEL endpoint (defaults to OpenLIT Cloud)
    otel_endpoint = os.environ.get(
        "OTEL_ENDPOINT",
        "http://localhost:4318",  # Default to local OpenLIT instance
    )

    # Determine if using OpenLIT Cloud or self-hosted
    use_cloud = "cloud.openlit.io" in otel_endpoint or os.environ.get("OPENLIT_USE_CLOUD", "false").lower() == "true"

    # Initialize OpenLIT SDK
    # OpenLIT provides automatic instrumentation for popular LLM frameworks
    if use_cloud and api_key:
        # For OpenLIT Cloud
        openlit.init(
            otlp_endpoint=otel_endpoint,
            otlp_headers={"Authorization": f"Bearer {api_key}"},
            application_name=os.environ.get("OPENLIT_APP_NAME", "bedrock-agentcore-agent"),
            environment=os.environ.get("OPENLIT_ENVIRONMENT", "production"),
        )
        print(f"OpenLIT initialized with Cloud endpoint: {otel_endpoint}")
    else:
        # For self-hosted OpenLIT
        openlit.init(
            otlp_endpoint=otel_endpoint,
            application_name=os.environ.get("OPENLIT_APP_NAME", "bedrock-agentcore-agent"),
            environment=os.environ.get("OPENLIT_ENVIRONMENT", "production"),
            disable_batch=False,
        )
        print(f"OpenLIT initialized with self-hosted endpoint: {otel_endpoint}")
