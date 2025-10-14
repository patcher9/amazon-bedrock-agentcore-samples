# Amazon Bedrock Agent Integration with OpenLIT

This example contains a demo of a Personal Assistant Agent built on top of [Bedrock AgentCore Agents](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) with OpenLIT observability.


## Prerequisites

- Python 3.11 or higher
- OpenLIT (Cloud or Self-hosted)
- AWS Account with appropriate permissions
- Access to the following AWS services:
   - Amazon Bedrock


## OpenLIT Instrumentation

> [!TIP]
> For detailed setup instructions, configuration options, and advanced use cases, please refer to the [OpenLIT Documentation](https://docs.openlit.io/).

Bedrock AgentCore comes with [Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) support out-of-the-box.
Hence, we just need to initialize the [OpenLIT SDK](https://github.com/openlit/openlit) to send the data to OpenLIT for comprehensive LLM observability.

We simplified this process, hiding all the complexity inside [openlit_config.py](./openlit_config.py).

### Configuration Options

#### Self-hosted OpenLIT

For self-hosted OpenLIT instances, configure the `OTEL_ENDPOINT` environment variable with your OpenLIT OTLP endpoint:

```bash
export OTEL_ENDPOINT=http://your-openlit-host:4318
```

#### OpenLIT Cloud

For OpenLIT Cloud, you need to configure both the endpoint and API key:

```bash
export OTEL_ENDPOINT=https://otlp.openlit.io
export OPENLIT_API_KEY=your_api_key
export OPENLIT_USE_CLOUD=true
```

The API key can also be read from the filesystem under `/etc/secrets/openlit_api_key` for secure deployments.


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

#### Option 1: Self-hosted OpenLIT

1. Follow the [OpenLIT self-hosting guide](https://docs.openlit.io/latest/installation) to deploy OpenLIT
2. Once deployed, note your OpenLIT OTLP endpoint (typically `http://your-host:4318`)
3. Set the environment variable:

```bash
export OTEL_ENDPOINT=http://your-openlit-host:4318
```

#### Option 2: OpenLIT Cloud

1. Sign up for [OpenLIT Cloud](https://cloud.openlit.io)
2. Create a new project and obtain your API key
3. Set the environment variables:

```bash
export OPENLIT_API_KEY=your_api_key
export OTEL_ENDPOINT=https://otlp.openlit.io
export OPENLIT_USE_CLOUD=true
```

### Optional Configuration

You can customize the application name and environment:

```bash
export OPENLIT_APP_NAME=my-bedrock-agent
export OPENLIT_ENVIRONMENT=production
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

## Viewing Traces in OpenLIT

Once your agent is running and processing requests, you can view the observability data:

### Self-hosted OpenLIT
1. Navigate to your OpenLIT dashboard at `http://your-openlit-host:3000`
2. Click on "Traces" or "Metrics" to view telemetry data
3. Filter by application name (default: `bedrock-agentcore-agent`)

### OpenLIT Cloud
1. Go to https://cloud.openlit.io
2. Select your project
3. Navigate to the "Traces" section

### What You'll See

OpenLIT provides comprehensive observability including:
- **Request Traces**: Full trace of agent invocations from request to response
- **LLM Metrics**: Token usage, latency, and cost tracking for Bedrock model calls
- **Tool Calls**: Detailed traces of tool executions (calculator, weather, etc.)
- **Error Tracking**: Automatic capture of errors and exceptions
- **Performance Analytics**: Request rates, p50/p95/p99 latencies, and throughput
- **Cost Analysis**: Real-time cost tracking and optimization recommendations

Now you have full observability of your Bedrock AgentCore Agents in OpenLIT!

## Architecture

```
┌─────────────────┐
│   Your Agent    │
│  (Strands SDK)  │
└────────┬────────┘
         │
         │ OpenTelemetry
         │ (via OpenLIT SDK)
         │
         ▼
┌─────────────────┐
│    OpenLIT      │
│  (Cloud/Self)   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
│ (Visualization) │
└─────────────────┘
```

## Features

- **Zero-code instrumentation**: OpenLIT automatically instruments Bedrock and LLM calls
- **Flexible deployment**: Works with both self-hosted and cloud deployments
- **Comprehensive metrics**: Tracks tokens, costs, latency, and errors
- **Open standards**: Built on OpenTelemetry for vendor neutrality
- **Real-time monitoring**: Live dashboards and alerting capabilities

## Troubleshooting

### Connection Issues

If you're having trouble connecting to OpenLIT:

1. Verify your OTEL endpoint is correct and accessible
2. Check that OpenLIT is running (for self-hosted deployments)
3. Ensure your API key is valid (for cloud deployments)
4. Check firewall rules and network connectivity

### No Data Appearing

If traces aren't showing up:

1. Verify the OpenLIT SDK is initialized before importing the agent
2. Check the console output for initialization messages
3. Ensure environment variables are set correctly
4. Verify your application name matches in the dashboard

## Additional Resources

- [OpenLIT Documentation](https://docs.openlit.io/)
- [OpenLIT GitHub](https://github.com/openlit/openlit)
- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Strands Agents Documentation](https://strandsagents.com/)
