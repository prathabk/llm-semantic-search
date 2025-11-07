"""
Typesense Service - Handle vector database operations
"""
import os
import requests
from typing import List, Dict, Any, Optional


class TypesenseService:
    """Service to interact with Typesense for document storage and search"""

    def __init__(
        self,
        host: str = 'localhost',
        port: int = 8108,
        api_key: Optional[str] = None,
        collection_name: str = 'llm-semantic-search'
    ):
        """
        Initialize Typesense service

        Args:
            host: Typesense host
            port: Typesense port
            api_key: API key (reads from env if not provided)
            collection_name: Collection name
        """
        self.host = host
        self.port = port
        self.api_key = api_key or os.getenv('TYPESENSE_API_KEY', 'vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se')
        self.collection_name = collection_name
        self.base_url = f'http://{host}:{port}'
        self.headers = {'X-TYPESENSE-API-KEY': self.api_key}

    def create_collection(self, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create or recreate collection with schema

        Args:
            schema: Collection schema (uses default if not provided)

        Returns:
            API response
        """
        if not schema:
            schema = {
                "name": self.collection_name,
                "fields": [
                    {"name": "name", "type": "string", "optional": True},
                    {"name": "gender", "type": "string", "facet": True},
                    {"name": "likes_color", "type": "string", "facet": True, "optional": True},
                    {"name": "likes_food", "type": "string", "facet": True, "optional": True},
                    {"name": "text", "type": "string"}
                ]
            }

        # Delete collection if exists
        try:
            self.delete_collection()
        except:
            pass  # Collection might not exist

        # Create new collection
        response = requests.post(
            f'{self.base_url}/collections',
            json=schema,
            headers=self.headers
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create collection: {response.text}")

        return response.json()

    def delete_collection(self) -> Dict[str, Any]:
        """Delete the collection"""
        response = requests.delete(
            f'{self.base_url}/collections/{self.collection_name}',
            headers=self.headers
        )

        if response.status_code not in [200, 404]:
            raise Exception(f"Failed to delete collection: {response.text}")

        return response.json() if response.status_code == 200 else {}

    def create_collection_for_chunks(self) -> Dict[str, Any]:
        """
        Create collection specifically for text chunks

        Returns:
            API response
        """
        schema = {
            "name": self.collection_name,
            "fields": [
                {"name": "chunk_id", "type": "int32"},
                {"name": "text", "type": "string"},
                {"name": "strategy", "type": "string", "facet": True},
                {"name": "metadata", "type": "string", "optional": True},
                {"name": "chunk_index", "type": "int32"}
            ]
        }

        # Delete collection if exists
        try:
            self.delete_collection()
        except:
            pass  # Collection might not exist

        # Create new collection
        response = requests.post(
            f'{self.base_url}/collections',
            json=schema,
            headers=self.headers
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create collection: {response.text}")

        return response.json()

    def insert_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Insert multiple documents into collection

        Args:
            documents: List of documents to insert

        Returns:
            Insert results
        """
        import json
        import time

        # Prepare documents with IDs and flatten nested structures
        docs_with_ids = []
        timestamp = int(time.time() * 1000)  # Use millisecond timestamp for uniqueness

        for i, doc in enumerate(documents):
            doc_copy = doc.copy()

            # Flatten nested 'likes' object if present
            if 'likes' in doc_copy and isinstance(doc_copy['likes'], dict):
                likes = doc_copy.pop('likes')
                if 'color' in likes:
                    doc_copy['likes_color'] = likes['color']
                if 'food' in likes:
                    doc_copy['likes_food'] = likes['food']

            # Generate unique ID using timestamp + index to avoid conflicts when appending
            if 'id' not in doc_copy:
                doc_copy['id'] = f"{timestamp}_{i}"
            docs_with_ids.append(doc_copy)

        # Import documents - each document as a JSON line
        import_data = '\n'.join([json.dumps(doc) for doc in docs_with_ids])

        response = requests.post(
            f'{self.base_url}/collections/{self.collection_name}/documents/import',
            data=import_data,
            headers={**self.headers, 'Content-Type': 'text/plain'}
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to insert documents: {response.text}")

        return {
            "success": True,
            "count": len(docs_with_ids),
            "results": response.text
        }

    def search(
        self,
        q: str = '*',
        filter_by: str = '',
        query_by: str = 'text',
        per_page: int = 250
    ) -> Dict[str, Any]:
        """
        Search documents

        Args:
            q: Search query
            filter_by: Filter expression
            query_by: Fields to query
            per_page: Results per page

        Returns:
            Search results
        """
        params = {
            'q': q,
            'query_by': query_by,
            'per_page': per_page
        }

        if filter_by:
            params['filter_by'] = filter_by

        response = requests.get(
            f'{self.base_url}/collections/{self.collection_name}/documents/search',
            params=params,
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Search failed: {response.text}")

        return response.json()

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        response = requests.get(
            f'{self.base_url}/collections/{self.collection_name}',
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get collection info: {response.text}")

        return response.json()

    def health_check(self) -> Dict[str, Any]:
        """
        Check if Typesense is healthy

        Returns:
            Dictionary with 'healthy' bool and optional 'error' message
        """
        try:
            response = requests.get(f'{self.base_url}/health', timeout=2)
            if response.status_code == 200:
                return {'healthy': True}
            else:
                return {
                    'healthy': False,
                    'error': f'Typesense returned status {response.status_code}'
                }
        except requests.exceptions.ConnectionError:
            return {
                'healthy': False,
                'error': f'Cannot connect to Typesense at {self.base_url}. Is it running?'
            }
        except requests.exceptions.Timeout:
            return {
                'healthy': False,
                'error': 'Typesense connection timed out'
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': f'Typesense error: {str(e)}'
            }

    def create_vector_collection(self, embedding_dim: int = 768) -> Dict[str, Any]:
        """
        Create collection with vector search support

        Args:
            embedding_dim: Dimension of embedding vectors (default: 768 for nomic-embed-text)

        Returns:
            API response
        """
        schema = {
            "name": self.collection_name,
            "fields": [
                {"name": "text", "type": "string"},
                {"name": "embedding", "type": "float[]", "num_dim": embedding_dim}
            ]
        }

        # Delete collection if exists
        try:
            self.delete_collection()
        except:
            pass  # Collection might not exist

        # Create new collection
        response = requests.post(
            f'{self.base_url}/collections',
            json=schema,
            headers=self.headers
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create collection: {response.text}")

        return response.json()

    def vector_search(
        self,
        query_embedding: List[float],
        k: int = 5
    ) -> Dict[str, Any]:
        """
        Search documents using vector similarity

        Args:
            query_embedding: Query embedding vector
            k: Number of results to return

        Returns:
            Search results
        """
        # Format the vector query for Typesense
        embedding_str = ','.join([str(x) for x in query_embedding])
        vector_query = f'embedding:([{embedding_str}], k:{k})'

        # Use multi_search endpoint to avoid URL length limits
        search_params = {
            'collection': self.collection_name,
            'q': '*',
            'vector_query': vector_query,
            'exclude_fields': 'embedding'
        }

        response = requests.post(
            f'{self.base_url}/multi_search',
            json={'searches': [search_params]},
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Vector search failed: {response.text}")

        # Extract results from multi_search response format
        result = response.json()
        if 'results' in result and len(result['results']) > 0:
            return result['results'][0]
        return result

    def create_auto_embedding_collection(self, model_name: str = 'ts/all-MiniLM-L12-v2') -> Dict[str, Any]:
        """
        Create collection with auto-embedding support using Typesense's built-in models

        Args:
            model_name: Typesense embedding model (default: ts/all-MiniLM-L12-v2)

        Returns:
            API response
        """
        schema = {
            "name": self.collection_name,
            "fields": [
                {
                    "name": "text",
                    "type": "string"
                },
                {
                    "name": "embedding",
                    "type": "float[]",
                    "embed": {
                        "from": ["text"],
                        "model_config": {
                            "model_name": model_name
                        }
                    }
                }
            ]
        }

        # Delete collection if exists
        try:
            self.delete_collection()
        except:
            pass  # Collection might not exist

        # Create new collection
        response = requests.post(
            f'{self.base_url}/collections',
            json=schema,
            headers=self.headers
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create collection: {response.text}")

        return response.json()

    def semantic_search(
        self,
        query: str,
        k: int = 5
    ) -> Dict[str, Any]:
        """
        Search documents using semantic similarity with auto-generated embeddings

        Args:
            query: Search query text
            k: Number of results to return

        Returns:
            Search results
        """
        params = {
            'q': query,
            'query_by': 'embedding',
            'exclude_fields': 'embedding',
            'per_page': k
        }

        response = requests.get(
            f'{self.base_url}/collections/{self.collection_name}/documents/search',
            params=params,
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Semantic search failed: {response.text}")

        return response.json()

    def hybrid_search(
        self,
        query: str,
        filter_by: str = '',
        query_by: str = 'text',
        per_page: int = 250
    ) -> Dict[str, Any]:
        """
        Perform hybrid search combining keyword search with optional filters

        This method performs text-based search on the specified fields,
        which can be combined with filters for better results.

        Args:
            query: Search query
            filter_by: Filter expression
            query_by: Fields to query (default: 'text')
            per_page: Results per page

        Returns:
            Search results
        """
        params = {
            'q': query,
            'query_by': query_by,
            'per_page': per_page,
            'sort_by': '_text_match:desc'  # Sort by text match score
        }

        if filter_by:
            params['filter_by'] = filter_by

        response = requests.get(
            f'{self.base_url}/collections/{self.collection_name}/documents/search',
            params=params,
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Hybrid search failed: {response.text}")

        return response.json()
