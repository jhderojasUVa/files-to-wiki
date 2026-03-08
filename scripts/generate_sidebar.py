import os
import sys

WIKI_DIR = 'wiki'
SIDEBAR_FILE = os.path.join(WIKI_DIR, '_Sidebar.md')

def generate_sidebar():
    if not os.path.exists(WIKI_DIR):
        print(f"Directory {WIKI_DIR} does not exist.")
        sys.exit(1)
        
    lines = ["# Wiki Documentation\n\n"]
    
    # We walk the directory
    for root, dirs, files in os.walk(WIKI_DIR):
        dirs.sort()
        files.sort()
        
        rel_path = os.path.relpath(root, WIKI_DIR)
        
        md_files = [f for f in files if f.endswith('.md') and f not in ('_Sidebar.md', 'Home.md')]
        
        # Add Home if in the root WIKI_DIR
        if rel_path == '.' and 'Home.md' in files:
            md_files.insert(0, 'Home.md')

        if rel_path == '.':
            depth = 0
        else:
            depth = rel_path.count(os.sep) + 1
            
            # Check if this folder or any subfolder has markdown files
            has_md = False
            for r, _, fs in os.walk(root):
                if any(f.endswith('.md') and f != '_Sidebar.md' for f in fs):
                    has_md = True
                    break
                    
            if has_md:
                name = os.path.basename(root).replace('-', ' ').title()
                indent = "  " * (depth - 1)
                lines.append(f"{indent}- **{name}**\n")

        for file in md_files:
            file_path = os.path.join(root, file)
            # Link to the page. GitHub Wiki URLs are based on the filename without `.md`,
            # Spaces are kept as spaces (or %20), or hyphens depending on how it was created
            page_name = os.path.splitext(file)[0]
            display_name = page_name.replace('-', ' ')
            indent = "  " * depth
            
            # Use relative paths for links depending on depth, or just absolute paths
            # In GitHub wiki, links are often absolute to the wiki root.
            link_path = os.path.join(rel_path, page_name) if rel_path != '.' else page_name
            link_path = link_path.replace(os.sep, '/')
            
            repo = os.environ.get('GITHUB_REPOSITORY')
            if repo:
                link_path = f"/{repo}/wiki/{link_path}"
            
            lines.append(f"{indent}- [{display_name}]({link_path})\n")
            
    with open(SIDEBAR_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Successfully generated {SIDEBAR_FILE}")

if __name__ == '__main__':
    generate_sidebar()
