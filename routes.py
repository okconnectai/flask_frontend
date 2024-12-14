from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from models import User, Account, UserAccount, Plan, AccountPlan
from database import db
from app import app

@app.route('/meus-dados')
@login_required
def meus_dados():
    # Buscar conta atual do usuário
    user_account = UserAccount.query.filter_by(id_user=current_user.id_user).first()
    
    if not user_account:
        flash('Conta não encontrada', 'error')
        return redirect(url_for('index'))
    
    # Buscar plano atual
    account_plan = AccountPlan.query.filter_by(
        id_account=user_account.id_account,
        active=True
    ).first()
    
    plan = None
    if account_plan:
        plan = Plan.query.get(account_plan.id_plan)
    
    return render_template('meus_dados.html',
        account=user_account.account,
        account_plan=account_plan,
        plan=plan,
        now=datetime.utcnow(),
        active_page='meus_dados'
    )

@app.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    try:
        data = request.json
        
        # Atualizar dados do usuário
        current_user.name = data.get('name', current_user.name)
        current_user.email = data.get('email', current_user.email)
        current_user.whatsapp = data.get('whatsapp', current_user.whatsapp)
        current_user.cpf_cnpj = data.get('cpf_cnpj', current_user.cpf_cnpj)
        
        # Buscar conta do usuário
        user_account = UserAccount.query.filter_by(id_user=current_user.id_user).first()
        if user_account:
            # Atualizar dados da empresa
            account = user_account.account
            account.name = data.get('company_name', account.name)
            account.niche = data.get('niche', account.niche)
            account.goals = data.get('goals', account.goals)
        
        db.session.commit()
        
        flash('Dados atualizados com sucesso!', 'success')
        return jsonify({'status': 'success'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    try:
        data = request.json
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        
        if not current_user.check_password(current_password):
            return jsonify({
                'status': 'error',
                'message': 'Senha atual incorreta'
            }), 400
        
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Senha alterada com sucesso!', 'success')
        return jsonify({'status': 'success'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
