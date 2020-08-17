import webbrowser,os

def set_search_key(search_key,page):


    injectjs = r"C:\Users\46321\Desktop\裁判文书\inject.js"

    with open(injectjs, "r", encoding="UTF8") as f:
        current = f.readlines()
        print(current)
        current[0] = f'search_key = "{search_key}";\n'
        current[1] = f'page = {page};\n'

    with open(injectjs, "w", encoding="UTF8") as f:
        f.writelines(current)



if __name__ == '__main__':

    set_search_key(search_key="百度",page=5)
    webbrowser.open('http://wenshu.court.gov.cn/')
    # os.system('taskkill /F /IM chrome.exe')