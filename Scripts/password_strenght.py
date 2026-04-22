passwd = input("Enter your password: ")
has_digit = any(char.isdigit() for char in passwd)
has_symbol = any(not char.isalnum() for char in passwd)
if len(passwd) < 6:
    print("Password is too short. It should be at least 6 characters long.")
elif has_digit and has_symbol:
    print("Password is strong.")
elif has_digit:
    print("Password is moderate. Consider adding symbols for a stronger password.")
else:
    print("Password is weak. Consider adding digits and symbols for a stronger password.")