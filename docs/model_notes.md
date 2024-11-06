# Models Notes

Note: The following has been created using GenAI for easy comparison and initial exploration. For more accurate information I am using [LLM Leaderboard](https://artificialanalysis.ai/leaderboards/models) and the direct sites for models.

#### Embedding Models

##### Local Embedding Models
| Aspect | all-MiniLM-L6-v2 | bge-small-en | bge-base-en | e5-large | jina-base-en | gte-large | multilingual-e5-large |
|--------|------------------|---------------|--------------|-----------|---------------|------------|---------------------|
| Provider | HuggingFace | HuggingFace | HuggingFace | HuggingFace | Jina AI | HuggingFace | HuggingFace |
| Dimensions | *384* | *384* | *768* | *1024* | *768* | *1024* | *1024* |
| Context Window | 512 tokens | 512 tokens | 512 tokens | 512 tokens | 512 tokens | 512 tokens | 512 tokens |
| Performance | • GPU: 10K tokens/s<br>• CPU: 2K tokens/s<br>• 8-bit: 15K tokens/s | • GPU: 12K tokens/s<br>• CPU: 3K tokens/s<br>• 8-bit: 18K tokens/s | • GPU: 8K tokens/s<br>• CPU: 1.5K tokens/s<br>• 8-bit: 12K tokens/s | • GPU: 6K tokens/s<br>• CPU: 1K tokens/s<br>• 8-bit: 9K tokens/s | • GPU: 8K tokens/s<br>• CPU: 1.5K tokens/s<br>• 8-bit: 12K tokens/s | • GPU: 5K tokens/s<br>• CPU: 800 tokens/s<br>• 8-bit: 8K tokens/s | • GPU: 4K tokens/s<br>• CPU: 600 tokens/s<br>• 8-bit: 7K tokens/s |
| Hardware Requirements | • GPU: RTX 3060<br>• RAM: 8GB<br>• Storage: 500MB<br>• 8-bit: 4GB RAM | • GPU: RTX 3060<br>• RAM: 8GB<br>• Storage: 500MB<br>• 8-bit: 4GB RAM | • GPU: RTX 3060<br>• RAM: 16GB<br>• Storage: 1GB<br>• 8-bit: 8GB RAM | • GPU: RTX 3070<br>• RAM: 32GB<br>• Storage: 2GB<br>• 8-bit: 16GB RAM | • GPU: RTX 3060<br>• RAM: 16GB<br>• Storage: 1GB<br>• 8-bit: 8GB RAM | • GPU: RTX 3070<br>• RAM: 32GB<br>• Storage: 2GB<br>• 8-bit: 16GB RAM | • GPU: RTX 3070<br>• RAM: 32GB<br>• Storage: 2.5GB<br>• 8-bit: 16GB RAM |
| Features | • Small size<br>• Fast inference<br>• Good quality | • RAG optimized<br>• Fast inference<br>• Compact | • Better quality<br>• More features<br>• Balanced size | • High quality<br>• Rich features<br>• Research grade | • Production ready<br>• Good balance<br>• Enterprise use | • High quality<br>• Semantic search<br>• General purpose | • Multilingual<br>• High quality<br>• Cross-lingual |
| Best for | • Cost control<br>• Basic RAG<br>• Edge devices | • RAG-specific<br>• Fast deployment<br>• Edge devices | • Better quality<br>• Production<br>• General use | • Research<br>• High accuracy<br>• Complex tasks | • Production<br>• Balanced use<br>• Enterprise | • General purpose<br>• Semantic search<br>• Research | • Multilingual apps<br>• Cross-lingual<br>• Research |

##### Hosted Embedding Models
|   | embed-english-v3.0 | embed-english-light-v3.0 | text-embedding-004 | all-MiniLM-L6-v2 | bge-small-en | bge-base-en | e5-large |
|--------|-------------------|-------------------------|-------------------|------------------|---------------|--------------|-----------|
| Provider | Cohere | Cohere | Google | OpenAI | HuggingFace | HuggingFace | HuggingFace | HuggingFace |
| Dimensions | 1024 | 384 | 3072 | 3072 | 384 | 384 | 768 | 1024 |
| Context Window | 512 tokens | 512 tokens | 8192 tokens | 8192 tokens | 512 tokens | 512 tokens | 512 tokens | 512 tokens |
| Performance | • ~150ms latency<br>• ~8K tokens/sec<br>• High throughput | • ~120ms latency<br>• ~10K tokens/sec<br>• Better throughput | • ~200ms latency<br>• ~8K tokens/sec<br>• Premium quality | • ~200ms latency<br>• ~8K tokens/sec<br>• Premium quality | • ~100ms latency<br>• ~15K tokens/sec<br>• Fast inference | • ~80ms latency<br>• ~18K tokens/sec<br>• Fastest inference | • ~120ms latency<br>• ~12K tokens/sec<br>• Good balance | • ~150ms latency<br>• ~10K tokens/sec<br>• High quality |
| Features | • Multilingual<br>• Semantic search<br>• Cross-encoding | • Lightweight<br>• Fast inference<br>• RAG optimized | • Google ecosystem<br>• High quality<br>• Advanced features | • OpenAI ecosystem<br>• High quality<br>• Advanced features | • Small size<br>• Fast inference<br>• Good quality | • RAG optimized<br>• Fast inference<br>• Compact | • Better quality<br>• More features<br>• Balanced size | • High quality<br>• Rich features<br>• Research grade |
| Best for | • High accuracy<br>• Production use<br>• General purpose | • Fast inference<br>• Cost-effective<br>• RAG | • Premium quality<br>• Google ecosystem<br>• Production | • Premium quality<br>• OpenAI ecosystem<br>• Production | • Cost control<br>• Basic RAG<br>• Quick setup | • RAG-specific<br>• Fast deployment<br>• High volume | • Production<br>• General use<br>• Balanced needs | • Research<br>• High accuracy<br>• Complex tasks |

#### Text Generation Models

##### Local Text Generation Models
| Aspect | llama-2-70b | llama-2-13b | mistral-7b | openchat-3.5 | phi-2 | all-MiniLM-L6-v2 | bge-large |
|--------|-------------|--------------|-------------|---------------|--------|------------------|------------|
| Provider | Meta | Meta | Mistral | HF | Microsoft | HF | HF |
| Context Window | 4K tokens | 4K tokens | 32K tokens | 8K tokens | 2K tokens | 512 tokens | 32K tokens |
| Performance | • GPU: 30 tokens/s<br>• CPU: 2 tokens/s<br>• 8-bit: 40 tokens/s | • GPU: 50 tokens/s<br>• CPU: 5 tokens/s<br>• 8-bit: 70 tokens/s | • GPU: 80 tokens/s<br>• CPU: 15 tokens/s<br>• 8-bit: 100 tokens/s | • GPU: 100 tokens/s<br>• CPU: 20 tokens/s<br>• 8-bit: 120 tokens/s | • GPU: 150 tokens/s<br>• CPU: 30 tokens/s<br>• 8-bit: 180 tokens/s | • GPU: 120 tokens/s<br>• CPU: 25 tokens/s<br>• 8-bit: 150 tokens/s | • GPU: 70 tokens/s<br>• CPU: 10 tokens/s<br>• 8-bit: 90 tokens/s |
| Hardware Requirements | • GPU: A100 80GB×2<br>• RAM: 200GB<br>• Storage: 350GB<br>• 4-bit: 80GB RAM<br>• 8-bit: 160GB RAM | • GPU: A6000 48GB<br>• RAM: 52GB<br>• Storage: 60GB<br>• 4-bit: 16GB RAM<br>• 8-bit: 32GB RAM | • GPU: RTX 4090<br>• RAM: 32GB<br>• Storage: 40GB<br>• 4-bit: 8GB RAM<br>• 8-bit: 16GB RAM | • GPU: RTX 3090<br>• RAM: 24GB<br>• Storage: 30GB<br>• 4-bit: 6GB RAM<br>• 8-bit: 12GB RAM | • GPU: RTX 3060<br>• RAM: 16GB<br>• Storage: 20GB<br>• 4-bit: 3GB RAM<br>• 8-bit: 6GB RAM | • GPU: RTX 3060<br>• RAM: 8GB<br>• Storage: 2GB<br>• 8-bit: 4GB RAM | • GPU: RTX 3080<br>• RAM: 24GB<br>• Storage: 30GB<br>• 8-bit: 12GB RAM |
| Quantization Options | • GGUF<br>• GPTQ<br>• AWQ<br>• 4-bit to 16-bit | • GGUF<br>• GPTQ<br>• AWQ<br>• 4-bit to 16-bit | • GGUF<br>• GPTQ<br>• AWQ<br>• 4-bit to 16-bit | • GGUF<br>• GPTQ<br>• 4-bit to 16-bit | • GGUF<br>• GPTQ<br>• 4-bit to 8-bit | • FP16<br>• INT8<br>• ONNX | • FP16<br>• INT8<br>• ONNX |
| Inference Frameworks | • llama.cpp<br>• vLLM<br>• text-generation-inference<br>• ExLlama | • llama.cpp<br>• vLLM<br>• text-generation-inference<br>• ExLlama | • llama.cpp<br>• vLLM<br>• text-generation-inference<br>• ExLlama | • llama.cpp<br>• vLLM<br>• text-generation-inference | • llama.cpp<br>• vLLM<br>• Basic transformers | • transformers<br>• ONNX Runtime | • transformers<br>• ONNX Runtime |
| Features | • Open source<br>• Local control<br>• Customizable<br>• All precisions | • Open source<br>• Good balance<br>• RAG suitable<br>• All precisions | • Open source<br>• Instruction tuned<br>• RAG optimized<br>• All precisions | • Chat focused<br>• Good quality<br>• Easy setup<br>• Limited precisions | • Small size<br>• Fast inference<br>• Code capable<br>• Limited precisions | • Small size<br>• Fast inference<br>• Good quality | • Better quality<br

##### Hosted Text Generation Models
| Aspect | gemini-pro | command | command-light | claude-3-opus | claude-3-sonnet | mistral-small | bge-large | all-MiniLM-L6-v2 | mistral-7b |
|--------|------------|---------|---------------|---------------|-----------------|---------------|------------|------------------|-------------|
| Provider | Google | Cohere | Cohere | Anthropic | Anthropic | Mistral AI | HuggingFace | HuggingFace | HuggingFace |
| Context Window | 32K tokens | 128K tokens | 32K tokens | 200K tokens | 200K tokens | 32K tokens | 32K tokens | 512 tokens | 32K tokens |
| Performance | • ~1-2s latency<br>• 150 tokens/s<br>• High throughput | • ~2-3s latency<br>• 100 tokens/s<br>• Good throughput | • ~1-2s latency<br>• 120 tokens/s<br>• High throughput | • ~2-3s latency<br>• 150 tokens/s<br>• Complex reasoning | • ~1-2s latency<br>• 180 tokens/s<br>• Balanced performance | • ~1s latency<br>• 200 tokens/s<br>• Fast reßsponses | • ~2s latency<br>• 100 tokens/s<br>• Good throughput | • ~1s latency<br>• 150 tokens/s<br>• High throughput | • ~1.5s latency<br>• 120 tokens/s<br>• Good throughput |
| Features | • Structured output<br>• Function calling<br>• Multi-turn chat | • Custom prompts<br>• RAG optimized<br>• Summarization | • Faster responses<br>• Core features<br>• Cost effective | • Advanced reasoning<br>• Tool use<br>• Code generation | • Balanced capabilities<br>• Tool use<br>• Cost effective | • Good reasoning<br>• RAG optimized<br>• Cost effective | • Open source base<br>• RAG optimized<br>• Easy integration | • Small size<br>• Fast inference<br>• Good quality | • Open source base<br>• Instruction tuned<br>• RAG optimized |
| Best for | • General purpose<br>• RAG applications<br>• Cost-sensitive | • Document analysis<br>• Summarization<br>• RAG systems | • Quick responses<br>• Simple tasks<br>• High volume | • Complex reasoning<br>• Premium quality<br>• Long context | • Balanced use<br>• General tasks<br>• Good quality | • Production use<br>• Cost efficiency<br>• Quick responses | • Production<br>• Quick setup<br>• Serverless | • Basic RAG<br>• Quick deployment<br>• Serverless | • RAG systems<br>• General use<br>• Serverless |
