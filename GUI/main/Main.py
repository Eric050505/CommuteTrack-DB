import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow

import User
import add_L
import add_S
import admin
import c_alight
import c_board
import card_add
import card_ride
import change_pass
import delete_L
import delete_S
import delete_self
import modify_L
import modify_S
import p_alight
import p_board
import passenger_add
import passenger_inf
import passenger_ride
import place_new_station
import query_adjacent_stations
import read_lines
import read_path_least_stations
import read_stations
import read_two_stations_price
import read_unf_c_rides
import read_unf_p_rides
import remove_station_in_line
import user_ability
import user_delete
from Error import Ui_Error
from LogWindow import Ui_LogWindow
from MainMenu import Ui_MainMenu
from RigesterWindow import Ui_RigesterWindow

un = ""
pw = ""
p_i = ""
c_c = ""
permi = ""


class MyMainForm(QMainWindow, Ui_LogWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.LogIn_2.clicked.connect(self.display)
        # 添加退出按钮信号和槽。调用close函数
        self.Register.clicked.connect(self.GotoRigester)

    def display(self):

        # 利用line Edit控件对象text()函数获取界面输入
        username = self.UserName.text()
        password = self.Password_2.text()
        result = requests.get(f'http://10.27.117.57:8000/user/{username}')
        dic = result.json()
        try:
            s = dic["detail"]
            self.UserTips.setText("No such user")
            self.PasswordTips.setText("")
        except:
            # if dic["detail"]!="User not found":
            #     a=1

            if dic["password"] == password:
                global un
                global pw
                global p_i
                global c_c
                global permi
                un = username
                pw = password
                p_i = dic["passenger_id"]
                c_c = dic["card_code"]
                permi = dic["permission"]
                self.GoToMainMenu()
            else:
                self.UserTips.setText("")
                self.PasswordTips.setText("Password error")
        # else:

        # conn = psycopg2.connect(
        #     dbname="postgres",
        #     user="postgres",
        #     password="1278876776qwer",
        #     host="localhost",
        #     port="5432"
        # )
        #
        # # 创建一个游标对象
        # cur = conn.cursor()
        #
        # # 执行 SQL 查询
        # cur.execute("select pg_user.usename,pg_user.passwd from pg_user")
        #
        # # 获取结果
        # rows = cur.fetchall()
        # exist = False
        # cur.close()
        # conn.close()
        # # 处理结果
        # for row in rows:
        #     if (username == row[0]):
        #         exist = True
        #         try:
        #             # 连接到 PostgreSQL 数据库
        #             conn2 = psycopg2.connect(
        #                 dbname="postgres",
        #                 user=username,
        #                 password=password,
        #                 host="localhost",
        #                 port="5432"
        #             )
        #             conn2.close()  # 关闭连接
        #             self.UserTips.setText("accept")
        #             global un
        #             global pw
        #             un = username
        #             pw = password
        #             print(un)
        #             print(pw)
        #             self.GoToMainMenu()
        #
        #         except:
        #             self.UserTips.setText("")
        #             self.PasswordTips.setText("Password error")
        #
        # # 关闭游标和数据库连接
        # if (exist == False):
        #     self.UserTips.setText("No such user")
        #     self.PasswordTips.setText("")

    def GotoRigester(self):
        self.RegisterWindow = MyRigesterForm()
        self.RegisterWindow.setWindowTitle("Register")
        self.RegisterWindow.show()
        self.close()

    def GoToMainMenu(self):
        self.MenuWindow = MyMenuForm()
        self.MenuWindow.setWindowTitle("Menu")
        self.MenuWindow.show()
        self.close()


class MyRigesterForm(QMainWindow, Ui_RigesterWindow):
    def __init__(self, parent=None):
        super(MyRigesterForm, self).__init__(parent)
        self.setupUi0(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.Register_2.clicked.connect(self.createUser)
        # 添加退出按钮信号和槽。调用close函数
        self.Back.clicked.connect(self.GotoLogin)

    def createUser(self):
        username = self.UserName.text()
        password = self.Password_2.text()
        identity = self.identityInput.text()

        result = requests.get(f'http://10.27.117.57:8000/user/{username}')
        dic = result.json()
        print(result.text)
        if (len(identity) == 18 or (len(identity) == 9 and identity.isdigit())):
            try:
                s = dic["detail"]
                if len(identity) == 18:
                    passen = requests.get(f'http://10.27.117.57:8000/passengers/{identity}')
                    dic = passen.json()

                    try:
                        a = dic["passenger_id"]
                        data = {
                            "user_name": username,
                            "password": password,
                            "passenger_id": identity,
                            "permission": "normal"
                        }
                        response = requests.post('http://10.27.117.57:8000/add_user', json=data)
                        res = response.json()
                        self.PasswordTips.setText(res["message"])
                    except:
                        self.IdentityTips.setText("No such people")
                else:
                    passen = requests.get(f'http://10.27.117.57:8000/cards/{identity}')
                    dic = passen.json()

                    try:
                        a = dic["code"]
                        data = {
                            "user_name": username,
                            "password": password,
                            "card_code": identity,
                            "permission": "normal"
                        }
                        response = requests.post('http://10.27.117.57:8000/add_user', json=data)
                        res = response.json()
                        print(response.text)
                        self.PasswordTips.setText(res["message"])
                    except:
                        self.IdentityTips.setText("No such card")
            except:
                self.UserTips.setText("There is such user")

        else:
            self.IdentityTips.setText("Please input 18 id or 9 numbers")

    def GotoLogin(self):
        self.mainWindow = MyMainForm()
        self.mainWindow.setWindowTitle("Log in")
        self.mainWindow.show()
        self.close()


class MyMenuForm(QMainWindow, Ui_MainMenu):
    def __init__(self, parent=None):
        super(MyMenuForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()

        self.Admin.clicked.connect(self.AWindow)
        self.users.clicked.connect(self.UWindow)

        self.changeUser.clicked.connect(self.Back)
        self.Exit.clicked.connect(self.close)

    def AWindow(self):
        print(un)
        print(pw)
        result = requests.get(f'http://10.27.117.57:8000/user/{un}')
        dic = result.json()
        if dic["permission"] == "admin":
            self.mainWindow = MyAWindowForm()
            self.mainWindow.setWindowTitle("Admin")
            self.mainWindow.show()
            self.close()
        else:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.tips.setText("You are not administrator")
            self.mainWindow.show()
        # try:
        #     conn = psycopg2.connect(
        #         dbname="postgres",
        #         user=un,
        #         password=pw,
        #         host="localhost",
        #         port="5432"
        #     )
        #
        #     # 创建游标对象
        #     cur = conn.cursor()
        #
        #     # 构建创建用户的 SQL 命令
        #
        #     cur.execute(
        #         "insert into passenger (passenger_id, id_number, name, phone_number, gender, district) VALUES " +
        #         "(0,0,0,0,0,0)")
        #     cur.execute("delete from passenger where passenger_id='0'")
        #     # 提交事务
        #     conn.commit()
        #
        #     # 关闭连接
        #     cur.close()
        #     conn.close()
        #     self.mainWindow = MyAWindowForm()
        #     self.mainWindow.setWindowTitle("Admin")
        #     self.mainWindow.show()
        #     self.close()
        # except:
        #     self.mainWindow = MyErrorForm()
        #     self.mainWindow.setWindowTitle("Error")
        #     self.mainWindow.tips.setText("You are not administrator")
        #     self.mainWindow.show()

    def UWindow(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()

    def Back(self):
        self.mainWindow = MyMainForm()
        self.mainWindow.setWindowTitle("Log in")
        self.mainWindow.show()
        self.close()


class MyErrorForm(QMainWindow, Ui_Error):
    def __init__(self, parent=None):
        super(MyErrorForm, self).__init__(parent)
        self.setupUi(self)


class MyAWindowForm(QMainWindow, admin.Ui_Form):
    def __init__(self, parent=None):
        super(MyAWindowForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.Back.clicked.connect(self.back)
        self.add_line.clicked.connect(self.add_l)
        self.add_station.clicked.connect(self.add_s)
        self.delete_line.clicked.connect(self.form3)
        self.delete_station.clicked.connect(self.form4)
        self.modify_line.clicked.connect(self.form5)
        self.modify_station.clicked.connect(self.form6)
        self.add_station_3.clicked.connect(self.form7)
        self.delete_station_3.clicked.connect(self.form8)
        self.passenger_up.clicked.connect(self.form9)
        self.passenger_down.clicked.connect(self.form10)
        self.card_up.clicked.connect(self.form11)
        self.card_down.clicked.connect(self.form12)
        self.passenger_not_down.clicked.connect(self.form13)
        self.card_not_down.clicked.connect(self.form14)
        self.modify_user.clicked.connect(self.form20)
        self.delete_user.clicked.connect(self.form21)
        self.information.clicked.connect(self.form22)
        self.passenger_add.clicked.connect(self.form27)
        self.card_add.clicked.connect(self.form28)

    def back(self):
        self.mainWindow = MyMenuForm()
        self.mainWindow.setWindowTitle("Menu")
        self.mainWindow.show()
        self.close()

    def add_l(self):
        self.mainWindow = MyForm1()
        self.mainWindow.setWindowTitle("add line")
        self.mainWindow.show()
        self.close()

    def add_s(self):
        self.mainWindow = MyForm2()
        self.mainWindow.setWindowTitle("add station")
        self.mainWindow.show()
        self.close()

    def form3(self):
        self.mainWindow = MyForm3()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form4(self):
        self.mainWindow = MyForm4()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form5(self):
        self.mainWindow = MyForm5()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form6(self):
        self.mainWindow = MyForm6()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form7(self):
        self.mainWindow = MyForm7()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form8(self):
        self.mainWindow = MyForm8()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form9(self):
        self.mainWindow = MyForm9()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form10(self):
        self.mainWindow = MyForm10()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form11(self):
        self.mainWindow = MyForm11()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form12(self):
        self.mainWindow = MyForm12()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form13(self):
        self.mainWindow = MyForm13()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form14(self):
        self.mainWindow = MyForm14()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form20(self):
        self.mainWindow = MyForm20()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form21(self):
        self.mainWindow = MyForm21()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form22(self):
        self.mainWindow = MyForm22()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form27(self):
        self.mainWindow = MyForm27()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form28(self):
        self.mainWindow = MyForm28()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()


class MyPWindowForm(QMainWindow, User.Ui_Form):
    def __init__(self, parent=None):
        super(MyPWindowForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.Back.clicked.connect(self.back)
        self.after_station.clicked.connect(self.form15)
        self.lines.clicked.connect(self.form16)
        self.prices.clicked.connect(self.form17)
        self.shortest.clicked.connect(self.form18)
        self.pushButton.clicked.connect(self.form19)
        self.passenger.clicked.connect(self.form23)
        self.card.clicked.connect(self.form24)
        self.change_pass.clicked.connect(self.form25)
        self.delete_self.clicked.connect(self.form26)

    def back(self):
        self.mainWindow = MyMenuForm()
        self.mainWindow.setWindowTitle("Menu")
        self.mainWindow.show()
        self.close()

    def form15(self):
        self.mainWindow = MyForm15()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form16(self):
        self.mainWindow = MyForm16()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form17(self):
        self.mainWindow = MyForm17()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form18(self):
        self.mainWindow = MyForm18()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form19(self):
        self.mainWindow = MyForm19()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form23(self):
        self.mainWindow = MyForm23()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form24(self):
        self.mainWindow = MyForm24()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form25(self):
        self.mainWindow = MyForm25()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()

    def form26(self):
        self.mainWindow = MyForm26()
        self.mainWindow.setWindowTitle("")
        self.mainWindow.show()
        self.close()


# functions windows


class MyForm1(QMainWindow, add_L.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm1, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            name = self.name_input.text()
            intro = self.intro_input.text()
            url = self.url_input.text()
            color = self.color_input.text()
            open = self.open_input.text()
            start = self.start_input.text()
            end = self.end_input.text()
            mileage = self.mileage_input.text()
            speed = self.speed_input.text()
            data = {"chinese_name": name,
                    "start_time": start,
                    "end_time": end,
                    "mileage": mileage,
                    "color": color,
                    "first_opening": open,
                    "intro": intro,
                    "url": url,
                    "running_speed": speed
                    }

            result = requests.post('http://10.27.117.57:8000/add_line', json=data)

            self.out.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm2(QMainWindow, add_S.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm2, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)

        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            data = {
                "chinese_name": self.chinese_input.text(),
                "english_name": self.english_input.text(),
                "district": self.district_input.text(),
                "intro": self.intro_input.text(),
                "status": self.status_input.text()
            }
            result = requests.post('http://10.27.117.57:8000/add_station', json=data)

            self.out.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm3(QMainWindow, delete_L.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm3, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)

        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            line_id = self.id_input.text()

            result = requests.delete(f'http://10.27.117.57:8000/delete_line/{line_id}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm4(QMainWindow, delete_S.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm4, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            id = self.id_input.text()

            result = requests.delete(f'http://10.27.117.57:8000/delete_station/{id}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm5(QMainWindow, modify_L.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm5, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            line_id = self.id_input.text()
            name = self.name_input.text()
            intro = self.intro_input.text()
            url = self.url_input.text()
            color = self.color_input.text()
            open = self.open_input.text()
            start = self.start_input.text()
            end = self.end_input.text()
            mileage = self.mileage_input.text()
            speed = self.speed_input.text()
            data = {"chinese_name": name,
                    "start_time": start,
                    "end_time": end,
                    "mileage": mileage,
                    "color": color,
                    "first_opening": open,
                    "intro": intro,
                    "url": url,
                    "running_speed": speed
                    }

            result = requests.put(f'http://10.27.117.57:8000/modify_line/{line_id}', json=data)

            self.out.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm6(QMainWindow, modify_S.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm6, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            station_id = self.id_input.text()
            data = {
                "chinese_name": self.chinese_input.text(),
                "english_name": self.english_input.text(),
                "district": self.district_input.text(),
                "intro": self.intro_input.text(),
                "status": self.status_input.text()
            }
            result = requests.put(f'http://10.27.117.57:8000/modify_station/{station_id}', json=data)

            self.out.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm7(QMainWindow, place_new_station.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm7, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            line_id = self.id_input.text()
            sta = self.station_input.text()
            nu = self.num_input.text()
            stations = sta.split(",")
            nums = nu.split(",")
            print(stations)
            stations1 = [int(x) for x in stations]
            nums1 = [int(x) for x in nums]
            list = []
            for a, b in zip(stations1, nums1):
                di = {
                    "station_id": a,
                    "nums": b
                }
                list.append(di)
            print(list)

            result = requests.post(f'http://10.27.117.57:8000/place_new_stations/{line_id}', json=list)

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm8(QMainWindow, remove_station_in_line.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm8, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            line_id = self.id_input.text()
            station_id = self.station_input.text()

            result = requests.delete(f'http://10.27.117.57:8000/remove_station_in_line/{line_id}/{station_id}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm9(QMainWindow, p_board.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm9, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            passenger_id = self.id_input.text()
            start_station = self.station_input.text()

            result = requests.post(f'http://10.27.117.57:8000/p_board/{passenger_id}/{start_station}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm10(QMainWindow, p_alight.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm10, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            passenger_id = self.id_input.text()
            start_station = self.station_input.text()
            end_station = self.end_input.text()

            result = requests.post(f'http://10.27.117.57:8000/p_alight/{passenger_id}/{start_station}/{end_station}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm11(QMainWindow, c_board.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm11, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            card_code = self.id_input.text()
            start_station = self.station_input.text()

            result = requests.post(f'http://10.27.117.57:8000/c_board/{card_code}/{start_station}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm12(QMainWindow, c_alight.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm12, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            card_code = self.id_input.text()
            start_station = self.station_input.text()
            end_station = self.end_input.text()

            result = requests.post(f'http://10.27.117.57:8000/c_alight/{card_code}/{start_station}/{end_station}')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm13(QMainWindow, read_unf_p_rides.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm13, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            result = requests.get('http://10.27.117.57:8000/unfinished_passenger_rides')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm14(QMainWindow, read_unf_c_rides.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm14, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            result = requests.get('http://10.27.117.57:8000/unfinished_card_rides')

            self.textBrowser.setText(result.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm15(QMainWindow, query_adjacent_stations.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm15, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            line_id = self.id_input.text()
            station_id = self.station_input.text()
            n = self.n_input.text()

            result = requests.get(f'http://10.27.117.57:8000/adjacent_stations/{line_id}/{station_id}/{n}')
            dic = result.json()
            output_str = ""
            for key, value in dic.items():
                output_str += f"{key}: {value}\n"
            print(output_str)
            self.textBrowser.setText(output_str)

        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm16(QMainWindow, read_lines.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm16, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            line_id = self.id_input.text()

            result = requests.get(f'http://10.27.117.57:8000/lines/{line_id}')

            output_str = ""
            dic = result.json()
            # 遍历字典的键值对，将每个键值对的输出添加到字符串中，并在每行之间添加换行符
            for key, value in dic.items():
                output_str += f"{key}: {value}\n"
            print(output_str)
            self.textBrowser.setText(output_str)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm17(QMainWindow, read_two_stations_price.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm17, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            start_station = self.start_input.text()
            end_station = self.end_input.text()

            result = requests.get(f'http://10.27.117.57:8000/price/{start_station}/{end_station}')
            dic = result.json()
            output_str = ""
            # 遍历字典的键值对，将每个键值对的输出添加到字符串中，并在每行之间添加换行符
            for key, value in dic.items():
                output_str += f"{key}: {value}\n"
            print(output_str)
            self.textBrowser.setText(output_str)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm18(QMainWindow, read_path_least_stations.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm18, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        try:

            start_station = self.station_input.text()
            end_station = self.end_input.text()

            result = requests.get(f'http://10.27.117.57:8000/path_least_stations/{start_station}/{end_station}')
            result2 = requests.get(f'http://10.27.117.57:8000/path_shortest_time/{start_station}/{end_station}')
            result3 = requests.get(f'http://10.27.117.57:8000/path_multi_least_stations/{start_station}/{end_station}')
            self.textBrowser.setText("min stations:" + result.text)
            self.textBrowser.append("min time:" + result2.text)
            self.textBrowser.append("else:" + result3.text)
        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm19(QMainWindow, read_stations.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm19, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)

        self.OK.clicked.connect(self.func)

    def func(self):
        try:
            station_id = self.id_input.text()

            result = requests.get(f'http://10.27.117.57:8000/stations/{station_id}')

            output_str = ""
            dic = result.json()
            # 遍历字典的键值对，将每个键值对的输出添加到字符串中，并在每行之间添加换行符
            for key, value in dic.items():
                output_str += f"{key}: {value}\n"

            self.textBrowser.setText(output_str)

        except:
            self.mainWindow = MyErrorForm()
            self.mainWindow.setWindowTitle("Error")
            self.mainWindow.show()

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm20(QMainWindow, user_ability.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm20, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        user_name = self.user_input.text()
        if (self.ability_input.text() != "admin"):
            per = "normal"
        else:
            per = "admin"
        password = ""
        if self.password_input.text() != "":
            password = self.password_input.text()
        else:
            password = pw
        data = {

            "password": password,
            "permission": per
        }
        result = requests.post(f'http://10.27.117.57:8000/modify_user/{user_name}', json=data)

        self.textBrowser.setText(result.text)

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm21(QMainWindow, user_delete.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm21, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)

        self.OK.clicked.connect(self.func)

    def func(self):
        user_name = self.user_input.text()
        response = requests.get(f'http://10.27.117.57:8000/user/{user_name}')
        di = response.json()
        data = {
            "password": di["password"]
        }
        result = requests.delete(f'http://10.27.117.57:8000/delete_user/{user_name}', json=data)

        self.textBrowser.setText(result.text)

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm22(QMainWindow, passenger_inf.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm22, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)
        self.OK2.clicked.connect(self.func2)

    def func(self):
        passenger_id = self.passenger_id_input.text()
        start_station = self.start_station_input.text()
        end_station = self.end_station_input.text()
        start_time = self.start_time_input.text()
        end_time = self.end_time_input.text()
        data1 = {
        }
        if start_station != "":
            data1.update({"start_station": start_station})
        if end_station != "":
            data1.update({"end_station": end_station})
        if start_time != "":
            data1.update({"start_time": start_time})
        if end_time != "":
            data1.update({"end_time": end_time})
        result1 = requests.get(f'http://10.27.117.57:8000/passenger_ride/{passenger_id}', json=data1)
        try:
            output = ""
            response = result1.json()
            for item in response:
                for key, value in item.items():
                    output += f"{key}: {value}\n"
                output += "\n"  # 添加空行，以分隔每个字典的输出

            self.textBrowser.setText(output)
        except:
            self.textBrowser.setText(result1.text)

    def func2(self):

        card_code = self.card_code_input.text()
        start_station = self.start_station_input.text()
        end_station = self.end_station_input.text()
        start_time = self.start_time_input.text()
        end_time = self.end_time_input.text()
        data2 = {
        }
        if start_station != "":
            data2.update({"start_station": start_station})
        if end_station != "":
            data2.update({"end_station": end_station})
        if start_time != "":
            data2.update({"start_time": start_time})
        if end_time != "":
            data2.update({"end_time": end_time})
        result2 = requests.get(f'http://10.27.117.57:8000/card_ride/{card_code}', json=data2)
        try:
            output = ""
            response = result2.json()
            for item in response:
                for key, value in item.items():
                    output += f"{key}: {value}\n"
                output += "\n"  # 添加空行，以分隔每个字典的输出

            self.textBrowser2.setText(output)
        except:
            self.textBrowser2.setText(result2.text)

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm23(QMainWindow, passenger_ride.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm23, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        print(p_i)
        print(c_c)
        if (p_i is not None):
            passenger_id = p_i
            start_station = self.start_station_input.text()
            end_station = self.end_station_input.text()
            start_time = self.start_time_input.text()
            end_time = self.end_time_input.text()
            data1 = {
            }
            if start_station != "":
                data1.update({"start_station": start_station})
            if end_station != "":
                data1.update({"end_station": end_station})
            if start_time != "":
                data1.update({"start_time": start_time})
            if end_time != "":
                data1.update({"end_time": end_time})
            result = requests.get(f'http://10.27.117.57:8000/passenger_ride/{passenger_id}', json=data1)
            try:
                output = ""
                response = result.json()
                for item in response:
                    for key, value in item.items():
                        output += f"{key}: {value}\n"
                    output += "\n"  # 添加空行，以分隔每个字典的输出

                self.textBrowser.setText(output)
            except:
                self.textBrowser.setText(result.text)
        else:
            self.textBrowser.setText("You are not passenger")

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm24(QMainWindow, card_ride.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm24, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)

        self.OK.clicked.connect(self.func)

    def func(self):
        if (str(c_c) is not None):
            response = requests.get(f'http://10.27.117.57:8000/user/{un}')
            di = response.json()
            if di["card_code"] == c_c:
                card_code = self.code_input.text()

                print(type(card_code))
                start_station = self.start_station_input.text()
                end_station = self.end_station_input.text()
                start_time = self.start_time_input.text()
                end_time = self.end_time_input.text()
                data1 = {}
                if start_station != "":
                    data1.update({"start_station": start_station})
                if end_station != "":
                    data1.update({"end_station": end_station})
                if start_time != "":
                    data1.update({"start_time": start_time})
                if end_time != "":
                    data1.update({"end_time": end_time})
                result = requests.get(f'http://10.27.117.57:8000/card_ride/{card_code}', json=data1)
                try:
                    output = ""
                    response = result.json()
                    for item in response:
                        for key, value in item.items():
                            output += f"{key}: {value}\n"
                        output += "\n"  # 添加空行，以分隔每个字典的输出

                    self.textBrowser.setText(output)
                except:
                    self.textBrowser.setText(result.text)
            else:
                print(c_c)
                print(type(c_c))
                print(di["card_code"])
                self.textBrowser.setText("You can only query yourself card")


        else:
            self.textBrowser.setText("You do not have card")

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm25(QMainWindow, change_pass.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm25, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        o_password = self.old_pass_input.text()
        n_password = self.new_pass_input.text()
        print(pw)
        print(o_password)

        if (o_password == pw):
            user_name = un
            data = {

                "password": n_password,
                "permission": permi
            }
            result = requests.post(f'http://10.27.117.57:8000/modify_user/{user_name}', json=data)

            self.textBrowser.setText(result.text)
            self.mainWindow = MyMainForm()
            self.mainWindow.setWindowTitle("Log in")
            self.mainWindow.show()
            self.close()
        else:
            self.textBrowser.setText("password error")

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm26(QMainWindow, delete_self.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm26, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        if (pw == self.pass_input.text()):
            user_name = un
            data = {
                "user_name": un,
                "password": pw
            }

            result = requests.delete(f'http://10.27.117.57:8000/delete_user/{user_name}', json=data)
            self.textBrowser.setText(result.text)
            self.mainWindow = MyMainForm()
            self.mainWindow.setWindowTitle("Log in")
            self.mainWindow.show()
            self.close()

    def exit(self):
        self.mainWindow = MyPWindowForm()
        self.mainWindow.setWindowTitle("User")
        self.mainWindow.show()
        self.close()


class MyForm27(QMainWindow, passenger_add.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm27, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        data = {
            "name": self.name_input.text(),
            "gender": self.gender_input.text(),
            "id_number": self.id_input.text(),
            "district": self.district_input.text(),
            "phone_number": self.phone_input.text()
        }

        result = requests.post(f'http://10.27.117.57:8000/add_passenger', json=data)
        self.textBrowser.setText(result.text)

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


class MyForm28(QMainWindow, card_add.Ui_modify_L):
    def __init__(self, parent=None):
        super(MyForm28, self).__init__(parent)
        self.setupUi(self)

        self.Exit.clicked.connect(self.exit)
        self.OK.clicked.connect(self.func)

    def func(self):
        data = {
            "code": self.id_input.text(),
            "money": self.remain_input.text()
        }

        result = requests.post(f'http://10.27.117.57:8000/add_card', json=data)
        self.textBrowser.setText(result.text)

    def exit(self):
        self.mainWindow = MyAWindowForm()
        self.mainWindow.setWindowTitle("Admin")
        self.mainWindow.show()
        self.close()


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    myWin.setWindowTitle("Log in")
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
