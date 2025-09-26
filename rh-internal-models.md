# https://developer.models.corp.redhat.com/
## Notes:
- All endpoints are Red Hat internal deployments
- All models support OpenAI-compatible API calls
- Context limits: Granite models = 4096 tokens, Mistral = 8192 tokens
- Embedding models use `/v1/embeddings` endpoint instead of `/v1/chat/completions`
- Choose different models for analysis vs anonymization based on your performance/quality needs
## Granite 3.0 8B Instruct
```yaml
ai_analysis:
  endpoint: "https://granite-3-0-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "1afe83cf97b36b54b4176f3e9cb7c970"
  model: "ibm-granite/granite-3.0-8b-instruct"
  max_context_tokens: 4096
```
## Granite 3.1 8B Instruct
```yaml
ai_analysis:
  endpoint: "https://granite-3-1-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "38818632fa3bcbd0c04f2c0384e83d45"
  model: "ibm-granite/granite-3.1-8b-instruct"
  max_context_tokens: 4096
```
## Granite 3.2 8B Instruct (Latest)
```yaml
ai_analysis:
  endpoint: "https://granite-3-2-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "c7bd727773d70979c2cbea0853293e54"
  model: "ibm-granite/granite-3.2-8b-instruct"
  max_context_tokens: 4096
```
## Granite 8B Code Instruct (Best for Code)
```yaml
ai_analysis:
  endpoint: "https://granite-8b-code-instruct-4k--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "58220634b97fdaccccc66a65b09c9073"
  model: "ibm-granite/granite-8b-code-instruct-4k"
  max_context_tokens: 4096
```
## Mistral 7B Instruct
```yaml
ai_analysis:
  endpoint: "https://mistral-7b-instruct-v0-3--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "9866e28fb139eec85e7d2fa583964364"
  model: "mistralai/Mistral-7B-Instruct-v0.3"
  max_context_tokens: 8192
```
## Dual AI Architecture Examples
### Example 1: Granite 3.2 for Analysis + Mistral for Anonymization
```yaml
# High-quality analysis with latest Granite model
ai_analysis:
  endpoint: "https://granite-3-2-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "c7bd727773d70979c2cbea0853293e54"
  model: "ibm-granite/granite-3.2-8b-instruct"
  max_context_tokens: 4096

# Fast anonymization with Mistral
ai_anonymization:
  endpoint: "https://mistral-7b-instruct-v0-3--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "9866e28fb139eec85e7d2fa583964364"
  model: "mistralai/Mistral-7B-Instruct-v0.3"
  enabled: true
  max_context_tokens: 8192
```
### Example 2: Code-Focused Analysis + Granite 3.0 for Anonymization
```yaml
# Code analysis with specialized Granite Code model
ai_analysis:
  endpoint: "https://granite-8b-code-instruct-4k--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "58220634b97fdaccccc66a65b09c9073"
  model: "ibm-granite/granite-8b-code-instruct-4k"
  max_context_tokens: 4096

# General anonymization with Granite 3.0
ai_anonymization:
  endpoint: "https://granite-3-0-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "1afe83cf97b36b54b4176f3e9cb7c970"
  model: "ibm-granite/granite-3.0-8b-instruct"
  enabled: true
  max_context_tokens: 4096
```
### Example 3: Same Model for Both (Simplified Setup)
```yaml
# Use Granite 3.2 for both analysis and anonymization
ai_analysis:
  endpoint: "https://granite-3-2-8b-instruct--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "c7bd727773d70979c2cbea0853293e54"
  model: "ibm-granite/granite-3.2-8b-instruct"
  max_context_tokens: 4096

# Anonymization will automatically use ai_analysis config since ai_anonymization is not specified
```
### Example 4: Mistral for Both (High Context)
```yaml
# Use Mistral 7B for both (has larger context window)
ai_analysis:
  endpoint: "https://mistral-7b-instruct-v0-3--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/chat/completions"
  api_key: "9866e28fb139eec85e7d2fa583964364"
  model: "mistralai/Mistral-7B-Instruct-v0.3"
  max_context_tokens: 8192

# Anonymization will automatically use ai_analysis config
```
## Embedding Models (For Future Extensions)
### ModernBERT Embeddings
```yaml
ai_embeddings:
  endpoint: "https://modernbert-embed-base--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/embeddings"
  api_key: "32499854da5a1b911934db9260d4e1af"
  model: "nomic-ai/modernbert-embed-base"
```
### Nomic Embeddings
```yaml
ai_embeddings:
  endpoint: "https://nomic-embed-text-v1-5--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443/v1/embeddings"
  api_key: "100114b7832a56f55e61acd5c7bed7b3"
  model: "nomic-ai/nomic-embed-text-v1.5"
```