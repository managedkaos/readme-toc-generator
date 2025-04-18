import os
import logging
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") == "True" else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

TOC_START = "<!-- TocStart -->"
TOC_END = "<!-- TocEnd -->"


def extract_title_from_readme(readme_path: str) -> Optional[str]:
    """Extract the H1 title from a README.md file."""
    try:
        with open(readme_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("# "):
                    title = line.strip()[2:]  # Remove '# ' to extract the title
                    logging.debug(f"Found title '{title}' in {readme_path}")
                    return title
        logging.debug(f"No H1 title found in {readme_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading {readme_path}: {str(e)}")
        return None


def insert_toc_in_readme(readme_path: str, toc_content: str) -> bool:
    """Insert or update the table of contents in a README.md file."""
    try:
        with open(readme_path, "r", encoding="utf-8") as file:
            content = file.read()

        toc_start = content.find(TOC_START)
        toc_end = content.find(TOC_END)

        if toc_start == -1 or toc_end == -1:
            logging.debug(f"No TOC markers found in {readme_path}")
            return False

        if toc_end <= toc_start:
            logging.error(f"Invalid TOC markers in {readme_path}")
            return False

        # Ensure there's a newline before the TOC_END marker
        new_content = (
            content[: toc_start + len(TOC_START) + 1]
            + toc_content
            + "\n"
            + content[toc_end:]
        )

        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(new_content)

        logging.debug(f"Updated TOC in {readme_path}")
        return True
    except Exception as e:
        logging.error(f"Error updating TOC in {readme_path}: {str(e)}")
        return False


def generate_toc_for_directory(directory_path: str, root_dir: str) -> str:
    """Generate a table of contents for a directory and its subdirectories."""
    toc_links: List[str] = []

    # Process subdirectories
    for root, dirs, files in os.walk(directory_path):
        # Skip the current directory as we don't want to include the current file in its own TOC
        if root == directory_path:
            continue

        if "README.md" in files:
            readme_path = os.path.join(root, "README.md")
            title = extract_title_from_readme(readme_path)
            if title:
                relative_path = os.path.relpath(readme_path, start=root_dir)
                link = f"- [{title}](./{relative_path})"
                toc_links.append(link)

    return "\n".join(toc_links)


def update_readmes(root_dir: str) -> None:
    """Update all README files in the directory structure with TOCs."""
    logging.debug(f"Starting TOC generation in {root_dir}")

    # Process the root README first
    root_readme = os.path.join(root_dir, "README.md")
    if os.path.exists(root_readme):
        toc_content = generate_toc_for_directory(root_dir, root_dir)
        if toc_content:
            insert_toc_in_readme(root_readme, toc_content)

    # Process all subdirectories
    for root, dirs, files in os.walk(root_dir):
        readme_path = os.path.join(root, "README.md")
        if os.path.exists(readme_path):
            toc_content = generate_toc_for_directory(root, root_dir)
            if toc_content:
                insert_toc_in_readme(readme_path, toc_content)


if __name__ == "__main__":
    root_directory = os.getenv("PROJECT_HOME", os.getcwd())
    update_readmes(root_directory)
