#!/usr/bin/env python3
"""
Portfolio Content Generator
Automates the generation of new tags, writeups, and projects for the cybersecurity portfolio.
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import argparse
from typing import List, Dict, Set

class PortfolioGenerator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.tags_dir = self.base_dir / "tags"
        self.writeups_dir = self.base_dir / "writeups"
        self.template_dir = self.base_dir / "templates"
        
        # Ensure directories exist
        self.tags_dir.mkdir(exist_ok=True)
        self.writeups_dir.mkdir(exist_ok=True)
        self.template_dir.mkdir(exist_ok=True)
        
        # Load existing data
        self.existing_tags = self._load_existing_tags()
        self.existing_writeups = self._load_existing_writeups()
        self.existing_projects = self._load_existing_projects()

    def _load_existing_tags(self) -> Set[str]:
        """Load existing tags from tag files."""
        tags = set()
        if self.tags_dir.exists():
            for tag_file in self.tags_dir.glob("tag-*.html"):
                tag_name = tag_file.stem.replace("tag-", "")
                tags.add(tag_name)
        return tags

    def _load_existing_writeups(self) -> List[Dict]:
        """Load existing writeups from writeup files."""
        writeups = []
        if self.writeups_dir.exists():
            # Get all writeup files and sort by creation time (oldest first)
            writeup_files = list(self.writeups_dir.glob("writeup-*.html"))
            writeup_files.sort(key=lambda x: x.stat().st_ctime)  # Sort by creation time
            
            for writeup_file in writeup_files:
                writeup_data = self._extract_writeup_metadata(writeup_file)
                if writeup_data:
                    writeups.append(writeup_data)
        return writeups

    def _load_existing_projects(self) -> List[Dict]:
        """Load existing projects from projects.html."""
        projects = []
        projects_file = self.base_dir / "projects.html"
        if projects_file.exists():
            # This is a simplified extraction - you might want to enhance this
            projects = self._extract_projects_from_html(projects_file)
        return projects

    def _extract_writeup_metadata(self, writeup_file: Path) -> Dict:
        """Extract metadata from a writeup HTML file."""
        try:
            with open(writeup_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
            title = title_match.group(1) if title_match else writeup_file.stem.replace("writeup-", "").replace("-", " ").title()
            
            # Extract dates
            created_match = re.search(r'Created:\s*([^<\n]+)', content)
            updated_match = re.search(r'Updated:\s*([^<\n]+)', content)
            
            created_date = created_match.group(1).strip() if created_match else ""
            updated_date = updated_match.group(1).strip() if updated_match else ""
            
            # Extract machine photo URL
            machine_photo_match = re.search(r'<img[^>]*src="([^"]*)"[^>]*alt="Machine Photo"', content)
            machine_photo = machine_photo_match.group(1) if machine_photo_match else ""
            
            # Extract tags
            tags = []
            tag_matches = re.findall(r'tag-([^"]+)\.html', content)
            tags = list(set(tag_matches))
            
            # Extract machine information
            difficulty = ""
            os_type = ""
            ip_address = ""
            
            # Look for machine information in the HTML
            difficulty_match = re.search(r'Difficulty:\s*([^<]+)', content)
            if difficulty_match:
                difficulty = difficulty_match.group(1).strip()
            
            os_match = re.search(r'OS:\s*([^<]+)', content)
            if os_match:
                os_type = os_match.group(1).strip()
            
            ip_match = re.search(r'IP:\s*([^<]+)', content)
            if ip_match:
                ip_address = ip_match.group(1).strip()
            
            return {
                'title': title,
                'filename': writeup_file.name,
                'created_date': created_date,
                'updated_date': updated_date,
                'machine_photo': machine_photo,
                'tags': tags,
                'difficulty': difficulty,
                'os_type': os_type,
                'ip_address': ip_address
            }
        except Exception as e:
            print(f"Error extracting metadata from {writeup_file}: {e}")
            return None

    def _extract_projects_from_html(self, projects_file: Path) -> List[Dict]:
        """Extract project information from projects.html."""
        projects = []
        try:
            with open(projects_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find project cards with better regex to handle whitespace
            project_matches = re.findall(r'<h5[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>\s*([^<]+?)\s*</a>', content)
            
            for href, title in project_matches:
                # Clean up the title by removing extra whitespace
                clean_title = title.strip()
                projects.append({
                    'title': clean_title,
                    'url': href,
                    'date': ''  # You might want to extract this from the HTML
                })
        except Exception as e:
            print(f"Error extracting projects: {e}")
        
        return projects

    def create_tag(self, tag_name: str, description: str = "", writeup_titles: List[str] = None) -> bool:
        """Create a new tag HTML file and optionally add it to specified writeups."""
        tag_filename = f"tag-{tag_name}.html"
        tag_path = self.tags_dir / tag_filename
        
        if tag_path.exists():
            print(f"Tag '{tag_name}' already exists!")
            return False
        
        # Create tag HTML content
        tag_content = self._generate_tag_html(tag_name, description)
        
        try:
            with open(tag_path, 'w', encoding='utf-8') as f:
                f.write(tag_content)
            
            print(f"✅ Created tag: {tag_filename}")
            self.existing_tags.add(tag_name)
            
            # Add tag to specified writeups
            if writeup_titles:
                self._add_tag_to_writeups(tag_name, writeup_titles)
            
            return True
        except Exception as e:
            print(f"❌ Error creating tag {tag_name}: {e}")
            return False

    def _add_tag_to_writeups(self, tag_name: str, writeup_titles: List[str]):
        """Add a tag to specified writeups."""
        for title in writeup_titles:
            # Find the writeup by title
            writeup_to_update = None
            for writeup in self.existing_writeups:
                if writeup['title'].lower() == title.lower():
                    writeup_to_update = writeup
                    break
            
            if not writeup_to_update:
                print(f"⚠️  Writeup '{title}' not found, skipping...")
                continue
            
            # Check if tag is already in the writeup
            if tag_name in writeup_to_update['tags']:
                print(f"ℹ️  Tag '{tag_name}' already exists in '{title}', skipping...")
                continue
            
            # Add tag to writeup
            writeup_to_update['tags'].append(tag_name)
            
            # Update the writeup file
            writeup_file = self.writeups_dir / writeup_to_update['filename']
            if writeup_file.exists():
                self._update_writeup_tags(writeup_file, writeup_to_update['tags'])
                print(f"✅ Added tag '{tag_name}' to '{title}'")
            else:
                print(f"❌ Writeup file not found: {writeup_to_update['filename']}")

    def _update_writeup_tags(self, writeup_file: Path, tags: List[str]):
        """Update the tags in a writeup HTML file."""
        try:
            with open(writeup_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new tag links
            tag_links = '\n'.join([f'<a href="../tags/tag-{tag}.html" class="tag-badge me-1">{tag}</a>' for tag in tags])
            
            # Find and replace the tag container
            start_marker = '<div class="tag-container mb-4">'
            end_marker = '</div>'
            
            start_pos = content.find(start_marker)
            if start_pos == -1:
                print(f"❌ Could not find tag container in {writeup_file.name}")
                return
            
            end_pos = content.find(end_marker, start_pos + len(start_marker))
            if end_pos == -1:
                print(f"❌ Could not find end of tag container in {writeup_file.name}")
                return
            
            # Replace the tag content
            new_content = content[:start_pos + len(start_marker)] + '\n                        ' + tag_links + '\n                    ' + content[end_pos:]
            
            with open(writeup_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
        except Exception as e:
            print(f"❌ Error updating tags in {writeup_file.name}: {e}")

    def create_writeup(self, title: str, tags: List[str], machine_photo: str = "", 
                      created_date: str = None, updated_date: str = None,
                      difficulty: str = "", os_type: str = "", ip_address: str = "") -> bool:
        """Create a new writeup HTML file."""
        # Generate filename from title
        filename = f"writeup-{title.lower().replace(' ', '-').replace(':', '').replace('.', '')}.html"
        writeup_path = self.writeups_dir / filename
        
        # Check if writeup already exists
        if writeup_path.exists():
            print(f"❌ Writeup '{title}' already exists!")
            print(f"   File: {filename}")
            print(f"   Please use a different title or remove the existing writeup first.")
            return False
        
        # Set default dates
        if not created_date:
            created_date = datetime.now().strftime("%B %d, %Y")
        if not updated_date:
            updated_date = created_date
        
        # Validate tags
        for tag in tags:
            if tag not in self.existing_tags:
                print(f"⚠️  Warning: Tag '{tag}' doesn't exist. Creating it...")
                self.create_tag(tag)
        
        # Create writeup HTML content
        writeup_content = self._generate_writeup_html(title, tags, machine_photo, created_date, updated_date, difficulty, os_type, ip_address)
        
        try:
            with open(writeup_path, 'w', encoding='utf-8') as f:
                f.write(writeup_content)
            
            print(f"✅ Created writeup: {filename}")
            
            # Add to existing writeups (will be at the end due to creation order)
            self.existing_writeups.append({
                'title': title,
                'filename': filename,
                'created_date': created_date,
                'updated_date': updated_date,
                'machine_photo': machine_photo,
                'tags': tags,
                'difficulty': difficulty,
                'os_type': os_type,
                'ip_address': ip_address
            })
            
            return True
        except Exception as e:
            print(f"❌ Error creating writeup {title}: {e}")
            return False

    def remove_writeup(self, title: str) -> bool:
        """Remove a writeup from the portfolio."""
        # Generate filename from title
        filename = f"writeup-{title.lower().replace(' ', '-').replace(':', '').replace('.', '')}.html"
        writeup_path = self.writeups_dir / filename
        
        # Find the writeup in existing writeups
        writeup_to_remove = None
        for writeup in self.existing_writeups:
            if writeup['filename'] == filename:
                writeup_to_remove = writeup
                break
        
        if not writeup_to_remove:
            print(f"❌ Writeup '{title}' not found!")
            return False
        
        # Store tags before removing writeup
        tags_to_check = writeup_to_remove['tags'].copy()
        
        # Remove the writeup file
        try:
            if writeup_path.exists():
                writeup_path.unlink()
                print(f"✅ Deleted writeup file: {filename}")
            else:
                print(f"⚠️  Writeup file not found: {filename}")
        except Exception as e:
            print(f"❌ Error deleting writeup file: {e}")
            return False
        
        # Remove from existing writeups list
        self.existing_writeups.remove(writeup_to_remove)
        print(f"✅ Removed writeup from portfolio: {title}")
        
        # Remove broken links from tag pages
        print("🔄 Removing broken links from tag pages...")
        self._remove_broken_links_from_tags(filename)
        
        # Clean up unused tags
        print("🔄 Cleaning up unused tags...")
        self._cleanup_unused_tags(tags_to_check)
        
        # Update the main pages to reflect the removal
        print("🔄 Updating main pages...")
        self.update_main_pages()
        
        return True

    def _remove_broken_links_from_tags(self, filename: str):
        """Remove broken links to a deleted writeup from all tag pages."""
        # Get the writeup title from filename
        title = filename.replace('writeup-', '').replace('.html', '').replace('-', ' ').title()
        
        # Find all tag files
        tag_files = list(self.tags_dir.glob("tag-*.html"))
        
        for tag_file in tag_files:
            try:
                with open(tag_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove the entire writeup card that contains the broken link
                # Look for the pattern: <div class="col-lg-6 col-xl-4 mb-4 writeup-card">...writeup-filename...<div>
                pattern = rf'<div class="col-lg-6 col-xl-4 mb-4 writeup-card"[^>]*>.*?{re.escape(filename)}.*?</div>\s*</div>\s*</div>'
                new_content = re.sub(pattern, '', content, flags=re.DOTALL)
                
                # If content changed, write it back
                if new_content != content:
                    with open(tag_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Removed broken link from {tag_file.name}")
                    
            except Exception as e:
                print(f"❌ Error updating {tag_file.name}: {e}")

    def _cleanup_unused_tags(self, tags_to_check: List[str]):
        """Remove tag files that are no longer used by any writeup."""
        # Get all currently used tags
        all_used_tags = set()
        for writeup in self.existing_writeups:
            all_used_tags.update(writeup['tags'])
        
        # Check which tags from the deleted writeup are no longer used
        unused_tags = [tag for tag in tags_to_check if tag not in all_used_tags]
        
        for tag in unused_tags:
            tag_file = self.tags_dir / f"tag-{tag}.html"
            if tag_file.exists():
                try:
                    tag_file.unlink()
                    print(f"✅ Deleted unused tag file: tag-{tag}.html")
                except Exception as e:
                    print(f"❌ Error deleting tag file {tag_file.name}: {e}")

    def remove_tag(self, tag_name: str, from_writeups: List[str] = None) -> bool:
        """Remove a tag and optionally remove it from specific writeups."""
        tag_file = self.tags_dir / f"tag-{tag_name}.html"
        
        if not tag_file.exists():
            print(f"❌ Tag '{tag_name}' not found!")
            return False
        
        # If specific writeups are specified, remove tag only from those writeups
        if from_writeups:
            self._remove_tag_from_writeups(tag_name, from_writeups)
        else:
            # Remove tag from all writeups that use it
            writeups_with_tag = [w for w in self.existing_writeups if tag_name in w['tags']]
            if writeups_with_tag:
                writeup_titles = [w['title'] for w in writeups_with_tag]
                self._remove_tag_from_writeups(tag_name, writeup_titles)
        
        # Check if tag is still used by any writeup
        remaining_writeups_with_tag = [w for w in self.existing_writeups if tag_name in w['tags']]
        
        if not remaining_writeups_with_tag:
            # Tag is no longer used, delete the tag file
            try:
                tag_file.unlink()
                self.existing_tags.discard(tag_name)
                print(f"✅ Deleted unused tag: {tag_name}")
            except Exception as e:
                print(f"❌ Error deleting tag file: {e}")
                return False
        else:
            print(f"ℹ️  Tag '{tag_name}' is still used by other writeups, keeping tag file")
        
        return True

    def _remove_tag_from_writeups(self, tag_name: str, writeup_titles: List[str]):
        """Remove a tag from specified writeups."""
        for title in writeup_titles:
            # Find the writeup by title
            writeup_to_update = None
            for writeup in self.existing_writeups:
                if writeup['title'].lower() == title.lower():
                    writeup_to_update = writeup
                    break
            
            if not writeup_to_update:
                print(f"⚠️  Writeup '{title}' not found, skipping...")
                continue
            
            # Check if tag exists in the writeup
            if tag_name not in writeup_to_update['tags']:
                print(f"ℹ️  Tag '{tag_name}' not found in '{title}', skipping...")
                continue
            
            # Remove tag from writeup
            writeup_to_update['tags'].remove(tag_name)
            
            # Update the writeup file
            writeup_file = self.writeups_dir / writeup_to_update['filename']
            if writeup_file.exists():
                self._update_writeup_tags(writeup_file, writeup_to_update['tags'])
                print(f"✅ Removed tag '{tag_name}' from '{title}'")
            else:
                print(f"❌ Writeup file not found: {writeup_to_update['filename']}")

    def create_project(self, title: str, description: str, project_url: str, date: str = None) -> bool:
        """Create a new project entry."""
        if not date:
            date = datetime.now().strftime("%B %d, %Y")
        
        # Add to existing projects
        self.existing_projects.append({
            'title': title,
            'description': description,
            'url': project_url,
            'date': date
        })
        
        print(f"✅ Added project: {title}")
        return True

    def update_main_pages(self):
        """Update the main HTML pages with new content."""
        self._update_writeups_page()
        self._update_tags_page()
        self._update_projects_page()
        self._update_home_page()
        self._update_all_tag_pages()
        print("✅ Updated all main pages")

    def _update_all_tag_pages(self):
        """Update all individual tag pages with current writeups."""
        # Get all currently used tags
        all_used_tags = set()
        for writeup in self.existing_writeups:
            all_used_tags.update(writeup['tags'])
        
        # Update each tag page
        for tag in all_used_tags:
            self._update_single_tag_page(tag)

    def _update_single_tag_page(self, tag_name: str):
        """Update a single tag page with current writeups that use this tag."""
        tag_file = self.tags_dir / f"tag-{tag_name}.html"
        
        if not tag_file.exists():
            print(f"⚠️  Tag file {tag_file.name} not found, skipping...")
            return
        
        try:
            # Find writeups that use this tag
            writeups_with_tag = [w for w in self.existing_writeups if tag_name in w['tags']]
            
            # Generate writeup cards for this tag
            writeup_cards_html = self._generate_writeup_cards_for_tag(writeups_with_tag)
            
            # Read the current tag file
            with open(tag_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the writeups container in the tag page
            start_marker = '<div class="row" id="writeupsContainer">'
            end_marker = '</div>\n\n                </main>'
            
            start_pos = content.find(start_marker)
            if start_pos == -1:
                print(f"❌ Could not find writeups container in {tag_file.name}")
                return
            
            end_pos = content.find(end_marker, start_pos)
            if end_pos == -1:
                print(f"❌ Could not find end of writeups container in {tag_file.name}")
                return
            
            # Replace the writeups content
            new_content = content[:start_pos + len(start_marker)] + '\n' + writeup_cards_html + '\n' + content[end_pos:]
            
            with open(tag_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated {tag_file.name}")
            
        except Exception as e:
            print(f"❌ Error updating {tag_file.name}: {e}")

    def _generate_writeup_cards_for_tag(self, writeups: List[Dict]) -> str:
        """Generate HTML for writeup cards to be displayed on a tag page."""
        html_parts = []
        
        for writeup in writeups:
            # Generate tag links for this writeup (excluding the current tag)
            tag_links = '\n'.join([f'<a href="tag-{tag}.html" class="tag-badge me-1">{tag}</a>' for tag in writeup['tags']])
            
            # Get the machine photo for this writeup
            machine_photo = writeup.get('machine_photo', 'https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/example.png')
            
            html_parts.append(f'''    <div class="col-lg-6 col-xl-4 mb-4 writeup-card" data-category="">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-body d-flex align-items-start gap-3">
                <div class="flex-grow-1">
                    <h5 class="card-title mb-2 writeup-title">
                        <a href="../writeups/{writeup['filename']}" class="text-decoration-none">
                            {writeup['title']}
                        </a>
                    </h5>
                    <p class="card-text project-excerpt mb-2">
                        {writeup['title']} This writeup documents the discovery and analysis...
                    </p>
                    <small class="project-date mb-2">
                        <i class="fas fa-calendar me-1"></i>{writeup['created_date']}
                    </small>
                    
                    <div class="tag-container">
                        {tag_links}
                    </div>
                    
                </div>
                <div class="d-none d-md-block">
                    <img
                        src="{machine_photo}"
                        alt="Writeup image"
                        class="writeup-thumb"
                    />
                </div>
            </div>
        </div>
    </div>''')
        
        return '\n'.join(html_parts)

    def _generate_tag_html(self, tag_name: str, description: str) -> str:
        """Generate HTML content for a tag page."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tag: {tag_name} - V01</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <link href="../assets/css/style.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style="background-color:#212529 !important;">
        <div class="container">
            <a class="navbar-brand" href="../index.html">
                <i class="fas fa-skull me-2"></i>V01
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="../index.html">
                            <i class="fas fa-home me-1"></i>Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../writeups.html">
                            <i class="fas fa-file-alt me-1"></i>Writeups
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../projects.html">
                            <i class="fas fa-code me-1"></i>Projects
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../tags.html">
                            <i class="fas fa-tags me-1"></i>Tags
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content with Sidebar -->
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar">
                <div class="sidebar-content">
                    <div class="profile-section text-center mb-4">
                        <img src="https://hackmyvm.eu/img/u/218d122cff717db7624e56a4d380872c.jpg" 
                             alt="V01" class="profile-avatar mb-3">
                        <h5 class="text-white mb-2">V01</h5>
                        <p class="text-white-50 mb-3">Pentester, CTF player</p>
                        <p class="text-white-50 mb-3">ACCH Team</p>
                        <a href="https://github.com/EndlssNightmare" 
                           target="_blank" class="btn btn-outline-light btn-sm">
                            <i class="fab fa-github me-1"></i>GitHub
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="col-md-9 col-lg-10 main-content">
                <main class="my-4">
                    
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="../index.html">Home</a></li>
                            <li class="breadcrumb-item"><a href="../tags.html">Tags</a></li>
                            <li class="breadcrumb-item active" aria-current="page">{tag_name}</li>
                        </ol>
                    </nav>

                    <div class="mb-4">
                        <h2><i class="fas fa-tag me-2"></i>Tag: {tag_name}</h2>
                        {f'<p class="text-muted">{description}</p>' if description else ''}
                    </div>

                    <div class="row" id="writeupsContainer">
                        <!-- Writeups with this tag will be listed here -->
                    </div>

                </main>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-light py-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <p class="mb-0">© 2025 V01</p>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="../assets/js/script.js"></script>
    <script src="../assets/js/search.js"></script>
</body>
</html>"""

    def _generate_writeup_html(self, title: str, tags: List[str], machine_photo: str, 
                              created_date: str, updated_date: str, difficulty: str = "", 
                              os_type: str = "", ip_address: str = "") -> str:
        """Generate HTML content for a writeup page."""
        tag_links = '\n'.join([f'<a href="../tags/tag-{tag}.html" class="tag-badge me-1">{tag}</a>' for tag in tags])
        
        # Generate machine information HTML if any info is provided
        machine_info_html = ""
        if difficulty or os_type or ip_address:
            machine_info_parts = []
            if difficulty:
                machine_info_parts.append(f'<span class="badge bg-primary me-2"><i class="fas fa-star me-1"></i>Difficulty: {difficulty}</span>')
            if os_type:
                machine_info_parts.append(f'<span class="badge bg-info me-2"><i class="fas fa-desktop me-1"></i>OS: {os_type}</span>')
            if ip_address:
                machine_info_parts.append(f'<span class="badge bg-secondary me-2"><i class="fas fa-network-wired me-1"></i>IP: {ip_address}</span>')
            
            machine_info_html = f'''
                                    <div class="machine-info mb-3">
                                        <h6 class="text-muted mb-2"><i class="fas fa-server me-1"></i>Machine Information:</h6>
                                        <div class="d-flex flex-wrap">
                                            {''.join(machine_info_parts)}
                                        </div>
                                    </div>'''
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - V01</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <link href="../assets/css/style.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style="background-color:#212529 !important;">
        <div class="container">
            <a class="navbar-brand" href="../index.html">
                <i class="fas fa-skull me-2"></i>V01
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="../index.html">
                            <i class="fas fa-home me-1"></i>Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../writeups.html">
                            <i class="fas fa-file-alt me-1"></i>Writeups
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../projects.html">
                            <i class="fas fa-code me-1"></i>Projects
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../tags.html">
                            <i class="fas fa-tags me-1"></i>Tags
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content with Sidebar -->
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar">
                <div class="sidebar-content">
                    <div class="profile-section text-center mb-4">
                        <img src="https://hackmyvm.eu/img/u/218d122cff717db7624e56a4d380872c.jpg" 
                             alt="V01" class="profile-avatar mb-3">
                        <h5 class="text-white mb-2">V01</h5>
                        <p class="text-white-50 mb-3">Pentester, CTF player</p>
                        <p class="text-white-50 mb-3">ACCH Team</p>
                        <a href="https://github.com/EndlssNightmare" 
                           target="_blank" class="btn btn-outline-light btn-sm">
                            <i class="fab fa-github me-1"></i>GitHub
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="col-md-9 col-lg-10 main-content">
                <main class="my-4">
                    
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="../index.html">Home</a></li>
                            <li class="breadcrumb-item"><a href="../writeups.html">Writeups</a></li>
                            <li class="breadcrumb-item active" aria-current="page">{title}</li>
                        </ol>
                    </nav>

                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-start gap-4">
                                <div class="flex-grow-1">
                                    <h1 class="card-title mb-3">{title}</h1>
                                    
                                    <div class="mb-3">
                                        <small class="text-muted">
                                            <i class="fas fa-calendar me-1"></i>Created: {created_date}
                                            
                                            <br><i class="fas fa-edit me-1"></i>Updated: {updated_date}
                                        </small>
                                    </div>

                                    <div class="tag-container mb-4">
                                        {tag_links}
                                    </div>
                                    
                                    {machine_info_html}
                                </div>
                                
                                {f'<div class="d-none d-md-block"><img src="{machine_photo}" alt="Machine Photo" class="img-fluid rounded" style="max-width: 300px; height: auto;"></div>' if machine_photo else ''}
                            </div>

                            <div id="markdown-content" class="markdown-content" style="display: none;">
# Overview

Add your writeup content here using **markdown** syntax!

## Initial Reconnaissance

Describe your initial reconnaissance process...

### Example Commands

```bash
nmap -sC -sV -p- 10.10.10.10
```

### Key Findings

- Port 80: HTTP service
- Port 22: SSH service
- Port 445: SMB service

## Exploitation

Detail your exploitation steps...

### Code Example

```python
import requests

url = "http://10.10.10.10/admin"
data = {{"username": "admin", "password": "password"}}
response = requests.post(url, data=data)
```

## Privilege Escalation

Explain privilege escalation techniques used...

### Important Notes

> **Note**: Always document your methodology and findings clearly.

## Conclusion

Summarize your findings and lessons learned...
                            </div>
                        </div>
                    </div>

                </main>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-light py-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <p class="mb-0">© 2025 V01</p>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="../assets/js/script.js"></script>
    <script src="../assets/js/search.js"></script>
    <script>
        // Initialize markdown processing
        document.addEventListener('DOMContentLoaded', function() {{
            const markdownContainer = document.getElementById('markdown-content');
            if (markdownContainer) {{
                // Configure marked.js options
                marked.setOptions({{
                    breaks: true,
                    gfm: true,
                    highlight: function(code, lang) {{
                        if (lang && Prism.languages[lang]) {{
                            return Prism.highlight(code, Prism.languages[lang], lang);
                        }}
                        return code;
                    }}
                }});
                
                // Convert markdown to HTML
                const markdownText = markdownContainer.textContent;
                markdownContainer.innerHTML = marked.parse(markdownText);
                markdownContainer.style.display = 'block';
                
                // Re-highlight code blocks with Prism
                Prism.highlightAll();
            }}
        }});
    </script>
</body>
</html>"""

    def _update_writeups_page(self):
        """Update the writeups.html page with all writeups."""
        writeups_file = self.base_dir / "writeups.html"
        if not writeups_file.exists():
            print("❌ writeups.html not found!")
            return
        
        try:
            with open(writeups_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the writeups container
            start_marker = '<div class="row" id="writeupsContainer">'
            end_marker = '</div>\n\n                </main>'
            
            start_pos = content.find(start_marker)
            if start_pos == -1:
                print("❌ Could not find writeups container in writeups.html")
                return
            
            # Find the end of the writeups container
            end_pos = content.find(end_marker, start_pos)
            if end_pos == -1:
                print("❌ Could not find end of writeups container")
                return
            
            # Generate new writeups content
            writeups_content = self._generate_writeups_grid()
            
            # Replace only the writeups content, preserving the rest
            new_content = content[:start_pos + len(start_marker)] + '\n' + writeups_content + '\n' + content[end_pos:]
            
            with open(writeups_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Updated writeups.html")
        except Exception as e:
            print(f"❌ Error updating writeups.html: {e}")

    def _update_tags_page(self):
        """Update the tags.html page with all tags."""
        tags_file = self.base_dir / "tags.html"
        if not tags_file.exists():
            print("❌ tags.html not found!")
            return
        
        try:
            with open(tags_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the tags container
            start_marker = '<div class="row" id="tagsContainer">'
            end_marker = '</div>\n\n                </main>'
            
            start_pos = content.find(start_marker)
            if start_pos == -1:
                print("❌ Could not find tags container in tags.html")
                return
            
            end_pos = content.find(end_marker, start_pos)
            if end_pos == -1:
                print("❌ Could not find end of tags container")
                return
            
            # Generate new tags content
            tags_content = self._generate_tags_grid()
            
            # Replace the content
            new_content = content[:start_pos + len(start_marker)] + '\n' + tags_content + '\n' + content[end_pos:]
            
            with open(tags_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Updated tags.html")
        except Exception as e:
            print(f"❌ Error updating tags.html: {e}")

    def _update_projects_page(self):
        """Update the projects.html page with all projects."""
        projects_file = self.base_dir / "projects.html"
        if not projects_file.exists():
            print("❌ projects.html not found!")
            return
        
        try:
            with open(projects_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the projects container - look for the row after the Projects heading
            start_marker = '<div class="mb-4">\n    <h2><i class="fas fa-code me-2"></i>Projects</h2>\n</div>\n\n<div class="row">'
            end_marker = '</div>\n\n                </main>'
            
            start_pos = content.find(start_marker)
            if start_pos == -1:
                print("❌ Could not find projects container in projects.html")
                return
            
            end_pos = content.find(end_marker, start_pos)
            if end_pos == -1:
                print("❌ Could not find end of projects container")
                return
            
            # Generate new projects content
            projects_content = self._generate_projects_grid()
            
            # Replace the content
            new_content = content[:start_pos + len(start_marker)] + '\n' + projects_content + '\n' + content[end_pos:]
            
            with open(projects_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Updated projects.html")
        except Exception as e:
            print(f"❌ Error updating projects.html: {e}")

    def _update_home_page(self):
        """Update the index.html page with recent posts."""
        home_file = self.base_dir / "index.html"
        if not home_file.exists():
            print("❌ index.html not found!")
            return
        
        try:
            with open(home_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the specific row that contains the writeup cards
            # Look for the row after "Recent Posts" heading
            start_marker = '<div class="mb-4">\n    <h2><i class="fas fa-clock me-2"></i>Recent Posts</h2>\n</div>\n\n<div class="row">'
            end_marker = '</div>\n\n                </main>'
            
            start_pos = content.find(start_marker)
            if start_pos == -1:
                print("❌ Could not find recent posts container in index.html")
                return
            
            end_pos = content.find(end_marker, start_pos)
            if end_pos == -1:
                print("❌ Could not find end of recent posts section")
                return
            
            # Generate new recent posts content (show latest 4 writeups)
            recent_posts_content = self._generate_recent_posts()
            
            # Replace only the writeup cards section, preserving the rest
            new_content = content[:start_pos + len(start_marker)] + '\n' + recent_posts_content + '\n' + content[end_pos:]
            
            with open(home_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Updated index.html")
        except Exception as e:
            print(f"❌ Error updating index.html: {e}")

    def _generate_writeups_grid(self):
        """Generate HTML for writeups grid."""
        html_parts = []
        
        for writeup in self.existing_writeups:
            tag_links = '\n'.join([f'<a href="tags/tag-{tag}.html" class="tag-badge me-1">{tag}</a>' for tag in writeup['tags']])
            
            # Get the machine photo for this writeup
            machine_photo = writeup.get('machine_photo', 'https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/example.png')
            
            html_parts.append(f'''    <div class="col-lg-6 col-xl-4 mb-4 writeup-card" data-category="">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-body d-flex align-items-start gap-3">
                <div class="flex-grow-1">
                    <h5 class="card-title mb-2 writeup-title">
                        <a href="writeups/{writeup['filename']}" class="text-decoration-none">
                            {writeup['title']}
                        </a>
                    </h5>
                    <p class="card-text project-excerpt mb-2">
                        {writeup['title']} This writeup documents the discovery and analysis...
                    </p>
                    <small class="project-date mb-2">
                        <i class="fas fa-calendar me-1"></i>{writeup['created_date']}
                    </small>
                    
                    <div class="tag-container">
                        {tag_links}
                    </div>
                    
                </div>
                <div class="d-none d-md-block">
                    <img
                        src="{machine_photo}"
                        alt="Writeup image"
                        class="writeup-thumb"
                    />
                </div>
            </div>
        </div>
    </div>''')
        
        return '\n'.join(html_parts)

    def _generate_tags_grid(self):
        """Generate HTML for tags grid."""
        html_parts = []
        
        for tag in sorted(self.existing_tags):
            html_parts.append(f'''    <div class="col-auto mb-2 tag-card" data-category="">
        <a href="tags/tag-{tag}.html" class="tag-badge">{tag}</a>
    </div>''')
        
        return '\n'.join(html_parts)

    def _generate_projects_grid(self):
        """Generate HTML for projects grid."""
        html_parts = []
        
        for project in self.existing_projects:
            # Handle missing description gracefully
            description = project.get('description', f"{project['title']} - A cybersecurity project.")
            date = project.get('date', 'January 01, 2024')
            
            html_parts.append(f'''    <div class="col-lg-6 col-xl-4 mb-4 project-card" data-category="">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-body">
                <h5 class="card-title mb-2">
                    <a href="{project['url']}" target="_blank" class="text-decoration-none">
                        {project['title']}
                    </a>
                </h5>
                <p class="card-text project-excerpt mb-2">
                    {description}
                </p>
                <small class="project-date">
                    <i class="fas fa-calendar me-1"></i>{date}
                </small>
            </div>
        </div>
    </div>''')
        
        return '\n'.join(html_parts)

    def _generate_recent_posts(self):
        """Generate HTML for recent posts on home page."""
        html_parts = []
        
        # Show ALL writeups on home page (newest first)
        recent_writeups = self.existing_writeups[::-1]
        
        for writeup in recent_writeups:
            tag_links = '\n'.join([f'<a href="tags/tag-{tag}.html" class="tag-badge me-1">{tag}</a>' for tag in writeup['tags']])
            
            # Get the machine photo for this writeup
            machine_photo = writeup.get('machine_photo', 'https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/example.png')
            
            html_parts.append(f'''    <div class="col-12 mb-4 writeup-card" data-category="">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-body d-flex align-items-start gap-3">
                <div class="flex-grow-1">
                    <h5 class="card-title mb-2 writeup-title">
                        <a href="writeups/{writeup['filename']}" class="text-decoration-none">
                            {writeup['title']}
                        </a>
                    </h5>
                    <p class="card-text project-excerpt mb-2">
                        {writeup['title']} This writeup documents the discovery and analysis...
                    </p>
                    <small class="project-date mb-2">
                        <i class="fas fa-calendar me-1"></i>{writeup['created_date']}
                    </small>
                                                
                            <div class="tag-container">
                                {tag_links}
                            </div>
                            
                </div>
                <div class="d-none d-md-block">
                    <img
                        src="{machine_photo}"
                        alt="Writeup image"
                        class="writeup-thumb"
                    />
                </div>
            </div>
        </div>
    </div>''')
        
        return '\n'.join(html_parts)

    def list_content(self):
        """List all existing content."""
        print("\n📊 Current Portfolio Content:")
        print(f"\n🏷️  Tags ({len(self.existing_tags)}):")
        for tag in sorted(self.existing_tags):
            print(f"  - {tag}")
        
        print(f"\n📝 Writeups ({len(self.existing_writeups)}):")
        for writeup in self.existing_writeups:
            print(f"  - {writeup['title']} ({writeup['filename']})")
        
        print(f"\n💻 Projects ({len(self.existing_projects)}):")
        for project in self.existing_projects:
            print(f"  - {project['title']}")

def main():
    parser = argparse.ArgumentParser(description="Portfolio Content Generator")
    parser.add_argument("--base-dir", default=".", help="Base directory of the portfolio")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create tag command
    tag_parser = subparsers.add_parser("tag", help="Create a new tag")
    tag_parser.add_argument("name", help="Tag name")
    tag_parser.add_argument("--description", default="", help="Tag description")
    tag_parser.add_argument("--writeups", nargs="*", help="Writeup titles to add this tag to")
    
    # Create writeup command
    writeup_parser = subparsers.add_parser("writeup", help="Create a new writeup")
    writeup_parser.add_argument("title", help="Writeup title")
    writeup_parser.add_argument("--tags", nargs="+", required=True, help="Tags for the writeup")
    writeup_parser.add_argument("--machine-photo", default="", help="Machine photo URL for the writeup")
    writeup_parser.add_argument("--created-date", help="Creation date (format: Month DD, YYYY)")
    writeup_parser.add_argument("--updated-date", help="Update date (format: Month DD, YYYY)")
    writeup_parser.add_argument("--difficulty", default="", help="Machine difficulty (e.g., Easy, Medium, Hard)")
    writeup_parser.add_argument("--os", default="", help="Operating system (e.g., Linux, Windows)")
    writeup_parser.add_argument("--ip", default="", help="Machine IP address")
    
    # Remove writeup command
    remove_parser = subparsers.add_parser("remove", help="Remove a writeup")
    remove_parser.add_argument("title", help="Writeup title to remove")
    
    # Remove tag command
    remove_tag_parser = subparsers.add_parser("remove-tag", help="Remove a tag")
    remove_tag_parser.add_argument("name", help="Tag name to remove")
    remove_tag_parser.add_argument("--from-writeups", nargs="*", help="Writeup titles to remove this tag from (if not specified, removes from all writeups)")
    
    # Create project command
    project_parser = subparsers.add_parser("project", help="Add a new project")
    project_parser.add_argument("title", help="Project title")
    project_parser.add_argument("description", help="Project description")
    project_parser.add_argument("project_url", help="Project URL")
    project_parser.add_argument("--date", help="Project date (format: Month DD, YYYY)")
    
    # List content command
    subparsers.add_parser("list", help="List all existing content")
    
    # Update pages command
    subparsers.add_parser("update", help="Update all main pages")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    generator = PortfolioGenerator(args.base_dir)
    
    if args.command == "tag":
        generator.create_tag(args.name, args.description, args.writeups)
    elif args.command == "writeup":
        generator.create_writeup(args.title, args.tags, args.machine_photo, 
                               args.created_date, args.updated_date,
                               args.difficulty, args.os, args.ip)
    elif args.command == "remove":
        generator.remove_writeup(args.title)
    elif args.command == "remove-tag":
        generator.remove_tag(args.name, args.from_writeups)
    elif args.command == "project":
        generator.create_project(args.title, args.description, args.project_url, args.date)
    elif args.command == "list":
        generator.list_content()
    elif args.command == "update":
        generator.update_main_pages()

if __name__ == "__main__":
    main()
