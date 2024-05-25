from fastapi import APIRouter, File, UploadFile, Body
from pypdf import PdfMerger
from fastapi.responses import StreamingResponse
import io
import sys
import os
from PyPDF2 import PdfReader, PdfWriter
import json
from pydantic import BaseModel

router = APIRouter()


@router.post("/merge", tags=["manipulation"])
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

@router.post("/metadata/update", tags=["manipulation"])
async def update_pdf_metadata(file: UploadFile = File(...), metadata: str = Body(...)):
    # Create a PdfWriter object
    pdf_reader = PdfReader(file.file)
    pdf_writer = PdfWriter()
    pdf_writer.clone_document_from_reader(pdf_reader)
    
    # Update the metadata
    pdf_writer.add_metadata(json.loads(metadata))
    
    # Create a BytesIO object and write the modified PDF to it
    fileobj = io.BytesIO()
    pdf_writer.write(fileobj)

    # Setting up request
    headers = {"Content-Disposition": f"attachment; filename=updated_{file.filename}"}
    fileobj.seek(0)
    return StreamingResponse(
        fileobj, headers=headers
    )

@router.post("/metadata", tags=["analysis"])
async def get_pdf_metadata(file: UploadFile = File(...)):
    # Read the PDF file
    pdf = PdfReader(file.file)
    # Get the metadata
    metadata = pdf.metadata
    return metadata

@router.post("/pagesize", tags=["analysis"])
async def analyze_pdf(file: UploadFile = File(...)):
    # Read the PDF file
    pdf = PdfReader(file.file)

    # Analyze each page
    page_sizes = []
    for page_num in range(len(pdf.pages)):
        # Get the page
        page = pdf.pages[page_num]

        # Convert the page to a byte stream to get its size
        writer = PdfWriter()
        writer.add_page(page)
        fileobj = io.BytesIO()
        writer.write(fileobj)
        size_kb = len(fileobj.getvalue()) / 1024  # Convert bytes to kilobytes

        page_sizes.append({"page": page_num + 1, "size_kb": size_kb})

    return page_sizes

@router.get("/ping", tags=["utils"])
async def ping():
    return 'pong!'