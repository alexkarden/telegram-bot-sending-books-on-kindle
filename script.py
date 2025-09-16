import logging
import os
import re
from pathlib import Path


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@kindle\.com$", re.IGNORECASE)


def is_email_simple(s: str) -> bool:
    return bool(s and EMAIL_RE.match(s))


def sanitize_filename(name: str) -> str:
    name = Path(name).name
    name = re.sub(r"[^A-Za-z0-9.\-]", "", name)
    return name


def delete_file(file_path: str) -> bool:
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        logging.exception("Ошибка при удалении документа %s", e)
        return False
