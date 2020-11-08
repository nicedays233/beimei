import webbrowser as web
import time
import os

urllist = [
    'https://blog.csdn.net/qq_35050438/article/details/107965725' ,
    'https://blog.csdn.net/qq_35050438/article/details/107953836' ,
    'https://blog.csdn.net/qq_35050438/article/details/107952647' ,
    'https://blog.csdn.net/qq_35050438/article/details/107409978' ,
    'https://blog.csdn.net/qq_35050438/article/details/107795341' ,
    'https://blog.csdn.net/qq_35050438/article/details/107673242' ,
    'https://blog.csdn.net/qq_35050438/article/details/107673373' ,
    'https://blog.csdn.net/qq_35050438/article/details/108073546' ,
    'https://blog.csdn.net/qq_35050438/article/details/108176439' ,
    'https://blog.csdn.net/qq_35050438/article/details/108197737' ,
    'https://blog.csdn.net/qq_35050438/article/details/107659087' ,
    'https://blog.csdn.net/qq_35050438/article/details/107161923' ,
    'https://blog.csdn.net/qq_35050438/article/details/104673494' ,
    'https://blog.csdn.net/qq_35050438/article/details/103529037',
    'https://blog.csdn.net/qq_35050438/article/details/103506898',
    'https://blog.csdn.net/qq_35050438/article/details/103489986',
    'https://blog.csdn.net/qq_35050438/article/details/106799791',
    'https://blog.csdn.net/qq_35050438/article/details/106368859',
    'https://blog.csdn.net/qq_35050438/article/details/106114465',
    'https://blog.csdn.net/qq_35050438/article/details/108311426',
    'https://blog.csdn.net/qq_35050438/article/details/108302136',
    'https://blog.csdn.net/qq_35050438/article/details/108298006',
    'https://blog.csdn.net/qq_35050438/article/details/108423402',
    'https://blog.csdn.net/qq_35050438/article/details/108420203',
    'https://blog.csdn.net/qq_35050438/article/details/108750249',
    'https://blog.csdn.net/qq_35050438/article/details/108750003',
    'https://blog.csdn.net/qq_35050438/article/details/108423402',
    'https://blog.csdn.net/qq_35050438/article/details/108750313',
    'https://blog.csdn.net/qq_35050438/article/details/108839400'



]

for j in range(0 , 10000):  # 设置循环的总次数
    i = 0
    while i < 1:  # 一次打开浏览器访问的循环次数
        for url in urllist:
            web.open(url)  # 访问网址地址，语法 .open(url,new=0,Autorasise=True),设置 new 的值不同有不同的效果0、1、2
            i = i + 1
            time.sleep(3)  # 设置每次打开新页面的等待时间
    else:

        time.sleep(10)  # 设置每次等待关闭浏览器的时间
        os.system('taskkill /IM chrome.exe')  # 你设置的默认使用浏览器，其他的更换下就行
