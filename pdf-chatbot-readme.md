# Intelligent PDF Chatbot

## Project Properties

### Technical Specifications
- **Language**: Python
- **Framework**: Streamlit
- **Machine Learning Library**: scikit-learn
- **NLP Model**: Ollama (llama3.2)
- **Text Processing**: TF-IDF Vectorization
- **Similarity Metric**: Cosine Similarity

### Key Technologies
- Natural Language Processing
- Document Retrieval
- Contextual Question Answering
- Machine Learning-based Text Analysis

### Core Capabilities
- PDF Text Extraction
- Semantic Context Retrieval
- Intelligent Summarization
- Topic Difficulty Analysis
- Conversational AI Interface

## Overview

This Intelligent PDF Chatbot is a Streamlit application that allows users to interact with PDF documents using advanced natural language processing capabilities. Leveraging Ollama for language model interactions and scikit-learn for text processing, the chatbot can:

- Upload and analyze PDF documents
- Generate comprehensive summaries
- Identify challenging topics
- Provide context-aware responses to user queries

## Prerequisites

### System Requirements
- Python 3.8+
- pip (Python package manager)

### Dependencies
- Streamlit
- Ollama
- PyPDF2
- NumPy
- scikit-learn

## Installation

### 1. Ollama Installation

#### macOS
```bash
curl https://ollama.ai/install.sh | sh
```

#### Windows
- Download the installer from [Ollama's official website](https://ollama.ai)
- Run the executable and follow installation instructions

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull Language Model
```bash
ollama pull llama3.2
```

### 3. Python Environment Setup
```bash
# Create a virtual environment
python -m venv pdf_chatbot_env

# Activate the environment
# On Windows
pdf_chatbot_env\Scripts\activate
# On macOS/Linux
source pdf_chatbot_env/bin/activate

# Install dependencies
pip install streamlit ollama PyPDF2 numpy scikit-learn
```

## Running the Application

1. Ensure Ollama is running in the background
2. Navigate to the project directory
3. Run the Streamlit app:
```bash
streamlit run pdf_chatbot.py
```

## Features

### PDF Analysis
- Upload PDF documents
- Generate comprehensive summaries
- Identify challenging topics in the document

### Intelligent Chat
- Context-aware responses based on uploaded PDF
- Fallback to general chat when no PDF is loaded
- Conversation history tracking

## Usage Tips

- Upload a PDF using the sidebar
- Click "Generate Comprehensive Summary" to get an overview
- Click "Identify Difficult Topics" for study insights
- Ask questions about the PDF content
- Use "Clear Chat History" to reset conversation

## Customization

- Modify `PDFChatbot` class to change:
  - Chunk size
  - Number of context chunks
  - Language model

## Troubleshooting

- Ensure Ollama is running before starting the app
- Check internet connection for model downloads
- Verify Python dependencies are correctly installed

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.

## License

MIT License

Copyright (c) 2024 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

- [Ollama](https://ollama.ai)
- [Streamlit](https://streamlit.io)
- [scikit-learn](https://scikit-learn.org)
