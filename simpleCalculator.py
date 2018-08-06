def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

exp = raw_input()
symble = ["+", "-"]
symbleList=[]
numberList=[]
number = []

for e in exp:
    if RepresentsInt(e):
        number.append(e)
    elif e in symble:
        symbleList.append(e)
        numberList.append(''.join(number))
        number=[]

if len(number) != 0:
    numberList.append(''.join(number))

print(numberList)
print(symbleList)

print(len(numberList))

while len(numberList) >= 2:

    for s in symbleList:

        a = int(numberList[0])
        b = int(numberList[1])

        if s == "+":
            t = a+b
        else:
            t = a-b

        numberList.remove(numberList[1])
        numberList.remove(numberList[0])
        
        numberList = [t]+numberList

print("result "+ str(numberList[0]))
        




    

    