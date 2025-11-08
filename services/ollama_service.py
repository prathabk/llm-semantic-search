"""
Ollama Service - Handle LLM interactions for text structuring
"""
import json
import subprocess
import re
from typing import List, Dict, Any, Optional


class OllamaService:
    """Service to interact with Ollama for text processing"""

    AVAILABLE_MODELS = [
        'gemma3:270m',
        'gemma3:1b',
        'gemma3:4b',
        'gemma3:12b'
    ]

    def __init__(self, model: str = 'gemma3:1b'):
        """
        Initialize Ollama service

        Args:
            model: The Ollama model to use (default: gemma2:2b)
        """
        self.model = model

    def structure_text(self, text: str, schema_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert unstructured text to structured JSON using LLM

        Args:
            text: Unstructured text to process
            schema_hint: Optional hint about the desired schema

        Returns:
            Structured data as dictionary
        """
        if not schema_hint:
            schema_hint = """
            Extract information in this JSON format:
            {
                "name": "person's name if mentioned, otherwise null",
                "gender": "boy or girl",
                "likes": {
                    "color": "favorite color",
                    "food": "favorite food"
                },
                "text": "original text"
            }
            """

        prompt = f"""You are a data extraction assistant. Convert the following text into structured JSON.

Schema: {schema_hint}

Text: {text}

Return ONLY valid JSON, no explanations or markdown. If a field is not mentioned, use null or best guess."""

        try:
            # Call Ollama CLI
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                raise Exception(f"Ollama error: {result.stderr}")

            # Parse JSON response
            response = result.stdout.strip()

            # Extract JSON from response (handle markdown code blocks)
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                response = response[json_start:json_end].strip()
            elif '```' in response:
                json_start = response.find('```') + 3
                json_end = response.find('```', json_start)
                response = response[json_start:json_end].strip()

            structured_data = json.loads(response)

            # Ensure text field is preserved
            if 'text' not in structured_data:
                structured_data['text'] = text

            return structured_data

        except subprocess.TimeoutExpired:
            raise Exception("Ollama request timed out")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {result.stdout}")
        except Exception as e:
            raise Exception(f"Ollama processing failed: {str(e)}")

    def structure_batch(self, texts: List[str], schema_hint: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Process multiple texts into structured data

        Args:
            texts: List of unstructured texts
            schema_hint: Optional schema hint

        Returns:
            List of structured data dictionaries
        """
        results = []
        for text in texts:
            if text.strip():  # Skip empty lines
                structured = self.structure_text(text.strip(), schema_hint)
                results.append(structured)
        return results

    def structure_log_line(self, log_line: str) -> Dict[str, Any]:
        """
        Parse nginx log line into structured data

        Expected format:
        2024-01-15 10:23:45 [INFO] 192.168.1.100 - GET /api/users - 200 - 45ms - requestId: req_001 userId: user_123

        Args:
            log_line: Single nginx log line

        Returns:
            Structured log data dictionary
        """
        # Regex pattern to parse nginx log format
        pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(\S+)\s+-\s+(\w+)\s+(\S+)\s+-\s+(\d+)\s+-\s+(\d+)ms\s+-\s+requestId:\s+(\S+)\s+userId:\s+(\S+)(?:\s+-\s+(.*))?$'

        match = re.match(pattern, log_line.strip())

        if not match:
            # If regex doesn't match, return basic structure with the raw log
            return {
                'timestamp': '',
                'log_level': 'UNKNOWN',
                'ip_address': '',
                'http_method': '',
                'endpoint': '',
                'status_code': 0,
                'response_time': 0,
                'request_id': '',
                'user_id': '',
                'error_message': '',
                'text': log_line,
                'parse_error': True
            }

        # Extract matched groups
        timestamp = match.group(1)
        log_level = match.group(2)
        ip_address = match.group(3)
        http_method = match.group(4)
        endpoint = match.group(5)
        status_code = int(match.group(6))
        response_time = int(match.group(7))
        request_id = match.group(8)
        user_id = match.group(9)
        error_message = match.group(10) if match.group(10) else ''

        return {
            'timestamp': timestamp,
            'log_level': log_level,
            'ip_address': ip_address,
            'http_method': http_method,
            'endpoint': endpoint,
            'status_code': status_code,
            'response_time': response_time,
            'request_id': request_id,
            'user_id': user_id,
            'error_message': error_message,
            'text': log_line,
            'parse_error': False
        }

    def structure_logs_batch(self, log_lines: List[str]) -> List[Dict[str, Any]]:
        """
        Parse multiple nginx log lines into structured data

        Args:
            log_lines: List of nginx log lines

        Returns:
            List of structured log data dictionaries
        """
        results = []
        for log_line in log_lines:
            if log_line.strip():  # Skip empty lines
                structured = self.structure_log_line(log_line.strip())
                results.append(structured)
        return results

    def extract_search_keywords(self, natural_query: str) -> str:
        """
        Extract search keywords from natural language query

        Args:
            natural_query: Natural language query from user

        Returns:
            Search keywords suitable for text search
        """
        prompt = f"""Extract only the key search terms from this question. Return ONLY the important keywords that should be searched in logs, without any extra words or explanations.

Question: {natural_query}

Rules:
- Extract only nouns, technical terms, and error types
- Remove question words (what, when, where, how, why, find, show, provide, etc.)
- Remove filler words (the, and, or, a, an, in, on, at, etc.)
- Keep technical terms like "timeout", "error", "failure", "database", "authentication"
- Keep specific identifiers if mentioned (user IDs, request IDs, endpoints)
- Return 2-5 keywords maximum

Keywords:"""

        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                # Fallback: return original query
                return natural_query

            keywords = result.stdout.strip()

            # Clean up the response (remove quotes, extra whitespace)
            keywords = keywords.replace('"', '').replace("'", '').strip()

            # If response is empty or too long, return original
            if not keywords or len(keywords) > 100:
                return natural_query

            return keywords

        except Exception as e:
            # Fallback: return original query
            print(f"Keyword extraction failed: {e}")
            return natural_query

    def translate_query_to_filter(self, query: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate natural language query to Typesense filter

        Args:
            query: Natural language query
            schema: Schema of the data

        Returns:
            Dictionary with filter_by and q parameters for Typesense
        """
        # Detect meta-analytical queries that need all data
        query_lower = query.lower()
        meta_patterns = [
            'how many colors', 'how many foods', 'what colors', 'what foods',
            'list all colors', 'list all foods', 'show all colors', 'show all foods',
            'colors are mentioned', 'foods are mentioned', 'colors mentioned', 'foods mentioned',
            'distinct colors', 'distinct foods', 'unique colors', 'unique foods',
            'different colors', 'different foods'
        ]

        # If it's a meta-analytical query, return all documents
        if any(pattern in query_lower for pattern in meta_patterns):
            print(f"Meta-analytical query detected: {query}")
            return {
                "q": "*",
                "filter_by": "",
                "natural_answer": f"analysis of all data to answer: {query}"
            }

        prompt = f"""You are a query translator. Convert natural language queries into Typesense search filters.

AVAILABLE FIELDS (use exactly these names):
- name: person's name (string)
- gender: "boy" or "girl" (NOT "male"/"female")
- likes_color: favorite color (string)
- likes_food: favorite food (string)
- text: full text content (string)

Query: "{query}"

RULES:
1. Use exact field names from above
2. Use := for exact match, : for contains
3. Combine filters with &&
4. For food/color queries, use likes_food or likes_color
5. For gender queries, use "boy" or "girl"
6. For counting/listing queries about specific attributes, use appropriate filter
7. For aggregate queries (how many distinct X), fetch all documents with q="*" and filter_by=""

Return ONLY valid JSON:
{{
    "q": "keyword or *",
    "filter_by": "field_name:=value && field_name:value",
    "natural_answer": "description"
}}

EXAMPLES:
Query: "how many boys like blue color"
{{"q": "*", "filter_by": "gender:=boy && likes_color:=blue", "natural_answer": "boys who like blue color"}}

Query: "girls who like biryani"
{{"q": "*", "filter_by": "gender:=girl && likes_food:biryani", "natural_answer": "girls who like biryani"}}

Query: "who likes red color"
{{"q": "*", "filter_by": "likes_color:=red", "natural_answer": "people who like red color"}}

Query: "find people who like curd rice"
{{"q": "*", "filter_by": "likes_food:curd rice", "natural_answer": "people who like curd rice"}}

Query: "list all boys"
{{"q": "*", "filter_by": "gender:=boy", "natural_answer": "all boys"}}

Query: "list all people"
{{"q": "*", "filter_by": "", "natural_answer": "all people in the database"}}

Now process: "{query}"
Return JSON only, no explanation:"""

        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=20
            )

            if result.returncode != 0:
                raise Exception(f"Ollama error: {result.stderr}")

            response = result.stdout.strip()

            # Extract JSON from response
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                response = response[json_start:json_end].strip()
            elif '```' in response:
                json_start = response.find('```') + 3
                json_end = response.find('```', json_start)
                response = response[json_start:json_end].strip()

            query_params = json.loads(response)

            # Validate filter_by doesn't contain invalid field names
            filter_by = query_params.get('filter_by', '')
            if filter_by and 'field:' in filter_by.lower():
                # LLM used placeholder "field" instead of actual field name
                # Try to infer the correct filter based on query keywords
                query_lower = query.lower()

                # Simple keyword-based fallback
                filters = []
                if 'boy' in query_lower and 'girl' not in query_lower:
                    filters.append('gender:=boy')
                elif 'girl' in query_lower and 'boy' not in query_lower:
                    filters.append('gender:=girl')

                # Color keywords
                colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'white']
                for color in colors:
                    if color in query_lower:
                        filters.append(f'likes_color:={color}')
                        break

                # Food keywords
                foods = ['rice', 'biryani', 'briyani', 'curd', 'sambar', 'chicken']
                for food in foods:
                    if food in query_lower:
                        # Handle multi-word foods
                        if 'curd rice' in query_lower:
                            filters.append('likes_food:curd rice')
                        elif 'sambar rice' in query_lower:
                            filters.append('likes_food:sambar rice')
                        elif 'chicken' in query_lower and 'biryani' in query_lower:
                            filters.append('likes_food:chicken biryani')
                        else:
                            filters.append(f'likes_food:{food}')
                        break

                query_params['filter_by'] = ' && '.join(filters) if filters else ''

            return query_params

        except Exception as e:
            # Fallback to simple search
            return {
                "q": query,
                "filter_by": "",
                "natural_answer": f"search results for: {query}"
            }

    def generate_natural_answer(
        self,
        query: str,
        results: List[Dict[str, Any]],
        found_count: int,
        custom_instructions: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a natural language answer based on query and results

        Args:
            query: The original user query
            results: List of matching documents
            found_count: Number of results found
            custom_instructions: Optional custom instruction template with {query}, {found_count}, {search_results} placeholders

        Returns:
            Dictionary with 'answer' and 'context' (the prompt sent to LLM)
        """
        if found_count == 0:
            return {
                "answer": "No results found for your query.",
                "context": ""
            }

        # Prepare context from results
        context = []
        for result in results:
            doc = result.get('document', {})
            context.append({
                'name': doc.get('name', 'Unknown'),
                'gender': doc.get('gender', ''),
                'likes_color': doc.get('likes_color', ''),
                'likes_food': doc.get('likes_food', ''),
                'text': doc.get('text', '')
            })

        # Use custom instructions if provided, otherwise use default
        if custom_instructions:
            # Replace placeholders in custom template
            prompt = custom_instructions.replace('{query}', query)
            prompt = prompt.replace('{found_count}', str(found_count))
            prompt = prompt.replace('{search_results}', json.dumps(context, indent=2))
        else:
            # Default prompt
            prompt = f"""You are a helpful assistant that answers questions based on search results.

User Question: {query}

Search Results ({found_count} found):
{json.dumps(context, indent=2)}

Instructions:
- Answer the question ACCURATELY by counting ALL results provided above
- The search results already contain ONLY the matching documents, so count ALL of them
- If asked "how many people", count the total number of results ({found_count})
- If asked "how many", provide ACCURATE count based on ALL {found_count} results
- When counting by gender: count each gender from ALL results (boy/girl/unknown)
- Example: If there are 2 results with blue color, say "2 people like blue color"
- If asked "who" or "list names", list ALL names from the results
- If asked about preferences, describe what ALL of them like
- DO NOT filter or reduce the count - use ALL {found_count} results
- Be precise with numbers and list names when relevant
- Use natural language

Answer based on ALL {found_count} results:"""

        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=20
            )

            if result.returncode != 0:
                raise Exception(f"Ollama error: {result.stderr}")

            answer = result.stdout.strip()
            return {
                "answer": answer,
                "context": prompt
            }

        except Exception as e:
            # Fallback to simple answer
            names = [doc.get('name', 'Unknown') for doc in context if doc.get('name')]
            fallback_answer = f"Found {found_count} result(s): {', '.join(names)}" if names else f"Found {found_count} matching documents"
            return {
                "answer": fallback_answer,
                "context": prompt
            }

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using Ollama model

        Args:
            prompt: The prompt for text generation
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            # Call Ollama CLI
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                raise Exception(f"Ollama error: {result.stderr}")

            # Return generated text
            response = result.stdout.strip()
            return response

        except subprocess.TimeoutExpired:
            raise Exception("Ollama request timed out")
        except Exception as e:
            raise Exception(f"Text generation failed: {str(e)}")

    @staticmethod
    def check_ollama_availability() -> Dict[str, Any]:
        """
        Check if Ollama is installed and running

        Returns:
            Dictionary with 'available' bool and optional 'error' message
        """
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return {'available': True, 'models': result.stdout}
            else:
                return {
                    'available': False,
                    'error': 'Ollama command failed. Is it installed?'
                }
        except FileNotFoundError:
            return {
                'available': False,
                'error': 'Ollama is not installed. Please install from https://ollama.ai'
            }
        except subprocess.TimeoutExpired:
            return {
                'available': False,
                'error': 'Ollama command timed out. Is the service running?'
            }
        except Exception as e:
            return {
                'available': False,
                'error': f'Ollama error: {str(e)}'
            }

    @staticmethod
    def get_available_models() -> List[str]:
        """Get list of available Ollama models"""
        return OllamaService.AVAILABLE_MODELS

    def generate_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Generate embedding vector for text using Ollama

        Args:
            text: Text to generate embedding for
            model: Optional model override (uses instance model if not provided)

        Returns:
            List of floats representing the embedding vector
        """
        try:
            import requests

            embedding_model = model or self.model

            # Use Ollama API to generate embeddings
            response = requests.post(
                'http://localhost:11434/api/embeddings',
                json={
                    'model': embedding_model,
                    'prompt': text
                },
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"Ollama embedding API error: {response.text}")

            result = response.json()
            return result['embedding']

        except Exception as e:
            raise Exception(f"Embedding generation failed: {str(e)}")

    def generate_embedding_batch(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of texts to generate embeddings for
            model: Optional model override

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text, model)
            embeddings.append(embedding)
        return embeddings
