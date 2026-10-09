import pymysql
from fastapi import FastAPI
from model_classes import ApiData, CreateUserApiData

app = FastAPI()

def get_db_connection():
    connection = pymysql.connect(host="localhost",user="root", password="Veerappa@2040",database="courses_db",port=3306,cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.get("/get-user")
def get_user(req:ApiData):
    connection = get_db_connection()
    query = "select * from users where user_id = %s;"
    user_id = req.user_id
    cursor = connection.cursor()
    cursor.execute(query,user_id)

    user = cursor.fetchall()

    print(user)
    connection.close()

    return {"user_name":user}

@app.post("/create-user")
def create_user(req:CreateUserApiData):
    connection = get_db_connection()
    cursor = connection.cursor()
    create_user_query = "insert into users(name,password)values(%s,%s)"
    cursor.execute(create_user_query,(req.name,req.password))

    connection.commit()
    connection.close()

    return {"data":req}