import os


def extract_title_from_readme(readme_path):
    """Extract the H1 title from a README.md file."""
    with open(readme_path, "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
        if first_line.startswith("# "):
            return first_line[2:]  # Remove '# ' to extract the title
    return None


def generate_toc_for_directory(root_dir):
    toc = []
    for section in next(os.walk(root_dir))[1]:  # Get first-level directories only
        section_path = os.path.join(root_dir, section)
        for root, dirs, files in os.walk(section_path):
            if "README.md" in files:
                readme_path = os.path.join(root, "README.md")
                title = extract_title_from_readme(readme_path)
                if title:
                    relative_path = os.path.relpath(readme_path, start=root_dir)
                    link = f"- [{title}](./{relative_path})"
                    toc.append((section, link))

    # Organize and format output
    toc.sort(key=lambda x: x[0])  # Sort by section name
    markdown_output = ""
    current_section = None
    for section, link in toc:
        if current_section != section:
            if current_section is not None:
                markdown_output += "\n"  # Add a newline between sections
            current_section = section
            markdown_output += f"# {section}\n"
        markdown_output += link + "\n"

    return markdown_output


if __name__ == "__main__":
    root_directory = os.getenv("PROJECT_HOME", os.getcwd())
    table_of_contents = generate_toc_for_directory(root_directory)
    print(table_of_contents)
