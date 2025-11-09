#!/usr/bin/env python3
"""
Convert Jinja2 templates to static HTML for GitHub Pages
"""
import re
import os
from pathlib import Path

# Templates to convert (learning pages - slides only, no backend demos)
LEARNING_PAGES = [
    'index.html',
    'knowledge_encoding.html',
    'llm_overview.html',
    'llm_models.html',
    'embeddings.html',
    'vectors.html',
    'chunking.html',
    'demo_chunking_strategies.html',
    'vector_database_slides.html',
    'semantic_search.html',
]

# Demo page (special handling - info page only)
DEMO_PAGE = 'demo.html'

def convert_template_to_static(template_path, output_path):
    """Convert a Jinja2 template to static HTML"""

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace url_for with static paths
    # Pattern: {{ url_for('static', filename='path/to/file') }}
    content = re.sub(
        r"{{\s*url_for\('static',\s*filename='([^']+)'\)\s*}}",
        r'static/\1',
        content
    )

    # Replace route links with .html extensions
    # href="/route" -> href="route.html"
    content = re.sub(r'href="/([\w-]+)"', r'href="\1.html"', content)

    # Special case: href="/" -> href="index.html"
    content = content.replace('href="/"', 'href="index.html"')

    # Write to output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Converted: {template_path} -> {output_path}")

def create_demo_info_page(output_path):
    """Create an informational demo page for static hosting"""

    content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Demos - Semantic Search Course</title>
    <link rel="stylesheet" href="static/css/style.css">
    <style>
        .info-banner {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 2px solid #2563eb;
            border-radius: 12px;
            padding: 32px;
            margin: 32px 0;
            text-align: center;
        }
        .info-banner h2 {
            color: #1e40af;
            margin-top: 0;
        }
        .demo-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 32px;
        }
        .demo-card {
            background: var(--surface);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 24px;
        }
        .demo-card h3 {
            margin-top: 0;
            color: var(--primary);
        }
        .requires-backend {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px;
            margin: 16px 0;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="home-link">← Back to Home</a>

        <header>
            <h1>🚀 Interactive Demos</h1>
            <p class="subtitle">Hands-on Semantic Search with LLMs</p>
        </header>

        <div class="content">
            <div class="info-banner">
                <h2>📌 Interactive Demos Require Local Setup</h2>
                <p style="font-size: 1.1em; line-height: 1.8; margin: 16px 0;">
                    The interactive demos connect to <strong>Ollama</strong> (LLM) and <strong>Typesense</strong> (vector database)<br>
                    which need to be running locally on your machine.
                </p>
                <p style="margin-top: 20px;">
                    <a href="https://github.com/your-username/llm-semantic-search#running-the-application"
                       target="_blank"
                       style="display: inline-block; background: var(--primary); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;">
                        📖 View Installation Guide
                    </a>
                </p>
            </div>

            <h2 style="margin-top: 48px;">Available Demos (Local Setup Required)</h2>

            <div class="demo-list">
                <div class="demo-card">
                    <h3>🔄 Full Pipeline Demo</h3>
                    <p>Complete workflow: Structure text with LLM → Store in Typesense → Query with natural language</p>
                    <div class="requires-backend">
                        <strong>Requires:</strong> Ollama + Typesense running locally
                    </div>
                </div>

                <div class="demo-card">
                    <h3>⚡ Query Demo</h3>
                    <p>Simplified interface for querying pre-loaded data with generative and static answers</p>
                    <div class="requires-backend">
                        <strong>Requires:</strong> Ollama + Typesense running locally
                    </div>
                </div>

                <div class="demo-card">
                    <h3>📊 Similarity Techniques</h3>
                    <p>Compare different similarity algorithms: Jaccard, Cosine, BM25, TF-IDF</p>
                    <div class="requires-backend">
                        <strong>Requires:</strong> Flask backend running
                    </div>
                </div>

                <div class="demo-card">
                    <h3>✂️ Chunking Strategies</h3>
                    <p>Interactive demo showing different text chunking approaches with Typesense</p>
                    <div class="requires-backend">
                        <strong>Requires:</strong> Ollama + Typesense running locally
                    </div>
                </div>

                <div class="demo-card">
                    <h3>💾 Typesense Vector Search</h3>
                    <p>Explore vector similarity search with automatic embeddings</p>
                    <div class="requires-backend">
                        <strong>Requires:</strong> Typesense running locally
                    </div>
                </div>

                <div class="demo-card">
                    <h3>📝 Log Analysis Demo</h3>
                    <p>Semantic search on application logs using LLM-powered parsing</p>
                    <div class="requires-backend">
                        <strong>Requires:</strong> Ollama + Typesense running locally
                    </div>
                </div>
            </div>

            <div style="background: var(--bg); border-radius: 12px; padding: 32px; margin: 48px 0;">
                <h2 style="margin-top: 0;">🎓 Want to Run Demos Locally?</h2>
                <p style="font-size: 1.05em; line-height: 1.8;">
                    Follow these steps to get the interactive demos running on your machine:
                </p>
                <ol style="line-height: 2; font-size: 1.05em;">
                    <li><strong>Clone the repository:</strong> <code>git clone https://github.com/your-username/llm-semantic-search.git</code></li>
                    <li><strong>Install dependencies:</strong> <code>pip install -r requirements.txt</code></li>
                    <li><strong>Start Typesense:</strong> See <a href="https://github.com/your-username/llm-semantic-search#prerequisites" target="_blank">Prerequisites section</a></li>
                    <li><strong>Install Ollama:</strong> <code>curl -fsSL https://ollama.ai/install.sh | sh</code></li>
                    <li><strong>Pull LLM model:</strong> <code>ollama pull gemma3:1b</code></li>
                    <li><strong>Run the app:</strong> <code>python3 app.py</code></li>
                    <li><strong>Open browser:</strong> <a href="http://localhost:9010/demo" target="_blank">http://localhost:9010/demo</a></li>
                </ol>
            </div>

            <div style="text-align: center; margin: 48px 0;">
                <a href="index.html" style="text-decoration: none;">
                    <button class="action-btn" style="padding: 16px 32px; font-size: 1.125em;">
                        ← Back to Learning Modules
                    </button>
                </a>
            </div>
        </div>
    </div>
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Created demo info page: {output_path}")

def main():
    """Main conversion process"""

    templates_dir = Path('templates')
    output_dir = Path('docs')

    print("🔄 Converting templates to static HTML for GitHub Pages...\n")

    # Convert learning pages
    for template in LEARNING_PAGES:
        if template == 'index.html':
            # Skip index.html as we already created it manually
            continue

        template_path = templates_dir / template
        output_path = output_dir / template

        if template_path.exists():
            convert_template_to_static(template_path, output_path)
        else:
            print(f"⚠️  Template not found: {template_path}")

    # Create demo info page
    demo_output = output_dir / DEMO_PAGE
    create_demo_info_page(demo_output)

    print(f"\n✅ Conversion complete! Static site ready in '{output_dir}/' folder")
    print(f"\n📝 Next steps:")
    print(f"   1. Update GitHub repo URLs in demo.html")
    print(f"   2. Enable GitHub Pages in repo settings")
    print(f"   3. Set source to 'docs' folder")
    print(f"   4. Visit: https://your-username.github.io/llm-semantic-search/")

if __name__ == '__main__':
    main()
