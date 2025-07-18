# TufaTooling

A Python toolkit for AI model inference and benchmarking.

## Features

- OpenRouter API integration for inference with various AI models
- Support for both chat and completion formats
- Streaming responses
- Flexible parameter configuration
- Clean, Pythonic API

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/TufaTooling.git
cd TufaTooling

# Install the package
pip install -e .

# For development dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Example

```python
from tooling.utils.inference.inference import generate

# Set your API key as an environment variable
# export OPENROUTER_API_KEY='your_api_key_here'

# Simple generation with a string prompt
response = generate(
    prompt="Explain quantum computing in simple terms.",
    model="anthropic/claude-3-sonnet-20240229",
    max_tokens=500,
    temperature=0.7
)

if 'choices' in response and len(response['choices']) > 0:
    print(response['choices'][0]['message']['content'])
```

### Chat Format

```python
from tooling.utils.inference.inference import OpenRouter

client = OpenRouter()

chat_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are three ways to improve code quality?"}
]

response = client.generate(
    prompt=chat_messages,
    model="openai/gpt-4-turbo",
    max_tokens=800,
    temperature=0.8
)

if 'choices' in response and len(response['choices']) > 0:
    print(response['choices'][0]['message']['content'])
```

### Streaming Responses

```python
from tooling.utils.inference.inference import OpenRouter

client = OpenRouter()

stream_response = client.generate(
    prompt="Write a short poem about programming.",
    model="anthropic/claude-3-haiku-20240307",
    max_tokens=200,
    temperature=0.9,
    stream=True
)

# Process the streaming response
for chunk in client.stream_tokens(stream_response):
    print(chunk, end='', flush=True)
```

### Using the Model Class

```python
from tooling.utils.models.model import Model

# Create a reusable model with fixed configuration
model = Model(
    model="anthropic/claude-3-haiku-20240307",
    max_tokens=300,
    temperature=0.8
)

# Generate text with the model
response = model.generate(
    prompt="Explain the concept of functional programming."
)

if 'choices' in response and len(response['choices']) > 0:
    print(response['choices'][0]['message']['content'])
```

## Available Models

OpenRouter supports a wide range of models from different providers, including:

- OpenAI (gpt-3.5-turbo, gpt-4-turbo, etc.)
- Anthropic (claude-3-opus, claude-3-sonnet, claude-3-haiku, etc.)
- Meta (llama-3, etc.)
- Mistral (mistral-small, mistral-medium, etc.)
- And many others

For a complete and up-to-date list of supported models, please refer to the [OpenRouter documentation](https://openrouter.ai/docs).

## Configuration

The `generate` function and `OpenRouter` class support the following parameters:

| Parameter | Description | Default |
| --- | --- | --- |
| `prompt` | Text prompt or list of chat messages | (Required) |
| `model` | Model identifier to use | "anthropic/claude-3-opus-20240229" |
| `api_key` | OpenRouter API key | From environment variable |
| `max_tokens` | Maximum number of tokens to generate | 1024 |
| `temperature` | Sampling temperature (0.0 to 1.0) | 0.7 |
| `top_p` | Nucleus sampling parameter | 0.95 |
| `top_k` | Top-k sampling parameter | None |
| `stream` | Whether to stream the response | False |

Additional parameters can be passed as keyword arguments.

## License

MIT
# TufaTooling
