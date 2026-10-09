from pydantic import BaseModel

class ApiData(BaseModel):
    user_id : int

class CreateUserApiData(BaseModel):
    name : str
    password : str