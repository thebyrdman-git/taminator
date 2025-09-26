# Fabric Configuration for LiteLLM Red Hat Models

Your LiteLLM proxy is now configured with master key authentication for Fabric integration.

## 🔑 **Master Key for Fabric**

```bash
export OPENAI_API_KEY="***REMOVED***"
export OPENAI_BASE_URL="http://localhost:4000/v1"
```

## 🎨 **Fabric Configuration**

### Option 1: Environment Variables (Recommended)
Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# LiteLLM Red Hat Models for Fabric
export OPENAI_API_KEY="***REMOVED***"
export OPENAI_BASE_URL="http://localhost:4000/v1"
export OPENAI_DEFAULT_MODEL="granite-3.2-8b-instruct"
```

Then reload your shell:
```bash
source ~/.bashrc
```

### Option 2: Fabric Config File
Create or update `~/.config/fabric/.env`:

```bash
# Red Hat LiteLLM Configuration
OPENAI_API_KEY=***REMOVED***
OPENAI_BASE_URL=http://localhost:4000/v1
DEFAULT_MODEL=granite-3.2-8b-instruct
```

### Option 3: Direct Command Line
Use Fabric with explicit configuration:

```bash
fabric --model granite-3.2-8b-instruct --base-url http://localhost:4000/v1 --api-key ***REMOVED***
```

## 🤖 **Available Models for Fabric**

| Model Name | Best For | Context Limit |
|------------|----------|---------------|
| `granite-3.2-8b-instruct` | General tasks (Default) | 4096 tokens |
| `granite-8b-code-instruct` | Code analysis & generation | 4096 tokens |
| `mistral-7b-instruct` | Larger context tasks | 8192 tokens |
| `granite-3.1-8b-instruct` | Alternative general model | 4096 tokens |
| `granite-3.0-8b-instruct` | Alternative general model | 4096 tokens |

## 🧪 **Test Fabric Integration**

### Basic Test
```bash
echo "Hello, this is a test" | fabric --pattern summarize
```

### Code Analysis Test
```bash
cat some_code.py | fabric --pattern analyze_code --model granite-8b-code-instruct
```

### Larger Context Test
```bash
cat large_document.txt | fabric --pattern extract_insights --model mistral-7b-instruct
```

## 🔧 **Fabric Pattern Examples**

### Using Default Model (Granite 3.2)
```bash
# Basic patterns
echo "Complex technical document..." | fabric --pattern summarize
echo "Business requirements..." | fabric --pattern analyze_claims
echo "Meeting notes..." | fabric --pattern extract_actions

# Creative patterns  
echo "Blog post idea..." | fabric --pattern write_essay
echo "Product description..." | fabric --pattern improve_writing
```

### Using Code-Specialized Model
```bash
# Code patterns
cat app.py | fabric --pattern analyze_code --model granite-8b-code-instruct
cat bugs.log | fabric --pattern find_root_cause --model granite-8b-code-instruct
cat requirements.txt | fabric --pattern create_security_update --model granite-8b-code-instruct
```

### Using High-Context Model
```bash
# Large document analysis
cat report.pdf | fabric --pattern extract_insights --model mistral-7b-instruct
cat meeting_transcript.txt | fabric --pattern summarize --model mistral-7b-instruct
```

## 🔒 **Authentication Details**

- **Master Key**: `***REMOVED***`
- **API Base**: `http://localhost:4000/v1`
- **Auth Type**: Bearer token (OpenAI compatible)
- **Required**: Yes (API key must be provided)

## 📊 **Usage Examples**

### With pai-fabric-compliant
If you have the PAI fabric wrapper:
```bash
# It should automatically use the local LiteLLM proxy
echo "Document content..." | pai-fabric-compliant --pattern analyze
```

### Direct OpenAI SDK (Python)
```python
import openai

client = openai.OpenAI(
    api_key="***REMOVED***",
    base_url="http://localhost:4000/v1"
)

response = client.chat.completions.create(
    model="granite-3.2-8b-instruct",
    messages=[{"role": "user", "content": "Analyze this text..."}]
)
```

### cURL Examples
```bash
# Chat completion
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer ***REMOVED***" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "granite-3.2-8b-instruct",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 150
  }'

# List models
curl -H "Authorization: Bearer ***REMOVED***" \
  http://localhost:4000/v1/models
```

## 🚨 **Troubleshooting**

### Fabric Can't Connect
```bash
# Check if LiteLLM is running
pai-litellm-service status

# Test authentication manually
curl -H "Authorization: Bearer ***REMOVED***" \
  http://localhost:4000/v1/models
```

### "No Healthy Deployments" Error
This indicates the LiteLLM proxy can't reach Red Hat internal endpoints:
- Ensure you're connected to Red Hat VPN
- Check network connectivity to internal domains
- Verify API keys are current

### Environment Variables Not Working
```bash
# Check current environment
env | grep OPENAI

# Reload shell configuration
source ~/.bashrc

# Test with explicit parameters
fabric --api-key ***REMOVED*** --base-url http://localhost:4000/v1
```

## 🎯 **Best Practices**

1. **Model Selection**:
   - Use `granite-3.2-8b-instruct` for most tasks
   - Use `granite-8b-code-instruct` for code analysis
   - Use `mistral-7b-instruct` for large documents

2. **Performance**:
   - LiteLLM proxy runs locally (fast)
   - All models are Red Hat internal (compliant)
   - Auto-starts at login (always available)

3. **Security**:
   - Master key is local-only
   - No external API calls
   - Full Red Hat compliance

---

*✅ Authentication Configured Successfully*  
*🔑 Master Key: `***REMOVED***`*  
*🌐 API Base: `http://localhost:4000/v1`*  

*Ready for Fabric integration!*
