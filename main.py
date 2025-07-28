#!/usr/bin/env python3
"""
Shakespeare Transformer CLI Tool

A command-line tool that transforms modern English sentences into Shakespearean English
using the Ollama API.
"""

import argparse
import json
import os
import sys
import requests
from typing import Optional, Dict, Any


class ShakespeareTransformer:
    """Main class for handling Shakespeare text transformation."""
    
    def __init__(self, ollama_host: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the transformer with Ollama API configuration.
        
        Args:
            ollama_host: The Ollama API host URL
            model: The default model to use
        """
        self.ollama_host = (ollama_host or os.getenv("OLLAMA_HOST", "http://localhost:11434")).rstrip('/')
        self.default_model = model or os.getenv("OLLAMA_MODEL", "llama2")
        self.api_endpoint = f"{self.ollama_host}/api/generate"
        
    def transform_to_shakespeare(self, sentence: str, model: Optional[str] = None) -> Optional[str]:
        """
        Transform a modern English sentence to Shakespearean English.
        
        Args:
            sentence: The modern English sentence to transform
            model: The Ollama model to use for transformation (uses default if None)
            
        Returns:
            The transformed Shakespearean text or None if transformation fails
        """
        if not sentence.strip():
            raise ValueError("Input sentence cannot be empty")
            
        # Use provided model or fall back to default
        selected_model = model or self.default_model
            
        # Craft a specific prompt for Shakespeare transformation
        prompt = f"""Transform the following modern English sentence into Shakespearean English. 
Use archaic vocabulary, thou/thee/thy pronouns, and elizabethan sentence structure. 
Only return the transformed sentence, nothing else.

Modern sentence: "{sentence}"

Shakespearean version:"""

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                transformed_text = result.get("response", "").strip()
                
                if transformed_text:
                    # Clean up the response - remove any extra formatting or explanations
                    lines = transformed_text.split('\n')
                    for line in lines:
                        cleaned_line = line.strip()
                        if cleaned_line and not cleaned_line.startswith(('Transform', 'Modern', 'Shakespearean')):
                            return cleaned_line
                    
                    return transformed_text
                else:
                    raise RuntimeError("Empty response from Ollama API")
                    
            elif response.status_code == 404:
                raise RuntimeError(f"Model '{selected_model}' not found. Please ensure the model is installed in Ollama.")
            else:
                raise RuntimeError(f"API request failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"Cannot connect to Ollama API at {self.ollama_host}. Please ensure Ollama is running.")
        except requests.exceptions.Timeout:
            raise RuntimeError("Request to Ollama API timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error occurred: {str(e)}")
        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON response from Ollama API")


def validate_input(sentence: str) -> str:
    """
    Validate and clean the input sentence.
    
    Args:
        sentence: The input sentence to validate
        
    Returns:
        The cleaned sentence
        
    Raises:
        ValueError: If the sentence is invalid
    """
    if not sentence:
        raise ValueError("Please provide a sentence to transform")
        
    sentence = sentence.strip()
    
    if not sentence:
        raise ValueError("Sentence cannot be empty or contain only whitespace")
        
    if len(sentence) > 1000:
        raise ValueError("Sentence is too long (maximum 1000 characters)")
        
    return sentence


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Transform modern English sentences to Shakespearean English using Ollama API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello, how are you today?"
  %(prog)s "I am going to the store" --model llama2
  %(prog)s "What a beautiful day!" --host http://192.168.1.100:11434

Note: Ensure Ollama is running and has a compatible model installed (e.g., llama2, mistral).
        """
    )
    
    parser.add_argument(
        "sentence",
        help="The sentence to transform into Shakespearean English"
    )
    
    parser.add_argument(
        "--model",
        default=None,
        help="Ollama model to use for transformation (default from OLLAMA_MODEL env var or 'llama2')"
    )
    
    parser.add_argument(
        "--host",
        default=None,
        help="Ollama API host URL (default from OLLAMA_HOST env var or 'http://localhost:11434')"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate input
        sentence = validate_input(args.sentence)
        
        if args.verbose:
            print(f"Original sentence: {sentence}")
        
        # Initialize transformer with optional overrides
        transformer = ShakespeareTransformer(ollama_host=args.host, model=args.model)
        
        if args.verbose:
            print(f"Ollama host: {transformer.ollama_host}")
            print(f"Using model: {transformer.default_model}")
            print("Transforming...")
        
        # Perform transformation
        result = transformer.transform_to_shakespeare(sentence)
        
        if result:
            print(result)
        else:
            print("Error: Failed to transform sentence", file=sys.stderr)
            sys.exit(1)
            
    except ValueError as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
