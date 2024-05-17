from fastapi import APIRouter, File, UploadFile
from pypdf import PdfMerger
from fastapi.responses import StreamingResponse
import io
import sys
import os

router = APIRouter()

@router.post("/merge")
async def merge_pdfs(files: list[UploadFile] = File(...), filename: str = 'result.pdf'):
    merger = PdfMerger()

    for pdf in files:
        merger.append(fileobj=pdf.file)

    # Create a blank file object
    fileobj = io.BytesIO()
    merger.write(fileobj)

    # Setting up request
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    fileobj.seek(0)
    return StreamingResponse(
        fileobj, headers=headers
    )
