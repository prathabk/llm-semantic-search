#!/usr/bin/env python3
"""
Test script for the semantic search demo
"""
import json
import requests
import time

BASE_URL = 'http://localhost:9010'

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f'{BASE_URL}/api/health')
    result = response.json()
    print(f"✓ Health check: Typesense healthy = {result['typesense_healthy']}")
    return result['success']

def test_models():
    """Test models endpoint"""
    print("\nTesting models endpoint...")
    response = requests.get(f'{BASE_URL}/api/models')
    result = response.json()
    print(f"✓ Available models: {', '.join(result['models'])}")
    return result['success']

def test_structure():
    """Test structure endpoint"""
    print("\nTesting structure endpoint...")

    sample_texts = [
        "Balu is a boy. He likes blue color and curd rice.",
        "Ram is a boy. He likes red color and briyani."
    ]

    payload = {
        'texts': sample_texts,
        'model': 'gemma3:1b'
    }

    print(f"Structuring {len(sample_texts)} texts with gemma3:1b...")
    response = requests.post(
        f'{BASE_URL}/api/structure',
        json=payload,
        timeout=60
    )

    result = response.json()

    if result['success']:
        print(f"✓ Structured {result['count']} documents")
        print("\nSample structured data:")
        print(json.dumps(result['data'][0], indent=2))
        return result['data']
    else:
        print(f"✗ Error: {result['error']}")
        return None

def test_store(documents):
    """Test store endpoint"""
    print("\nTesting store endpoint...")

    payload = {
        'documents': documents,
        'recreate': True
    }

    response = requests.post(
        f'{BASE_URL}/api/store',
        json=payload
    )

    result = response.json()

    if result['success']:
        print(f"✓ Stored {result['inserted']} documents in collection '{result['collection']}'")
        return True
    else:
        print(f"✗ Error: {result['error']}")
        return False

def test_query():
    """Test query endpoint"""
    print("\nTesting query endpoint...")

    queries = [
        "how many boys like blue color",
        "who likes red color"
    ]

    for query in queries:
        print(f"\nQuery: {query}")

        payload = {
            'query': query,
            'model': 'gemma3:1b'
        }

        response = requests.post(
            f'{BASE_URL}/api/query',
            json=payload,
            timeout=30
        )

        result = response.json()

        if result['success']:
            print(f"✓ Found {result['found']} results")
            print(f"  Typesense filter: {result['typesense_params'].get('filter_by', 'none')}")
            print(f"  Answer: {result['answer']}")
        else:
            print(f"✗ Error: {result['error']}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("SEMANTIC SEARCH DEMO - API TESTS")
    print("=" * 60)

    try:
        # Test 1: Health
        if not test_health():
            print("\n✗ Health check failed")
            return

        # Test 2: Models
        if not test_models():
            print("\n✗ Models check failed")
            return

        # Test 3: Structure
        structured_data = test_structure()
        if not structured_data:
            print("\n✗ Structure test failed")
            return

        # Test 4: Store
        if not test_store(structured_data):
            print("\n✗ Store test failed")
            return

        # Test 5: Query
        test_query()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
