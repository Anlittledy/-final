import sys,os
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
#解决环境变量的问题 http://t.zoukankan.com/IaCorse-p-12024428.html

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader

#程序主界面
class FinalHelp:

    def __init__(self):
        self.ui = QUiLoader().load('main.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)

#登录按钮
    def pushButton_1(self):
        name = str(self.ui.lineEdit_1.text())
        passw = str(self.ui.lineEdit_2.text())

        if name == 'admin' and passw == 'admin': #管理员登录
            self.ui.textBrowser_1.setText(str('管理员登陆成功！'))
            self.ui.hide()
            global am
            am = AdminMain()
            am.ui.show()
            return


        with open('password.txt', 'r', encoding='utf-8') as f: #普通用户登录
            pass_inf = f.readlines()
        for i in range(len(pass_inf)):
            list1 =eval(pass_inf[i])
            if list1[0] == name  and list1[1] == passw:
                self.ui.textBrowser_1.setText(str('密码正确，即将进入用户界面'))
                self.ui.hide()
                global um
                um = UserMain()
                um.ui.show()
                return
        self.ui.textBrowser_1.setText(str('用户名或密码错误'))

#注册按钮
    def pushButton_2(self):
        self.ui.hide()
        global re
        re = register()
        re.ui.show()
        return

#注册界面
class register:
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('register.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)

    def pushButton_1(self): #获取注册信息
        name1 = str(self.ui.lineEdit_1.text()) #姓名
        tel1 = str(self.ui.lineEdit_2.text()) #电话
        passw1 = str(self.ui.lineEdit_3.text()) #密码
        mail1 = str(self.ui.lineEdit_4.text()) #邮箱
        info1 = '[' + "'" + name1 + "'" + ',' + "'" + tel1 +  "'" + ',' + "'" + passw1 + "'" + ',' + "'" + mail1 + "'"+']'
        with open('newuser.txt', 'a', encoding='utf-8') as f:  # 注册申请以列表形式存储
            if os.path.getsize('newuser.txt') != 0:
                f.write('\n')  # 换行\n保证数据在文件中按行存储，这样在查询时用f.readlines()才能正确查询
            f.write(info1)

        self.ui.textBrowser_1.setText(str('注册申请已提交，请等待管理员审核'))
        self.ui.lineEdit_1.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        return

#返回主界面
    def pushButton_2(self):
        self.ui.hide()
        global ma
        ma = FinalHelp()
        ma.ui.show()
        return

#管理员注册管理界面
class Admin:
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('admin.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4)
        self.doNewUsers()



    def doNewUsers(self): #读取并显示注册申请
        if os.path.getsize('newuser.txt') != 0:
            with open('newuser.txt', 'r', encoding='utf-8') as f:  # 把文件信息全部提取出来
                pass_inf2 = f.readlines()
            len2 = len(pass_inf2)
            self.ui.textBrowser_4.setText(str('当前还有' + str(len2) + '条注册申请'))

            list2 = eval(pass_inf2[0])
            self.ui.textBrowser_1.setText(str(list2[0]))
            self.ui.textBrowser_2.setText(str(list2[1]))
            self.ui.textBrowser_3.setText(str(list2[3]))
        else:
            self.ui.textBrowser_4.setText('当前没有新的注册申请')
            self.ui.textBrowser_1.setText('')
            self.ui.textBrowser_2.setText('')
            self.ui.textBrowser_3.setText('')



    def pushButton_1(self): #通过注册申请，删除申请信息，存放入密码本中
        if os.path.getsize('newuser.txt') != 0:
            f = open('newuser.txt', 'r', encoding='utf-8')
            pass_inf2 = eval(f.readline())
            info2 = '[' + "'" + pass_inf2[1] + "'" + ',' + "'" + pass_inf2[2] + "'" + ']'
            f2 = open('password.txt', 'a', encoding='utf-8')
            if os.path.getsize('password.txt') != 0:
                f2.write('\n')
            f2.write(info2)
            with open('newuser.txt', 'r', encoding='utf-8') as f3:
                pass_inf3 = f3.readlines()
            pass_inf3.pop(0)
            with open('newuser.txt', 'w', encoding='utf-8') as f3:
                for temp in pass_inf3:
                    f3.write(str(temp))
            self.doNewUsers()
        else:
            return

        return

    def pushButton_2(self): #拒绝注册申请，删除申请信息
        if os.path.getsize('newuser.txt') != 0:
            with open('newuser.txt', 'r', encoding='utf-8') as f3:  # 把文件信息全部提取出来
                pass_inf3 = f3.readlines()
            pass_inf3.pop(0)
            with open('newuser.txt', 'w', encoding='utf-8') as f3:  #
                for temp in pass_inf3:
                    f3.write(str(temp))  # 存储必须以str类型，否则就报错
            self.doNewUsers()
        else:
            return
        return

    def pushButton_3(self): #返回主界面
        self.ui.hide()
        global ma
        ma = FinalHelp()
        ma.ui.show()
        return

    def pushButton_4(self): #返回管理员主界面
        self.ui.hide()
        global am
        am = AdminMain()
        am.ui.show()
        return

#管理员主界面
class AdminMain:
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('adminmain.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4)

    def pushButton_1(self): #管理新用户
        self.ui.hide()
        global ad
        ad = Admin()
        ad.ui.show()
        return

    def pushButton_2(self): #添加物品类型
        self.ui.hide()
        global ni
        ni = NewItem()
        ni.ui.show()
        return

    def pushButton_3(self): #返回主界面
        self.ui.hide()
        global ma
        ma = FinalHelp()
        ma.ui.show()
        return

    def pushButton_4(self): #删除物品类型
        self.ui.hide()
        global dc
        dc = DelClass()
        dc.ui.show()
        return

#添加新的类型
class NewItem:
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('newclass.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)

    def pushButton_1(self): #将新的类型写入'newclass.txt'
        newclass = str(self.ui.lineEdit_1.text())
        self.ui.lineEdit_1.clear()
        listn = []
        listn.append(newclass)
        if self.ui.lineEdit_2.text() != '':
            listn.append(self.ui.lineEdit_2.text())
        if self.ui.lineEdit_3.text() != '':
            listn.append(self.ui.lineEdit_3.text())
        if self.ui.lineEdit_4.text() != '':
            listn.append(self.ui.lineEdit_4.text())
        if self.ui.lineEdit_5.text() != '':
            listn.append(self.ui.lineEdit_5.text())
        if self.ui.lineEdit_6.text() != '':
            listn.append(self.ui.lineEdit_6.text())

        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        f = open('newclass.txt', 'a', encoding='utf-8')
        if os.path.getsize('newclass.txt') != 0:
            f.write('\n')
        f.write(str(listn))

        return

    def pushButton_2(self): #返回到管理员主界面
        self.ui.hide()
        global am
        am = AdminMain()
        am.ui.show()
        return

#删除物品类型
class DelClass:
    def __init__(self):
        self.ui = QUiLoader().load('delclass.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)

        listn = []
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            listn.append(list1[0])
        self.ui.comboBox.addItems(listn)
        self.ui.textBrowser.setText('请注意，删除物品类型将导致该类型下所有物品信息全部被删除！')


    def pushButton_1(self): #返回到管理员界面
        self.ui.hide()
        global am
        am = AdminMain()
        am.ui.show()
        return

    def pushButton_2(self): #删除选中的物品类型
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        tmp = []

        delitem = self.ui.comboBox.currentText()
        for i in range(len(classinfo)):
            tmp = eval(classinfo[i])
            if tmp[0] == delitem:
                classinfo.pop(i)
                break

        tmp = eval(classinfo[-1])
        classinfo.pop(-1)
        classinfo.append(str(tmp)) #去除末尾的换行符

        with open('newclass.txt', 'w', encoding='utf-8') as f3:  #
            for temp in classinfo:
                f3.write(str(temp))
        with open(str(tmp[0] + '.txt'), 'w', encoding='utf-8') as f4:  #
            f4.write('')

        listn = []
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            listn.append(list1[0])
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(listn)
        self.ui.textBrowser.setText('删除成功')


        return

#用户主界面
class UserMain:
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('usermain.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4)

    def pushButton_1(self): #用户添加物品信息
        self.ui.hide()
        global ua
        ua = UserAdd()
        ua.ui.show()
        return

    def pushButton_2(self): #用户删除物品信息
        self.ui.hide()
        global ud
        ud = UserDel()
        ud.ui.show()
        return

    def pushButton_3(self): #用户搜索物品信息
        self.ui.hide()
        global us
        us = UserSch()
        us.ui.show()
        return

    def pushButton_4(self): #返回主界面
        self.ui.hide()
        global ma
        ma = FinalHelp()
        ma.ui.show()
        return

#用户添加物品信息
class UserAdd:
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('useradd.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        self.ui.label_1.setText('')
        self.ui.label_2.setText('')
        self.ui.label_3.setText('')
        self.ui.label_4.setText('')
        self.ui.label_5.setText('')

        #初始化复选框和标签
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        list1 = eval(classinfo[0])
        for j in range(len(list1) - 1):
            if j == 0:
                self.ui.label_1.setText(str(list1[j + 1]))
            if j == 1:
                self.ui.label_2.setText(str(list1[j + 1]))
            if j == 2:
                self.ui.label_3.setText(str(list1[j + 1]))
            if j == 3:
                self.ui.label_4.setText(str(list1[j + 1]))
            if j == 4:
                self.ui.label_5.setText(str(list1[j + 1]))

        listn = []
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            listn.append(list1[0])
        self.ui.comboBox.addItems(listn)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)


    def selectionchange(self): #复选框内容改变时，显示新的物品属性
        self.ui.label_1.setText('')
        self.ui.label_2.setText('')
        self.ui.label_3.setText('')
        self.ui.label_4.setText('')
        self.ui.label_5.setText('')
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            if list1[0] == self.ui.comboBox.currentText():
                for j in range(len(list1)-1):
                    if j == 0 :
                        self.ui.label_1.setText(str(list1[j+1]))
                    if j == 1 :
                        self.ui.label_2.setText(str(list1[j+1]))
                    if j == 2 :
                        self.ui.label_3.setText(str(list1[j+1]))
                    if j == 3 :
                        self.ui.label_4.setText(str(list1[j+1]))
                    if j == 4 :
                        self.ui.label_5.setText(str(list1[j+1]))
        return



    def pushButton_1(self): #返回主界面
        self.ui.hide()
        global um
        um = UserMain()
        um.ui.show()
        return

    def pushButton_2(self): #添加物品，从'newclass.txt'中读出物品属性，写入物品类型对应的文件中
        newclass = self.ui.comboBox.currentText()
        lenl = 0
        listl = []
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            if list1[0] == self.ui.comboBox.currentText():
                lenl = len(list1)-1

        strl = str(self.ui.lineEdit_6.text())
        listl.append(strl)
        strl = str(self.ui.lineEdit_7.text())
        listl.append(strl)
        strl = str(self.ui.lineEdit_8.text())
        listl.append(strl)
        strl = str(self.ui.lineEdit_9.text())
        listl.append(strl)
        strl = str(self.ui.lineEdit_10.text())
        listl.append(strl)

        for i in range(lenl):
            if i == 0:
                strl = str(self.ui.lineEdit_1.text())
                listl.append(strl)
            if i == 1:
                strl = str(self.ui.lineEdit_2.text())
                listl.append(strl)
            if i == 2:
                strl = str(self.ui.lineEdit_3.text())
                listl.append(strl)
            if i == 3:
                strl = str(self.ui.lineEdit_4.text())
                listl.append(strl)
            if i == 4:
                strl = str(self.ui.lineEdit_5.text())
                listl.append(strl)

        for i in range(len(listl)):
            if listl[i] == '':
                self.ui.textBrowser.setText(str('添加失败，物品属性不能为空'))
                return

        f2 = open(str(newclass) + ".txt" , 'a', encoding= 'utf-8')
        if os.path.getsize(str(newclass) + '.txt') != 0:
            f2.write('\n')
        f2.write(str(listl))

        self.ui.lineEdit_1.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()
        self.ui.lineEdit_8.clear()
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_10.clear()
        self.ui.textBrowser.setText(str('添加成功'))

        return


#用户删除物品信息
class UserDel:
    num = 0 #当前读取的物品序号
    nummax = 0 #物品总数量
    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('userdel.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4)
        self.ui.label_6.setText('')
        self.ui.label_7.setText('')
        self.ui.label_8.setText('')
        self.ui.label_9.setText('')
        self.ui.label_10.setText('')
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        list1 = eval(classinfo[0])
        for j in range(len(list1) - 1):
            if j == 0:
                self.ui.label_6.setText(str(list1[j + 1]))
            if j == 1:
                self.ui.label_7.setText(str(list1[j + 1]))
            if j == 2:
                self.ui.label_8.setText(str(list1[j + 1]))
            if j == 3:
                self.ui.label_9.setText(str(list1[j + 1]))
            if j == 4:
                self.ui.label_10.setText(str(list1[j + 1]))

        #初始化物品属性标签栏和物品内容
        listn = []
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            listn.append(list1[0])

        self.ui.comboBox.addItems(listn)

        tmp = eval(classinfo[0])
        with open(str(tmp[0]) + '.txt', 'r', encoding='utf-8') as f2:
            classinfo2 = f2.readlines()
        self.nummax = len(classinfo2)
        tmp2 = eval(classinfo2[0])
        for j in range(len(tmp2)):
            if j == 0:
                self.ui.textBrowser_1.setText(str(tmp2[j]))
            if j == 1:
                self.ui.textBrowser_2.setText(str(tmp2[j]))
            if j == 2:
                self.ui.textBrowser_3.setText(str(tmp2[j]))
            if j == 3:
                self.ui.textBrowser_4.setText(str(tmp2[j]))
            if j == 4:
                self.ui.textBrowser_5.setText(str(tmp2[j]))
            if j == 5:
                self.ui.textBrowser_6.setText(str(tmp2[j]))
            if j == 6:
                self.ui.textBrowser_7.setText(str(tmp2[j]))
            if j == 7:
                self.ui.textBrowser_8.setText(str(tmp2[j]))
            if j == 8:
                self.ui.textBrowser_9.setText(str(tmp2[j]))
            if j == 9:
                self.ui.textBrowser_10.setText(str(tmp2[j]))
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)

    def pushButton_1(self): #查看上一条内容
        if self.num == 0 :
            return
        else:
            self.num -= 1
            self.refresh()
        return

    def pushButton_2(self): #回到用户主界面
        self.ui.hide()
        global um
        um = UserMain()
        um.ui.show()
        return

    def pushButton_3(self): #查看下一条内容
        if self.num == self.nummax-1 :
            return
        else:
            self.num += 1
            self.refresh()
        return

    def pushButton_4(self): #删除物品

        cur = self.ui.comboBox.currentText()
        with open(str(cur) + '.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        if len(classinfo) == 0:
            return
        classinfo.pop(self.num)

        tmp = []
        tmp = eval(classinfo[-1])
        classinfo.pop(-1)
        classinfo.append(str(tmp))  # 去除末尾的换行符

        with open(str(cur) + '.txt', 'w', encoding='utf-8') as f3:  #
            for temp in classinfo:
                f3.write(str(temp))

        if self.num == self.nummax - 1 :
            self.num -= 1
        self.nummax -= 1
        self.refresh()
        return

    def selectionchange(self): #复选框内容改变后重置标签
        self.num = 0
        cur = self.ui.comboBox.currentText()
        with open(str(cur) + '.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        if len(classinfo) == 0:
            return
        self.nummax = len(classinfo)
        with open('newclass.txt', 'r', encoding='utf-8') as f2:
            classinfo2 = f2.readlines()
        for i in range(len(classinfo2)):
            listt = eval(classinfo2[i])
            if listt[0] == cur:
                for j in range(len(listt)-1):
                    if j == 0:
                        self.ui.label_6.setText(str(listt[j + 1]))
                    if j == 1:
                        self.ui.label_7.setText(str(listt[j + 1]))
                    if j == 2:
                        self.ui.label_8.setText(str(listt[j + 1]))
                    if j == 3:
                        self.ui.label_9.setText(str(listt[j + 1]))
                    if j == 4:
                        self.ui.label_10.setText(str(listt[j + 1]))

        self.refresh()
        return

    def refresh(self): #刷新显示的内容
        cur = self.ui.comboBox.currentText()
        with open(str(cur) + '.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        if len(classinfo) == 0:
            return
        list1 = eval(classinfo[self.num])
        for j in range(len(list1)):
            if j == 0:
                self.ui.textBrowser_1.setText(str(list1[j]))
            if j == 1:
                self.ui.textBrowser_2.setText(str(list1[j]))
            if j == 2:
                self.ui.textBrowser_3.setText(str(list1[j]))
            if j == 3:
                self.ui.textBrowser_4.setText(str(list1[j]))
            if j == 4:
                self.ui.textBrowser_5.setText(str(list1[j]))
            if j == 5:
                self.ui.textBrowser_6.setText(str(list1[j]))
            if j == 6:
                self.ui.textBrowser_7.setText(str(list1[j]))
            if j == 7:
                self.ui.textBrowser_8.setText(str(list1[j]))
            if j == 8:
                self.ui.textBrowser_9.setText(str(list1[j]))
            if j == 9:
                self.ui.textBrowser_10.setText(str(list1[j]))
        return

#用户搜索物品
class UserSch:
    def __init__(self):
        self.ui = QUiLoader().load('usersch.ui')
        self.ui.pushButton_1.clicked.connect(self.pushButton_1)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        self.ui.label_6.setText('')
        self.ui.label_7.setText('')
        self.ui.label_8.setText('')
        self.ui.label_9.setText('')
        self.ui.label_10.setText('')
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        list1 = eval(classinfo[0])
        for j in range(len(list1) - 1):
            if j == 0:
                self.ui.label_6.setText(str(list1[j + 1]))
            if j == 1:
                self.ui.label_7.setText(str(list1[j + 1]))
            if j == 2:
                self.ui.label_8.setText(str(list1[j + 1]))
            if j == 3:
                self.ui.label_9.setText(str(list1[j + 1]))
            if j == 4:
                self.ui.label_10.setText(str(list1[j + 1]))

        listn = []
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            listn.append(list1[0])
        self.ui.comboBox.addItems(listn)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)

    def pushButton_1(self): #按照关键字在物品名称和说明中查询物品
        self.ui.textBrowser_1.clear()
        self.ui.textBrowser_2.clear()
        self.ui.textBrowser_3.clear()
        self.ui.textBrowser_4.clear()
        self.ui.textBrowser_5.clear()
        self.ui.textBrowser_6.clear()
        self.ui.textBrowser_7.clear()
        self.ui.textBrowser_8.clear()
        self.ui.textBrowser_9.clear()
        self.ui.textBrowser_10.clear()
        sch = self.ui.lineEdit.text()
        cclass = self.ui.comboBox.currentText()
        with open(str(cclass) + '.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()

        if sch == '' :
            for i in range(len(classinfo)):
                listl = eval(classinfo[i])
                for j in range(len(listl)):
                    if j == 0:
                        self.ui.textBrowser_1.append(str(listl[j]))
                    if j == 1:
                        self.ui.textBrowser_2.append(str(listl[j]))
                    if j == 2:
                        self.ui.textBrowser_3.append(str(listl[j]))
                    if j == 3:
                        self.ui.textBrowser_4.append(str(listl[j]))
                    if j == 4:
                        self.ui.textBrowser_5.append(str(listl[j]))
                    if j == 5:
                        self.ui.textBrowser_6.append(str(listl[j]))
                    if j == 6:
                        self.ui.textBrowser_7.append(str(listl[j]))
                    if j == 7:
                        self.ui.textBrowser_8.append(str(listl[j]))
                    if j == 8:
                        self.ui.textBrowser_9.append(str(listl[j]))
                    if j == 9:
                        self.ui.textBrowser_10.append(str(listl[j]))

        else:
            listn = []
            for i in range(len(classinfo)):
                listl = eval(classinfo[i])
                if sch in listl[0] or sch in listl[1]:
                    listn.append(listl)
            for i in range(len(listn)):
                for j in range(len(listn[i])):
                    if j == 0:
                        self.ui.textBrowser_1.append(str(listn[i][j]))
                    if j == 1:
                        self.ui.textBrowser_2.append(str(listn[i][j]))
                    if j == 2:
                        self.ui.textBrowser_3.append(str(listn[i][j]))
                    if j == 3:
                        self.ui.textBrowser_4.append(str(listn[i][j]))
                    if j == 4:
                        self.ui.textBrowser_5.append(str(listn[i][j]))
                    if j == 5:
                        self.ui.textBrowser_6.append(str(listn[i][j]))
                    if j == 6:
                        self.ui.textBrowser_7.append(str(listn[i][j]))
                    if j == 7:
                        self.ui.textBrowser_8.append(str(listn[i][j]))
                    if j == 8:
                        self.ui.textBrowser_9.append(str(listn[i][j]))
                    if j == 9:
                        self.ui.textBrowser_10.append(str(listn[i][j]))
        return

    def pushButton_2(self): #返回用户主界面
        self.ui.hide()
        global um
        um = UserMain()
        um.ui.show()
        return

    def selectionchange(self): #更改选择后，更新标签信息
        self.ui.label_6.setText('')
        self.ui.label_7.setText('')
        self.ui.label_8.setText('')
        self.ui.label_9.setText('')
        self.ui.label_10.setText('')
        with open('newclass.txt', 'r', encoding='utf-8') as f1:
            classinfo = f1.readlines()
        for i in range(len(classinfo)):
            list1 = eval(classinfo[i])
            if list1[0] == self.ui.comboBox.currentText():
                for j in range(len(list1)-1):
                    if j == 0 :
                        self.ui.label_6.setText(str(list1[j+1]))
                    if j == 1 :
                        self.ui.label_7.setText(str(list1[j+1]))
                    if j == 2 :
                        self.ui.label_8.setText(str(list1[j+1]))
                    if j == 3 :
                        self.ui.label_9.setText(str(list1[j+1]))
                    if j == 4 :
                        self.ui.label_10.setText(str(list1[j+1]))
        self.ui.textBrowser_1.clear()
        self.ui.textBrowser_2.clear()
        self.ui.textBrowser_3.clear()
        self.ui.textBrowser_4.clear()
        self.ui.textBrowser_5.clear()
        self.ui.textBrowser_6.clear()
        self.ui.textBrowser_7.clear()
        self.ui.textBrowser_8.clear()
        self.ui.textBrowser_9.clear()
        self.ui.textBrowser_10.clear()

        return



app = QApplication([])
Final = FinalHelp()
Final.ui.show()
app.exec_()
