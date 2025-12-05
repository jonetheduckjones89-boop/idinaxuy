from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from dotenv import load_dotenv
from services.ai_agent import analyze_document, chat_with_document, rewrite_text, generate_next_steps
from services.models import ChatRequest, RewriteRequest, NextStepsRequest
from utils.helpers import generate_job_id, ensure_upload_dir

load_dotenv()

app = FastAPI(title="Shadows Medical AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://my-frontend.onrender.com", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = ensure_upload_dir(BASE_DIR)

print(f"Starting Shadows Backend...")
print(f"Base Directory: {BASE_DIR}")
print(f"Upload Directory: {UPLOAD_DIR}")

# In-memory storage
RESULTS_DB = {}

@app.get("/")
def read_root():
    return {"status": "Shadows AI Backend is running"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    job_id = generate_job_id()
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        analysis_result = await analyze_document(file_path, file.filename, job_id)
        RESULTS_DB[job_id] = {
            "status": "processed",
            "data": analysis_result,
            "file_path": file_path
        }
        return {"jobId": job_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results")
def get_results(jobId: str):
    if jobId not in RESULTS_DB:
        raise HTTPException(status_code=404, detail="Job not found")
    return RESULTS_DB[jobId]["data"]

@app.get("/api/status")
def get_status(jobId: str):
    if jobId not in RESULTS_DB:
        return {"status": "not_found"}
    return {"status": "processed", "percent": 100}

@app.post("/api/chat")
async def chat(payload: ChatRequest):
    if payload.jobId not in RESULTS_DB:
        raise HTTPException(status_code=404, detail="Job not found")
    
    file_path = RESULTS_DB[payload.jobId]["file_path"]
    response = await chat_with_document(payload.message, payload.history, file_path)
    
    return {
        "reply": response,
        "sources": ["Document Analysis"]
    }

@app.post("/api/rewrite")
async def rewrite(payload: RewriteRequest):
    rewritten = await rewrite_text(payload.text, payload.style)
    return {"text": rewritten}

@app.post("/api/next-steps")
async def next_steps(payload: NextStepsRequest):
    if payload.jobId not in RESULTS_DB:
        raise HTTPException(status_code=404, detail="Job not found")
    
    file_path = RESULTS_DB[payload.jobId]["file_path"]
    steps = await generate_next_steps(file_path)
    return {"steps": steps}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
