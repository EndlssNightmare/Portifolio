# V01 - Cybersecurity Portfolio

A static portfolio website showcasing cybersecurity writeups and projects, hosted on GitHub Pages with an organized folder structure.

## 🌐 Live Site
Visit: [https://yourusername.github.io/v01-portfolio](https://yourusername.github.io/v01-portfolio)

## 🛡️ Features

- **Dark Theme**: Modern dark UI optimized for cybersecurity content
- **Writeups**: Detailed walkthroughs of CTF machines and security challenges
- **Projects**: Showcase of security tools and projects
- **Tags**: Categorization and filtering of content
- **Responsive Design**: Works on desktop and mobile devices
- **Static Generation**: Pre-built HTML for fast loading on GitHub Pages
- **Organized Structure**: Clean folder organization for easy maintenance

## 📝 Content

### Current Writeups
- **Nocturnal Walkthrough** - IDOR vulnerability exploitation
- **EscapeTwo Walkthrough** - Windows domain compromise
- **Haze Walkthrough** - Splunk and GMSA abuse
- **Titanic Walkthrough** - Linux privilege escalation

### Current Projects
- **Knock-Tool** - Port knocking automation
- **Digispark Scripts** - USB attack payloads
- **MullvScript** - Network security scripts
- **zsh-configs** - Custom shell configurations

## 🚀 Deployment

This site is automatically deployed via GitHub Actions. When you push changes to the main branch, the site will automatically update.

### Manual Deployment
1. Push the contents of this directory to your GitHub repository
2. Go to repository Settings > Pages
3. Set Source to "Deploy from a branch"
4. Select "main" branch and "/ (root)" folder
5. Click Save

## 🛠️ Development

### Local Development
To run this site locally, simply open `index.html` in your browser or use a local server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

### Adding Content
To add new content, you'll need to:
1. Edit the source files in the main repository
2. Regenerate the static site
3. Push the updated files

## 📁 Organized File Structure

```
├── index.html                    # Home page
├── writeups.html                 # All writeups listing
├── projects.html                 # All projects listing
├── tags.html                     # All tags listing
├── README.md                     # This file
├── writeups/                     # Individual writeup pages
│   ├── writeup-nocturnal-walkthrough.html
│   ├── writeup-escapetwo-walkthrough.html
│   ├── writeup-haze-walkthrough.html
│   └── writeup-titanic-walkthrough.html
├── tags/                         # Tag-specific filtered pages
│   ├── tag-htb.html
│   ├── tag-windows.html
│   ├── tag-linux.html
│   ├── tag-web.html
│   ├── tag-privilege-escalation.html
│   └── ... (20 total tag pages)
├── assets/                       # CSS, JS, and other assets
│   ├── css/
│   │   └── style.css             # Main stylesheet
│   ├── js/
│   │   ├── script.js             # Main JavaScript
│   │   └── search.js             # Search functionality
│   └── images/                   # Image assets (if any)
├── docs/                         # Documentation
│   ├── DEPLOYMENT.md             # Deployment instructions
│   └── SUMMARY.md                # File structure summary
└── .github/workflows/            # GitHub Actions
    └── deploy.yml                # Deployment workflow
```

## 🎨 Customization

### Styling
- Edit `assets/css/style.css` to modify the appearance
- The site uses Bootstrap 5 for responsive design

### Content
- **Writeups**: Add new HTML files to the `writeups/` folder
- **Projects**: Edit `projects.html` to add new projects
- **Tags**: Create new HTML files in the `tags/` folder for new tags

### Navigation
- All internal links use relative paths for proper organization
- Writeup links point to `writeups/filename.html`
- Tag links point to `tags/tag-name.html`
- Asset links use `assets/css/` and `assets/js/` paths

## 📊 Content Summary

### Writeups (4 total)
- **Nocturnal** - IDOR, HTB, Web
- **EscapeTwo** - Windows, MSSQL, WinRM, ADCS, Domain
- **Haze** - Windows, Splunk, BloodHound, GMSA, Shadow Credentials, Privilege Escalation
- **Titanic** - Linux, Apache, Gitea, Arbitrary File Read, SQLite, CVE-2024-41817, Privilege Escalation

### Projects (4 total)
- **Knock-Tool** - Port knocking automation
- **Digispark Scripts** - USB attack payloads
- **MullvScript** - Network security scripts
- **zsh-configs** - Custom shell configurations

### Tags (20 total)
- htb, windows, linux, web, privilege-escalation, idor, mssql, winrm, adcs, domain, splunk, bloodhound, gmsa, shadow-credentials, apache, gitea, arbitrary-file-read, sqlite, cve-2024-41817

## 🎯 Features Included

✅ **Dark Theme** - Professional cybersecurity aesthetic  
✅ **Responsive Design** - Works on all devices  
✅ **Tag Filtering** - Easy content discovery  
✅ **Clean Navigation** - Intuitive user experience  
✅ **GitHub Integration** - Links to your repositories  
✅ **Static Generation** - Fast loading times  
✅ **SEO Optimized** - Search engine friendly  
✅ **Organized Structure** - Easy maintenance and updates  

## 🔧 Customization Notes

- Update GitHub username in all HTML files
- Modify colors in `assets/css/style.css`
- Add new writeups by creating new HTML files in `writeups/` folder
- Add new projects by editing `projects.html`
- Add new tags by creating new HTML files in `tags/` folder

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📞 Contact

- **GitHub**: [@EndlssNightmare](https://github.com/EndlssNightmare)
- **Portfolio**: [V01 Cybersecurity Portfolio](https://yourusername.github.io/v01-portfolio)

---

**Built with ❤️ for the cybersecurity community**



