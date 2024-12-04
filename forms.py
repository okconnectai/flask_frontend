from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=35)])
    whatsapp = StringField('WhatsApp', validators=[DataRequired(), Length(min=10, max=15)])
    account_name = StringField('Nome da Empresa', validators=[DataRequired(), Length(min=2, max=100)])
    cpf_cnpj = StringField('CNPJ ou CPF', validators=[DataRequired(), Length(min=2, max=100)])
    niche = StringField('Nicho de Atuação', validators=[DataRequired(), Length(min=2, max=100)])
    goals = TextAreaField('Descreva sua principal dificuldade com atendimentos e o que espera alcançar', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Cadastrar')
