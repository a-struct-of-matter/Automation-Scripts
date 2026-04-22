logs = ["Fail", "Fail", "Fail", "Fail", "Pass", "Pass", "Fail"]
count = 0
for log in logs:
    if log == "Fail":
        count+=1
    if log == "Pass":
        break
print("Number of consecutive fails before first pass:", count)