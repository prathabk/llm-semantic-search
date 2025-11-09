# GitHub Pages Deployment Checklist

Complete checklist for deploying the Semantic Search Learning Portal to GitHub Pages.

## ✅ Pre-Deployment

- [x] **Convert templates to static HTML**
  ```bash
  python3 convert_to_static.py
  ```

- [x] **Verify static files exist**
  ```bash
  ls -la docs/
  # Should see: index.html, *.html files, static/ folder, .nojekyll
  ```

- [ ] **Update GitHub repository URLs** in the following files:
  - `README.md` - Replace `your-username` with actual username
  - `docs/demo.html` - Replace `your-username` with actual username
  - `docs/index.html` - Update demo link if needed

- [ ] **Test locally** (optional but recommended)
  ```bash
  python3 -m http.server 8000 --directory docs/
  # Visit: http://localhost:8000
  ```

## 📤 Deployment Steps

### 1. Commit Changes

```bash
# Stage all docs files
git add docs/

# Stage conversion script and guides
git add convert_to_static.py
git add GITHUB_PAGES_SETUP.md
git add DEPLOYMENT_CHECKLIST.md

# Commit
git commit -m "Add static site for GitHub Pages hosting

- Convert Jinja2 templates to static HTML
- Add conversion script
- Include GitHub Pages setup guide
- Learning slides fully functional
- Demo page shows local installation instructions
"

# Push to GitHub
git push origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (gear icon)
3. In the left sidebar, click **Pages**
4. Under **Source**:
   - Select **Deploy from a branch**
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### 3. Wait for Deployment

- GitHub Pages takes 2-5 minutes to build and deploy
- You'll see a message: "Your site is ready to be published at https://..."
- Refresh the Pages settings to see the live URL

### 4. Verify Deployment

Visit your site: `https://YOUR-USERNAME.github.io/llm-semantic-search/`

**Check these pages**:
- [ ] Home page loads with navigation cards
- [ ] Knowledge Encoding slides work
- [ ] LLM Overview slides work
- [ ] Chunking Strategies slides work
- [ ] Vector Database slides work
- [ ] Semantic Search slides work
- [ ] Demo page shows installation instructions
- [ ] CSS styling loads correctly
- [ ] Slide navigation (arrows, indicators) works
- [ ] Mobile responsive design works

## 🐛 Troubleshooting

### Issue: 404 Error on GitHub Pages

**Solution**:
1. Verify `docs/` folder exists in main branch
2. Check GitHub Pages settings point to `/docs` folder
3. Wait 5 minutes and clear browser cache
4. Ensure `.nojekyll` file exists in docs/

### Issue: CSS Not Loading

**Solution**:
1. Open browser dev tools (F12) → Console
2. Check for 404 errors on CSS files
3. Verify `docs/static/css/` folder exists
4. Check HTML files reference `static/css/style.css` (not absolute paths)

### Issue: Broken Links Between Pages

**Solution**:
1. Verify all links use `.html` extension
2. Re-run conversion: `python3 convert_to_static.py`
3. Check no `{{ url_for }}` remains: `grep -r "url_for" docs/`

### Issue: Slides Don't Advance

**Solution**:
1. Check browser console for JavaScript errors
2. Verify `static/js/` files exist
3. Test keyboard arrows (← →) and click indicators

## 🎨 Custom Domain (Optional)

To use a custom domain like `learn-semantic-search.com`:

1. **Add CNAME file**:
   ```bash
   echo "learn-semantic-search.com" > docs/CNAME
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS** with your domain provider:
   ```
   Type: A
   Host: @
   Value: 185.199.108.153

   Type: A
   Host: @
   Value: 185.199.109.153

   Type: A
   Host: @
   Value: 185.199.110.153

   Type: A
   Host: @
   Value: 185.199.111.153

   Type: CNAME
   Host: www
   Value: YOUR-USERNAME.github.io
   ```

3. **Enable HTTPS** in GitHub Pages settings (automatic after DNS propagates)

## 📊 Post-Deployment

### Share Your Site

- [ ] Update README with live demo link
- [ ] Share on social media
- [ ] Add to portfolio
- [ ] Submit to educational resources lists

### Monitor Traffic (Optional)

Add Google Analytics:

1. Create GA property
2. Add tracking code to all HTML files in `docs/`
3. Re-run conversion script to preserve changes

### SEO Optimization (Optional)

```bash
# Add meta tags to templates, then reconvert
# Example: description, keywords, og:image for social sharing
```

## 🔄 Updating Content

When you add new slides or update existing ones:

```bash
# 1. Edit template in templates/
vim templates/new_concept.html

# 2. Add route in app.py (for local testing)

# 3. Test locally
python3 app.py
# Visit: http://localhost:9010/new-concept

# 4. Convert to static
python3 convert_to_static.py

# 5. Commit and push
git add docs/new_concept.html
git commit -m "Add new concept: ..."
git push

# 6. Wait 2-3 minutes for GitHub Pages to rebuild
```

## ✅ Final Checklist

Before announcing your site publicly:

- [ ] All learning modules load correctly
- [ ] Slide navigation works (keyboard + mouse)
- [ ] Mobile responsive
- [ ] No broken links
- [ ] CSS/JS loads correctly
- [ ] Demo page explains local setup
- [ ] README has correct URLs
- [ ] GitHub repo has description and topics
- [ ] LICENSE file exists
- [ ] CONTRIBUTING guide exists

## 🎉 You're Live!

Your Semantic Search Learning Portal is now publicly accessible!

**Next Steps**:
- Share with the community
- Gather feedback
- Add more content
- Consider translating to other languages

---

**Questions?** See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) or open an issue.
