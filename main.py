from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import uuid
from typing import List

# Imports updated for unfolded structure
from preprocessing.geospatial_align import align_images
from analytics.flood_detector import FloodDetector
from analytics.fire_detector import FireDetector
from analytics.urban_growth import UrbanGrowthAnalyzer
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent

app = FastAPI(title="Satellite Image Intelligence API")

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Initialize detectors
flood_detector = FloodDetector()
fire_detector = FireDetector()
urban_analyzer = UrbanGrowthAnalyzer()
analysis_agent = AnalysisAgent()
report_agent = ReportAgent()

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_id": file_id, "filename": file.filename, "path": file_path}

@app.post("/analyze")
async def run_analysis(file_id: str, background_tasks: BackgroundTasks):
    # This would normally load the image and run the detectors
    # Here we simulate the process
    results = {
        "flood_area": 12.4,
        "urban_growth": 25,
        "veg_loss": 11,
        "wildfire": True,
        "insights": "Preliminary analysis shows significant urban expansion."
    }
    
    summary = analysis_agent.summarize_findings(results)
    report_filename = f"report_{file_id}.pdf"
    report_path = os.path.join(REPORT_DIR, report_filename)
    
    # Generate report in background
    background_tasks.add_task(report_agent.generate_pdf_report, results, summary, report_path)
    
    return {
        "file_id": file_id,
        "results": results,
        "summary": summary,
        "report_url": f"/report/{report_filename}"
    }

@app.get("/report/{filename}")
async def get_report(filename: str):
    path = os.path.join(REPORT_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse(content={"error": "Report not found"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
