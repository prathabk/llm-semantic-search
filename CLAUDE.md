# CLAUDE.md - Project Guidelines for Semantic Search Learning Portal

This document provides guidelines for maintaining consistency across all illustrations, visualizations, and content in the Semantic Search with LLM learning portal.

## Design System

### Color Palette

Use CSS variables defined in `static/css/style.css`:

```css
--primary: #2563eb           /* Primary blue for buttons, links, accents */
--primary-dark: #1e40af      /* Darker blue for hover states */
--text: #0f172a              /* Main text color */
--text-secondary: #64748b    /* Secondary text, labels */
--bg: #f8fafc                /* Page background */
--surface: #ffffff           /* Card/surface background */
--border: #e2e8f0            /* Borders, dividers */
--shadow: rgba(15, 23, 42, 0.08)  /* Subtle shadows */
```

### Additional Colors for Visualizations

- **Red**: `#ef4444` (for Vector A, errors, warnings)
- **Green**: `#10b981` (for Vector B, success states)
- **Yellow**: `#fef3c7` (for highlights, important notes)
- **Gray (light)**: `#cbd5e1` (for secondary/ghost elements)

### Typography

- **Font Family**: `-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', system-ui, sans-serif`
- **Monospace**: `'SF Mono', Monaco, 'Courier New', monospace`

**Font Weights & Sizes**:
- `h1`: 2.5em, 700 weight, -0.025em letter-spacing
- `h2`: 1.875em, 700 weight, -0.025em letter-spacing
- `h3`: 1.375em, 600 weight
- Body text: 1em, 400 weight, 1.75 line-height
- Secondary text: 0.9375em, 400-500 weight
- Code/Math: 0.9375em, monospace

### Spacing Scale

Use consistent spacing multiples of 8px:
- `8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px, 56px`

## Layout Guidelines

### Container Structure

```html
<div class="container">
    <a href="/" class="home-link">← Back to Home</a>

    <header>
        <h1>📊 Page Title</h1>
        <p class="subtitle">Short Description</p>
    </header>

    <div class="content">
        <!-- Main content here -->
    </div>
</div>
```

### Card Components

**Navigation Cards** (Home page):
```html
<a href="/route" class="nav-card">
    <h2>🎨 Title</h2>
    <p>Description text explaining the concept.</p>
</a>
```

**Example Boxes** (Content pages):
```html
<div class="example-box">
    <h3>Example Title</h3>
    <p>Content here...</p>
</div>
```

**Interactive Sections**:
```html
<div class="interactive-section">
    <p style="text-align: center; margin-bottom: 10px;">
        <strong>Interactive Demo:</strong> Description
    </p>

    <canvas id="canvasId" width="600" height="400"></canvas>

    <div class="controls">
        <div class="control-group">
            <label for="inputId">Label:</label>
            <input type="range" id="inputId" min="0" max="10" value="5">
            <span id="valueId">5</span>
        </div>
    </div>

    <div class="vector-math">
        Mathematical formulas or output
    </div>
</div>
```

## Slide-Based Carousel Presentation Format

**All concept pages should use the slide carousel format for presentation-style learning.**

### Why Use Slide Format?

- **Focus**: One concept at a time keeps learners focused
- **Progressive**: Natural progression through material
- **Presentation-ready**: Can be used for teaching/presenting
- **Professional**: Modern, clean interface
- **Navigation**: Easy to jump between concepts or review
- **Engagement**: Interactive elements work seamlessly within slides

### Slide Structure

Include `carousel.css` in addition to main stylesheet:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/carousel.css') }}">
```

### Container Setup with Carousel

```html
<div class="container">
    <a href="/" class="home-link">← Back to Home</a>

    <!-- Progress Bar -->
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>

    <!-- Carousel Container -->
    <div class="carousel-container">
        <div class="carousel-wrapper" id="carouselWrapper">

            <!-- Slide 1: Title Slide -->
            <div class="slide">
                <div class="slide-content title-slide">
                    <h1>📊 Concept Name</h1>
                    <p class="subtitle">Short Description</p>
                    <div class="course-info">
                        <p>Introduction paragraph...</p>
                        <p style="margin-top: 24px; color: var(--text-secondary);">
                            Use arrow keys or buttons below to navigate
                        </p>
                    </div>
                </div>
            </div>

            <!-- Slide 2: Content Slide -->
            <div class="slide">
                <div class="slide-content">
                    <div class="slide-header">
                        <h2>Slide Title</h2>
                        <p class="slide-subtitle">Subtitle</p>
                    </div>

                    <!-- Content here -->
                    <p>Content...</p>

                    <div class="example-box">
                        <h3>Example</h3>
                        <p>Example content...</p>
                    </div>
                </div>
            </div>

            <!-- Add more slides... -->

            <!-- Final Slide: Key Takeaways -->
            <div class="slide">
                <div class="slide-content">
                    <div class="slide-header">
                        <h2>Key Takeaways</h2>
                        <p class="slide-subtitle">Summary</p>
                    </div>

                    <ul style="font-size: 1.125em; line-height: 2;">
                        <li>Takeaway 1</li>
                        <li>Takeaway 2</li>
                    </ul>

                    <div style="text-align: center; margin-top: 60px;">
                        <a href="/next-concept" style="text-decoration: none;">
                            <button class="action-btn" style="padding: 16px 32px; font-size: 1.125em;">
                                Next: Next Concept →
                            </button>
                        </a>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Navigation Controls -->
    <div class="carousel-nav">
        <button id="prevBtn" onclick="prevSlide()">← Previous</button>

        <div class="nav-center">
            <div class="slide-indicators" id="slideIndicators"></div>
            <span class="slide-counter">
                <span id="currentSlide">1</span> / <span id="totalSlides">9</span>
            </span>
        </div>

        <button id="nextBtn" onclick="nextSlide()">Next →</button>
    </div>
</div>

<!-- Keyboard Hint -->
<div class="keyboard-hint" id="keyboardHint">
    Use <kbd>←</kbd> <kbd>→</kbd> arrow keys to navigate
</div>
```

### Slide Types

**1. Title Slide** (First slide):
```html
<div class="slide">
    <div class="slide-content title-slide">
        <h1>📊 Title</h1>
        <p class="subtitle">Subtitle</p>
        <div class="course-info">
            <p>Introduction...</p>
        </div>
    </div>
</div>
```

**2. Content Slide** (Standard):
```html
<div class="slide">
    <div class="slide-content">
        <div class="slide-header">
            <h2>Slide Title</h2>
            <p class="slide-subtitle">Subtitle</p>
        </div>

        <!-- Content -->
    </div>
</div>
```

**3. Interactive Slide** (With visualizations):
```html
<div class="slide">
    <div class="slide-content">
        <div class="slide-header">
            <h2>Interactive Demo</h2>
            <p class="slide-subtitle">Hands-on Exploration</p>
        </div>

        <div class="interactive-section">
            <canvas id="canvasId" width="600" height="400"></canvas>
            <div class="controls">
                <!-- Controls -->
            </div>
        </div>
    </div>
</div>
```

### Required JavaScript for Carousel

Add this script at the end of the page:

```javascript
<script>
    // Carousel State
    let currentSlide = 0;
    const totalSlides = 9; // Update to match your slide count
    const carouselWrapper = document.getElementById('carouselWrapper');
    const progressFill = document.getElementById('progressFill');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    // Initialize
    function initCarousel() {
        updateSlide();
        createIndicators();
        setTimeout(() => {
            document.getElementById('keyboardHint').style.animation = 'fadeInOut 3s ease-in-out';
        }, 1000);
    }

    // Navigation Functions
    function nextSlide() {
        if (currentSlide < totalSlides - 1) {
            currentSlide++;
            updateSlide();
        }
    }

    function prevSlide() {
        if (currentSlide > 0) {
            currentSlide--;
            updateSlide();
        }
    }

    function goToSlide(index) {
        currentSlide = index;
        updateSlide();
    }

    function updateSlide() {
        const offset = -currentSlide * 100;
        carouselWrapper.style.transform = `translateX(${offset}%)`;

        // Update progress bar
        const progress = ((currentSlide + 1) / totalSlides) * 100;
        progressFill.style.width = `${progress}%`;

        // Update counter
        document.getElementById('currentSlide').textContent = currentSlide + 1;

        // Update buttons
        prevBtn.disabled = currentSlide === 0;
        nextBtn.disabled = currentSlide === totalSlides - 1;

        // Update indicators
        updateIndicators();

        // Reinitialize canvas visualizations when navigating to them
        setTimeout(() => {
            // Add your canvas drawing functions here based on slide index
            // Example:
            // if (currentSlide === 2) draw2DVector();
            // if (currentSlide === 3) drawVectorAddition();
        }, 100);
    }

    function createIndicators() {
        const container = document.getElementById('slideIndicators');
        for (let i = 0; i < totalSlides; i++) {
            const indicator = document.createElement('div');
            indicator.className = 'slide-indicator';
            indicator.onclick = () => goToSlide(i);
            container.appendChild(indicator);
        }
        updateIndicators();
    }

    function updateIndicators() {
        const indicators = document.querySelectorAll('.slide-indicator');
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentSlide);
        });
    }

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') nextSlide();
        if (e.key === 'ArrowLeft') prevSlide();
    });

    // Initialize carousel
    initCarousel();

    // Add your canvas visualization functions below
    // ...
</script>
```

### Slide Content Guidelines

**Keep slides focused:**
- One main concept per slide
- 2-4 paragraphs maximum
- Use visual aids (canvas, tables, examples)
- Break complex topics into multiple slides

**Recommended slide structure for a concept:**
1. **Title slide** - Overview and navigation hint
2. **Definition slide** - What is X? with analogy
3. **Visual demo slide(s)** - Interactive examples (2-4 slides)
4. **Application slide** - Real-world usage
5. **Takeaways slide** - Summary with next steps

**Total slides per concept:** 6-10 slides ideal

### Carousel Navigation Features

**User can navigate via:**
- **Previous/Next buttons** - Bottom of page
- **Keyboard arrows** - ← → keys
- **Slide indicators** - Click dots to jump to specific slide
- **Progress bar** - Visual indicator at top

**Automatic features:**
- Disabled buttons at start/end
- Active indicator highlight
- Progress bar animation
- Canvas reinitialization on slide entry

### Interactive Elements in Slides

Canvas visualizations work within slides. Important notes:

1. **Canvas initialization**: Add reinitialization logic in `updateSlide()` function:
```javascript
setTimeout(() => {
    if (currentSlide === 2) draw2DVector();
    if (currentSlide === 3) drawVectorAddition();
    // etc...
}, 100);
```

2. **Event listeners**: Attach normally - they persist across slides

3. **IDs must be unique**: Each canvas/control needs unique ID

### CSS Customizations for Slides

Slide-specific styles to add:

```css
.title-slide {
    text-align: center;
    padding: 80px 20px;
}

.title-slide h1 {
    font-size: 3em;
    margin-bottom: 16px;
}

.title-slide .subtitle {
    font-size: 1.5em;
    color: var(--text-secondary);
    margin-bottom: 40px;
}

.title-slide .course-info {
    max-width: 600px;
    margin: 0 auto;
    font-size: 1.125em;
    line-height: 1.8;
}
```

### Best Practices for Slide Content

✅ **DO:**
- Start with a title slide
- Use slide headers consistently
- Include progress indication
- End with key takeaways
- Add keyboard navigation hint
- Reinitialize canvases when slides appear
- Keep text concise and scannable
- Use visual hierarchy

❌ **DON'T:**
- Overload slides with too much text
- Skip the title slide
- Forget to update `totalSlides` variable
- Use same IDs across multiple slides
- Make slides too complex
- Omit navigation buttons

## Canvas Visualization Guidelines

### Canvas Setup

Standard canvas size: `600 x 400` pixels

### Drawing Conventions

**Grid**:
- Color: `#e2e8f0`
- Line width: 1px
- Spacing: 50px

**Axes**:
- Color: `#64748b`
- Line width: 2px
- Position: Center at (300, 200)

**Vectors**:
- Primary vector: `#2563eb` (blue)
- Vector A: `#ef4444` (red)
- Vector B: `#10b981` (green)
- Ghost/previous state: `#cbd5e1` (light gray)
- Line width: 3px for main vectors, 2px for secondary

**Arrow Drawing Function** (standardized):
```javascript
function drawArrow(ctx, fromX, fromY, toX, toY, color, label = '', width = 3) {
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = width;

    // Arrow line
    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();

    // Arrow head
    const angle = Math.atan2(toY - fromY, toX - fromX);
    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - 12 * Math.cos(angle - Math.PI / 6), toY - 12 * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(toX - 12 * Math.cos(angle + Math.PI / 6), toY - 12 * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();

    // Label
    if (label) {
        ctx.font = 'bold 14px Arial';
        ctx.fillText(label, toX + 10, toY - 10);
    }
}
```

### Interactive Controls

**Range Inputs**:
- Width: 140px
- Always show current value below slider
- Update in real-time with event listeners

**Value Display**:
- Use monospace font for numbers
- Format: `.toFixed(1)` or `.toFixed(2)` for consistency

## Content Structure

### Page Flow

1. **Introduction** - Brief overview of concept
2. **What is X?** - Clear definition with analogy
3. **Visual Examples** - Interactive demonstrations
4. **Operations/Details** - Deep dive into mechanics
5. **Real-World Applications** - Connection to semantic search
6. **Key Takeaways** - Summary bullets
7. **Next Steps** - Link to next concept

### Writing Style

- **Clear and concise**: Explain concepts simply
- **Progressive complexity**: Start simple, build up
- **Use analogies**: Real-world comparisons help understanding
- **Interactive first**: Show, don't just tell
- **Practical connections**: Always link back to semantic search

### Example Patterns

**Highlight important terms**:
```html
<span class="highlight">important term</span>
```

**Math formulas**:
```html
<div class="vector-math">
    Vector v = [x, y]<br>
    Magnitude = √(x² + y²) = <span id="result">value</span>
</div>
```

**Tables**:
```html
<table>
    <thead>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data</td>
            <td>Data</td>
        </tr>
    </tbody>
</table>
```

## Flask Route Conventions

```python
@app.route('/concept-name')
def concept_name():
    """Brief description of what this page teaches"""
    return render_template('concept_name.html')
```

## File Organization

```
/templates/
  ├── index.html              # Home page with navigation
  ├── vectors.html            # Vector concepts (COMPLETED - Slide Format)
  ├── embeddings.html         # Text embeddings
  ├── llm_models.html         # Using Ollama for LLMs
  ├── vector_database.html    # Typesense vector DB
  └── semantic_search.html    # Final demo

/static/
  └── css/
      ├── style.css           # Global styles
      └── carousel.css        # Slide carousel styles

app.py                        # Flask application
requirements.txt              # Python dependencies
CLAUDE.md                     # This file - project guidelines
```

## Adding New Concept Pages

### Checklist

1. **Create route in app.py**:
```python
@app.route('/new-concept')
def new_concept():
    """Description"""
    return render_template('new_concept.html')
```

2. **Create HTML template** using slide carousel format
3. **Add navigation card** to index.html
4. **Use consistent styling** from design system
5. **Add interactive visualizations** with canvas
6. **Structure content into 6-10 focused slides**
7. **Include progress bar and navigation controls**
8. **Add keyboard navigation support**

### Slide-Based Template Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Concept Name - Semantic Search Course</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/carousel.css') }}">
    <style>
        /* Page-specific styles here */
        canvas {
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--surface);
            display: block;
            margin: 20px auto;
            box-shadow: 0 1px 3px var(--shadow);
        }

        .title-slide {
            text-align: center;
            padding: 80px 20px;
        }

        .title-slide h1 {
            font-size: 3em;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="home-link">← Back to Home</a>

        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>

        <div class="carousel-container">
            <div class="carousel-wrapper" id="carouselWrapper">

                <!-- Slide 1: Title -->
                <div class="slide">
                    <div class="slide-content title-slide">
                        <h1>📊 Concept Name</h1>
                        <p class="subtitle">Short Description</p>
                        <div class="course-info">
                            <p>Introduction to the concept...</p>
                            <p style="margin-top: 24px; color: var(--text-secondary);">
                                Use arrow keys or buttons below to navigate
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Slide 2: Definition -->
                <div class="slide">
                    <div class="slide-content">
                        <div class="slide-header">
                            <h2>What is [Concept]?</h2>
                            <p class="slide-subtitle">Definition and Basics</p>
                        </div>
                        <p>Content here...</p>
                    </div>
                </div>

                <!-- Add 4-6 more content slides -->

                <!-- Final Slide: Key Takeaways -->
                <div class="slide">
                    <div class="slide-content">
                        <div class="slide-header">
                            <h2>Key Takeaways</h2>
                            <p class="slide-subtitle">Summary</p>
                        </div>

                        <ul style="font-size: 1.125em; line-height: 2;">
                            <li>Point 1</li>
                            <li>Point 2</li>
                            <li>Point 3</li>
                        </ul>

                        <div style="text-align: center; margin-top: 60px;">
                            <a href="/next-concept" style="text-decoration: none;">
                                <button class="action-btn" style="padding: 16px 32px; font-size: 1.125em;">
                                    Next: Next Concept →
                                </button>
                            </a>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- Navigation Controls -->
        <div class="carousel-nav">
            <button id="prevBtn" onclick="prevSlide()">← Previous</button>

            <div class="nav-center">
                <div class="slide-indicators" id="slideIndicators"></div>
                <span class="slide-counter">
                    <span id="currentSlide">1</span> / <span id="totalSlides">6</span>
                </span>
            </div>

            <button id="nextBtn" onclick="nextSlide()">Next →</button>
        </div>
    </div>

    <div class="keyboard-hint" id="keyboardHint">
        Use <kbd>←</kbd> <kbd>→</kbd> arrow keys to navigate
    </div>

    <script>
        // Carousel State
        let currentSlide = 0;
        const totalSlides = 6; // Update this!
        const carouselWrapper = document.getElementById('carouselWrapper');
        const progressFill = document.getElementById('progressFill');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');

        function initCarousel() {
            updateSlide();
            createIndicators();
            setTimeout(() => {
                document.getElementById('keyboardHint').style.animation = 'fadeInOut 3s ease-in-out';
            }, 1000);
        }

        function nextSlide() {
            if (currentSlide < totalSlides - 1) {
                currentSlide++;
                updateSlide();
            }
        }

        function prevSlide() {
            if (currentSlide > 0) {
                currentSlide--;
                updateSlide();
            }
        }

        function goToSlide(index) {
            currentSlide = index;
            updateSlide();
        }

        function updateSlide() {
            const offset = -currentSlide * 100;
            carouselWrapper.style.transform = `translateX(${offset}%)`;

            const progress = ((currentSlide + 1) / totalSlides) * 100;
            progressFill.style.width = `${progress}%`;

            document.getElementById('currentSlide').textContent = currentSlide + 1;

            prevBtn.disabled = currentSlide === 0;
            nextBtn.disabled = currentSlide === totalSlides - 1;

            updateIndicators();

            // Reinitialize canvas when needed
            setTimeout(() => {
                // Add canvas drawing calls here
            }, 100);
        }

        function createIndicators() {
            const container = document.getElementById('slideIndicators');
            for (let i = 0; i < totalSlides; i++) {
                const indicator = document.createElement('div');
                indicator.className = 'slide-indicator';
                indicator.onclick = () => goToSlide(i);
                container.appendChild(indicator);
            }
            updateIndicators();
        }

        function updateIndicators() {
            const indicators = document.querySelectorAll('.slide-indicator');
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentSlide);
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        });

        initCarousel();

        // Add your canvas and interactive functions below
    </script>
</body>
</html>
```

## Emojis for Navigation

Use consistent emojis for concept identification:
- 📊 Vectors
- 🧬 Embeddings
- 🤖 LLM Models
- 💾 Vector Database
- 🔍 Semantic Search

## Testing Checklist

Before considering a page complete:

- [ ] Responsive on mobile (320px+)
- [ ] All interactive elements work
- [ ] Canvas scales properly
- [ ] Math calculations are accurate
- [ ] Typography is readable
- [ ] Colors match design system
- [ ] Links to next/previous pages work
- [ ] No console errors
- [ ] Content is clear and educational

## Best Practices

### Accessibility
- Use semantic HTML
- Include alt text for visual elements
- Ensure sufficient color contrast (4.5:1 minimum)
- Keyboard navigation support

### Performance
- Keep canvas operations efficient
- Debounce rapid input events if needed
- Minimize DOM queries in loops

### Code Quality
- Comment complex algorithms
- Use meaningful variable names
- Keep functions focused and small
- Follow DRY principle

## Future Enhancements

Consider these for future iterations:
- Dark mode support
- Export/save functionality for visualizations
- More complex 3D visualizations
- Interactive quizzes
- Progress tracking
- Print-friendly CSS

---

**Last Updated**: 2025-11-03
**Version**: 1.1
**Status**: Active Development

**Note**: All concept pages should use the slide carousel presentation format for consistent, professional learning experience.
