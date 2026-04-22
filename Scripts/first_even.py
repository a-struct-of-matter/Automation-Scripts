nums = list(map(int, input("Enter numbers: ").split()))
res = []
for num in nums:
    if num %2 != 0:
        res.append(num)
    elif num %2 == 0:
        break
print("First even number encountered. Odd numbers before it:", res, end = "")