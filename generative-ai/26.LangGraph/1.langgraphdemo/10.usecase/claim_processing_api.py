import shutil
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

source_policy_file = BASE_DIR / "insurance_data.txt"
target_policy_file = Path.cwd() / "insurance_data.txt"
if not target_policy_file.exists() and source_policy_file.exists():
    shutil.copyfile(source_policy_file, target_policy_file)

from claim_processing_agent import create_workflow

app = FastAPI()
graph = create_workflow()

class ClaimRequest(BaseModel):
    patient_id: str
    treatment_code: str
    claim_details: str
    
class ClaimResponse(BaseModel):
    ai_feedback: str
    final_decision: str

@app.post("/process_claim", response_model=ClaimResponse)
async def process_claim(request: ClaimRequest):
    
    input_state = {
    "patient_id": request.patient_id,
    "treatment_code": request.treatment_code,
    "claim_details": request.claim_details
    }
    result = graph.invoke(input_state, config = {"configurable": {"thread_id": "api-thread"}})
    return {
        "ai_feedback": result["ai_validation_feedback"],
        "final_decision": result["final_decision"]
    }
