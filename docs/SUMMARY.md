# V01 Portfolio - GitHub Pages Files Summary

## 📁 Complete File Structure

This directory contains everything needed to deploy your cybersecurity portfolio to GitHub Pages.

### 🏠 Main Pages
- `index.html` - Home page with recent writeups
- `writeups.html` - All writeups listing
- `projects.html` - All projects listing  
- `tags.html` - All available tags

### 📝 Individual Writeup Pages
- `writeup-nocturnal-walkthrough.html` - Nocturnal machine walkthrough
- `writeup-escapetwo-walkthrough.html` - EscapeTwo machine walkthrough
- `writeup-haze-walkthrough.html` - Haze machine walkthrough
- `writeup-titanic-walkthrough.html` - Titanic machine walkthrough

### 🏷️ Tag Filter Pages
- `tag-htb.html` - HackTheBox writeups
- `tag-windows.html` - Windows machines
- `tag-linux.html` - Linux machines
- `tag-web.html` - Web application security
- `tag-privilege-escalation.html` - Privilege escalation techniques
- `tag-idor.html` - IDOR vulnerabilities
- `tag-mssql.html` - MSSQL exploitation
- `tag-winrm.html` - WinRM access
- `tag-adcs.html` - Active Directory Certificate Services
- `tag-domain.html` - Domain compromise
- `tag-splunk.html` - Splunk exploitation
- `tag-bloodhound.html` - BloodHound enumeration
- `tag-gmsa.html` - Group Managed Service Accounts
- `tag-shadow-credentials.html` - Shadow credentials
- `tag-apache.html` - Apache server exploitation
- `tag-gitea.html` - Gitea server exploitation
- `tag-arbitrary-file-read.html` - Arbitrary file read vulnerabilities
- `tag-sqlite.html` - SQLite database exploitation
- `tag-cve-2024-41817.html` - CVE-2024-41817 exploitation

### 🎨 Assets
- `static/css/style.css` - Main stylesheet with dark theme
- `static/js/script.js` - Main JavaScript functionality
- `static/js/search.js` - Search functionality (minimal)

### ⚙️ Configuration
- `.github/workflows/deploy.yml` - GitHub Actions deployment workflow
- `README.md` - Portfolio documentation
- `DEPLOYMENT.md` - Deployment instructions
- `SUMMARY.md` - This file

## 🚀 Deployment Steps

1. **Create GitHub Repository**
   ```bash
   # Create a new repository on GitHub named "v01-portfolio"
   ```

2. **Upload Files**
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/v01-portfolio.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings > Pages
   - Set Source to "Deploy from a branch"
   - Select "main" branch and "/ (root)" folder
   - Click Save

4. **Your Site URL**
   - `https://yourusername.github.io/v01-portfolio`

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

## 🔧 Customization Notes

- Update GitHub username in all HTML files
- Modify colors in `static/css/style.css`
- Add new writeups by creating new HTML files
- Add new projects by editing `projects.html`
- Add new tags by creating new `tag-*.html` files

---

**Ready for GitHub Pages deployment! 🚀**
