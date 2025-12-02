"""
Search module for executing queries on Elasticsearch index.
Provides boolean/query_string search functionality.
"""

from .config import INDEX_NAME, DEFAULT_SEARCH_SIZE


def search_boolean_es(es_client, query_text, index_name=INDEX_NAME, size=DEFAULT_SEARCH_SIZE):
    """
    Execute a boolean/query_string search on multiple fields in Elasticsearch
    and return results.
    
    Args:
        es_client (Elasticsearch): Elasticsearch client instance.
        query_text (str): Boolean/query_string query to search.
        index_name (str): Elasticsearch index name.
        size (int): Number of results to return.
        
    Returns:
        dict: Search results from Elasticsearch.
    """
    try:
        # Multi-field query_string query
        query_body = {
            "query": {
                "query_string": {
                    "query": query_text,
                    "fields": [
                        "title",
                        "text",
                        "author",
                        "language",
                        "url",
                        "categories"
                    ]
                }
            }
        }

        # Execute search
        res = es_client.search(index=index_name, body=query_body, size=size)
        return res

    except Exception as e:
        print(f"Error querying Elasticsearch: {e}")
        return None


def display_search_results(search_results, query_text=""):
    """
    Display formatted search results.
    
    Args:
        search_results (dict): Search results from Elasticsearch.
        query_text (str): Original query text for display.
    """
    if not search_results:
        print("No results found.")
        return
    
    # Total hits
    total = search_results['hits']['total']['value'] if isinstance(search_results['hits']['total'], dict) else search_results['hits']['total']
    
    print(f"\n{'='*70}")
    print(f"Query: {query_text}")
    print(f"Total hits: {total}")
    print(f"{'='*70}\n")

    # Display each hit nicely
    for i, hit in enumerate(search_results['hits']['hits'], 1):
        print(f"Result #{i}")
        print(f"Score : {hit['_score']}")
        print(f"ID    : {hit['_id']}")
        print(f"Title : {hit['_source'].get('title', '(no title)')}")
        text = hit['_source'].get('text', '')
        snippet = text[:200] + ("..." if len(text) > 200 else "")
        print(f"Snippet:\n{snippet}")
        print(f"Author: {hit['_source'].get('author', '(no author)')}")
        print(f"Published: {hit['_source'].get('published', '(no date)')}")
        print(f"Language: {hit['_source'].get('language', '(no language)')}")
        print(f"URL: {hit['_source'].get('url', '(no url)')}")
        print(f"Categories: {hit['_source'].get('categories', '(no categories)')}")
        print(f"{'-'*70}\n")
