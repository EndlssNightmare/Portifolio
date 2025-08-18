# Organized Folder Structure

## 📁 Complete Organized Structure

This directory contains a well-organized cybersecurity portfolio optimized for GitHub Pages deployment.

```
v01-portfolio-organized/
├── 📄 index.html                    # Home page with recent writeups
├── 📄 writeups.html                 # All writeups listing page
├── 📄 projects.html                 # All projects listing page
├── 📄 tags.html                     # All tags listing page
├── 📄 README.md                     # Main documentation
├── 📁 writeups/                     # Individual writeup pages
│   ├── 📄 writeup-nocturnal-walkthrough.html
│   ├── 📄 writeup-escapetwo-walkthrough.html
│   ├── 📄 writeup-haze-walkthrough.html
│   └── 📄 writeup-titanic-walkthrough.html
├── 📁 tags/                         # Tag-specific filtered pages
│   ├── 📄 tag-htb.html
│   ├── 📄 tag-windows.html
│   ├── 📄 tag-linux.html
│   ├── 📄 tag-web.html
│   ├── 📄 tag-privilege-escalation.html
│   ├── 📄 tag-idor.html
│   ├── 📄 tag-mssql.html
│   ├── 📄 tag-winrm.html
│   ├── 📄 tag-adcs.html
│   ├── 📄 tag-domain.html
│   ├── 📄 tag-splunk.html
│   ├── 📄 tag-bloodhound.html
│   ├── 📄 tag-gmsa.html
│   ├── 📄 tag-shadow-credentials.html
│   ├── 📄 tag-apache.html
│   ├── 📄 tag-gitea.html
│   ├── 📄 tag-arbitrary-file-read.html
│   ├── 📄 tag-sqlite.html
│   └── 📄 tag-cve-2024-41817.html
├── 📁 assets/                       # CSS, JS, and other assets
│   ├── 📁 css/
│   │   └── 📄 style.css             # Main stylesheet with dark theme
│   ├── 📁 js/
│   │   ├── 📄 script.js             # Main JavaScript functionality
│   │   └── 📄 search.js             # Search functionality
│   └── 📁 images/                   # Image assets (ready for future use)
├── 📁 docs/                         # Documentation
│   ├── 📄 DEPLOYMENT.md             # Deployment instructions
│   ├── 📄 SUMMARY.md                # File structure summary
│   └── 📄 ORGANIZED_STRUCTURE.md    # This file
└── 📁 .github/workflows/            # GitHub Actions
    └── 📄 deploy.yml                # Auto-deployment workflow
```

## 🎯 Organization Benefits

### **1. Clear Separation of Concerns**
- **Main Pages**: Root level for primary navigation
- **Writeups**: Dedicated folder for individual walkthroughs
- **Tags**: Dedicated folder for filtered content
- **Assets**: Centralized styling and functionality
- **Documentation**: Organized guides and references

### **2. Easy Maintenance**
- **Add Writeups**: Simply create new HTML files in `writeups/` folder
- **Add Tags**: Create new HTML files in `tags/` folder
- **Update Styling**: Modify `assets/css/style.css`
- **Add Functionality**: Edit `assets/js/` files

### **3. Professional Structure**
- **SEO Friendly**: Clear URL structure (`/writeups/`, `/tags/`)
- **Scalable**: Easy to add hundreds of writeups and tags
- **Maintainable**: Logical organization for future updates
- **Collaborative**: Clear structure for team contributions

## 🔗 Link Structure

### **Internal Navigation**
- **Home → Writeups**: `writeups.html`
- **Home → Projects**: `projects.html`
- **Home → Tags**: `tags.html`
- **Writeups → Individual**: `writeups/writeup-name.html`
- **Tags → Individual**: `tags/tag-name.html`

### **Asset References**
- **CSS**: `assets/css/style.css`
- **JavaScript**: `assets/js/script.js` and `assets/js/search.js`
- **Images**: `assets/images/` (ready for future use)

### **Relative Paths**
All links use relative paths for proper organization:
- `../` to go up one directory level
- `./` for same directory
- No absolute paths for portability

## 📊 Content Organization

### **Writeups (4 files)**
```
writeups/
├── writeup-nocturnal-walkthrough.html    # IDOR, HTB, Web
├── writeup-escapetwo-walkthrough.html    # Windows, MSSQL, WinRM, ADCS, Domain
├── writeup-haze-walkthrough.html         # Windows, Splunk, BloodHound, GMSA
└── writeup-titanic-walkthrough.html      # Linux, Apache, Gitea, CVE-2024-41817
```

### **Tags (20 files)**
```
tags/
├── tag-htb.html                          # HackTheBox machines
├── tag-windows.html                      # Windows machines
├── tag-linux.html                        # Linux machines
├── tag-web.html                          # Web application security
├── tag-privilege-escalation.html         # Privilege escalation techniques
├── tag-idor.html                         # IDOR vulnerabilities
├── tag-mssql.html                        # MSSQL exploitation
├── tag-winrm.html                        # WinRM access
├── tag-adcs.html                         # Active Directory Certificate Services
├── tag-domain.html                       # Domain compromise
├── tag-splunk.html                       # Splunk exploitation
├── tag-bloodhound.html                   # BloodHound enumeration
├── tag-gmsa.html                         # Group Managed Service Accounts
├── tag-shadow-credentials.html           # Shadow credentials
├── tag-apache.html                       # Apache server exploitation
├── tag-gitea.html                        # Gitea server exploitation
├── tag-arbitrary-file-read.html          # Arbitrary file read vulnerabilities
├── tag-sqlite.html                       # SQLite database exploitation
├── tag-cve-2024-41817.html               # CVE-2024-41817 exploitation
└── tag-winrm.html                        # WinRM access
```

## 🚀 Deployment Ready

### **GitHub Pages Compatible**
- All paths are relative and GitHub Pages compatible
- No server-side dependencies
- Pure static HTML, CSS, and JavaScript

### **Easy Updates**
1. **Add Content**: Create new files in appropriate folders
2. **Update Links**: Use relative paths for navigation
3. **Deploy**: Push to GitHub for automatic deployment

### **Future Scalability**
- **100+ Writeups**: Simply add to `writeups/` folder
- **50+ Tags**: Add to `tags/` folder
- **Custom Assets**: Use `assets/images/` for images
- **Additional Pages**: Create new HTML files at root level

## 🎨 Customization Points

### **Styling**
- **Main Theme**: `assets/css/style.css`
- **Color Scheme**: CSS variables in `:root`
- **Responsive Design**: Bootstrap 5 integration

### **Content**
- **Writeups**: Add HTML files to `writeups/` folder
- **Projects**: Edit `projects.html`
- **Tags**: Create new HTML files in `tags/` folder

### **Functionality**
- **JavaScript**: Edit files in `assets/js/`
- **Search**: Modify `assets/js/search.js`
- **Navigation**: Update links in HTML files

---

**This organized structure makes your portfolio professional, maintainable, and ready for growth! 🚀**
