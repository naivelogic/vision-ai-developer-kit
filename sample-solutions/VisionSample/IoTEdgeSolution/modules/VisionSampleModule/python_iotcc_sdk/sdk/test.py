
import threading
import time
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi


def f():
    print("I n BackGroundTimer")
       
def main():

    url = "https://yadavsrorageaccount01.blob.core.windows.net/peabody/model.dlc"#"https://www.gstatic.com/webp/gallery3/2.png"#"http://aka.ms/ai-vision-dev-kit-default-model" #"https://www.gstatic.com/webp/gallery3/2.png"
    
    remotefile = urlopen(url)
    myurl = remotefile.url
    FileName = myurl.split("/")[-1]
    print("filename is :: %s",FileName)

    

    remotefile = urlopen(url)
    contentDisp = remotefile.info()['Content-Disposition']
    value, params = cgi.parse_header(contentDisp)
    filename = params["filename"]
    print("filename is :: " + filename)

if __name__ == '__main__':
    main()

"""     i=0
    startTime = time.time()
    while(i<100):
       # myThread = threading.Timer(3, f)
       # myThread.start()
        if time.time() - startTime > 3 :
            print("I n 3sec ")
            startTime = time.time()
        print(" I m in Main")
        i = i+1
        time.sleep(1) """