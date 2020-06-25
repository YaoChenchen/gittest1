# coding=utf-8

import threading, time

class MyObject:
    def __init__(self,oName):
        self.oName = oName

class People(MyObject):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        super(People, self).__init__()  #非多继承的可以不用放在第一行
        print "Init people: %s" % self.name


class Seeker(threading.Thread, People):
    def __init__(self, cond, name, age):
        super(Seeker, self).__init__()  #多继承的构造函数要放在第一行，并且不用把参数传进init
        self.name = name
        print self.name
        self.cond = cond

    def run(self):
        self.cond.acquire() #获取锁对象,开始占用锁
        print "我是Seeker，我已经把眼睛蒙上了"
        self.cond.wait()    #释放对锁的占用，同时线程挂起，直到被notify唤醒并且重新占有锁
        print "我是seeker，我找到你了躲藏者"
        self.cond.notify()
        self.cond.release()
        print "我是seeker，我赢了"


class Hider(threading.Thread, People):
    def __init__(self, cond, name, age):
        super(Hider, self).__init__()
        self.cond = cond

    def run(self):
        time.sleep(1)
        print "我是躲藏者，我还没动，我在等你把眼睛蒙上"
        self.cond.acquire() #确保1秒后，寻找者线程已经启动，并且已经把眼睛蒙上后挂起线程，等待躲藏者藏好,获取锁
        print "我是躲藏者，我开始躲了（躲好了）"
        self.cond.notify()  #在躲藏者线程已经藏好后，唤醒Seeker线程
        self.cond.wait()    #躲藏者已经躲好了，线程挂起（不动了）,释放锁
        self.cond.release() #藏好后，释放锁
        print "我是躲藏者，我输了，被你找到了"

cond = threading.Condition()
seeker = Seeker(cond, "xx", 22)
hider = Hider(cond, "小王", 22)
seeker.start()
hider.start()
print threading.enumerate()

