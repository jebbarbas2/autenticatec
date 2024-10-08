from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, redirect, url_for
from FlaskAImage import FlaskAImage
from Result import Result
from models.UserDAL import UserDAL
from validations import is_valid_str, is_valid_str_or_null
from flask_login import LoginManager, login_user, logout_user, login_required
from annonymus_required import anonymous_required

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id: int):
    return UserDAL.get_using_id(id)

@login_manager_app.unauthorized_handler
def status_401():
    return redirect('login')

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect('login')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('auth/register.html')
    elif request.method == "POST":
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
            
            user = UserDAL.create(email, password, first_name, last_name, username)
            return Result.create(201, 'User successfully registered', { 'id': user.id })
        except Exception as ex:
            return Result.from_exception(ex)
       
@app.route('/login', methods=["GET", "POST"])
@anonymous_required()
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    elif request.method == "POST":
        try:
            body = request.get_json()

            login = body.get('login')
            password = body.get('password')

            if not is_valid_str(login): raise Exception(f'Parameter "login" is required and can\'t be whitespaces') 
            if not is_valid_str(password): raise Exception(f'Parameter "password" is required and can\'t be whitespaces') 
            
            user = UserDAL.login_using_email_or_username(login, password)

            if user is None:
                return Result.from_not_found('User not found or incorrect password')
            
            login_user(user)
            return Result.from_data({ 'redirect_url': url_for('profile') })
        except Exception as ex:
            return Result.from_exception(ex)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route('/profile', methods=["GET"])
@login_required
def profile():
    return render_template('profile/index.html')


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
