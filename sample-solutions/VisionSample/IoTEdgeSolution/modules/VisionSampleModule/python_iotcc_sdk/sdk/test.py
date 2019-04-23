
import threading
import time


def f():
    print("I n BackGroundTimer")
       
def main():
    i=0
    startTime = time.time()
    while(i<100):
       # myThread = threading.Timer(3, f)
       # myThread.start()
        if time.time() - startTime > 3 :
            print("I n 3sec ")
            startTime = time.time()
        print(" I m in Main")
        i = i+1
        time.sleep(1)
if __name__ == '__main__':
    main()

