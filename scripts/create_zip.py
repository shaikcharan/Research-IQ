import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT_DIR / "ResearchIQ.zip"

EXCLUDE_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".idea",
    ".vscode"
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store"
}

EXCLUDE_FILES = {
    "ResearchIQ.zip",
    ".env"  # Never bundle secret keys
}

def create_archive():
    print(f"Creating archive at: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Modify dirs in-place to avoid descending into excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                if any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                    continue

                full_path = Path(root) / file
                rel_path = full_path.relative_to(ROOT_DIR)

                # Prepend top-level directory ResearchIQ/ in the archive
                archive_name = Path("ResearchIQ") / rel_path
                zip_file.write(full_path, archive_name)

    size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    print(f"Archive created successfully: {ZIP_PATH} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_archive()
