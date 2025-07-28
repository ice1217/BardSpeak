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

1. Install dependencies:
   ```bash
   pip install requests
   ```

2. Set up environment variables (optional):
   ```bash
   export OLLAMA_HOST="http://your-ollama-host:11434"
   export OLLAMA_MODEL="your-preferred-model"
   ```

3. Make the script executable (optional):
   ```bash
   chmod +x main.py
   