# GitHub Pages Setup Guide

This guide explains how to host the **Semantic Search Learning Portal** as static pages on GitHub Pages.

## 📌 What Works on GitHub Pages?

✅ **Learning Modules** (All slides work perfectly):
- 🧬 Knowledge Encoding
- 🤖 Understanding LLMs
- 🔧 LLM Models with Ollama
- ✂️ Text Chunking Strategies
- 💾 Typesense Vector Database
- 🔍 Semantic Search Pipeline & RAG

❌ **Interactive Demos** (Require local Flask/Ollama/Typesense):
- Full Pipeline Demo
- Query Demo
- Similarity Techniques Demo
- Log Analysis Demo

> **Note**: The demo page shows an informational message explaining how to run demos locally.

## 🚀 Quick Setup

### Option 1: Using the Conversion Script (Recommended)

1. **Run the conversion script** (already done if you see `docs/` folder):

   ```bash
   python3 convert_to_static.py
   ```

   This creates static HTML files in the `docs/` folder.

2. **Commit the changes**:

   ```bash
   git add docs/ convert_to_static.py
   git commit -m "Add static site for GitHub Pages"
   git push origin main
   ```

3. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select **Deploy from a branch**
   - Choose branch: `main` and folder: `/docs`
   - Click **Save**

4. **Wait a few minutes** and visit:
   ```
   https://YOUR-USERNAME.github.io/llm-semantic-search/
   ```

### Option 2: Manual Deployment

If you prefer to deploy from the root folder:

1. **Move all files from `docs/` to root**:

   ```bash
   cp docs/index.html ./
   cp -r docs/*.html ./
   # Keep static/ folder in place
   ```

2. **Update links** in HTML files to reference `static/` directly.

3. **Enable GitHub Pages** with root folder as source.

## 📁 Folder Structure

After running the conversion script:

```
llm-semantic-search/
├── docs/                           # GitHub Pages static site
│   ├── index.html                 # Home page (converted)
│   ├── knowledge_encoding.html    # Learning slides (converted)
│   ├── llm_overview.html
│   ├── vectors.html
│   ├── chunking.html
│   ├── semantic_search.html
│   ├── demo.html                  # Info page (runs locally only)
│   ├── static/                    # CSS/JS assets
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   └── carousel.css
│   │   └── js/
│   │       └── json-formatter.js
│   └── .nojekyll                  # Prevents Jekyll processing
│
├── templates/                     # Original Jinja2 templates
├── app.py                         # Flask app (for local demos)
├── convert_to_static.py           # Conversion script
└── README.md
```

## 🔧 How the Conversion Works

The `convert_to_static.py` script:

1. **Reads Jinja2 templates** from `templates/`
2. **Replaces Flask URLs**:
   - `{{ url_for('static', filename='css/style.css') }}` → `static/css/style.css`
3. **Converts route links**:
   - `href="/vectors"` → `href="vectors.html"`
   - `href="/"` → `href="index.html"`
4. **Copies static assets** (CSS, JS) to `docs/static/`
5. **Creates demo info page** explaining local setup requirement

## 🎨 Updating Content

### Adding New Learning Slides

1. **Create template** in `templates/` following CLAUDE.md guidelines
2. **Add route** in `app.py`
3. **Run conversion**:
   ```bash
   python3 convert_to_static.py
   ```
4. **Commit and push**:
   ```bash
   git add docs/
   git commit -m "Add new learning module"
   git push
   ```

### Updating Existing Pages

1. **Edit template** in `templates/`
2. **Re-run conversion**:
   ```bash
   python3 convert_to_static.py
   ```
3. **Commit and push**

## 🐛 Troubleshooting

### Pages Don't Load / 404 Errors

**Issue**: GitHub Pages shows 404 for your pages

**Solutions**:
- Verify `docs/` folder exists and contains HTML files
- Check GitHub Pages settings: Settings → Pages → Source should be `/docs`
- Wait 2-3 minutes after enabling GitHub Pages
- Clear browser cache

### CSS Not Loading

**Issue**: Pages show but styling is broken

**Solutions**:
- Verify `docs/static/css/` folder exists
- Check HTML files reference `static/css/style.css` (not `{{ url_for... }}`)
- Inspect browser console for 404 errors
- Ensure `.nojekyll` file exists in `docs/`

### Broken Links Between Pages

**Issue**: Clicking navigation cards shows 404

**Solutions**:
- Ensure all `href="/route"` are converted to `href="route.html"`
- Re-run conversion script: `python3 convert_to_static.py`
- Check that all learning pages exist in `docs/`

### Demos Don't Work

**Expected behavior**: Demos require local Flask app

**Solution**: The demo page now shows instructions for running locally. Users need to:
1. Clone the repository
2. Install dependencies
3. Run `python3 app.py`
4. Access demos at `http://localhost:9010/demo`

## 📝 Custom Domain (Optional)

To use a custom domain like `learn-semantic-search.com`:

1. **Create CNAME file** in `docs/`:
   ```bash
   echo "learn-semantic-search.com" > docs/CNAME
   ```

2. **Configure DNS** with your domain provider:
   ```
   Type: CNAME
   Name: www
   Value: YOUR-USERNAME.github.io
   ```

3. **Enable HTTPS** in GitHub Pages settings

## 🔄 Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Edit templates in templates/                            │
│    (Use Flask for local development & testing)             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Run: python3 convert_to_static.py                       │
│    (Converts Jinja2 → Static HTML in docs/)                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. git add docs/ && git commit && git push                 │
│    (Deploy to GitHub Pages automatically)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Visit: https://USERNAME.github.io/llm-semantic-search/  │
│    (Learning slides work, demos show info page)            │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 Live Demo

Once deployed, you can share your learning portal:

**Public URL**: `https://YOUR-USERNAME.github.io/llm-semantic-search/`

**Example**: `https://johndoe.github.io/llm-semantic-search/`

## ✅ What's Included in Static Version?

| Feature | Status | Notes |
|---------|--------|-------|
| Home Page | ✅ Works | Navigation to all modules |
| Knowledge Encoding Slides | ✅ Works | Full slide carousel |
| LLM Overview Slides | ✅ Works | Full slide carousel |
| Chunking Strategies Slides | ✅ Works | Full slide carousel |
| Vector Database Slides | ✅ Works | Full slide carousel |
| Semantic Search Slides | ✅ Works | Full slide carousel |
| Canvas Visualizations | ✅ Works | Pure JavaScript, no backend needed |
| Keyboard Navigation | ✅ Works | Arrow keys for slides |
| Mobile Responsive | ✅ Works | Touch/swipe support |
| Interactive Demos | ❌ Requires local setup | Shows installation guide |

## 📖 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Custom Domain Setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Repository README](README.md) - Full installation guide for local demos

---

**Questions?** Open an issue on GitHub or see the [main README](README.md).
