# LiteLLM Setup for Red Hat Internal Models

This document describes the LiteLLM setup for accessing Red Hat internal AI models through a unified OpenAI-compatible API interface.

## 🚀 Quick Start

### 1. Start the Proxy Server
```bash
# Start LiteLLM proxy on default port 4000
pai-litellm-proxy

# Or specify custom port
pai-litellm-proxy 8080
```

### 2. Test the Setup
```bash
# Run comprehensive tests
pai-litellm-test

# Or test with custom proxy URL
pai-litellm-test http://localhost:8080
```

### 3. Use in Your Applications
```bash
# Run example Python script
python pai-litellm-example.py

# Or with custom proxy URL
python pai-litellm-example.py http://localhost:8080
```

## 📋 Available Models

### Chat Completion Models

| Model Name | Description | Context Limit | Best For |
|------------|-------------|---------------|----------|
| `granite-3.2-8b-instruct` | Latest Granite model (Recommended) | 4096 tokens | General purpose tasks |
| `granite-3.1-8b-instruct` | Granite 3.1 | 4096 tokens | General purpose tasks |
| `granite-3.0-8b-instruct` | Granite 3.0 | 4096 tokens | General purpose tasks |
| `granite-8b-code-instruct` | Code-specialized Granite | 4096 tokens | Code generation & analysis |
| `mistral-7b-instruct` | Mistral 7B | 8192 tokens | Tasks requiring larger context |

### Embedding Models

| Model Name | Description | Use Case |
|------------|-------------|----------|
| `modernbert-embed-base` | ModernBERT embeddings | Document similarity, search |
| `nomic-embed-text` | Nomic text embeddings | Text analysis, clustering |

## 🔧 Configuration

The configuration is stored in `~/.config/litellm/config.yaml`. Key sections:

### Model Definitions
```yaml
model_list:
  - model_name: granite-3.2-8b-instruct
    litellm_params:
      model: ibm-granite/granite-3.2-8b-instruct
      api_base: https://granite-3-2-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1
      api_key: c7bd727773d70979c2cbea0853293e54
      max_tokens: 4096
```

### General Settings
```yaml
general_settings:
  completion_model: granite-3.2-8b-instruct  # Default model
  embedding_model: modernbert-embed-base     # Default embedding model
```

## 🌐 API Usage

### OpenAI-Compatible Endpoints

#### Chat Completions
```bash
curl -X POST "http://localhost:4000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-key" \
  -d '{
    "model": "granite-3.2-8b-instruct",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 150
  }'
```

#### Embeddings
```bash
curl -X POST "http://localhost:4000/v1/embeddings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-key" \
  -d '{
    "model": "modernbert-embed-base",
    "input": "This is a test sentence."
  }'
```

#### List Models
```bash
curl "http://localhost:4000/v1/models" \
  -H "Authorization: Bearer test-key"
```

### Python Usage

```python
import requests

# Chat completion
response = requests.post(
    "http://localhost:4000/v1/chat/completions",
    headers={"Authorization": "Bearer test-key"},
    json={
        "model": "granite-3.2-8b-instruct",
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 150
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Using OpenAI Python Library

```python
from openai import OpenAI

# Configure client to use local proxy
client = OpenAI(
    api_key="test-key",  # Can be any string
    base_url="http://localhost:4000/v1"
)

# Chat completion
response = client.chat.completions.create(
    model="granite-3.2-8b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=150
)

print(response.choices[0].message.content)

# Embeddings
embedding = client.embeddings.create(
    model="modernbert-embed-base",
    input="This is a test sentence."
)

print(embedding.data[0].embedding[:5])  # First 5 dimensions
```

## 🛠️ PAI Integration Scripts

| Script | Purpose |
|--------|---------|
| `pai-litellm-proxy` | Start LiteLLM proxy server with full logging |
| `pai-litellm-test` | Comprehensive testing of all models |
| `pai-litellm-start` | Quick start proxy for testing |
| `pai-litellm-example.py` | Python example demonstrating usage |

## 🔒 Security & Compliance

- All models are Red Hat internal deployments
- API keys are pre-configured for Red Hat internal access
- No external API calls - everything stays within Red Hat infrastructure
- Compliant with Red Hat AI policy requirements

## 🚨 Troubleshooting

### Proxy Won't Start
```bash
# Check if port is in use
sudo netstat -tlnp | grep :4000

# Kill existing process if needed
pkill -f litellm

# Check configuration syntax
python -c "import yaml; yaml.safe_load(open('~/.config/litellm/config.yaml'))"
```

### Models Not Responding
- Verify Red Hat VPN connection
- Check network access to internal endpoints
- Confirm API keys are valid and current

### Dependencies Missing
```bash
# Reinstall with proxy dependencies
pip install --upgrade 'litellm[proxy]'
```

## 📚 Additional Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Red Hat AI Models Portal](https://developer.models.corp.redhat.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference) (for interface compatibility)

## 🎯 Model Selection Guidelines

### For General Tasks
- **Primary**: `granite-3.2-8b-instruct` (latest and most capable)
- **Fallback**: `granite-3.1-8b-instruct`

### For Code Generation
- **Primary**: `granite-8b-code-instruct` (specialized for code)
- **Fallback**: `granite-3.2-8b-instruct`

### For Large Context Tasks
- **Primary**: `mistral-7b-instruct` (8192 token context)

### For Embeddings
- **Primary**: `modernbert-embed-base`
- **Alternative**: `nomic-embed-text`

---

*Part of the PAI (Personal AI Infrastructure) System*  
*For Red Hat Internal Use - Compliant with AI Policy Requirements*
