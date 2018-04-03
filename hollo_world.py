#ss
#sushiquan
from platform import python_version
import sys
print("Hello world!")
print('python', python_version())

a = 20
b = 20

if ( a is b ):
   print ("1 - a 和 b 有相同的标识")
else:
   print ("1 - a 和 b 没有相同的标识")

if ( id(a) == id(b) ):
   print ("2 - a 和 b 有相同的标识")
else:
   print ("2 - a 和 b 没有相同的标识")
a, b = 0, 1
n=1
print(a)
print(b)

while b < 10:
    print('n =',n)
    print(a)
    print(b)

    a, b = b, a+b
    n = n+1
var1 = 100
if var1:
   print("1 - if 表达式条件为 true")
   print(var1)

var2 = 0
if var2:
   print("2 - if 表达式条件为 true")
   print(var2)
print("Good bye!")


# 可写函数说明
def printinfo(name, age):
   "打印任何传入的字符串"
   print("名字: ", name);
   print("年龄: ", age);
   return;


# 调用printinfo函数
printinfo(50, "runoob");


def printinfo(arg1, *vartuple):
   "打印任何传入的参数"
   print("输出: ")
   print("arg1 =" ,arg1)
   for var in vartuple:
      print(var)
   return;


# 调用printinfo 函数
printinfo(70, 60, 50);

a = [1, 2, 3, 4, 5]

dir()

if __name__ == '__main__':
   print('程序自身在运行')
else:
   print('我来自另一模块')

f = open("C:/Users/Administrator/Desktop/foo.txt", "r")

str = f.readlines()
print(str)

# 关闭打开的文件
f.close()


for arg in sys.argv:
    try:
        f = open(arg, 'r')
    except IOError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()


class people:
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0
    #定义构造方法
    def __init__(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))

#单继承示例
class student(people):
    grade = ''
    def __init__(self,n,a,w,g):
        #调用父类的构函
        people.__init__(self,n,a,w)
        self.grade = g
    #覆写父类的方法
    def speak(self):
        print("%s 说: 我 %d 岁了，我在读 %d 年级"%(self.name,self.age,self.grade))

#另一个类，多重继承之前的准备
class speaker():
    topic = ''
    name = ''
    def __init__(self,n,t):
        self.name = n
        self.topic = t
    def speak(self):
        print("我叫 %s，我是一个演说家，我演讲的主题是 %s"%(self.name,self.topic))

#多重继承
class sample(speaker,student):
    a =''
    def __init__(self,n,a,w,g,t):
        student.__init__(self,n,a,w,g)
        speaker.__init__(self,n,t)

test = sample("Tim",25,80,4,"Python")
test.speak()  