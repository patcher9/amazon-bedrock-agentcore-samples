# Amazon Bedrock Agent Integration with OpenLIT

This example contains a demo of a Personal Assistant Agent built on top of [Bedrock AgentCore Agents](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) with OpenLIT observability.


## Prerequisites

- Python 3.11 or higher
- self-hosted OpenLIT
- AWS Account with appropriate permissions
- Access to the following AWS services:
   - Amazon Bedrock


## OpenLIT Instrumentation

> [!TIP]
> For detailed setup instructions, configuration options, and advanced use cases, please refer to the [OpenLIT Documentation](https://docs.openlit.io/latest/openlit/quickstart-ai-observability).

Bedrock AgentCore comes with [Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) support out-of-the-box.
Hence, we just need to register an [OpenTelemetry SDK](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/overview.md#sdk) for complete LLM and Agent Observability with OpenLIT.

We simplified this process, hiding all the complexity inside [openlit_config.py](./openlit_config.py). 
For sending data to OpenLIT, you can configure the OTEL_ENDPOINT env var with your OpenLIT URL for ingesting OTLP, for example: http://127.0.0.1:4318.

### Configuration Options

Configure the `OTEL_ENDPOINT` environment variable with your OpenLIT OTLP endpoint. **No authentication or OTLP headers are required** as OpenLIT is an open-source self-hosted solution:

```bash
export OTEL_ENDPOINT=http://your-openlit-host:4318
```


## How to use

### Setting your AWS keys

Follow the [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html) to configure your AWS Role with the correct policies.
Afterwards, you can set your AWS keys in your environment variables by running the following command in your terminal:

```bash
export AWS_ACCESS_KEY_ID=your_api_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=your_region
```

Ensure your account has access to the model `us.anthropic.claude-3-7-sonnet-20250219-v1:0` used in this example. Please refer to the
[Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-permissions.html) to see how to enable access to the model.
You can change the model used by configuring the environment variable `BEDROCK_MODEL_ID`.

### Setting up OpenLIT

1. Follow the [OpenLIT installation guide](https://docs.openlit.io/latest/openlit/installation) to deploy OpenLIT
2. Once deployed, note your OpenLIT OTLP endpoint (typically `http://your-host:4318`)
3. Set the environment variable:

```bash
export OTEL_ENDPOINT=http://your-openlit-host:4318
```

> **Note**: OpenLIT is an open-source self-hosted solution and requires no authentication or API keys by default to send telemetry but can be configured. Only the OTLP endpoint is needed.

### Optional Configuration

You can customize the application name and environment:

```bash
export SERVICE_NAME=bedrock-agentcore-agent
export DEPLOYMENT_ENVIRONMENT=production
```

### Run the app

You can start the example with the following command:

```bash
uv run main.py
```

This will create an HTTP server that listens on port `8080` that implements the required `/invocations` endpoint for processing the agent's requirements.

The Agent is now ready to be deployed. The best practice is to package code as a container and push to ECR using CI/CD pipelines and IaC.
You can follow the guide
[here](https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/01-tutorials/01-AgentCore-runtime/01-hosting-agent/01-strands-with-bedrock-model/runtime_with_strands_and_bedrock_models.ipynb)
to have a full step-by-step tutorial.

You can interact with your agent with the following command:

```bash
curl -X POST http://127.0.0.1:8080/invocations --data '{"prompt": "What is the weather now?"}'
```

![Dashboard](./openlit-dashboard.jpg)

![Tracing](./openlit-traces.png)
