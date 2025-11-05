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

    def insert_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Insert multiple documents into collection

        Args:
            documents: List of documents to insert

        Returns:
            Insert results
        """
        import json

        # Prepare documents with IDs and flatten nested structures
        docs_with_ids = []
        for i, doc in enumerate(documents):
            doc_copy = doc.copy()

            # Flatten nested 'likes' object if present
            if 'likes' in doc_copy and isinstance(doc_copy['likes'], dict):
                likes = doc_copy.pop('likes')
                if 'color' in likes:
                    doc_copy['likes_color'] = likes['color']
                if 'food' in likes:
                    doc_copy['likes_food'] = likes['food']

            if 'id' not in doc_copy:
                doc_copy['id'] = str(i + 1)
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
