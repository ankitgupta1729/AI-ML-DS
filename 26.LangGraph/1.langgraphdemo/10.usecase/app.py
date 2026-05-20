import shutil
from pathlib import Path

import chainlit as cl
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

source_policy_file = BASE_DIR / "insurance_data.txt"
target_policy_file = Path.cwd() / "insurance_data.txt"
if not target_policy_file.exists() and source_policy_file.exists():
    shutil.copyfile(source_policy_file, target_policy_file)

from claim_processing_agent import create_workflow
from langgraph.types import Command

graph = create_workflow()

conversation_stage = "get_patient_id"
claim_info = {}
thread = {"configurable": {"thread_id": "101"}}

@cl.on_chat_start
async def on_start():
    global conversation_stage
    conversation_stage = "get_patient_id"
    await cl.Message(content="Welcome to the Claim Validation Assistant!").send()
    await cl.Message(content="Please enter the **Patient ID**:").send()
    
@cl.on_message
async def handle_message(message):
    global conversation_stage, claim_info
    if conversation_stage == "get_patient_id":
        claim_info["patient_id"] = message.content.strip()
        await cl.Message(content="Please enter the **Treatment Code (e.g., Z12.31)**:").send()
        conversation_stage = "get_treatment_code"
        return
    if conversation_stage == "get_treatment_code":
        claim_info["treatment_code"] = message.content.strip()
        await cl.Message(content="Please enter the **Claim Details**:").send()
        conversation_stage = "get_claim_details"
        return
    if conversation_stage == "get_claim_details":
        claim_info["claim_details"] = message.content.strip()
        await cl.Message(content="Validating Claim.. Please wait").send()
        
        state = graph.invoke(claim_info, config=thread)
        # TODO: Human in the loop
        tasks = graph.get_state(config=thread).tasks
        
        if tasks:
            feedback = tasks[0].interrupts[0].value.get("feedback")
            await cl.Message(content=f"Human Review needed \n \n {feedback}").send()
            await cl.Message(content=f"Would you like to approve the claim? (yes/no)").send()
            conversation_stage = "await_approval"
            return
            
        # No interrupt, display the results directly
        await show_results(state)
        conversation_stage = "restart" 
        return
    
    if conversation_stage == "await_approval":
        # TODO: Human in the loop
        if message.content.strip().lower() == "yes":
            state = graph.invoke(Command(resume="Approved"), config=thread)
        else:
            state = graph.invoke(Command(resume="Rejected"), config=thread)
        await cl.Message(content=state.get("storage_status", "Claim review completed.")).send()
        await show_results(state)
        conversation_stage = "restart"
        return
            
    if conversation_stage == "restart" and message.content.strip().lower() == "restart":
        claim_info = {}
        conversation_stage = "get_patient_id"
        await cl.Message(content="Restarting process..Please enter the **Patient ID**:").send()
        return
    
    await cl.Message(content="I didn't understand that. Please follow the instructions.").send()
    
async def show_results(state):
    await cl.Message(content="\ud83d\udcc4 **Claim Summary:**").send()

    await cl.Message(
        content=f"\U0001f464 Patient Data:\n{state['patient_data']}"
    ).send()

    await cl.Message(
        content=f"\U0001f4b3 Insurance Data:\n{state['insurance_data']}"
    ).send()

    await cl.Message(
        content=f"\U0001f4dc Policy Docs:\n{state['policy_docs']}"
    ).send()

    await cl.Message(
        content=f"\U0001f916 AI Feedback:\n{state['ai_validation_feedback']}"
    ).send()

    await cl.Message(
        content=f"\ud83d\udccc Final Decision: **{state['final_decision']}**"
    ).send()

    await cl.Message(
        content=f"{state.get('storage_status', 'Storage status unavailable.')}\n\n\ud83d\udd04 Type `restart` to process another claim."
    ).send()
