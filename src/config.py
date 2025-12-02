"""
Configuration module for Elasticsearch News Indexing project.
Centralizes all configuration constants used across the project.
"""

from pathlib import Path

# Elasticsearch Configuration
ES_HOST = 'http://127.0.0.1'
ES_PORT = '9200'
ES_URL = f"{ES_HOST}:{ES_PORT}"

# Index Configuration
INDEX_NAME = 'esindex-v1.0'

# Data Processing Configuration
DATA_DIR = Path('free-news-datasets/News_Datasets')
NUM_ZIPS_TO_INDEX = 5000  # Change this to index more/fewer archives
BATCH_SIZE = 500
MAX_LIMIT = 2e6  # Maximum documents to index

# Search Configuration
DEFAULT_SEARCH_SIZE = 10
