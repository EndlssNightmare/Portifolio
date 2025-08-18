# Portfolio Content Generator

A Python script that automates the generation of new tags, writeups, and projects for your cybersecurity portfolio website.

## Features

- 🏷️ **Create new tags** with automatic HTML generation
- 📝 **Generate new writeups** with proper metadata and structure
- 💻 **Add new projects** to your portfolio
- 📊 **List existing content** for easy management
- 🔄 **Update main pages** automatically
- 🎨 **Consistent styling** with your existing portfolio design

## Installation

1. Make sure you have Python 3.6+ installed
2. The script uses only standard library modules (no additional dependencies)
3. Place the script in your portfolio root directory

## Usage

### Basic Commands

```bash
# List all existing content
python3 generate_content.py list

# Create a new tag
python3 generate_content.py tag "new-tag-name" --description "Tag description"

# Create a new writeup
python3 generate_content.py writeup "Machine Name Walkthrough" --tags htb windows privilege-escalation --machine-photo "https://example.com/machine-photo.png"

# Remove a writeup
python3 generate_content.py remove "Machine Name Walkthrough"

# Add a new project
python3 generate_content.py project "Project Name" "Project description" "https://github.com/user/project"

# Update all main pages
python3 generate_content.py update

**⚠️ Important**: The update command modifies your existing HTML files. Always backup your portfolio before running updates!

**✅ Update Functionality**: The update command now works correctly and will:
- Add new writeups to both the home page (recent posts) and writeups page
- Update the tags page with new tags (no duplicates)
- Update the projects page with new projects
- Preserve the existing layout and styling
```

### Detailed Examples

#### Creating a New Tag

```bash
python generate_content.py tag "buffer-overflow" --description "Buffer overflow vulnerabilities and exploitation techniques"
```

This will:
- Create `tags/tag-buffer-overflow.html`
- Generate a properly formatted tag page
- Add the tag to your existing tag collection

#### Creating a New Writeup

```bash
python generate_content.py writeup "HackTheBox - Machine Name" \
  --tags htb windows privilege-escalation mssql \
  --machine-photo "https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/example.png" \
  --created-date "January 25, 2025" \
  --updated-date "January 26, 2025"
```

This will:
- Create `writeups/writeup-hackthebox-machine-name.html`
- Generate a complete writeup template with proper structure
- Automatically create any missing tags
- Include metadata (dates, tags, machine photo)
- Add breadcrumb navigation

#### Removing a Writeup

```bash
python3 generate_content.py remove "HackTheBox - Machine Name"
```

This will:
- Delete the writeup file from `writeups/` directory
- Remove the writeup from both home page (recent posts) and writeups page
- Update all main pages automatically
- Clean up the portfolio without manual intervention

#### Adding a New Project

```bash
python generate_content.py project "Awesome Tool" \
  "A Python tool for automating penetration testing tasks" \
  "https://github.com/username/awesome-tool" \
  --date "January 25, 2025"
```

This will:
- Add the project to your portfolio collection
- Include project title, description, and URL
- Maintain consistent formatting with existing projects

#### Listing Current Content

```bash
python generate_content.py list
```

Output example:
```
📊 Current Portfolio Content:

🏷️  Tags (15):
  - adcs
  - apache
  - arbitrary-file-read
  - bloodhound
  - buffer-overflow
  - cve-2024-41817
  - domain
  - gitea
  - gmsa
  - htb
  - idor
  - linux
  - mssql
  - privilege-escalation
  - shadow-credentials
  - splunk
  - sqlite
  - web
  - windows
  - winrm

📝 Writeups (4):
  - Nocturnal Walkthrough (writeup-nocturnal-walkthrough.html)
  - EscapeTwo Walkthrough (writeup-escapetwo-walkthrough.html)
  - Haze Walkthrough (writeup-haze-walkthrough.html)
  - Titanic Walkthrough (writeup-titanic-walkthrough.html)

💻 Projects (4):
  - Knock-Tool
  - Digispark Scripts
  - MullvScript
  - zsh-configs
```

## File Structure

The script works with your existing portfolio structure:

```
Portfolio/
├── generate_content.py          # This script
├── index.html                   # Home page
├── writeups.html               # Writeups listing
├── projects.html               # Projects listing
├── tags.html                   # Tags listing
├── writeups/                   # Individual writeup files
│   ├── writeup-machine1.html
│   └── writeup-machine2.html
├── tags/                       # Individual tag pages
│   ├── tag-htb.html
│   └── tag-windows.html
└── assets/                     # CSS, JS, images
    ├── css/
    └── js/
```

## Generated Content

### Tag Pages
- Proper navigation with breadcrumbs
- Consistent styling with your portfolio
- Ready for writeup listings

### Writeup Pages
- Complete HTML structure
- Metadata section (title, dates, tags)
- Markdown-ready content area
- Proper navigation and styling
- Tag links that work with your existing system

### Project Integration
- Adds projects to your existing collection
- Maintains consistent formatting
- Ready for page updates

## Customization

### Modifying Templates

The script generates HTML templates that match your existing portfolio design. You can modify the template generation methods in the script:

- `_generate_tag_html()` - Customize tag page templates
- `_generate_writeup_html()` - Customize writeup page templates

### Adding New Features

The script is designed to be extensible. You can easily add:

- New content types
- Different template formats
- Additional metadata fields
- Custom validation rules

## Tips

1. **Tag Naming**: Use lowercase with hyphens (e.g., `privilege-escalation`, `buffer-overflow`)
2. **Tag Usage**: Pass tags as separate arguments, not as a single quoted string:
   ```bash
   # ✅ Correct way
   python3 generate_content.py writeup "Machine Name" --tags htb linux privilege-escalation
   
   # ❌ Wrong way (creates a single tag "htb linux")
   python3 generate_content.py writeup "Machine Name" --tags "htb linux"
   ```
3. **Writeup Titles**: Use descriptive titles that will work well as filenames
4. **Dates**: Use the format "Month DD, YYYY" (e.g., "January 25, 2025")
5. **Tags**: Create tags before using them in writeups, or let the script create them automatically
6. **Backup**: Always backup your portfolio before running updates

## Troubleshooting

### Common Issues

1. **Permission Errors**: Make sure the script has write permissions in your portfolio directory
2. **Encoding Issues**: The script uses UTF-8 encoding for all files
3. **Missing Dependencies**: The script uses only Python standard library

### Error Messages

- `Tag 'name' already exists!` - The tag was already created
- `Writeup 'title' already exists!` - A writeup with that title already exists
- `Warning: Tag 'name' doesn't exist. Creating it...` - The script will automatically create missing tags

## Future Enhancements

Potential improvements for the script:

- [ ] Automatic image URL generation
- [ ] Markdown to HTML conversion
- [ ] SEO optimization
- [ ] Social media integration
- [ ] Analytics tracking
- [ ] Backup and restore functionality
- [ ] Web interface for content management

## Contributing

Feel free to enhance the script by:

1. Adding new content types
2. Improving template generation
3. Adding validation rules
4. Creating additional utility functions
5. Improving error handling

## License

This script is part of your portfolio project. Use and modify as needed for your cybersecurity portfolio.
