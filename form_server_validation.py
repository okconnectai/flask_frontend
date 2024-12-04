import re

def validate_email(email):
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_pattern, email) is not None


def validate_password(password):
    password_pattern = r'^.{8,}$'  # At least 8 characters of any type
    return re.match(password_pattern, password) is not None


def format_and_validate_non_null(value, field_name):
    formatted_value = value.strip().title()
    if not formatted_value:
        raise ValueError(f'O campo {field_name} não pode ficar em branco.')
    return formatted_value


def validate_whatsapp(whatsapp):
    # Remove non-numeric characters
    whatsapp = whatsapp.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    # Ensure it is in the format 5531998257197
    if len(whatsapp) == 11:
        return '55' + whatsapp
    return None


def validate_cpf_cnpj(cpf_cnpj):
    # Add CPF/CNPJ validation logic here
    return True
