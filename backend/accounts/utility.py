from random import choices
from string import digits

def generate_otp():
    otp = ''.join(choices(digits, k=6))
    return otp
