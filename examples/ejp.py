if __name__ == '__main__':

    num = "11000000101010000111100010101010"
    num1 = num[0:8]
    print(num1)
    n1 = int(num1, 2)
    num2 = num[8:16]
    print(num2)
    n2 = int(num2, 2)
    num3 = num[16:24]
    print(num3)
    n3 = int(num3, 2)
    num4 = num[24:32]
    print(num4)
    n4 = int(num4, 2)
    address = str(n1) + "." + str(n2) + "." + str(n3) + "." + str(n4)
    print(address)
