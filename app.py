from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from forms import LoginForm, RegistrationForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
import requests
import base64
import json
import time
import hashlib
from form_server_validation import validate_email, validate_password, format_and_validate_non_null, validate_whatsapp, validate_cpf_cnpj

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define the base URL for the endpoints
global_base_url = 'https://wb.srv-69.okconnect.com.br'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Function to encode in Base64
def base64_encode(data):
    return base64.b64encode(data.encode()).decode()

# Function to create JWT
def create_jwt(email, user_id):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "id": user_id,
        "email": email,
        "exp": int(time.time()) + 3600  # Expires in 1 hour
    }
    encoded_header = base64_encode(json.dumps(header))
    encoded_payload = base64_encode(json.dumps(payload))
    signature = 'dummy_signature'
    return f"{encoded_header}.{encoded_payload}.{signature}"

# Function to create MD5 hash
def create_md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar link de recuperação')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    whatsapp = StringField('Whatsapp', validators=[DataRequired()])
    account_name = StringField('Account Name', validators=[DataRequired()])
    niche = StringField('Niche', validators=[DataRequired()])
    cpf_cnpj = StringField('CPF/CNPJ', validators=[DataRequired()])
    goals = StringField('Goals', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        response = requests.post(f'{global_base_url}/webhook/loginUser', json={
            'username': form.username.data,
            'password': form.password.data  # Enviando a senha sem hash
        })
        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]  # Access the first element of the list
                if 'status' in data and data['status'] == 'success':
                    user = User(1)  # Dummy user
                    login_user(user)
                    flash(data['message'])
                    return redirect(url_for('admin'))
                else:
                    flash(data.get('message', 'Erro desconhecido'), 'error')
            else:
                flash('Resposta inesperada do servidor.', 'error')
        except ValueError:
            flash('Erro ao processar a resposta do servidor.', 'error')
    return render_template('login.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        response = requests.post(f'{global_base_url}/webhook/forgotPassword', json={
            'email': form.email.data
        })
        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]  # Access the first element of the list
                if 'status' in data and data['status'] == 'success':
                    flash(data['message'], 'info')
                else:
                    flash(data.get('message', 'Erro desconhecido'), 'error')
            else:
                flash('Resposta inesperada do servidor.', 'error')
        except ValueError:
            flash('Erro ao processar a resposta do servidor.', 'error')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Format and validate fields
            formatted_name = format_and_validate_non_null(form.name.data, 'Nome')
            formatted_account_name = format_and_validate_non_null(form.account_name.data, 'Nome da Empresa')
            formatted_niche = format_and_validate_non_null(form.niche.data, 'Nicho')
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('register.html', form=form)

        # Validate email
        if not validate_email(form.email.data):
            flash('Por favor, insira um email válido.', 'error')
            return render_template('register.html', form=form)

        # Validate password
        if not validate_password(form.password.data):
            flash('A senha deve ter no mínimo 8 caracteres.', 'error')
            return render_template('register.html', form=form)

        # Validate goals
        if len(form.goals.data.strip()) < 100:
            flash('Descreva suas principais dificuldades e problemas que deseja resolver com nossa solução!', 'error')
            return render_template('register.html', form=form)

        # Validate and format whatsapp
        formatted_whatsapp = validate_whatsapp(form.whatsapp.data)
        if not formatted_whatsapp:
            flash('Número de WhatsApp inválido.', 'error')
            return render_template('register.html', form=form)

        # Validate CPF/CNPJ
        if not validate_cpf_cnpj(form.cpf_cnpj.data):
            flash('CPF ou CNPJ inválido.', 'error')
            return render_template('register.html', form=form)

        # Logic to register the user goes here
        response = requests.post(f'{global_base_url}/webhook/userRegister', json={
            'name': formatted_name,
            'email': form.email.data,
            'password': form.password.data,  # Consider hashing the password before sending
            'whatsapp': formatted_whatsapp,
            'account_name': formatted_account_name,
            'niche': formatted_niche,
            'cpf_cnpj': form.cpf_cnpj.data,
            'goals': form.goals.data
        })

        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]  # Access the first element of the list
                if 'status' in data and data['status'] == 'success':
                    flash(data['message'], 'success')
                    return redirect(url_for('login'))
                else:
                    flash(data.get('message', 'Erro desconhecido'), 'error')
            else:
                flash('Resposta inesperada do servidor.', 'error')
        except ValueError:
            flash('Erro ao processar a resposta do servidor.', 'error')
    return render_template('register.html', form=form)

@app.route('/admin')
@login_required
def admin():
    return "Welcome to the admin area!"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
