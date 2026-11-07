"""Local attachment storage and provider input capabilities."""
import base64
import mimetypes
from pathlib import Path
from config import ATTACHMENTS_DIR

# Provider support is independent of whether a file can be stored locally.
FILE_EXTENSIONS = {'.pdf', '.txt', '.md', '.json', '.html', '.htm', '.xml', '.csv', '.tsv', '.doc', '.docx', '.rtf', '.odt', '.ppt', '.pptx', '.xls', '.xlsx', '.py', '.js', '.css', '.c', '.cpp', '.h', '.sql'}
IMAGE_TYPES = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif'}


def attachment_path(item):
    return Path(ATTACHMENTS_DIR) / str(item.patient_id) / item.storage_key


def support_status(item):
    ext = Path(item.original_name).suffix.lower()
    return 'disponible' if ext in FILE_EXTENSIONS or ext in IMAGE_TYPES else 'formato_no_admitido'


def provider_input(item):
    ext = Path(item.original_name).suffix.lower()
    if support_status(item) != 'disponible':
        raise ValueError('El proveedor no admite este formato para consulta.')
    data = base64.b64encode(attachment_path(item).read_bytes()).decode('ascii')
    if ext in IMAGE_TYPES:
        return {'type': 'input_image', 'image_url': f'data:{IMAGE_TYPES[ext]};base64,{data}', 'detail': 'auto'}
    mime = 'text/xml' if ext == '.xml' else (mimetypes.guess_type(item.original_name)[0] or 'text/plain')
    return {'type': 'input_file', 'filename': item.original_name, 'file_data': f'data:{mime};base64,{data}'}
