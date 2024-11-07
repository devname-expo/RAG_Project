# RAG_Project
A Retrieval Augmented Generation (RAG) pipeline that can answer user’s questions based on the provided documents.

To run a query
```bash
python src/main.py --query "Who were the pitchers on the Australian softball team\'s roster at the 2020 Summer Olympics?"
```

To recreate embeddings vector db
```bash
python3 POC/main.py       
```# RAG Project

A Retrieval Augmented Generation (RAG) pipeline that enables natural language querying of document collections using state-of-the-art language models and vector similarity search.

## Overview

This project implements a RAG (Retrieval Augmented Generation) system that:
- Processes and embeds documents into a vector database
- Retrieves relevant context based on user queries
- Generates text answers using the retrieved information

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/devname-expo/RAG_Project
cd RAG_Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Query the System

To ask questions about your documents:

```bash
python src/main.py --query "Your question here"
```

Example:
```bash
python src/main.py --query "Who were the pitchers on the Australian softball team's roster at the 2020 Summer Olympics?"
```

### Rebuild Vector Database

To recreate the document embeddings database:

```bash
python3 POC/main.py
```

Note: This step is required when:
- Adding new documents to the system
- Changing the embedding model
- Modifying the document processing pipeline

