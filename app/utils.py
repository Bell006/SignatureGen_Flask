import re
from unidecode import unidecode

from app.app_error import AppError

# List of states and their abbreviations
states = {
    'GOIAS': 'GO',
    'SAO PAULO': 'SP',
    'PARA': 'PA',
    'MINAS GERAIS': 'MG',
    'RIO DE JANEIRO': 'RJ',
    'TOCANTINS': 'TO',
    'MATO GROSSO': 'MT',
    'RORAIMA': 'RO',
    'BAHIA': 'BA',
    'ALAGOAS': 'AL',
    'ACRE': 'AC',
    'AMAPÁ': 'AP'
}

def format_phone_number(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Check if the number has exactly 11 digits
    if len(digits) != 11 and len(digits) != 10:
        raise AppError("Celular: DDD + 9 + número | Fixo: DDD + número", 400)

    # Remove leading zero if present
    if digits.startswith('0'):
        digits = digits[1:]

    if len(digits) == 11:
        formatted_phone = f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}"
    else:
        formatted_phone = f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"

    return formatted_phone

def get_state_abbreviation(state_name):
    state_formatted = unidecode(state_name.upper())

    if state_formatted in states:
        return states[state_formatted]
    else:
        raise AppError("Estado inválido.", 404)

def validate_name(name):
    # Split the name into words
    words = name.split()
    
    # Check the number of words
    if len(words) < 2 or len(words) > 3:
        raise AppError("Insira apenas o primeiro nome e um sobrenome.", 400)