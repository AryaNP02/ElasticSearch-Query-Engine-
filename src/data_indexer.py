"""
Data indexing module for Elasticsearch.
Handles reading JSON files from various sources and bulk indexing to Elasticsearch.
"""

import json
import zipfile
from pathlib import Path
from elasticsearch import helpers


def iter_jsons_in_path(path: Path):
    """
    Yield (doc_id, doc) for JSONs found inside a directory, a zip file, or a single JSON file.
    
    - If `path` is a directory: walk and yield every .json under it (recursive).
    - If `path` is a .zip file: iterate members that end with .json.
    - If `path` is a .json file: read it.
    
    Args:
        path (Path): Path to directory, zip file, or JSON file.
        
    Yields:
        tuple: (doc_id, doc) where doc_id is unique identifier and doc is the document dict.
    """
    if path.is_dir():
        # walk directory for json files
        for p in sorted(path.rglob('*.json')):
            try:
                with open(p, 'rb') as fh:
                    raw = fh.read()
                    try:
                        s = raw.decode('utf-8')
                    except Exception:
                        s = raw.decode('latin-1')
                    data = json.loads(s)
                    doc_id = data.get('uuid') or data.get('thread', {}).get('uuid') or f"{path.name}/{p.name}"
                    doc = {
                        'uuid': doc_id,
                        'title': data.get('title'),
                        'text': data.get('text'),
                        'author': data.get('author'),
                        'published': data.get('published'),
                        'language': data.get('language'),
                        'sentiment': data.get('sentiment'),
                        'categories': data.get('categories'),
                        'url': data.get('url')
                    }
                    yield doc_id, doc
            except Exception as e:
                print(f'Failed reading {p}: {e}')
    elif path.suffix.lower() == '.zip':
        # Handle zip files
        with zipfile.ZipFile(path, 'r') as zf:
            for name in zf.namelist():
                if not name.lower().endswith('.json'):
                    continue
                try:
                    with zf.open(name) as fh:
                        raw = fh.read()
                        try:
                            s = raw.decode('utf-8')
                        except Exception:
                            s = raw.decode('latin-1')
                        data = json.loads(s)
                        doc_id = data.get('uuid') or data.get('thread', {}).get('uuid') or f"{path.stem}/{name}"
                        doc = {
                            'uuid': doc_id,
                            'title': data.get('title'),
                            'text': data.get('text'),
                            'author': data.get('author'),
                            'published': data.get('published'),
                            'language': data.get('language'),
                            'sentiment': data.get('sentiment'),
                            'categories': data.get('categories'),
                            'url': data.get('url')
                        }
                        yield doc_id, doc
                except Exception as e:
                    print(f'Failed reading {name} in {path}: {e}')
    elif path.is_file() and path.suffix.lower() == '.json':
        # Handle single JSON file
        try:
            with open(path, 'rb') as fh:
                raw = fh.read()
                try:
                    s = raw.decode('utf-8')
                except Exception:
                    s = raw.decode('latin-1')
                data = json.loads(s)
                doc_id = data.get('uuid') or data.get('thread', {}).get('uuid') or path.name
                doc = {
                    'uuid': doc_id,
                    'title': data.get('title'),
                    'text': data.get('text'),
                    'author': data.get('author'),
                    'published': data.get('published'),
                    'language': data.get('language'),
                    'sentiment': data.get('sentiment'),
                    'categories': data.get('categories'),
                    'url': data.get('url')
                }
                yield doc_id, doc
        except Exception as e:
            print(f'Failed reading {path}: {e}')
    else:
        print(f'Skipping unsupported path type: {path}')


def bulk_index(es_client, index_name, docs_iter, batch_size=500):
    """
    Bulk index documents to Elasticsearch.
    
    Args:
        es_client (Elasticsearch): Elasticsearch client instance.
        index_name (str): Name of the index to bulk index into.
        docs_iter (iterator): Iterator of (doc_id, doc) tuples.
        batch_size (int): Number of documents to process per batch.
        
    Returns:
        int: Total number of documents indexed.
    """
    actions = []
    total = 0
    
    for doc_id, doc in docs_iter:
        actions.append({
            '_index': index_name,
            '_id': doc_id,
            '_source': doc
        })
        
        if len(actions) >= batch_size:
            helpers.bulk(es_client, actions)
            total += len(actions)
            actions = []
    
    # Index remaining documents
    if actions:
        helpers.bulk(es_client, actions)
        total += len(actions)
    
    return total
