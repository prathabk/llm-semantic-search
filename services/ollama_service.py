"""
Ollama Service - Handle LLM interactions for text structuring
"""
import json
import subprocess
from typing import List, Dict, Any, Optional


class OllamaService:
    """Service to interact with Ollama for text processing"""

    AVAILABLE_MODELS = [
        'gemma3:270m',
        'gemma3:1b',
        'gemma3:4b'
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
        found_count: int
    ) -> str:
        """
        Generate a natural language answer based on query and results

        Args:
            query: The original user query
            results: List of matching documents
            found_count: Number of results found

        Returns:
            Natural language answer string
        """
        if found_count == 0:
            return "No results found for your query."

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

        prompt = f"""You are a helpful assistant that answers questions based on search results.

User Question: {query}

Search Results ({found_count} found):
{json.dumps(context, indent=2)}

Instructions:
- Answer the question directly and naturally
- If asked "how many", provide count with details (e.g., "1 boy" or "3 boys and 2 girls")
- If asked "who" or "list names", list the names clearly
- If asked about preferences, describe what they like
- If asked about colors/foods mentioned, analyze all results and count unique values
- For "how many colors mentioned", count distinct colors from likes_color field
- For "how many foods mentioned", count distinct foods from likes_food field
- Be concise but informative
- Use natural language

Answer:"""

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
            return answer

        except Exception as e:
            # Fallback to simple answer
            names = [doc.get('name', 'Unknown') for doc in context if doc.get('name')]
            if names:
                return f"Found {found_count} result(s): {', '.join(names)}"
            return f"Found {found_count} matching documents"

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
