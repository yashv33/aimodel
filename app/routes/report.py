import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.extractor import extract_text_from_pdf

from app.services.summarizer import summarize_lab_report
from app.services.pdf_generator import generate_pdf_report

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

router = APIRouter(prefix="/report", tags=["report"])

@router.post("/generate/")
async def generate_report(file: UploadFile = File(...)):
    # Save uploaded PDF
    unique_id = str(uuid.uuid4())
    pdf_path = os.path.join(REPORTS_DIR, f"{unique_id}_uploaded.pdf")

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text_from_pdf(pdf_path)
    if not text:
        raise HTTPException(status_code=400, detail="Failed to extract text.")

    # Use LLM to summarize
    ai_text = summarize_lab_report(text)

    # Generate AI PDF
    out_pdf_path = os.path.join(REPORTS_DIR, f"{unique_id}_ai_report.pdf")
    generate_pdf_report(ai_text, out_pdf_path)

    return {
        "report_id": unique_id,
        "download_url": f"/report/download/{unique_id}"
    }

@router.get("/download/{report_id}")
async def download_report(report_id: str):
    out_pdf_path = os.path.join(REPORTS_DIR, f"{report_id}_ai_report.pdf")
    if not os.path.exists(out_pdf_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    return FileResponse(out_pdf_path, media_type="application/pdf")
