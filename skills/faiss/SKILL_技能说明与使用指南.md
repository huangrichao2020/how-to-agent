---
name: faiss
description: Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index types (Flat, IVF, HNSW). Use for fast k-NN search, large-scale vector retrieval, or when you need pure similarity search without metadata. Best for high-performance applications.
version: 1.1.0
author: Orchestra Research
license: MIT
tags: [RAG, FAISS, Similarity Search, Vector Search, Facebook AI, GPU Acceleration, Billion-Scale, K-NN, HNSW, High Performance, Large Scale]
dependencies: [faiss-cpu, faiss-gpu, numpy]
yao_category: "数据类"
---

# FAISS - Efficient Similarity Search

Facebook AI's library for billion-scale vector similarity search.

## When to use FAISS

**Use FAISS when:**
- Need fast similarity search on large vector datasets (millions/billions)
- GPU acceleration required
- Pure vector similarity (no metadata filtering needed)
- High throughput, low latency critical
- Offline/batch processing of embeddings

**Use alternatives instead:**
- **Chroma/Pinecone**: Need metadata filtering
- **Weaviate**: Need full database features
- **Annoy**: Simpler, fewer features

## Quick start

### Installation

```bash
# CPU only
pip install faiss-cpu

# GPU support
pip install faiss-gpu
```

### Basic usage

```python
import faiss
import numpy as np

# Create sample data (1000 vectors, 128 dimensions)
d = 128
nb = 1000
vectors = np.random.random((nb, d)).astype('float32')

# Create index
index = faiss.IndexFlatL2(d)  # L2 distance
index.add(vectors)             # Add vectors

# Search
k = 5  # Find 5 nearest neighbors
query = np.random.random((1, d)).astype('float32')
distances, indices = index.search(query, k)

print(f"Nearest neighbors: {indices}")
print(f"Distances: {distances}")
```

## Index types

### 1. Flat (exact search)

```python
# L2 (Euclidean) distance
index = faiss.IndexFlatL2(d)

# Inner product (cosine similarity if normalized)
index = faiss.IndexFlatIP(d)

# Slowest, most accurate
```

### 2. IVF (inverted file) - Fast approximate

```python
# Create quantizer
quantizer = faiss.IndexFlatL2(d)

# IVF index with 100 clusters
nlist = 100
index = faiss.IndexIVFFlat(quantizer, d, nlist)

# Train on data
index.train(vectors)

# Add vectors
index.add(vectors)

# Search (nprobe = clusters to search)
index.nprobe = 10
distances, indices = index.search(query, k)
```

### 3. HNSW (Hierarchical NSW) - Best quality/speed

```python
# HNSW index
M = 32  # Number of connections per layer
index = faiss.IndexHNSWFlat(d, M)

# No training needed
index.add(vectors)

# Search
distances, indices = index.search(query, k)
```

### 4. Product Quantization - Memory efficient

```python
# PQ reduces memory by 16-32×
m = 8   # Number of subquantizers
nbits = 8
index = faiss.IndexPQ(d, m, nbits)

# Train and add
index.train(vectors)
index.add(vectors)
```

## Save and load

```python
# Save index
faiss.write_index(index, "large.index")

# Load index
index = faiss.read_index("large.index")

# Continue using
distances, indices = index.search(query, k)
```

## GPU acceleration

```python
# Single GPU
res = faiss.StandardGpuResources()
index_cpu = faiss.IndexFlatL2(d)
index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu)  # GPU 0

# Multi-GPU
index_gpu = faiss.index_cpu_to_all_gpus(index_cpu)

# 10-100× faster than CPU
```

## LangChain integration

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Create FAISS vector store
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())

# Save
vectorstore.save_local("faiss_index")

# Load
vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

# Search
results = vectorstore.similarity_search("query", k=5)
```

## LlamaIndex integration

```python
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss

# Create FAISS index
d = 1536
faiss_index = faiss.IndexFlatL2(d)

vector_store = FaissVectorStore(faiss_index=faiss_index)
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ValueError: Wrong dimensionality` | Query dim ≠ index dim | Verify `d` matches; check `index.d` |
| `RuntimeError: Error in faiss::...` | Empty index search | Ensure `index.ntotal > 0` before search |
| `IndexError: Cannot add to trained index` | Adding after training (IVF/PQ) | Call `add()` after `train()`, not before |
| `RuntimeError: Error in faiss::gpu` | GPU OOM | Reduce batch size, use CPU fallback |
| `IOError: Error reading index file` | Corrupted/incompatible index file | Verify version match; use `faiss.read_index()` with proper args |
| `ValueError: array is not C contiguous` | Non-contiguous numpy array | Use `np.ascontiguousarray(arr)` |
| `AssertionError: nprobe > nlist` | nprobe exceeds nlist | Set `nprobe <= nlist` |

### Robust Search Pattern

```python
import faiss
import numpy as np

def safe_search(index, query, k=5):
    """Search with comprehensive validation."""
    # Validate query
    query = np.ascontiguousarray(query).astype('float32')
    
    # Check dimension match
    if query.shape[-1] != index.d:
        raise ValueError(f"Dimension mismatch: query={query.shape[-1]}, index={index.d}")
    
    # Check index has data
    if index.ntotal == 0:
        raise RuntimeError("Index is empty. Add vectors before searching.")
    
    # Adjust k if index has fewer vectors
    k = min(k, index.ntotal)
    
    # Adjust nprobe for IVF indices
    if hasattr(index, 'nprobe') and hasattr(index, 'nlist'):
        index.nprobe = min(index.nprobe, index.nlist)
    
    return index.search(query, k)
```

### Safe Index Loading

```python
import faiss
import os

def safe_load_index(path):
    """Load index with validation and fallback."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Index file not found: {path}")
    
    try:
        index = faiss.read_index(path)
        # Validate
        if index.ntotal == 0:
            raise RuntimeError(f"Loaded index is empty: {path}")
        print(f"Loaded index: {index.ntotal} vectors, dim={index.d}")
        return index
    except Exception as e:
        raise RuntimeError(f"Failed to load index {path}: {e}")
```

### GPU Fallback Pattern

```python
def create_index_with_gpu(d, use_gpu=True):
    """Create index with GPU fallback."""
    index = faiss.IndexFlatL2(d)
    
    if use_gpu:
        try:
            res = faiss.StandardGpuResources()
            index = faiss.index_cpu_to_gpu(res, 0, index)
            print("Using GPU acceleration")
        except Exception as e:
            print(f"GPU unavailable, falling back to CPU: {e}")
    
    return index
```

## Best practices

1. **Choose right index type** - Flat for <10K, IVF for 10K-1M, HNSW for quality
2. **Normalize for cosine** - Use IndexFlatIP with normalized vectors
3. **Use GPU for large datasets** - 10-100× faster
4. **Save trained indices** - Training is expensive
5. **Tune nprobe/ef_search** - Balance speed/accuracy
6. **Monitor memory** - PQ for large datasets
7. **Batch queries** - Better GPU utilization
8. **Always validate dimensions** before add/search operations

## Performance

| Index Type | Build Time | Search Time | Memory | Accuracy |
|------------|------------|-------------|--------|----------|
| Flat | Fast | Slow | High | 100% |
| IVF | Medium | Fast | Medium | 95-99% |
| HNSW | Slow | Fastest | High | 99% |
| PQ | Medium | Fast | Low | 90-95% |

## Resources

- **GitHub**: https://github.com/facebookresearch/faiss
- **Wiki**: https://github.com/facebookresearch/faiss/wiki
- **License**: MIT

