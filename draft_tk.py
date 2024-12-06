from tkinter import *
import serial,time,re
import serial.tools.list_ports
import os
import json
import math
import CRC_16_XMODEM
import threading


# mytxtfile ="D:\\pycharm\\git-t\\Serial_Tool\\baocun.txt"
control_cmd_file = "D:\\pycharm\\git-t\\Serial_Tool\\control_to_gauges_cmd.json"
control_to_gauges_response_key = []
control_to_gauges_response_val = []
control_count = 0

bms_cmd_file ="D:\\pycharm\\git-t\\Serial_Tool\\bms_to_gauges_cmd.json"
bms_to_gauges_response_key = []
bms_to_gauges_response_val = []
bms_count = 0

other_bms_cmd_file = "D:\\pycharm\\git-t\\Serial_Tool\\other_bms_to_gauges.json"
other_bms_to_gauges_response_key = []
other_bms_to_gauges_response_val = []
other_bms_count = 0

enquiry_bms_cmd_file = "D:\\pycharm\\git-t\\Serial_Tool\\enquiry_bms.json"
enquiry_bms_key = []
enquiry_bms_val = []
enquiry_bms_count = 0

# 读取TXT文件，显示在tkinter的Text
# def in_f_txt():
#     if os.path.exists(mytxtfile):
#         a = open(mytxtfile, 'r', encoding='utf-8')
#         for id_names in a:
#             control_to_gauges_cmd_val.append(id_names)
#         print(control_to_gauges_cmd_val)
#         a.close()

# 读取json文件，显示在tkinter的Text
def read_control_json(file):
    global control_count
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
            jsonlist_key = load_dict.keys()
            keys = list(jsonlist_key)
            for key in keys:
                print(key)
                control_to_gauges_response_key.append(key)
            jsonlist_val = load_dict.values()
            values = list(jsonlist_val)
            for val in values:
                print(val)
                control_count += 1
                control_to_gauges_response_val.append(val)
        print(control_count)

def read_bms_json(file):
    global bms_count
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
            jsonlist_key = load_dict.keys()
            keys = list(jsonlist_key)
            for key in keys:
                print(key)
                bms_to_gauges_response_key.append(key)
            jsonlist_val = load_dict.values()
            values = list(jsonlist_val)
            for val in values:
                print(val)
                bms_count += 1
                bms_to_gauges_response_val.append(val)
        print(bms_count)

def read_other_bms_json(file):
    global other_bms_count
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
            jsonlist_key = load_dict.keys()
            keys = list(jsonlist_key)
            for key in keys:
                print(key)
                other_bms_to_gauges_response_key.append(key)
            jsonlist_val = load_dict.values()
            values = list(jsonlist_val)
            for val in values:
                print(val)
                other_bms_count += 1
                other_bms_to_gauges_response_val.append(val)
        print(other_bms_count)

def enquiry_bms_json(file):
    global enquiry_bms_count
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
            jsonlist_key = load_dict.keys()
            keys = list(jsonlist_key)
            for key in keys:
                print(key)
                enquiry_bms_key.append(key)
            jsonlist_val = load_dict.values()
            values = list(jsonlist_val)
            for val in values:
                print(val)
                enquiry_bms_count += 1
                enquiry_bms_val.append(val)
        print(enquiry_bms_count)

def port_test(send):
    # 创建串口对象
    ser = serial.Serial(port="COM4", baudrate=19200, stopbits=1, timeout=0.5)
    print("aaaa")
    # 判断串口是否打开
    if ser.is_open:
        print('open success.')
        ser.write(bytes.fromhex(send))
        print(type(send))
    else:
        print('open failed.')

    # 关闭串口
    ser.close()


class test_tool():
    def __init__(self,init_window_name):
        # 主窗口
        self.init_window_name = init_window_name
        self.ctr_cmd_opt = ["故障", "速度/0.1KM", "实时功率/W", "当前电压/mV", "当前电流/mA", "电机温度/1℃"]
        self.cust_text = []
        self.CheckVars = []
        self.cust_err = ["控制器通讯故障", "控制器过流保护", "控制器电流采样故障", "油门故障", "刹把故障",
                         "电机霍尔故障", "MOS上桥故障", "MOS下桥故障", "电池包短路断路","控制器温度传感器故障", "控制器温度过高"]

        self.ch1 = None
        self.ch2 = None

        self.inp1 = None
        self.inp2 = None
        self.btn1 = None
        self.btn2 = None
        self.a = None
        self.b = None

        self.button_list = []
        self.cmd = ["cmd1", "cmd2", "cmd3", "cmd4", "cmd5", "cmd6", "cmd7"]
        self.input_text = []

        # 临时变量
        self.temp_button = None
        self.temp_CheckVar = None
        self.temp_text = None
        self.temp_CheckBut = None

        # bms子窗口
        self.init_bms_window = None
        # 按钮
        self.bms_btn_relx = 0.03
        self.bms_btn_rely = 0.04
        # 复选框
        self.bms_check_relx = 0.12
        self.bms_check_rely = 0.04
        # 输入框
        self.bms_text_relx = 0.4
        self.bms_text_rely = 0.04
        self.bms_checkVar = []
        self.bms_text = []

        self.bms_time_text = None
        self.bms_numb_text = None
        self.bms_lb = None

        # 控制器应答仪表-子窗口
        self.init_ctr_window = None
        # 按钮
        self.ctr_btn_relx = 0.03
        self.ctr_btn_rely = 0.04
        # 复选框
        self.ctr_check_relx = 0.12
        self.ctr_check_rely = 0.04
        # 输入框
        self.ctr_text_relx = 0.4
        self.ctr_text_rely = 0.04
        self.ctr_checkVar = []
        self.ctr_text = []

        self.ctr_time_text = None
        self.ctr_numb_text = None
        self.ctr_lb = None
        # other bms子窗口
        self.init_other_bms_window = None
        # 按钮
        self.other_bms_btn_relx = 0.03
        self.other_bms_btn_rely = 0.04
        # 复选框
        self.other_bms_check_relx = 0.12
        self.other_bms_check_rely = 0.04
        # 输入框
        self.other_bms_text_relx = 0.4
        self.other_bms_text_rely = 0.04
        self.other_bms_checkVar = []
        self.other_bms_text = []

        self.other_bms_time_text = None
        self.other_bms_numb_text = None
        self.other_bms_lb = None

        # 查询 bms子窗口
        self.init_enquiry_bms_window = None
        # 按钮
        self.enquiry_bms_btn_relx = 0.03
        self.enquiry_bms_btn_rely = 0.04
        # 复选框
        self.enquiry_bms_check_relx = 0.12
        self.enquiry_bms_check_rely = 0.04
        # 输入框
        self.enquiry_bms_text_relx = 0.4
        self.enquiry_bms_text_rely = 0.04
        self.enquiry_bms_checkVar = []
        self.enquiry_bms_text = []

        self.enquiry_bms_time_text = None
        self.enquiry_bms_numb_text = None
        self.enquiry_bms_lb = None


        # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("上位机调试命令")  # 窗口名
        self.init_window_name.geometry('1400x800+10+10')#290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置

        self.btn2 = Button(self.init_window_name, text="自定义仪表发送运行命令", command = self.cmd_cust)    # self.cmd[i]
        self.btn2.place(relx = 0.05, rely =0.04)
        # 自定义命令的选项标签
        for i in range(6):
            self.lb1 = Label(self.init_window_name, text=self.ctr_cmd_opt[i], fg='black', font=("黑体", 12))
            self.lb1.place(relx = 0.1 + 0.1 * (i + 1), rely = 0.04)

        for i in range(5):
            self.temp_text = Entry(self.init_window_name)
            self.temp_text.place(relx=0.3 + i * 0.1, rely=0.09, relwidth=0.08, relheight=0.04)  # x,y,宽，高
            self.cust_text.append(self.temp_text)

        for i in range(0, 11):
            self.temp_CheckVar = IntVar()
            self.temp_CheckBut = Checkbutton(self.init_window_name, text=self.cust_err[i], variable=self.temp_CheckVar, onvalue=1, offvalue=0)  # '命令' + str(i)
            self.temp_CheckBut.place(relx = 0.2, rely = 0.08 + i * 0.03)
            self.CheckVars.append(self.temp_CheckVar)
    # bms应答命令窗口
    def bms_wind(self):
        self.init_bms_window = Toplevel(self.init_window_name)
        self.init_bms_window.geometry('1200x800')
        self.init_bms_window.title('BMS应答仪表测试')
        global enquiry_bms_count
        count = bms_count
        for i in range(0, count):
            # 按钮
            self.temp_button = Button(self.init_bms_window, text="发送", command = lambda n=i:self.bms_single_cmd(n))    # self.cmd[i]
            self.temp_button.place(relx = self.bms_btn_relx, rely =self.bms_btn_rely * (i + 1))
            # 复选框
            self.temp_CheckVar= IntVar()
            self.temp_CheckBut = Checkbutton(self.init_bms_window, text=bms_to_gauges_response_key[i], variable=self.temp_CheckVar, onvalue=1, offvalue=0)     #'命令' + str(i)
            self.temp_CheckBut.place(relx = self.bms_check_relx, rely =self.bms_check_rely * (i + 1))
            self.bms_checkVar.append(self.temp_CheckVar)
            # 输入框
            self.temp_text = Entry(self.init_bms_window)
            self.temp_text.place(relx = self.bms_text_relx, rely =self.bms_text_rely * (i + 1), relwidth=0.55, relheight=0.03)  # x,y,宽，高

            crc_temp = CRC_16_XMODEM.crc16_xmodem(bms_to_gauges_response_val[i])
            if crc_temp != "0":
                bms_to_gauges_response_val[i] = bms_to_gauges_response_val[i] + " " + crc_temp[0:2] + " " + crc_temp[2:]
            print("crc_test", crc_temp)

            self.temp_text.insert(0, bms_to_gauges_response_val[i])
            self.bms_text.append(self.temp_text)
            print(self.bms_checkVar[i])

            self.btn1 = Button(self.init_bms_window, text="循环发送", command=self.thread_cycle_cmd_bms)  # self.cmd[i]
            self.btn1.place(relx=0, rely=0)

            self.bms_lb = Label(self.init_bms_window, text="循环次数", fg='black', font=("黑体", 10))
            self.bms_lb.place(relx=0.1, rely=0)

            self.bms_numb_text = Entry(self.init_bms_window)
            self.bms_numb_text.place(relx=0.2, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高

            self.ctr_lb = Label(self.init_bms_window, text="间隔时间", fg='black', font=("黑体", 10))
            self.ctr_lb.place(relx=0.3, rely=0)

            self.bms_time_text = Entry(self.init_bms_window)
            self.bms_time_text.place(relx=0.4, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高
    # 控制器应答命令窗口
    def control_wind(self):
        self.init_ctr_window = Toplevel(self.init_window_name)
        self.init_ctr_window.geometry('700x800')
        self.init_ctr_window.title('控制器应答仪表测试')

        global control_count
        count = control_count
        for i in range(0, count):
            self.temp_button = Button(self.init_ctr_window, text="发送", command=lambda n=i: self.ctr_single_cmd(n))  # self.cmd[i]
            self.temp_button.place(relx=self.ctr_btn_relx, rely=self.ctr_btn_rely * (i + 1))

            self.temp_CheckVar = IntVar()
            self.temp_CheckBut = Checkbutton(self.init_ctr_window, text=control_to_gauges_response_key[i], variable=self.temp_CheckVar, onvalue=1, offvalue=0)  # '命令' + str(i)
            self.temp_CheckBut.place(relx=self.ctr_check_relx, rely=self.ctr_check_rely * (i + 1))
            self.ctr_checkVar.append(self.temp_CheckVar)

            self.temp_text = Entry(self.init_ctr_window)
            self.temp_text.place(relx=self.ctr_text_relx, rely=self.ctr_text_rely * (i + 1), relwidth=0.5, relheight=0.03)  # x,y,宽，高
            self.ctr_text.append(self.temp_text)

            crc_temp = CRC_16_XMODEM.crc16_xmodem(control_to_gauges_response_val[i])
            if crc_temp != "0":
                control_to_gauges_response_val[i] = control_to_gauges_response_val[i] + " " + crc_temp[0:2] + " " + crc_temp[2:]
            print("crc_test", crc_temp)
            self.temp_text.insert(0, control_to_gauges_response_val[i])
            print(self.ctr_checkVar[i])

        self.btn2 = Button(self.init_ctr_window, text="循环发送", command = self.thread_cycle_cmd_ctr)    # self.cmd[i]
        self.btn2.place(relx = 0, rely = 0)

        self.ctr_lb = Label(self.init_ctr_window, text="循环次数", fg='black', font=("黑体", 10))
        self.ctr_lb.place(relx=0.1, rely=0)

        self.ctr_numb_text = Entry(self.init_ctr_window)
        self.ctr_numb_text.place(relx=0.2, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高

        self.ctr_lb = Label(self.init_ctr_window, text="间隔时间", fg='black', font=("黑体", 10))
        self.ctr_lb.place(relx=0.3, rely=0)

        self.ctr_time_text = Entry(self.init_ctr_window)
        self.ctr_time_text.place(relx=0.4, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高

    def bms_utc_response_wind(self):
        self.init_other_bms_window = Toplevel(self.init_window_name)
        self.init_other_bms_window.geometry('700x800')
        self.init_other_bms_window.title('other_bms应答仪表')

        global other_bms_count
        count = other_bms_count
        for i in range(0, count):
            # 按钮
            self.temp_button = Button(self.init_other_bms_window, text="发送",
                                      command=lambda n=i: self.bms_single_cmd(n))  # self.cmd[i]
            self.temp_button.place(relx=self.other_bms_btn_relx, rely=self.other_bms_btn_rely * (i + 1))
            # 复选框
            self.temp_CheckVar = IntVar()
            self.temp_CheckBut = Checkbutton(self.init_other_bms_window, text=other_bms_to_gauges_response_key[i],
                                             variable=self.temp_CheckVar, onvalue=1, offvalue=0)  # '命令' + str(i)
            self.temp_CheckBut.place(relx=self.other_bms_check_relx, rely=self.other_bms_check_rely * (i + 1))
            self.other_bms_checkVar.append(self.temp_CheckVar)
            # 输入框
            self.temp_text = Entry(self.init_other_bms_window)
            self.temp_text.place(relx=self.other_bms_text_relx, rely=self.other_bms_text_rely * (i + 1), relwidth=0.55,
                                 relheight=0.03)  # x,y,宽，高

            crc_temp = CRC_16_XMODEM.crc16_xmodem(other_bms_to_gauges_response_val[i])
            if crc_temp != "0":
                other_bms_to_gauges_response_val[i] = other_bms_to_gauges_response_val[i] + " " + crc_temp[0:2] + " " + crc_temp[
                                                                                                              2:]
            print("crc_test", crc_temp)

            self.temp_text.insert(0, other_bms_to_gauges_response_val[i])
            self.other_bms_text.append(self.temp_text)
            print(self.other_bms_checkVar[i])

            self.btn1 = Button(self.init_other_bms_window, text="循环发送",
                               command=self.thread_cycle_cmd_bms)  # self.cmd[i]
            self.btn1.place(relx=0, rely=0)

            self.other_bms_lb = Label(self.init_other_bms_window, text="循环次数", fg='black', font=("黑体", 10))
            self.other_bms_lb.place(relx=0.1, rely=0)

            self.other_bms_numb_text = Entry(self.init_other_bms_window)
            self.other_bms_numb_text.place(relx=0.2, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高

            self.ctr_lb = Label(self.init_other_bms_window, text="间隔时间", fg='black', font=("黑体", 10))
            self.ctr_lb.place(relx=0.3, rely=0)

            self.other_bms_time_text = Entry(self.init_other_bms_window)
            self.other_bms_time_text.place(relx=0.4, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高

    def enquiry_bms_wind(self):
        self.init_enquiry_bms_window = Toplevel(self.init_window_name)
        self.init_enquiry_bms_window.geometry('700x800')
        self.init_enquiry_bms_window.title('查询_bms信息')

        global enquiry_bms_count
        count = enquiry_bms_count
        for i in range(0, count):
            # 按钮
            self.temp_button = Button(self.init_enquiry_bms_window, text="发送",
                                      command=lambda n=i: self.bms_single_cmd(n))  # self.cmd[i]
            self.temp_button.place(relx=self.enquiry_bms_btn_relx, rely=self.enquiry_bms_btn_rely * (i + 1))
            # 复选框
            self.temp_CheckVar = IntVar()
            self.temp_CheckBut = Checkbutton(self.init_enquiry_bms_window, text=enquiry_bms_key[i],
                                             variable=self.temp_CheckVar, onvalue=1, offvalue=0)  # '命令' + str(i)
            self.temp_CheckBut.place(relx=self.enquiry_bms_check_relx, rely=self.enquiry_bms_check_rely * (i + 1))
            self.enquiry_bms_checkVar.append(self.temp_CheckVar)
            # 输入框
            self.temp_text = Entry(self.init_enquiry_bms_window)
            self.temp_text.place(relx=self.enquiry_bms_text_relx, rely=self.enquiry_bms_text_rely * (i + 1),
                                 relwidth=0.55,
                                 relheight=0.03)  # x,y,宽，高

            crc_temp = CRC_16_XMODEM.crc16_xmodem(enquiry_bms_val[i])
            if crc_temp != "0":
                enquiry_bms_val[i] = enquiry_bms_val[i] + " " + crc_temp[0:2] + " " + crc_temp[2:]
            print("crc_test", crc_temp)

            self.temp_text.insert(0, enquiry_bms_val[i])
            self.enquiry_bms_text.append(self.temp_text)
            print(self.enquiry_bms_checkVar[i])

            self.btn1 = Button(self.init_enquiry_bms_window, text="循环发送",
                               command=self.thread_cycle_cmd_bms)  # self.cmd[i]
            self.btn1.place(relx=0, rely=0)

            self.enquiry_bms_lb = Label(self.init_enquiry_bms_window, text="循环次数", fg='black', font=("黑体", 10))
            self.enquiry_bms_lb.place(relx=0.1, rely=0)

            self.enquiry_bms_numb_text = Entry(self.init_enquiry_bms_window)
            self.enquiry_bms_numb_text.place(relx=0.2, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高

            self.ctr_lb = Label(self.init_enquiry_bms_window, text="间隔时间", fg='black', font=("黑体", 10))
            self.ctr_lb.place(relx=0.3, rely=0)

            self.enquiry_bms_time_text = Entry(self.init_enquiry_bms_window)
            self.enquiry_bms_time_text.place(relx=0.4, rely=0, relwidth=0.1, relheight=0.03)  # x,y,宽，高



    def thread_cycle_cmd_ctr(self):
        thread1 = threading.Thread(target = self.cycle_cmd_ctr, name="hi")
        thread1.start()

    def thread_cycle_cmd_bms(self):
        thread2 = threading.Thread(target = self.cycle_cmd_bms)
        thread2.start()

    # 选择命令循环发送
    def cycle_cmd_ctr(self):
        numb = self.ctr_numb_text.get()
        times = self.ctr_time_text.get()
        for j in range(int(numb)):
            for i in range(0,len(self.ctr_checkVar)):
                if self.ctr_checkVar[i].get() == 1:
                    print(f"您还没选择任何爱好项目{i}")
                    self.ctr_single_cmd(i)
                    time.sleep(0.001 * int(times)) #sleep是秒
    # 选择命令循环发送
    def cycle_cmd_bms(self):
        numb = self.ctr_numb_text.get()
        times = self.ctr_time_text.get()
        for j in range(int(numb)):
            for i in range(0,len(self.bms_checkVar)):
                if self.bms_checkVar[i].get() == 1:
                    print(f"您还没选择任何爱好项目{i}")
                    self.bms_single_cmd(i)
                    time.sleep(0.001 * int(times))  # sleep是秒
    # 读取复选框，发送命令
    def ctr_single_cmd(self, n):
        self.a = self.ctr_text[n].get()
        print(self.a)
        port_test(self.a)
    # 读取复选框，发送命令
    def bms_single_cmd(self, n):
        self.a = self.bms_text[n].get()
        print(self.a)
        port_test(self.a)

    # 自定义命令
    def cmd_cust(self):
        list_cust = "5A21200C0000000000000000000000005E1E"
        error = 0
        for i in range(0, 11):
            if self.CheckVars[i].get() == 1:
                error += math.pow(2, 15-i)
        err = str(hex(int(error)))
        a = err[2:]
        cmd_23 = a.rjust(4, "0")
        print("cmd_23", cmd_23)

        speed = str(hex(int(self.cust_text[0].get())))
        a = speed[2:]
        b = a.rjust(4, "0")
        cmd_45 = b[2:]+b[0:2]
        print("cmd_45", cmd_45)

        power = str(hex(int(self.cust_text[1].get())))
        a = power[2:]
        b = a.rjust(4, "0")
        cmd_67 = b[2:]+b[0:2]
        print("cmd_67", cmd_67)

        voltage = str(hex(int(self.cust_text[2].get())))
        a = voltage[2:]
        b = a.rjust(4, "0")
        cmd_89 = b[2:]+b[0:2]
        print("cmd_89", cmd_89)

        current = str(hex(int(self.cust_text[3].get())))
        a = current[2:]
        b = a.rjust(4, "0")
        cmd_AB = b[2:]+b[0:2]
        print("cmd_AB", cmd_AB)

        temp = int(self.cust_text[4].get()) + 50        #协议上要偏移50，以保证转成无符号数
        temperature = str(hex(temp))
        a = temperature[2:]
        b = a.rjust(2, "0")
        cmd_C = b
        print("cmd_C", cmd_C)

        list_cust1 = "5A21200C" + cmd_23 + cmd_45 + cmd_67 + cmd_89 +cmd_AB + cmd_C
        crc_sum = CRC_16_XMODEM.crc16_xmodem(list_cust1)
        # print(list_cust1)
        # print("crc_sum", crc_sum)
        list_cust2 = list_cust1 + crc_sum

        port_test(list_cust2)
        pass
def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    port = test_tool(init_window)
    # 设置根窗口默认属性
    port.set_init_window()
    main_menu = Menu(init_window)
    menu_file = Menu(main_menu)
    main_menu.add_cascade(label='菜单', menu=menu_file)   # 增加一个菜单栏
    main_menu.add_cascade(label='bms应答仪表测试', command=port.bms_wind)     #菜单栏直接加按钮
    main_menu.add_cascade(label='控制器应答仪表测试', command=port.control_wind)
    main_menu.add_cascade(label='other_bms应答', command=port.bms_utc_response_wind)
    main_menu.add_cascade(label='查询_bms', command=port.enquiry_bms_wind)
    # menu_file.add_command(label='bms应答仪表测试', command=port.new_wind)   # 在菜单中假按钮
    # menu_file.add_command(label='控制器应答仪表测试', command=port.control_wind)
    # menu_file.add_separator()
    # menu_file.add_command(label='退出', command=init_window.destroy)
    init_window.config(menu=main_menu)

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__ == '__main__':
    # in_f_txt()
    read_control_json(control_cmd_file)
    read_bms_json(bms_cmd_file)
    read_other_bms_json(other_bms_cmd_file)
    enquiry_bms_json(enquiry_bms_cmd_file)
    gui_start()
    # port_test('5A 21 20 0C 00 00 00 00 00 00 00 00 00 00 00 00 5E 1E')
