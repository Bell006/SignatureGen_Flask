import re
from unidecode import unidecode

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
    'ALAGOAS': 'AL'
}

def format_phone_number(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Remove leading zero if present
    if digits.startswith('0'):
        digits = digits[1:]
    # Ensure the phone number has the format 9xxxxxxxxx after the DDD
    if digits[2] != '9':
        digits = digits[:2] + '9' + digits[2:]
    # Check if the number has exactly 11 digits
    if len(digits) != 11:
        raise ValueError("Número de telefone deve conter exatamente 11 dígitos (DDD + 9 + número)")
    # Format the number as (xx) x xxxx-xxxx
    formatted_phone = f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}"
    return formatted_phone


def get_state_abbreviation(state_name):
    state_formatted = unidecode(state_name.upper())

    if state_formatted in states:
        return states[state_formatted]
    elif state_formatted in states.values():
        return state_formatted
    else:
        raise ValueError("Estado inválido.")

def validate_name(name):
    # Split the name into words
    words = name.split()
    
    # Check the number of words
    if len(words) < 2 or len(words) > 3:
        raise ValueError("Insira apenas o primeiro nome e um sobrenome")