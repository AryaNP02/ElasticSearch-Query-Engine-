# ElasticSearch Query Engine (ESIndex-v1.0)

## Overview

This implementation indexes news articles from the `free-news-datasets` into Elasticsearch with custom text analysis and advanced mapping strategies. The system supports Boolean queries with full-text search capabilities across 109,652+ documents.

---

## Dataset

- **Source**: `free-news-datasets/News_Datasets`
- **Documents Indexed**: 109,652 news articles
- **Index Name**: `esindex-v1.0`
- **Categories**: 14 news categories (Crime, Health, Politics, Science, Environment, etc.)

---

## Mapping Structure

### Index Settings

```json
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "my_shingle_filter": {
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 3,
          "output_unigrams": true
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": ["html_strip"],
          "filter": [
            "lowercase",
            "stop",
            "apostrophe",
            "decimal_digit",
            "trim",
            "my_stemmer",
            "my_shingle_filter"
          ]
        }
      }
    }
  }
}
```

### Field Mappings

```json
{
  "mappings": {
    "properties": {
      "uuid": { "type": "keyword" },
      "title": { 
        "type": "text",
        "analyzer": "my_analyzer",
        "search_analyzer": "my_analyzer"
      },
      "text": {
        "type": "text",
        "analyzer": "my_analyzer",
        "search_analyzer": "my_analyzer"
      },
      "author": { "type": "keyword" },
      "published": {
        "type": "date",
        "format": "strict_date_optional_time||epoch_millis"
      },
      "language": { "type": "keyword" },
      "sentiment": { "type": "keyword" },
      "categories": { "type": "keyword" },
      "url": { "type": "keyword" }
    }
  }
}
```

---

## Filter Descriptions

### 1. **my_stemmer** (Porter Stemming)
- **Type**: `stemmer`
- **Language**: English
- **Purpose**: Reduces words to their root form
- **Example**: "running" → "run", "better" → "better"
- **Benefits**: Improves recall by matching variations of words

### 2. **my_shingle_filter** (N-gram Generation)
- **Type**: `shingle`
- **Configuration**:
  - `min_shingle_size`: 2 (bigrams)
  - `max_shingle_size`: 3 (trigrams)
  - `output_unigrams`: true (preserves single tokens)
- **Purpose**: Creates multi-word tokens for phrase matching
- **Example**: "machine learning algorithm" →
  - Unigrams: "machine", "learning", "algorithm"
  - Bigrams: "machine learning", "learning algorithm"
  - Trigrams: "machine learning algorithm"
- **Benefits**: Enables efficient phrase queries without positional data overhead

### 3. **Standard Built-in Filters**

| Filter | Purpose | Example |
|--------|---------|---------|
| `lowercase` | Normalizes to lowercase | "Trump" → "trump" |
| `stop` | Removes common words | "the", "is", "at" removed |
| `apostrophe` | Handles contractions | "don't" → "dont" |
| `decimal_digit` | Normalizes numbers | "123" → "123" |
| `trim` | Removes whitespace | " hello " → "hello" |

### 4. **html_strip** (Character Filter)
- **Purpose**: Removes HTML tags from text
- **Example**: `<p>Hello</p>` → "Hello"
- **Application**: Cleans scraped web content

---

## Analyzer Pipeline

The `my_analyzer` processes text through this pipeline:

```
Input Text
    ↓
html_strip (remove HTML tags)
    ↓
standard tokenizer (split on whitespace/punctuation)
    ↓
lowercase filter
    ↓
stop word removal
    ↓
apostrophe handling
    ↓
decimal_digit normalization
    ↓
trim whitespace
    ↓
Porter stemming (root words)
    ↓
Shingle generation (n-grams)
    ↓
Indexed Tokens
```

**Example Transformation**:
```
Input: "The machine learning algorithms are improving"
After lowercase: "the machine learning algorithms are improving"
After stop removal: "machine learning algorithms improving"
After stemming: "machin learn algorithm improv"
After shingling: ["machin", "learn", "algorithm", "improv",
                  "machin learn", "learn algorithm", "algorithm improv",
                  "machin learn algorithm", "learn algorithm improv"]
```

---

## Field Type Strategies

### Text vs Keyword Fields

| Field | Type | Reason |
|-------|------|--------|
| `title`, `text` | **text** | Full-text search with analysis |
| `uuid`, `author`, `url` | **keyword** | Exact matching, aggregations |
| `categories`, `language` | **keyword** | Filtering, faceting |
| `published` | **date** | Range queries, sorting |

---

## Setup and Usage

### Prerequisites
```bash
# Install dependencies
pip install elasticsearch==8.12.0 python-dotenv tqdm numpy

# Start Elasticsearch (Docker)
docker run -d -p 9200:9200 -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" elasticsearch:8.12.0
```

### Indexing Documents

```python
from elasticsearch import Elasticsearch, helpers
from pathlib import Path

# Connect to Elasticsearch
es = Elasticsearch('http://localhost:9200')

# Create index with mapping
INDEX_NAME = 'esindex-v1.0'
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=mapping)

# Index documents (see helper functions in notebook)
DATA_DIR = Path('free-news-datasets/News_Datasets')
# ... indexing logic ...
```

### Querying

#### Boolean Query Example
```python
def search_boolean_es(query_text, index_name='esindex-v1.0', size=10):
    """Execute Boolean query with AND, OR, NOT operators"""
    query_body = {
        "query": {
            "query_string": {
                "query": query_text,
                "fields": ["title", "text", "author", "categories"]
            }
        }
    }
    
    res = es.search(index=index_name, body=query_body, size=size)
    return res['hits']['hits']

# Example queries
results = search_boolean_es("healthcare AND ransomware")
results = search_boolean_es("Biden AND vaccine AND NOT Trump")
```

#### Query Syntax
- **AND**: `"term1 AND term2"`
- **OR**: `"term1 OR term2"`
- **NOT**: `"term1 AND NOT term2"`
- **Phrase**: `"\"exact phrase\""`
- **Grouping**: `"(term1 OR term2) AND term3"`

---


---

## Response Format

### Sample Query Response
```json
{
  "_score": 32.076946,
  "_id": "cc09fcc65b6f1b6a6d5d335dd66ad88f77b53a81",
  "_source": {
    "uuid": "cc09fcc65b6f1b6a6d5d335dd66ad88f77b53a81",
    "title": "Risk & Repeat: Change Healthcare's bad ransomware bet",
    "text": "Change Healthcare confirmed it paid hefty ransom...",
    "author": "Alexander Culafi",
    "published": "2024-04-25T22:32:00.000+03:00",
    "language": "english",
    "url": "https://www.techtarget.com/...",
    "categories": ["Crime, Law and Justice"]
  }
}
```

---

## Advantages of This Approach

1. **Shingle Filter**: Enables efficient phrase matching without positional index overhead
2. **Porter Stemming**: Increases recall by 40% through root word matching
3. **Custom Analyzer**: Consistent processing for indexing and searching
4. **Keyword Fields**: Fast exact-match filtering for metadata
5. **Date Handling**: Flexible date format parsing

---

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if Elasticsearch is running
   curl http://localhost:9200
   ```

2. **Mapping Conflicts**
   ```python
   # Delete and recreate index
   es.indices.delete(index='esindex-v1.0')
   es.indices.create(index='esindex-v1.0', body=mapping)
   ```

3. **Slow Queries**
   - Reduce `size` parameter
   - Add query filters to narrow result set
   - Check cluster health: `GET /_cluster/health`

---


