"""
Elasticsearch client initialization and connection management.
Handles connection to Elasticsearch server.
"""

from elasticsearch import Elasticsearch
from .config import ES_URL


def create_es_client():
    """
    Create and test Elasticsearch client connection.
    
    Returns:
        Elasticsearch: Connected Elasticsearch client instance.
        
    Raises:
        Exception: If connection to Elasticsearch fails.
    """
    es = Elasticsearch(ES_URL)
    
    try:
        print(f'Connecting to Elasticsearch at {ES_URL}')
        if es.ping():
            print('✓ Successfully connected to Elasticsearch')
            return es
        else:
            raise Exception('Failed to ping Elasticsearch server')
    except Exception as e:
        print(f'✗ Error connecting to Elasticsearch: {e}')
        raise
