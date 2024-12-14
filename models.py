from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    whatsapp = db.Column(db.String(15))
    cpf_cnpj = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_id(self):
        return str(self.id_user)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id_account = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    niche = db.Column(db.String(255))
    goals = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserAccount(db.Model):
    __tablename__ = 'user_accounts'
    
    id_user_account = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE'))
    id_account = db.Column(db.Integer, db.ForeignKey('accounts.id_account', ondelete='CASCADE'))
    accept_token = db.Column(db.String(255))
    accept_at = db.Column(db.DateTime)
    first_login = db.Column(db.DateTime)
    role = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('user_accounts', lazy=True))
    account = db.relationship('Account', backref=db.backref('user_accounts', lazy=True))

class Plan(db.Model):
    __tablename__ = 'plans'
    
    id_plan = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_price = db.Column(db.Numeric(10, 2))
    yearly_price = db.Column(db.Numeric(10, 2))
    active = db.Column(db.Boolean, nullable=False, default=True)
    order_sort = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class AccountPlan(db.Model):
    __tablename__ = 'account_plans'
    
    id_account_plan = db.Column(db.Integer, primary_key=True)
    id_plan = db.Column(db.Integer, db.ForeignKey('plans.id_plan'))
    id_account = db.Column(db.Integer, db.ForeignKey('accounts.id_account'))
    active = db.Column(db.Boolean, nullable=False, default=True)
    next_renew_at = db.Column(db.DateTime)
    last_renew_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    plan = db.relationship('Plan', backref=db.backref('account_plans', lazy=True))
    account = db.relationship('Account', backref=db.backref('account_plans', lazy=True))
