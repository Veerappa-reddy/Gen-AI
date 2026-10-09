from fastapi import FastAPI
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

class loginApiData(BaseModel):
    email : str
    password : str

class chatApiData(BaseModel):
    user_message: str
    conv_id:int

@app.post("/login")
def login_func(req:loginApiData):
    return "Login success"

@app.post("/chat")
def chat_func(req:chatApiData):
    prompt = f"""
        Your are Sales AI Assistant for Mondelez Internal, respond user queries.

        Rules:
        Give output response in Telugu langauge
        user message : {req.user_message}
    """
    openai_client = openai.OpenAI(api_key=os.getenv("GEMINI_API_KEY"))
    ai_response = openai_client.responses.create(model="gpt-5.5",input=prompt)
    ai_response = ai_response.output_text

    return {"status":"success","ai_response":ai_response}
