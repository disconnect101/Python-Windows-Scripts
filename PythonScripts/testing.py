x = 5

def f():
    a = x
    print(a)

def main():
    global x
    x = 7
    f()

if __name__=='__main__':
    main()
    exit()