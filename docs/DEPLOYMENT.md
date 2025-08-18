# GitHub Pages Deployment Guide

## Quick Start

1. **Create a new repository** on GitHub named `v01-portfolio` (or your preferred name)

2. **Upload all files** from this directory to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/v01-portfolio.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to your repository Settings
   - Scroll down to "Pages" section
   - Set Source to "Deploy from a branch"
   - Select "main" branch and "/ (root)" folder
   - Click Save

4. **Your site will be available at**: `https://yourusername.github.io/v01-portfolio`

## File Structure

This directory contains everything needed for GitHub Pages:

```
├── index.html              # Home page
├── writeups.html           # All writeups listing
├── projects.html           # All projects listing
├── tags.html               # All tags listing
├── writeup-*.html          # Individual writeup pages
├── tag-*.html              # Tag-specific filtered pages
├── static/                 # Assets
│   ├── css/style.css       # Main stylesheet
│   └── js/                 # JavaScript files
└── .github/workflows/      # GitHub Actions (optional)
    └── deploy.yml          # Auto-deployment workflow
```

## Customization

### Update Links
- Edit `index.html` and other HTML files to update your GitHub username
- Update the sidebar GitHub link in all HTML files

### Add Content
- To add new writeups: Create new HTML files following the `writeup-*.html` pattern
- To add new projects: Edit `projects.html`
- To add new tags: Create new `tag-*.html` files

### Styling
- Edit `static/css/style.css` to modify colors, fonts, and layout

## Troubleshooting

### Site Not Loading
- Check that GitHub Pages is enabled in repository settings
- Ensure you're using the correct branch and folder
- Wait a few minutes for the first deployment

### Styling Issues
- Clear browser cache
- Check that all CSS and JS files are properly linked
- Verify file paths are correct

### Links Not Working
- Ensure all internal links use relative paths
- Check that all HTML files exist
- Verify tag links point to correct `tag-*.html` files

## Support

If you encounter issues:
1. Check the GitHub Pages documentation
2. Review the repository settings
3. Check the Actions tab for deployment logs
4. Open an issue in the repository

## Next Steps

After deployment:
1. Update the README.md with your actual GitHub username
2. Customize the content and styling
3. Add your own writeups and projects
4. Share your portfolio with the cybersecurity community!
