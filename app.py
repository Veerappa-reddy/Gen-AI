from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/")
def welcome():
    return {"message": "Hello World!!"}

@app.get("/home")
def home():
    print("Home coming")
    return {"message" : "home method coming"}

class InputData(BaseModel):
    user_message : str
    user_id:int

@app.post("/chat")
def chat(req:InputData):
    openai_client = openai.OpenAI(api_key=os.getenv("GEMINI_API_KEY")
    prompt="""
        Your are a Sales Assistant for Software Schools, we are providing classess in online in telug
    """
    ai_response = openai_client.responses.create(model="gpt-5.5",input=req.user_message)
    # ai_response = ai_response.output_text
    
    return{"status":"success","data":ai_response}

