import re
str = "hello world 22,hello flink,helle hadoop 123 222 33"
if re.match('hes', str):
    print("find!!!")
else:
    print("not found")

print(re.findall('[0-9]+', str))
print(re.search('[0-9]+', str).group(0))

str1 = "1998-5-6 123456 {action:1, type:10}"
print(re.search("(\\d{4}-\\d+-\\d+).*{\\w+:(\\d+).*:(\\d+)}", str1).group(1))

str2 = "ababa"
print(re.sub('','-', str2))
