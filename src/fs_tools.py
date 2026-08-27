from pathlib import Path
from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def read_file(filepath: str) -> dict:
    """
    Read a PDF, TXT, or DOCX resume and return extracted text.
    """

    path = Path(filepath)

    if not path.exists():
        return {
            "success": False,
            "error": f"File not found: {filepath}"
        }

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return {
            "success": False,
            "error": f"Unsupported file type: {path.suffix}"
        }

    try:
        extension = path.suffix.lower()

        if extension == ".pdf":
            text = _read_pdf(path)

        elif extension == ".txt":
            text = _read_txt(path)

        elif extension == ".docx":
            text = _read_docx(path)

        return {
            "success": True,
            "filepath": str(path),
            "filename": path.name,
            "file_type": extension,
            "text": text,
            "character_count": len(text)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "filepath": str(path)
        }


def _read_pdf(path: Path) -> str:
    """Extract text from PDF."""

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    return "\n".join(pages).strip()


def _read_txt(path: Path) -> str:
    """Read text file."""

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def _read_docx(path: Path) -> str:
    """Extract text from DOCX."""

    document = Document(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


def load_resumes(resume_directory: str = "resumes") -> list:
    """
    Load all supported resume files from a directory.
    """

    directory = Path(resume_directory)

    if not directory.exists():
        return []

    resumes = []

    for filepath in directory.iterdir():

        if filepath.is_file() and filepath.suffix.lower() in SUPPORTED_EXTENSIONS:

            result = read_file(str(filepath))

            if result["success"]:
                resumes.append(result)

    return resumes