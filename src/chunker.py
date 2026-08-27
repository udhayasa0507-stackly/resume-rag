import re


SECTION_NAMES = [
    "summary",
    "objective",
    "profile",
    "skills",
    "technical skills",
    "experience",
    "work experience",
    "employment",
    "education",
    "projects",
    "certifications",
    "achievements",
    "languages"
]


def normalize_text(text: str) -> str:
    """
    Clean unnecessary whitespace while preserving line structure.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def detect_section(line: str) -> str | None:
    """
    Detect whether a line represents a resume section heading.
    """

    cleaned = line.strip().lower()

    # Remove common punctuation
    cleaned = re.sub(r"[:\-]+$", "", cleaned)

    for section in SECTION_NAMES:
        if cleaned == section:
            return section.title()

    return None


def chunk_resume(text: str) -> list[dict]:
    """
    Split a resume into meaningful section-based chunks.
    """

    text = normalize_text(text)

    lines = text.split("\n")

    chunks = []

    current_section = "General"
    current_content = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        detected_section = detect_section(line)

        if detected_section:

            # Save previous section
            if current_content:
                content = "\n".join(current_content).strip()

                if content:
                    chunks.append({
                        "section": current_section,
                        "text": content
                    })

            # Start new section
            current_section = detected_section
            current_content = []

        else:
            current_content.append(line)

    # Save final section
    if current_content:
        content = "\n".join(current_content).strip()

        if content:
            chunks.append({
                "section": current_section,
                "text": content
            })

    return chunks