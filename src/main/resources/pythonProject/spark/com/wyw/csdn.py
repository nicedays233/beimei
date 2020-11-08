import webbrowser as web
import time
import os

urllist = [
    'https://blog.csdn.net/qq_35050438/article/details/108070805' ,
    'https://blog.csdn.net/qq_35050438/article/details/108057536' ,
    'https://blog.csdn.net/qq_35050438/article/details/107487733' ,
    'https://blog.csdn.net/qq_35050438/article/details/107342967' ,
    'https://blog.csdn.net/qq_35050438/article/details/107486152' ,
    'https://blog.csdn.net/qq_35050438/article/details/104095463' ,
    'https://blog.csdn.net/qq_35050438/article/details/107814265' ,
    'https://blog.csdn.net/qq_35050438/article/details/105591535' ,
    'https://blog.csdn.net/qq_35050438/article/details/104592116' ,
    'https://blog.csdn.net/qq_35050438/article/details/107187366' ,
    'https://blog.csdn.net/qq_35050438/article/details/107187366' ,
    'https://blog.csdn.net/qq_35050438/article/details/107001713' ,
    'https://blog.csdn.net/qq_35050438/article/details/107001713' ,
    'https://blog.csdn.net/qq_35050438/article/details/107836674',
    'https://blog.csdn.net/qq_35050438/article/details/107365890',
    'https://blog.csdn.net/qq_35050438/article/details/107148709',
    'https://blog.csdn.net/qq_35050438/article/details/106799791',
    'https://blog.csdn.net/qq_35050438/article/details/106368859',
    'https://blog.csdn.net/qq_35050438/article/details/106114465',
    'https://blog.csdn.net/qq_35050438/article/details/106695020'


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
