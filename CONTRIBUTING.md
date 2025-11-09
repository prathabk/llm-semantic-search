# Contributing to Semantic Search Learning Portal

First off, thank you for considering contributing to this project! 🎉

This is an educational project designed to help people learn about semantic search, LLMs, and vector databases through interactive examples. Contributions that make the learning experience better are always welcome.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Guidelines](#project-guidelines)
- [Contributing with AI Tools](#contributing-with-ai-tools)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details**:
  - OS and version
  - Python version
  - Browser and version
  - Typesense version
  - Ollama version and models

**Example bug report:**

```markdown
## Bug: Carousel navigation breaks on mobile Safari

**Environment:**
- iOS 16.5, Safari
- Python 3.10
- Typesense 27.1

**Steps to reproduce:**
1. Open /vectors on iPhone
2. Swipe to navigate slides
3. Slide indicator stops updating

**Expected:** Indicator should track current slide
**Actual:** Indicator stuck on slide 1

**Screenshot:** [attached]
```

### 💡 Suggesting Features

Feature suggestions are welcome! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly
3. **Explain the use case** - how does it improve learning?
4. **Provide examples** if applicable
5. **Consider scope** - does it fit the educational mission?

**Good feature requests:**

- ✅ "Add interactive visualization for attention mechanism"
- ✅ "Create quiz component to test understanding"
- ✅ "Add keyboard shortcuts for slide navigation"

**Out of scope:**

- ❌ Production-level monitoring/alerting
- ❌ User authentication system
- ❌ Commercial features

### 📚 Adding Learning Content

We especially welcome new educational content! Consider adding:

- **New concept pages**: Attention, transformers, RAG, fine-tuning, etc.
- **Interactive visualizations**: Canvas-based demos
- **Real-world examples**: Practical applications
- **Advanced demos**: Building on existing concepts

**Requirements for new content:**

1. ✅ Follow the **slide carousel format** (see CLAUDE.md)
2. ✅ Include **interactive elements** where possible
3. ✅ Use consistent **design system** (colors, fonts, spacing)
4. ✅ Add **clear explanations** with analogies
5. ✅ End with **key takeaways** slide
6. ✅ Link to next/previous concepts

### 🎨 Improving Design

Design improvements should:

- Follow the design system in `CLAUDE.md`
- Improve accessibility (color contrast, screen readers, keyboard nav)
- Enhance mobile responsiveness
- Maintain consistency across pages

### 🐞 Fixing Bugs

Bug fixes are always appreciated! Please:

1. Reference the issue number in your PR
2. Add tests if applicable
3. Update documentation if behavior changes

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Typesense server (Docker recommended)
- Ollama with at least `gemma3:1b` model

### Setup Steps

1. **Fork the repository**

   Click the "Fork" button on GitHub.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/llm-semantic-search.git
   cd llm-semantic-search
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/llm-semantic-search.git
   ```

4. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

6. **Start Typesense**

   ```bash
   docker run -d -p 8108:8108 -v $(pwd)/typesense-data:/data \
     typesense/typesense:27.1 --data-dir /data \
     --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se --enable-cors
   ```

7. **Pull Ollama models**

   ```bash
   ollama pull gemma3:1b
   ```

8. **Run the application**

   ```bash
   python3 app.py
   ```

9. **Verify everything works**

   - Visit http://localhost:9010
   - Navigate through learning pages
   - Try a demo
   - Run tests: `./venv/bin/python test_demo.py`

## Project Guidelines

### Design System

**IMPORTANT:** All UI changes must follow the design system in `CLAUDE.md`.

**Key principles:**

- Use CSS variables from `static/css/style.css`
- Follow slide carousel format for learning pages
- Maintain consistent spacing (8px increments)
- Use standard typography scale
- Keep color palette consistent

**Example: Adding a new page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>New Concept - Semantic Search Course</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/carousel.css') }}">
</head>
<body>
    <div class="container">
        <a href="/" class="home-link">← Back to Home</a>

        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>

        <div class="carousel-container">
            <div class="carousel-wrapper" id="carouselWrapper">
                <!-- Slides here -->
            </div>
        </div>

        <!-- Navigation controls -->
    </div>
</body>
</html>
```

See `templates/vectors.html` as reference implementation.

### Code Organization

```
New Service:
1. Create in services/
2. Export from services/__init__.py
3. Use in app.py endpoints
4. Document in DEMO_README.md

New Route:
1. Add to app.py with docstring
2. Create template in templates/
3. Link from navigation
4. Test manually

New Demo:
1. Create template following demo patterns
2. Add API endpoints if needed
3. Add to demo.html hub
4. Document in DEMO_README.md
```

### File Naming

- **Templates**: `snake_case.html` (e.g., `demo_chunking.html`)
- **Python**: `snake_case.py` (e.g., `ollama_service.py`)
- **CSS/JS**: `kebab-case.css` (e.g., `carousel.css`)
- **Routes**: `/kebab-case` (e.g., `/demo/chunking-strategies`)

## Contributing with AI Tools

This project is **optimized for AI-assisted development** with Claude Code and similar tools.

### Using Claude Code

1. **Read CLAUDE.md first**

   The AI will automatically read CLAUDE.md and follow the design system.

2. **Example prompts:**

   ```
   Add a new learning page about "RAG (Retrieval Augmented Generation)"
   following the slide carousel format in CLAUDE.md. Include:
   - 8-10 slides explaining RAG concept
   - Interactive visualization showing document retrieval
   - Code examples using our TypesenseService
   - Real-world applications
   - Key takeaways slide
   ```

   ```
   Create a new demo showing hybrid search (combining keyword + semantic)
   using existing TypesenseService. Add UI to toggle between search modes
   and visualize result differences.
   ```

3. **Review AI-generated code**

   - Test locally
   - Check design system compliance
   - Verify slide navigation works
   - Test on mobile
   - Run tests

4. **AI best practices:**

   - ✅ Reference CLAUDE.md in prompts
   - ✅ Ask for tests alongside code
   - ✅ Request inline documentation
   - ✅ Specify slide count for new pages
   - ❌ Don't blindly accept generated code
   - ❌ Don't skip manual testing

### Key Files for AI Context

When using AI tools, these files provide important context:

- **CLAUDE.md** - Design system, conventions, patterns
- **DEMO_README.md** - Architecture, API patterns
- **services/** - Service layer examples
- **templates/vectors.html** - Reference slide implementation

## Pull Request Process

### Before Submitting

- [ ] Read `CLAUDE.md` for design guidelines
- [ ] Test locally (run `python3 app.py`)
- [ ] Run test suite (`./venv/bin/python test_demo.py`)
- [ ] Check on mobile/different browsers
- [ ] Update documentation if needed
- [ ] Add yourself to CONTRIBUTORS.md (if exists)

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Design improvement
- [ ] Performance improvement

## Checklist

- [ ] Follows design system in CLAUDE.md
- [ ] Tested locally
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Mobile responsive
- [ ] No console errors

## Screenshots (if UI changes)

[Add screenshots]

## Additional Notes

Any context or discussion points
```

### Review Process

1. **Automated checks**: Tests must pass
2. **Code review**: Maintainer will review for:
   - Design system compliance
   - Code quality
   - Educational value
   - Performance
3. **Feedback**: Address review comments
4. **Approval**: Maintainer approves and merges

### After Merge

- Your contribution will be in the next release
- Update your fork: `git pull upstream main`
- Close related issues

## Style Guidelines

### Python Code

Follow PEP 8 with these specifics:

```python
# Good
def structure_text(text: str, model: str = 'gemma3:1b') -> Dict[str, Any]:
    """
    Structure unstructured text using LLM.

    Args:
        text: Input text to structure
        model: Ollama model name

    Returns:
        Structured data dictionary
    """
    # Implementation
    pass

# Bad - no types, no docstring
def structure_text(text, model='gemma3:1b'):
    pass
```

**Key points:**

- ✅ Use type hints
- ✅ Write docstrings
- ✅ 4 spaces (no tabs)
- ✅ Max line length: 100 chars
- ✅ Meaningful variable names

### HTML/Templates

```html
<!-- Good: Semantic, indented -->
<div class="slide-content">
    <div class="slide-header">
        <h2>Title</h2>
        <p class="slide-subtitle">Subtitle</p>
    </div>

    <div class="example-box">
        <p>Content</p>
    </div>
</div>

<!-- Bad: Inline styles, no structure -->
<div style="padding: 20px">
    <h2 style="color: blue">Title</h2>
    <p>Content</p>
</div>
```

**Key points:**

- ✅ Use semantic HTML
- ✅ Follow design system classes
- ✅ No inline styles (use CSS variables)
- ✅ Proper indentation
- ✅ Accessible (alt text, ARIA labels)

### JavaScript

```javascript
// Good: Clear, documented
function updateSlide() {
    const offset = -currentSlide * 100;
    carouselWrapper.style.transform = `translateX(${offset}%)`;

    // Update progress bar
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    progressFill.style.width = `${progress}%`;

    updateIndicators();
}

// Bad: Unclear, no structure
function update() {
    x.style.transform = `translateX(${-y * 100}%)`;
    z.style.width = `${((y + 1) / t) * 100}%`;
}
```

**Key points:**

- ✅ Meaningful names
- ✅ Comments for complex logic
- ✅ const/let (no var)
- ✅ ES6+ features OK
- ✅ Handle errors gracefully

### CSS

```css
/* Good: Uses variables, clear */
.slide-content {
    padding: var(--spacing-6);
    background: var(--surface);
    border-radius: 8px;
    box-shadow: 0 1px 3px var(--shadow);
}

/* Bad: Magic numbers, no variables */
.content {
    padding: 48px;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}
```

**Key points:**

- ✅ Use CSS variables from style.css
- ✅ Mobile-first responsive design
- ✅ Consistent spacing (8px increments)
- ✅ Clear class names

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Page loads without errors
- [ ] All interactive elements work
- [ ] Navigation (keyboard + mouse)
- [ ] Mobile responsive
- [ ] Different browsers (Chrome, Firefox, Safari)
- [ ] Typesense connection
- [ ] Ollama integration
- [ ] Console has no errors

### Automated Tests

Run the test suite:

```bash
./venv/bin/python test_demo.py
```

If adding new features, add tests:

```python
# In test_demo.py or new test file
def test_new_feature():
    """Test description"""
    # Setup
    service = NewService()

    # Execute
    result = service.new_method()

    # Assert
    assert result is not None
    assert 'expected_key' in result
```

### Testing New Learning Pages

1. Navigate through all slides
2. Test keyboard arrows (←/→)
3. Click slide indicators
4. Verify progress bar updates
5. Test on mobile (swipe if applicable)
6. Check canvas visualizations render
7. Verify all links work

## Documentation

### When to Update Docs

Update documentation when:

- ✅ Adding new features
- ✅ Changing API endpoints
- ✅ Modifying configuration
- ✅ Adding new dependencies
- ✅ Changing UI patterns
- ✅ Adding new learning content

### Which Docs to Update

**README.md**: User-facing changes
- Installation steps
- Usage examples
- API changes
- Troubleshooting

**CLAUDE.md**: Design/development changes
- New UI patterns
- Design system updates
- Code conventions
- Template structures

**DEMO_README.md**: Architecture changes
- New services
- API endpoints
- Demo patterns
- Technical details

**Inline docs**: All code
- Docstrings for functions/classes
- Comments for complex logic
- Type hints

### Documentation Style

```python
def process_query(query: str, model: str = 'gemma3:1b',
                 generative: bool = False) -> Dict[str, Any]:
    """
    Process natural language query and return results.

    Translates the natural language query to Typesense filters,
    executes the search, and optionally generates a natural
    language answer using the LLM.

    Args:
        query: Natural language question (e.g., "who likes blue?")
        model: Ollama model name for LLM operations
        generative: If True, generate natural language answer

    Returns:
        Dictionary with:
            - results: List of matching documents
            - answer: Natural language answer (if generative=True)
            - found: Number of results found

    Raises:
        ValueError: If query is empty
        ConnectionError: If Typesense is unreachable

    Example:
        >>> process_query("find boys who like blue", generative=True)
        {
            'results': [...],
            'answer': 'Found 2 boys who like blue: Balu, Ram',
            'found': 2
        }
    """
```

## Questions?

- **General questions**: [GitHub Discussions](https://github.com/your-username/llm-semantic-search/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/your-username/llm-semantic-search/issues)
- **Feature requests**: [GitHub Issues](https://github.com/your-username/llm-semantic-search/issues) with "enhancement" label

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md (if we create one)
- Release notes
- Project documentation

Thank you for contributing to making semantic search education accessible! 🚀

---

**Remember**: This is an educational project. Prioritize clarity and learning value over complexity. Every contribution should help someone understand these concepts better.
