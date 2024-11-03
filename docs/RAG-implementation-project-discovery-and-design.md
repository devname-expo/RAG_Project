# RAG Implementation: Project Discovery and Design

## Executive Summary
A concise analysis of implementing a Retrieval Augmented Generation (RAG) system with specific requirements focusing on cost-effectiveness, simplicity, and rapid deployment within a 4-day timeline, limited to 4-hour daily development sessions.

## 1. Project Requirements

### Core Requirements
- **Document Scope**: Process and analyze
  - Australia Women's Softball Team PDF
  - Renard R.31 PDF
- **Cost**: Zero-cost implementation if possible
- **Setup**: Simple deployment and operation
- **Scale**: Single-user system
- **Technology**: Utilize familiar tools/languages due to time constraints

### Out of Scope
- Monitoring and logging systems
- User interface development
- Multi-user functionality
- Authentication systems

## 2. Technical Analysis

### 2.1 Framework Comparison

| Framework | Key Strengths | Learning Curve | Performance |
|-----------|--------------|----------------|-------------|
| No Framework | - Complete control<br>- No dependencies<br>- Simple architecture<br>- Lightweight | - Requires RAG expertise<br>- Direct API knowledge<br>- Infrastructure expertise | - Highly optimizable<br>- No overhead<br>- Custom caching<br>- Direct control |
| LangChain | - Extensive integrations<br>- Advanced prompt engineering<br>- Built-in optimizations | - Steep initial learning<br>- Complex abstractions<br>- Extensive documentation | - Some overhead<br>- Built-in optimizations<br>- Effective caching<br>- Parallel processing |
| LlamaIndex | - Strong integrations<br>- RAG-focused<br>- Efficient document handling | - Moderate learning curve<br>- Clear documentation<br>- RAG-specific concepts | - Document optimized<br>- Efficient querying<br>- Smart caching |
| HayStack | - User-friendly<br>- Well-structured RAG workflows | - Gentle learning curve<br>- Practical examples<br>- Clear documentation | - Pipeline optimized<br>- Effective querying<br>- Built-in caching |
| Embedchain | - Simple setup<br>- Minimal code<br>- RAG-focused | - Gentle learning curve<br>- Basic documentation<br>- Simple concepts | - Depends on LangChain<br>- Basic optimizations<br>- Simple caching |

### 2.2 Document Processing Tools

| Tool | Strengths | Limitations | Best Use Cases |
|------|-----------|-------------|----------------|
| PyMuPDF | - Fast processing<br>- Simple API<br>- Wide PDF support | - PDF-only<br>- Limited complex layouts | - Quick extraction<br>- General PDF processing |
| pdfplumber | - User-friendly<br>- Layout analysis<br>- Table extraction | - Slower on large PDFs | - Structured content<br>- Table extraction |
| pdfminer.six | - Accurate extraction<br>- Fine-grained control | - Slower performance<br>- Steeper learning | - Complex layouts<br>- Detailed extraction |

### 2.3 LLM Services

#### Available Platforms and Free Tiers
| Service | Free Allocation | Notes |
|---------|----------------|--------|
| Google | - 15K req/min (Embedding)<br>- 2-15 req/min (Gemini)<br>- 32K-1M tokens/min | - Includes Pro and embedding models<br>- Cloud project required |
| Cohere | - 100/min (Embed)<br>- 20/min (Chat) | - 1,000 calls/month<br>- API key required |
| HuggingFace | - 1K req/day | - Community models available<br>- Steep learning curve |
| OpenAI | No free tier | |
| Anthropic | No free tier | |
| Mistral AI | No free tier | - Community models on HuggingFace |

### 2.4 Vector Database Options

| Database | Type | Free Tier | Optimal Use Case |
|----------|------|-----------|------------------|
| Pinecone | Hosted | - 1 Project<br>- 5 Indices<br>- 2GB storage | - Simple setup<br>- Small datasets |
| Qdrant | Hosted | - 1GB storage | - Medium datasets<br>- Open source |
| FAISS | Self-hosted | N/A | - Performance-critical<br>- Small-medium data |
| Chroma | Self-hosted | N/A | - Local development<br>- Simple setup |

## 3. Implementation Strategy

### 3.1 Key Priorities
1. Skills demonstration
2. Rapid development
3. Cost efficiency

### 3.2 Approach

Given my tight timeline, I've settled on a two-pronged approach that balances my goals of showcasing relevant skills and delivering a solid prototype on schedule and within budget.

#### Primary Path: Serverless AWS Implementation
My primary path will be a serverless implementation on AWS. This approach plays to my strengths, avoids infrastructure overhead, and should be achievable within the constraints. It's a chance to build something tangible that demonstrates my understanding of both RAG concepts and cloud engineering.

However, I recognize that the added complexity of a serverless architecture poses a risk to the aggressive timeline. To mitigate this, I'll aim to have a bare-bones end-to-end prototype working within the first 2-3 days. This will validate the approach early and give me time to course-correct if needed.

#### Backup Plan: Local Implementation
I've invest some effort during my initial research phase to prepare for a local implementation fallback. This gives me a "Plan B" if the serverless path proves too challenging. The local implementation will focus on simplicity, using established frameworks and following existing tutorials to ensure a working solution can be delivered within the timeline if needed.

### 3.3 Technical Decisions

#### Framework Strategy
**Decision**: No framework for serverless implementation

**Rationale**: While frameworks like LangChain offer rich features, their overhead and complexity would impact Lambda performance and potentially compromise my tight timeline. The direct approach using individual components offers me better control over Lambda-specific optimizations, clearer debugging paths, and a gentler learning curve, which is essential for my short implementation window.

#### PDF Processing
**Decision**: PyMuPDF 

**Rationale**: I selected PyMuPDF due to its lower memory footprint and faster execution time, which is crucial for Lambda performance and cost optimization. While pdfplumber offers superior table extraction capabilities, PyMuPDF's speed and efficiency better align with my RAG implementation needs.

#### LLM Service
**Decision**: Google Platform for both embedding and LLM services

**Rationale**: Having decided on hosted services due to Lambda constraints, I next considered whether to use multiple providers or a single platform for my embedding and LLM needs. While splitting services could provide more total quota headroom, I decided the complexity of managing multiple services wasn't justified for my short timeline. Using a single platform simplifies API key management, SDK setup, and monitoring, letting me focus on core functionality rather than service integration. I selected Google's platform for both embedding and LLM services because it offers generous free tier limits (15K/min for embeddings, 2-15/min for Gemini) that are more than sufficient for development and testing. Their text-embedding-004 model provides high-quality embeddings, while their Gemini models offer solid performance for text generation, making them well-suited for my RAG implementation. 

#### Vector Storage
**Decision**: Pinecone managed service

**Rationale**: For my vector storage needs in a serverless architecture, managed services are essential to avoid infrastructure overhead and minimize development complexity. While a local solution like Chroma with FAISS could work, setting up and managing database persistence would consume more time. The worst case expected combined latency of API calls to my chosen text generation service and either hosted solution (~500ms cold start) fits comfortably within Lambda's and API Gateway's timeout limits, making a managed solution viable. Between the available managed services, I've chosen Pinecone for my initial implementation. While both Pinecone and Qdrant offer suitable free tiers and would work well for my RAG prototype, my initial searches suggest Pinecone has more readily available RAG-specific tutorials and examples, which should help accelerate my development process.

#### Security
**Decision**: AWS Secrets Manager with API key validation

**Rationale**: I've opted against using a VPC since I'm only interfacing with public APIs and temporary S3 storage, avoiding unnecessary complexity and cold start delays. For security, I'll use AWS Secrets to store API keys and implement a simple API key check in the headers, which provides adequate protection for a prototype without overcomplicating authentication.

#### Local Implementation Fallback
**Decision**: LangChain with local HuggingFace models

**Rationale**:  If the serverless implementation proves too complex within the tight timeline, I'll switch to a local implementation using LangChain. Since performance overhead isn't a concern in a local environment, LangChain's rich feature set becomes more appealing. I'll also leverage the framework to implement local models rather than cloud services to keep things simple and avoid API key management. This gives me a reliable fallback option, since there are plenty of well-tested tutorials combining LangChain and HuggingFace that I can follow to get a working solution quickly.

### 3.4 Architecture

The serverless architecture will be deployed via CloudFormation, consisting of the following components:

#### API Layer
- **API Gateway**
  - POST /documents endpoint for PDF uploads
  - POST /query endpoint for RAG interactions
  - API key validation in request headers
  - CloudWatch logging integration

#### Processing Layer
- **Upload Handler Lambda**
  - Validates incoming PDFs
  - Performs size checking
  - Generates presigned S3 URLs
  - Initiates asynchronous processing
  - Maximum runtime: 30 seconds

- **PDF Processor Lambda**
  - Extracts text from PDFs using PyMuPDF
  - Implements text chunking strategies
  - Generates embeddings via Google API
  - Stores vectors in Pinecone
  - Cleans up temporary S3 storage
  - Maximum runtime: 10 minutes

- **Query Handler Lambda**
  - Processes user questions
  - Generates query embeddings
  - Performs vector similarity search
  - Constructs context from relevant chunks
  - Generates responses using Google Gemini
  - Maximum runtime: 30 seconds

#### Storage Layer
- **S3 Bucket**
  - Temporary storage for uploaded PDFs
  - Lifecycle policies for automatic cleanup
  - Event notifications for processing trigger

- **Pinecone**
  - Vector storage for embeddings
  - Managed service outside AWS

#### Security Layer
- **IAM Roles and Policies**
  - Least privilege access for each Lambda
  - S3 access permissions
  - Secrets Manager access

- **Secrets Manager**
  - Google API credentials
  - Pinecone API keys
  - Other service credentials

#### Infrastructure
- **Lambda Layers**
  - PyMuPDF and dependencies
  - Google API SDK
  - Pinecone client
  - Shared utilities

- **CloudWatch**
  - Basic Lambda logging
  - API Gateway access logs
  - Error tracking

All components will be defined in CloudFormation templates, enabling consistent deployment and environment replication.

## 4. Development Plan


### 4.1 Timeline Overview
- **Total Available Time**: 20 hours
  - Day 1: 6 hours 
  - Day 2: 5 hours 
  - Day 3: 5 hours 
  - Day 4: 4 hours 
- **Primary Focus**: Serverless AWS Implementation with CloudFormation

### 4.2 Time-Boxed Schedule

#### Day 1 (4 hours): Infrastructure Setup
- CloudFormation Development
  - Create base CloudFormation template
  - Define API Gateway resources
  - Configure Lambda function skeletons
  - Set up S3 bucket
  - Define IAM roles and policies

- Service Setup
  - Initialize Google Cloud project
  - Create Pinecone account
  - Deploy initial CloudFormation stack
  - Begin local implementation investigation

#### Day 2 (4 hours): Core Processing
- Upload Flow
  - Implement Upload Handler Lambda
  - Configure S3 event triggers
  - Update CloudFormation template
  - Test PDF upload flow

- Processing Implementation
  - Implement PDF Processor Lambda
  - Set up PyMuPDF layer
  - Test text extraction
  - Continue local implementation research

#### Day 3 (4 hours): Query Implementation
- Vector Operations
  - Set up Google embedding integration
  - Configure Pinecone storage
  - Update Lambda layers in CloudFormation

- Query Handler
  - Implement Query Handler Lambda
  - Basic RAG workflow
  - Integration testing
  - Complete local implementation spike

#### Day 4 (4 hours): Finalization and Presentation
- **Hours 1-2**: Final Development
  - Complete any remaining implementation
  - Final bug fixes
  - Performance optimization
  - Documentation updates

- **Hours 3-4**: Presentation Preparation
  - Prepare demo script
  - Test demo flow
  - Document key architectural decisions
  - Create presentation materials
  - Practice presentation

### 4.3 Risk Mitigation

#### Critical Checkpoints
- **Day 1 End**: CloudFormation stack deploys successfully
- **Day 2 End**: Working PDF upload and processing
- **Day 3 End**: Basic query functionality
- **Day 4 Mid-Point**: Implementation approach decision

#### Scope Constraints
- Focus on core RAG functionality only
- Minimal error handling
- Basic CloudFormation template
- No advanced IAM policies
- Limited optimization
- No advanced features
  
#### Fallback Triggers
- CloudFormation deployment issues exceed 1 hour
- Lambda layer configuration problems
- Integration issues span multiple sessions
- Performance problems require extensive debugging
- Any blocker that consumes more than 1 hour without progress

#### Decision Points
- **End of Day 2 (11 hours in)**: Major Implementation Decision
  - **Go Criteria for Serverless**:
    - CloudFormation stack stable
    - PDF pipeline working
    - Basic integrations successful
    - Debugging time <30 mins per issue

  - **Switch to Local If**:
    - CloudFormation still unstable
    - Multiple integration issues
    - Performance problems with PDF processing
    - Issues taking >1 hour to debug

- **Mid-Day 3 (13-14 hours in)**: Final Checkpoint
  - Last chance to switch to local implementation
  - Must have working query functionality by this point
  - Allows 8-9 hours to implement local solution if needed

#### Contingency Actions
- Switch to local implementation
- Use simpler processing approach
- Follow existing tutorials exactly
- Focus on single PDF if needed
- Manually deploy components if CloudFormation issues persist

## 5. References
- [The Pros and Cons of LangChain for Beginner Developers](https://dev.to/alexroor4/the-pros-and-cons-of-langchain-for-beginner-developers-25a7)
- [What is the difference between Embedchain and LangChain?](https://www.gettingstarted.ai/what-is-the-difference-between-embedchain-and-langchain/)
- [A Guide to Comparing Different LLM Chaining Frameworks](https://symbl.ai/developers/blog/a-guide-to-comparing-different-llm-chaining-frameworks/)
- [Best tools for your own AI agents and applications creating](https://medium.com/generative-world/harnessing-ai-a-tour-of-cutting-edge-tools-for-your-own-ai-agents-and-bots-creating-08f4333ddc0d)
- [An introduction to RAG tools and frameworks: Haystack, LangChain, and LlamaIndex](https://www.gettingstarted.ai/introduction-to-rag-ai-apps-and-frameworks-haystack-langchain-llamaindex/)
- [Navigating the Future of AI with Embedchain's RAG Framework](https://medium.com/@lawrenceteixeira/navigating-the-future-of-ai-with-embedchains-rag-framework-the-power-of-embedchain-s-vector-9df98601fb82)
- [Cohere: Introducing a Free Developer Tier + Simplified Pricing](https://cohere.com/blog/free-developer-tier-announcement)
- [Extracting Text from PDFs in Python](https://medium.com/@prathameshamrutkar3/extracting-text-from-pdfs-in-python-pypdf2-pdfminer-six-pdfplumber-and-pymupdf-db95dbe6295a)
- [LLM Leaderboard](https://artificialanalysis.ai/leaderboards/models/prompt-options/single/short)
- [OpenAI Embeddings, GPT-3.5, Pinecone and AWS Lambda: Building a Serverless QA Chatbot](https://www.antstack.com/blog/open-ai-embeddings-gpt-3-5-pinecone-and-aws-lambda-building-a-serverless-qa-chatbot/)
- [A beginner's guide to building a RAG application from scratch](https://learnbybuilding.ai/tutorials/rag-from-scratch)
- [Build your own RAG with Mistral-7B and LangChain](https://medium.com/@thakermadhav)