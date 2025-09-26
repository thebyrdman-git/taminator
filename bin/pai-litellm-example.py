#!/usr/bin/env python3

"""
pai-litellm-example.py - Example usage of Red Hat internal models via LiteLLM
Part of the PAI (Personal AI Infrastructure) System

This script demonstrates how to use the Red Hat internal models through
the LiteLLM proxy server for both chat completions and embeddings.

Usage:
    python pai-litellm-example.py [proxy_url]
    
Examples:
    python pai-litellm-example.py
    python pai-litellm-example.py http://localhost:4000
"""

import requests
import json
import sys
from typing import List, Dict, Any, Optional

class RedHatLiteLLMClient:
    """Client for interacting with Red Hat models via LiteLLM proxy."""
    
    def __init__(self, base_url: str = "http://localhost:4000"):
        """Initialize the client with proxy URL."""
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-key"  # LiteLLM doesn't validate this for our setup
        }
    
    def test_connection(self) -> bool:
        """Test if the LiteLLM proxy is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_models(self) -> List[Dict[str, Any]]:
        """Get list of available models."""
        try:
            response = requests.get(f"{self.base_url}/v1/models", headers=self.headers)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error getting models: {e}")
            return []
    
    def chat_completion(
        self, 
        model: str, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """Send a chat completion request."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Error with chat completion for {model}: {e}")
            return None
    
    def get_embedding(self, model: str, text: str) -> Optional[List[float]]:
        """Get embedding for text."""
        payload = {
            "model": model,
            "input": text
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/embeddings",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["data"][0]["embedding"]
            
        except Exception as e:
            print(f"Error getting embedding for {model}: {e}")
            return None

def main():
    """Main function to demonstrate Red Hat model usage."""
    
    # Get proxy URL from command line or use default
    proxy_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4000"
    
    print("🎭 Red Hat LiteLLM Example")
    print("=" * 50)
    print(f"Proxy URL: {proxy_url}")
    print()
    
    # Initialize client
    client = RedHatLiteLLMClient(proxy_url)
    
    # Test connection
    if not client.test_connection():
        print("❌ Cannot connect to LiteLLM proxy")
        print("Start the proxy with: pai-litellm-proxy")
        sys.exit(1)
    
    print("✅ Connected to LiteLLM proxy")
    
    # Get available models
    models = client.get_models()
    if not models:
        print("❌ No models available")
        sys.exit(1)
    
    print(f"📋 Available models: {len(models)}")
    for model in models:
        print(f"  - {model.get('id', 'unknown')}")
    print()
    
    # Test chat completion models
    chat_models = [
        "granite-3.2-8b-instruct",
        "granite-8b-code-instruct", 
        "mistral-7b-instruct"
    ]
    
    test_messages = [
        {"role": "user", "content": "Hello! Please write a brief haiku about artificial intelligence."}
    ]
    
    print("💬 Testing Chat Completion Models")
    print("-" * 40)
    
    for model in chat_models:
        print(f"\n🤖 Testing {model}:")
        
        response = client.chat_completion(model, test_messages, temperature=0.8, max_tokens=100)
        
        if response:
            print(f"✅ Response: {response.strip()}")
        else:
            print(f"❌ Failed to get response from {model}")
    
    # Test embedding models
    embedding_models = [
        "modernbert-embed-base",
        "nomic-embed-text"
    ]
    
    test_text = "Red Hat Enterprise Linux is a powerful operating system for enterprise environments."
    
    print("\n\n🔢 Testing Embedding Models")
    print("-" * 40)
    
    for model in embedding_models:
        print(f"\n📊 Testing {model}:")
        
        embedding = client.get_embedding(model, test_text)
        
        if embedding:
            print(f"✅ Generated embedding with {len(embedding)} dimensions")
            print(f"   First 5 values: {embedding[:5]}")
        else:
            print(f"❌ Failed to get embedding from {model}")
    
    # Code-specific test for Granite Code model
    print("\n\n💻 Testing Code Generation (Granite Code)")
    print("-" * 40)
    
    code_messages = [
        {"role": "user", "content": "Write a Python function to calculate the factorial of a number using recursion."}
    ]
    
    code_response = client.chat_completion(
        "granite-8b-code-instruct", 
        code_messages, 
        temperature=0.2,  # Lower temperature for code
        max_tokens=300
    )
    
    if code_response:
        print("✅ Code generation response:")
        print(code_response)
    else:
        print("❌ Failed to generate code")
    
    print("\n🎉 Example completed!")
    print("You can now use these models in your applications.")

if __name__ == "__main__":
    main()
