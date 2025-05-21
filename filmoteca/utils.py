import os
import uuid
from fastapi import UploadFile, HTTPException
from pathlib import Path
import aiofiles

UPLOAD_DIR = Path("posters")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_image(file: UploadFile) -> str:
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG allowed")
    if file.size and file.size > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Max size 2MB")

    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / filename

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return f"/posters/{filename}"
