import urllib.request;
response = urllib.request.urlopen("http://www.baidu.com/");
html = response.read();
print(html);

print(urllib.request.urlopen("http://www.baidu.com/").read());

ua_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"}

print(urllib.request.urlopen(urllib.request.Request("http://www.baidu.com/", headers = ua_headers)).read());