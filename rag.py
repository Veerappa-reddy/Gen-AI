from fastapi import FastAPI, UploadFile, File
import os
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from docx import Document
import chromadb
import uuid
from pydantic import BaseModel

app = FastAPI()

load_dotenv()

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chromadb = chromadb.PersistentClient("./vector_db")
courses_collection = chromadb.get_or_create_collection(name="courses")

def process_pdf(file):
    print("Processing Pdf file")
    data = ""
    pdf_reader = PdfReader(file.file)
    for page in pdf_reader.pages:
        data += page.extract_text()

    return data

def process_docx(file):
    print("Processing Doc file")
    data = ""
    doc_reader = Document(file.file)
    for para in doc_reader.paragraphs:
        data += para.text
    return data

def process_text(file):
    print("Processing Text File")
    data = file.file.read()
    return data

def convert_to_chunks(data):
    no_of_chars = len(data)
    size = 50
    chunks = []
    for index in range(0,no_of_chars,size):
        chunks.append(data[index : index + size])
    return chunks

@app.post("/add-files")
def add_files(file : UploadFile = File(...)):
   file_name = file.filename
   print(file_name)

   data = ""
   if (file_name.endswith(".pdf")):
        data = process_pdf(file)
   elif (file_name.endswith(".docx")):
        data = process_docx(file)
   elif (file_name.endswith(".txt")):
        data = process_text(file)

   chunks = convert_to_chunks(data)

#    print(chunks)
   responses = []
   for chunk in chunks:
    #    vectors = gemini_client.embeddings.create(input=chunk,model="text-embedding-3-small")
        result = gemini_client.models.embed_content(
            model="gemini-embedding-2",
            contents=chunk
        )
        vectors = result.embeddings[0].values
        chunk_id = uuid.uuid4()
        courses_collection.add(ids=[str(chunk_id)], embeddings=[vectors], documents=[chunk])
        responses.append({"id":str(chunk_id),"embeddings":vectors,"documents":chunk})


   return {"message" : "Ok","data":data, "file" : responses}

class RagApiData(BaseModel):
    user_msg:str    

@app.post("/chat")
def rag_chat(req:RagApiData):
    user_msg = req.user_msg
    