"""
Mapping configuration for Elasticsearch News Index.
Defines the schema, analyzers, and field mappings.
"""

MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                # English stemmer
                "my_stemmer": {"type": "stemmer", "language": "english"},
                # Create bigrams/trigrams for phrase search
                "my_shingle_filter": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 3,
                    "output_unigrams": True
                }
            },
            "analyzer": {
                "my_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    # Normalize, clean, stem, and create shingles
                    "filter": [
                        "lowercase", "stop", "apostrophe",
                        "decimal_digit", "trim",
                        "my_stemmer", "my_shingle_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "uuid": {"type": "keyword"},  # unique ID
            "title": {"type": "text", "analyzer": "my_analyzer", "search_analyzer": "my_analyzer"},
            "text": {"type": "text", "analyzer": "my_analyzer", "search_analyzer": "my_analyzer"},
            "author": {"type": "keyword"},  # exact match
            "published": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
            "language": {"type": "keyword"},
            "sentiment": {"type": "keyword"},
            "categories": {"type": "keyword"},
            "url": {"type": "keyword"}  # exact match for links
        }
    }
}
