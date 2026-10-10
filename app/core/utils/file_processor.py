import docx
import openpyxl
from zipfile import BadZipFile
from docx.opc.exceptions import PackageNotFoundError

def extract_text_from_file(file_path):
    if file_path.endswith('.docx'):
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except (BadZipFile, PackageNotFoundError):
            return "[Lỗi: Tệp docx bị lỗi nén OpenXML hoặc cấu trúc không tương thích]"
    return None