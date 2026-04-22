users = ["admin", "guest", "admin", "root", "admin", "guest", "admin", "guest"]

attempt= {}
for user in users:
    if user in attempt:
        attempt[user]+= 1
    else:
        attempt[user] = 1
for key,values in attempt.items():
    print(f"User: {key}, Attempts: {values}")