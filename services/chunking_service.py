"""
Chunking Service for text splitting strategies
"""
import re
from typing import List, Dict
from services import OllamaService


class ChunkingService:
    """Service for different text chunking strategies"""

    @staticmethod
    def chunk_text(text: str, strategy: str, model: str = 'gemma3:1b') -> List[Dict]:
        """
        Chunk text using specified strategy

        Args:
            text: The text to chunk
            strategy: 'sentence', 'sliding', or 'semantic'
            model: Model to use for semantic chunking

        Returns:
            List of chunk dictionaries with 'text' and 'metadata'
        """
        if strategy == 'sentence':
            return ChunkingService.sentence_chunking(text)
        elif strategy == 'sliding':
            return ChunkingService.sliding_window_chunking(text)
        elif strategy == 'semantic':
            return ChunkingService.semantic_chunking(text, model)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitter (can be improved with NLP libraries)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def sentence_chunking(text: str, sentences_per_chunk: int = 3) -> List[Dict]:
        """
        Sentence-based chunking: Group N sentences per chunk

        Args:
            text: Text to chunk
            sentences_per_chunk: Number of sentences per chunk

        Returns:
            List of chunks
        """
        sentences = ChunkingService.split_into_sentences(text)
        chunks = []

        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            chunk_text = ' '.join(chunk_sentences)

            chunks.append({
                'text': chunk_text,
                'metadata': f'Sentences {i+1}-{min(i+sentences_per_chunk, len(sentences))}'
            })

        return chunks

    @staticmethod
    def sliding_window_chunking(text: str, window_size: int = 3, stride: int = 2) -> List[Dict]:
        """
        Sliding window chunking: Overlapping chunks

        Args:
            text: Text to chunk
            window_size: Number of sentences per window
            stride: How many sentences to move forward

        Returns:
            List of chunks
        """
        sentences = ChunkingService.split_into_sentences(text)
        chunks = []

        for i in range(0, len(sentences), stride):
            chunk_sentences = sentences[i:i + window_size]
            if not chunk_sentences:
                break

            chunk_text = ' '.join(chunk_sentences)

            chunks.append({
                'text': chunk_text,
                'metadata': f'Window: Sentences {i+1}-{min(i+window_size, len(sentences))} (stride={stride})'
            })

            # Stop if we've covered all sentences
            if i + window_size >= len(sentences):
                break

        return chunks

    @staticmethod
    def semantic_chunking(text: str, model: str = 'gemma3:1b') -> List[Dict]:
        """
        Semantic chunking: Use LLM to identify topic boundaries

        Args:
            text: Text to chunk
            model: Ollama model to use

        Returns:
            List of chunks
        """
        sentences = ChunkingService.split_into_sentences(text)

        # Use LLM to identify topic boundaries
        ollama = OllamaService(model=model)

        # Create prompt for LLM to identify topics
        numbered_sentences = '\n'.join([f"{i+1}. {s}" for i, s in enumerate(sentences)])

        prompt = f"""Analyze the following sentences and identify topic boundaries. Group consecutive sentences that discuss the same topic or theme.

Sentences:
{numbered_sentences}

Provide topic groupings in this format:
Topic 1 (Sentences X-Y): Brief topic name
Topic 2 (Sentences Z-W): Brief topic name

Be concise. Only list the groupings."""

        try:
            response = ollama.generate_text(prompt)

            # Parse LLM response to extract groupings
            chunks = ChunkingService._parse_semantic_response(response, sentences)

            # Fallback to sentence chunking if parsing fails
            if not chunks:
                return ChunkingService.sentence_chunking(text)

            return chunks

        except Exception as e:
            print(f"Semantic chunking failed: {e}")
            # Fallback to sentence-based chunking
            return ChunkingService.sentence_chunking(text)

    @staticmethod
    def _parse_semantic_response(response: str, sentences: List[str]) -> List[Dict]:
        """Parse LLM response to extract topic groupings"""
        chunks = []

        # Try to extract sentence ranges from response
        # Look for patterns like "1-3", "4-6", etc.
        pattern = r'(\d+)-(\d+)'
        matches = re.findall(pattern, response)

        if matches:
            for start_str, end_str in matches:
                start = int(start_str) - 1  # Convert to 0-indexed
                end = int(end_str)

                if 0 <= start < len(sentences) and start < end <= len(sentences):
                    chunk_sentences = sentences[start:end]
                    chunk_text = ' '.join(chunk_sentences)

                    # Extract topic name from response if possible
                    topic_match = re.search(rf'{start_str}-{end_str}[:\)]?\s*(.+?)(?:\n|$)', response)
                    topic = topic_match.group(1).strip() if topic_match else f'Topic {len(chunks)+1}'

                    chunks.append({
                        'text': chunk_text,
                        'metadata': f'Topic: {topic} (Sentences {start+1}-{end})'
                    })

        return chunks
