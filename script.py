import os

def extract_title_from_readme(readme_path):
    """Extract the H1 title from a README.md file."""
    with open(readme_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('# '):
                return line.strip()[2:]  # Remove '# ' to extract the title
    return None

def insert_toc_in_readme(readme_path, toc_content):
    """Insert or update the table of contents in a README.md file."""
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    toc_start = content.find("<!-- TocStart -->")
    toc_end = content.find("<!-- TocEnd -->")

    if toc_start != -1 and toc_end != -1 and toc_end > toc_start:
        # Ensure there's a newline before the <!-- TocEnd --> marker
        new_content = content[:toc_start + len("<!-- TocStart -->\n")] + toc_content + "\n" + content[toc_end:]
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(new_content)


def generate_toc_for_subdirectory(section_path, root_dir):
    toc = []
    for root, dirs, files in os.walk(section_path):
        if 'README.md' in files:
            readme_path = os.path.join(root, 'README.md')
            title = extract_title_from_readme(readme_path)
            if title and os.path.relpath(root, start=section_path) != '.':
                relative_path = os.path.relpath(readme_path, start=root_dir)
                link = f"- [{title}](./{relative_path})"
                toc.append(link)
    return "\n".join(toc)

def update_subdirectory_readmes(root_dir):
    for section in next(os.walk(root_dir))[1]:  # Get first-level directories only
        section_path = os.path.join(root_dir, section)
        readme_path = os.path.join(section_path, 'README.md')
        if os.path.exists(readme_path):
            toc_content = generate_toc_for_subdirectory(section_path, root_dir)
            insert_toc_in_readme(readme_path, toc_content)

root_directory = '.'  # Start from the current directory
update_subdirectory_readmes(root_directory)
