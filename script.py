import os


def extract_title_from_readme(readme_path):
    """Extract the H1 title from a README.md file."""
    with open(readme_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("# "):
                return line.strip()[2:]  # Remove '# ' to extract the title
    return None


def insert_toc_in_readme(readme_path, toc_content):
    """Insert or update the table of contents in a README.md file."""
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    toc_start = content.find("<!-- TocStart -->")
    toc_end = content.find("<!-- TocEnd -->")

    if toc_start != -1 and toc_end != -1 and toc_end > toc_start:
        # Ensure there's a newline before the <!-- TocEnd --> marker
        new_content = (
            content[: toc_start + len("<!-- TocStart -->\n")] + toc_content + "\n" + content[toc_end:]
        )
        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(new_content)


def generate_toc_for_subdirectory(section_path, root_dir):
    toc_links = []
    subdirs = []

    for root, dirs, files in os.walk(section_path):
        if "README.md" in files and os.path.relpath(root, start=section_path) != ".":
            subdirs.append(root)

    # Sort the subdirectories to ensure a consistent order
    subdirs.sort()

    for subdir in subdirs:
        readme_path = os.path.join(subdir, "README.md")
        title = extract_title_from_readme(readme_path)
        if title:
            # Get the relative path from the section directory
            relative_path_from_section = os.path.relpath(
                readme_path, start=section_path
            )

            parts_after_first_slash = "/".join(
                relative_path_from_section.split("/")[0:]
            )

            link = f"- [{title}](./{parts_after_first_slash})"
            toc_links.append(link)

    return "\n".join(toc_links)


def update_subdirectory_readmes(root_dir):
    for section in next(os.walk(root_dir))[1]:  # Get first-level directories only
        section_path = os.path.join(root_dir, section)
        readme_path = os.path.join(section_path, "README.md")
        if os.path.exists(readme_path):
            toc_content = generate_toc_for_subdirectory(section_path, root_dir)
            insert_toc_in_readme(readme_path, toc_content)


if __name__ == "__main__":
    root_directory = os.getenv("PROJECT_HOME", os.getcwd())
    root_directory = "."  # Start from the current directory
    update_subdirectory_readmes(root_directory)
