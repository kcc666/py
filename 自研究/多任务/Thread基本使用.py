import time
import os
import threading

def sing():
    for i in range(1,6):
        print("唱~", i)
        time.sleep(0.5)


def dance():
    for i in range(1,6):
        print("跳~", i)
        time.sleep(0.5)


def main():
    os.system("cls")

    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()

    




if __name__ == "__main__":
    main()
