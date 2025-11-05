"""
Similarity algorithms for semantic search comparison
"""
import re
import math
from collections import Counter
from typing import List, Dict, Tuple


class SimilarityService:
    """Compare different similarity algorithms for semantic search"""

    # Sample documents for demonstration
    SAMPLE_DOCUMENTS = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast brown fox leaps over a sleepy canine.",
        "The cat sat on the mat and watched the dog sleep.",
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Python is a popular programming language for data science.",
        "JavaScript is widely used for web development.",
        "The weather is sunny and warm today.",
        "It's raining heavily with strong winds outside.",
        "Coffee and tea are popular caffeinated beverages."
    ]

    @staticmethod
    def preprocess_text(text: str) -> List[str]:
        """Convert text to lowercase and split into words"""
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.split()

    @staticmethod
    def jaccard_similarity(query: str, document: str) -> float:
        """
        Jaccard Similarity: |A ∩ B| / |A ∪ B|
        Set-based similarity measure
        """
        query_words = set(SimilarityService.preprocess_text(query))
        doc_words = set(SimilarityService.preprocess_text(document))

        if not query_words or not doc_words:
            return 0.0

        intersection = query_words.intersection(doc_words)
        union = query_words.union(doc_words)

        return len(intersection) / len(union) if union else 0.0

    @staticmethod
    def cosine_similarity_simple(query: str, document: str) -> float:
        """
        Simple Cosine Similarity using word counts
        cos(θ) = (A · B) / (||A|| × ||B||)
        """
        query_words = SimilarityService.preprocess_text(query)
        doc_words = SimilarityService.preprocess_text(document)

        # Create word frequency vectors
        query_counter = Counter(query_words)
        doc_counter = Counter(doc_words)

        # Get all unique words
        all_words = set(query_counter.keys()) | set(doc_counter.keys())

        if not all_words:
            return 0.0

        # Calculate dot product
        dot_product = sum(query_counter.get(word, 0) * doc_counter.get(word, 0)
                         for word in all_words)

        # Calculate magnitudes
        query_magnitude = math.sqrt(sum(count ** 2 for count in query_counter.values()))
        doc_magnitude = math.sqrt(sum(count ** 2 for count in doc_counter.values()))

        if query_magnitude == 0 or doc_magnitude == 0:
            return 0.0

        return dot_product / (query_magnitude * doc_magnitude)

    @staticmethod
    def compute_tf(words: List[str]) -> Dict[str, float]:
        """Compute Term Frequency"""
        word_count = Counter(words)
        total_words = len(words)
        return {word: count / total_words for word, count in word_count.items()}

    @staticmethod
    def compute_idf(documents: List[str]) -> Dict[str, float]:
        """Compute Inverse Document Frequency"""
        doc_count = len(documents)
        word_doc_count = Counter()

        for doc in documents:
            unique_words = set(SimilarityService.preprocess_text(doc))
            for word in unique_words:
                word_doc_count[word] += 1

        idf = {}
        for word, count in word_doc_count.items():
            idf[word] = math.log(doc_count / count)

        return idf

    @staticmethod
    def tfidf_similarity(query: str, document: str, all_documents: List[str]) -> float:
        """
        TF-IDF with Cosine Similarity
        TF-IDF = Term Frequency × Inverse Document Frequency
        """
        # Preprocess
        query_words = SimilarityService.preprocess_text(query)
        doc_words = SimilarityService.preprocess_text(document)

        if not query_words or not doc_words:
            return 0.0

        # Compute IDF from all documents
        idf = SimilarityService.compute_idf(all_documents + [query])

        # Compute TF
        query_tf = SimilarityService.compute_tf(query_words)
        doc_tf = SimilarityService.compute_tf(doc_words)

        # Compute TF-IDF vectors
        all_words = set(query_tf.keys()) | set(doc_tf.keys())

        query_tfidf = {word: query_tf.get(word, 0) * idf.get(word, 0)
                       for word in all_words}
        doc_tfidf = {word: doc_tf.get(word, 0) * idf.get(word, 0)
                     for word in all_words}

        # Calculate cosine similarity
        dot_product = sum(query_tfidf[word] * doc_tfidf[word] for word in all_words)

        query_magnitude = math.sqrt(sum(val ** 2 for val in query_tfidf.values()))
        doc_magnitude = math.sqrt(sum(val ** 2 for val in doc_tfidf.values()))

        if query_magnitude == 0 or doc_magnitude == 0:
            return 0.0

        return dot_product / (query_magnitude * doc_magnitude)

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """
        Levenshtein Distance (Edit Distance)
        Minimum number of edits to transform s1 to s2
        """
        if len(s1) < len(s2):
            return SimilarityService.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def levenshtein_similarity(query: str, document: str) -> float:
        """
        Normalized Levenshtein Similarity (0-1 range)
        1 - (distance / max_length)
        """
        query_lower = query.lower()
        doc_lower = document.lower()

        distance = SimilarityService.levenshtein_distance(query_lower, doc_lower)
        max_length = max(len(query_lower), len(doc_lower))

        if max_length == 0:
            return 1.0

        return 1 - (distance / max_length)

    @staticmethod
    def simple_word_overlap(query: str, document: str) -> float:
        """
        Simple word overlap score
        (Number of matching words) / (Total unique words in query)
        """
        query_words = set(SimilarityService.preprocess_text(query))
        doc_words = set(SimilarityService.preprocess_text(document))

        if not query_words:
            return 0.0

        matching_words = query_words.intersection(doc_words)
        return len(matching_words) / len(query_words)

    @classmethod
    def compare_all_methods(cls, query: str, documents: List[str] = None) -> Dict:
        """
        Compare all similarity methods and return ranked results
        """
        if documents is None:
            documents = cls.SAMPLE_DOCUMENTS

        results = {
            'jaccard': [],
            'cosine': [],
            'tfidf': [],
            'levenshtein': [],
            'word_overlap': []
        }

        # Calculate similarities for each document
        for i, doc in enumerate(documents):
            results['jaccard'].append({
                'doc_id': i,
                'document': doc,
                'score': cls.jaccard_similarity(query, doc)
            })

            results['cosine'].append({
                'doc_id': i,
                'document': doc,
                'score': cls.cosine_similarity_simple(query, doc)
            })

            results['tfidf'].append({
                'doc_id': i,
                'document': doc,
                'score': cls.tfidf_similarity(query, doc, documents)
            })

            results['levenshtein'].append({
                'doc_id': i,
                'document': doc,
                'score': cls.levenshtein_similarity(query, doc)
            })

            results['word_overlap'].append({
                'doc_id': i,
                'document': doc,
                'score': cls.simple_word_overlap(query, doc)
            })

        # Sort each method by score (descending)
        for method in results:
            results[method].sort(key=lambda x: x['score'], reverse=True)

        return results

    @staticmethod
    def get_method_info() -> Dict[str, Dict[str, str]]:
        """
        Return information about each similarity method
        """
        return {
            'jaccard': {
                'name': 'Jaccard Similarity',
                'description': 'Set-based similarity measuring overlap between word sets',
                'formula': '|A ∩ B| / |A ∪ B|',
                'pros': [
                    'Simple and intuitive',
                    'Fast computation',
                    'Good for keyword matching',
                    'No word frequency bias'
                ],
                'cons': [
                    'Ignores word frequency',
                    'No semantic understanding',
                    'Treats all words equally',
                    'No word order consideration'
                ],
                'best_for': 'Exact word matching, duplicate detection, simple keyword search',
                'color': '#ef4444'
            },
            'cosine': {
                'name': 'Cosine Similarity',
                'description': 'Vector-based similarity using word frequency counts',
                'formula': 'cos(θ) = (A · B) / (||A|| × ||B||)',
                'pros': [
                    'Considers word frequency',
                    'Scale-invariant',
                    'Widely used standard',
                    'Better than Jaccard for longer texts'
                ],
                'cons': [
                    'Still no semantic understanding',
                    'Ignores word order',
                    'Vulnerable to synonyms',
                    'Requires same vocabulary'
                ],
                'best_for': 'Document similarity, text classification, information retrieval',
                'color': '#10b981'
            },
            'tfidf': {
                'name': 'TF-IDF + Cosine',
                'description': 'Weighted similarity giving importance to rare words',
                'formula': 'TF-IDF(w) = TF(w) × log(N / DF(w))',
                'pros': [
                    'Reduces common word impact',
                    'Highlights distinctive terms',
                    'Industry standard for search',
                    'Better precision'
                ],
                'cons': [
                    'Requires document corpus',
                    'Still no semantics',
                    'Computationally expensive',
                    'Doesn\'t handle synonyms'
                ],
                'best_for': 'Search engines, document ranking, keyword extraction',
                'color': '#2563eb'
            },
            'levenshtein': {
                'name': 'Levenshtein Distance',
                'description': 'Character-level edit distance between strings',
                'formula': 'min(insertions, deletions, substitutions)',
                'pros': [
                    'Handles typos well',
                    'Character-level precision',
                    'Good for spelling correction',
                    'Detects near-duplicates'
                ],
                'cons': [
                    'Very slow for long texts',
                    'No semantic meaning',
                    'Poor for reworded content',
                    'Sensitive to length differences'
                ],
                'best_for': 'Spell checking, fuzzy matching, DNA sequencing',
                'color': '#f59e0b'
            },
            'word_overlap': {
                'name': 'Word Overlap',
                'description': 'Simple ratio of matching words to query words',
                'formula': '|matching words| / |query words|',
                'pros': [
                    'Extremely fast',
                    'Very simple to understand',
                    'Good baseline metric',
                    'No preprocessing needed'
                ],
                'cons': [
                    'Too simplistic',
                    'Ignores document length',
                    'No weighting scheme',
                    'Poor precision'
                ],
                'best_for': 'Quick baseline, initial filtering, keyword presence check',
                'color': '#8b5cf6'
            }
        }
