from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, jsonify, send_file
from FlaskAImage import FlaskAImage
from Result import Result
from models.User import User
from models.UserDAL import UserDAL

load_dotenv()

app = Flask(__name__)

def is_valid_str(param: any):
    if not param: return False
    if not isinstance(param, str): return False
    if param.isspace(): return False
    return True

def is_valid_str_or_null(param: any):
    if param is None: return True
    return is_valid_str(param)

@app.get("/")
def index():
    return render_template('home/index.html')

@app.get('/register')
def register_get():
    return render_template('auth/register.html')
    
@app.post('/register')
def register_post():    
    try:
        body = request.get_json()

        email = body.get('email')
        username = body.get('username')
        password = body.get('password')
        first_name = body.get('firstName')
        last_name = body.get('lastName')

        if not is_valid_str(email): raise Exception(f'Parameter "email" is required and can\'t be whitespaces') 
        if not is_valid_str(username): raise Exception(f'Parameter "username" is required and can\'t be whitespaces') 
        if not is_valid_str(password): raise Exception(f'Parameter "password" is required and can\'t be whitespaces') 
        if not is_valid_str(first_name): raise Exception(f'Parameter "firstName" is required and can\'t be whitespaces') 
        if not is_valid_str_or_null(last_name): raise Exception(f'Parameter "lastName" can\'t be whitespace') 
        
        user = User(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        row = UserDAL().create(user)

        return Result.from_data(row)
    except Exception as ex:
        return Result.from_exception(ex)

@app.post('/face-detection')
def face_detection():
    try:
        image = request.files['image'] 
        aimage = FlaskAImage(image) 

        embedding = aimage.to_embedding()
        print(len(embedding), embedding)

        return aimage.to_file()
    except Exception as ex:
        return Result.from_exception(ex)

def main():
    app.run(port=int(os.environ.get('PORT', 80)), debug=True)

if __name__ == "__main__":
    main()
