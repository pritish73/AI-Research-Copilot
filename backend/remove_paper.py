from pathlib import Path
from database import reload_database

PDF_DIR = Path("papers")
CHUNK_DIR = Path("chunks")


def remove_paper(paper_name):

    pdf_path = PDF_DIR / paper_name
    chunk_path = CHUNK_DIR / f"{Path(paper_name).stem}.txt"

    deleted = []

    if pdf_path.exists():
        pdf_path.unlink()
        deleted.append(pdf_path.name)

    if chunk_path.exists():
        chunk_path.unlink()
        deleted.append(chunk_path.name)

    print("\nRebuilding database...")

    reload_database()

    return {
        "success": True,
        "deleted": deleted
    }