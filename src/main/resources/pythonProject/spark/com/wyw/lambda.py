
# *以元组方式传入 **以字典方式传入
def name(arg1,*arg2,**arg3):
    print(arg1, '\t')
    print(arg2, '\t')
    print(arg3, '\t')

name(1,3,2,3,2,(321,23),2,3,e=2,f=3)
