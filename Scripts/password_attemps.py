import getpass as gp
from time import sleep
class Password:
    def __init__(self):
        self._password = "Gravity@5237"
    def ret_pass(self):
        return self._password
p = Password()
atttempt = 0
while True:
    passwd = gp.getpass("Enter your password: ")
    if passwd == p.ret_pass():
        print("Access Granted!")
        print("Welcome to the System")
        print("Loading.")
        sleep(2)
        print("Loading...")
        break
    else:
        print("Access Denied! Try again.")
        atttempt += 1
    if atttempt == 3:
        print("Too many failed attempts.Locking and Exiting...")
        print("Exited, Reverify to unlock account.")
        break


