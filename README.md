# Shakespeare Transformer CLI Tool

A Python command-line tool that transforms modern English sentences into Shakespearean English using the Ollama API.

## Features

- Transform modern English to Shakespearean English
- Command-line interface with argparse
- Configurable Ollama host and model
- Comprehensive error handling
- Input validation
- Verbose mode for debugging

## Prerequisites

- Python 3.6 or higher
- Ollama running locally or on a remote server
- A compatible language model installed in Ollama (e.g., llama2, mistral)

## Installation

1. Ensure you have the `requests` library installed:
   ```bash
   pip install requests
   ```

2. Make the script executable (optional):
   ```bash
   chmod +x shakespeare_transformer.py
   