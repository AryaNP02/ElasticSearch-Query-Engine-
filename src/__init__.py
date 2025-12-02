"""
Elasticsearch News Indexing Package

This package provides utilities for indexing and searching news articles
in Elasticsearch with advanced text analysis and query capabilities.
"""

from .config import (
    ES_HOST,
    ES_PORT,
    ES_URL,
    INDEX_NAME,
    DATA_DIR,
    NUM_ZIPS_TO_INDEX,
    BATCH_SIZE,
    MAX_LIMIT,
    DEFAULT_SEARCH_SIZE,
)
from .mapping import MAPPING
from .elasticsearch_client import create_es_client
from .data_indexer import iter_jsons_in_path, bulk_index
from .search import search_boolean_es, display_search_results

__all__ = [
    'ES_HOST',
    'ES_PORT',
    'ES_URL',
    'INDEX_NAME',
    'DATA_DIR',
    'NUM_ZIPS_TO_INDEX',
    'BATCH_SIZE',
    'MAX_LIMIT',
    'DEFAULT_SEARCH_SIZE',
    'MAPPING',
    'create_es_client',
    'iter_jsons_in_path',
    'bulk_index',
    'search_boolean_es',
    'display_search_results',
]
