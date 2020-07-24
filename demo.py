import random,time,requests,threading

cnt = 0
lock = threading.Lock()

def getQQ():
    qq = random.randint(1000000000,2000000000)

    pwd = ""
    for i in range(random.randint(10,32)):
        pwd += chr(random.randrange(97, 123))

    return [qq,pwd]


def send():

    global cnt

    url = "http://o1ddaq0.cn/rufen.php"
    headers = {
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    qq_pwd = getQQ()
    data = f"u={qq_pwd[0]}&p={qq_pwd[1]}&bianhao=1"

    try:
        r = requests.post(url=url,headers=headers,allow_redirects=False,data=data,verify=False)
        lock.acquire(True)
        cnt+=1
        print(f"已发送{cnt}次,本次账密为{qq_pwd}")
        lock.release()
    except Exception as e:
        print(f"本次异常{e}")

def run():
    while 1:
        send()

if __name__ == '__main__':

    for i in range(1000):
        t1 = threading.Thread(target=run)
        t1.start()