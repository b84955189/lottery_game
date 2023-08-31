#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   gui.py    
@Contact :   lking@lking.icu
@Author :    Jason
@Date :      4/2/2022 4:33 PM
@Description  Python version-3.10
GUI界面
"""
import logging
import time
import datetime
import webbrowser
import random
import webbrowser
import pystray
from PIL import Image
from pystray import MenuItem, Menu
from pathlib import Path

import tkinter as tk
import threading
import tkinter.filedialog
from func import ExcelFunc, CommonTools

ROOT_PATH = Path(__file__).parent.parent
ASSETS_PATH = ROOT_PATH / Path("./assets")
STUDENT_DATA_EXCEL_FILE = ROOT_PATH / Path("./data/StudentData.xlsx")
DEFAULT_OUTPUT_PATH = ROOT_PATH / Path("./out")
OFFSET_Y = -70
DEFAULT_TIME = datetime.datetime.now()

# 全局变量

# # 公共组件
window = ""
my_task_thread = ""
generate_btn = ''
var_display_text = ''
generate_btn_img = ''
processing_btn_img = ''

# # 日期
year_time_entry = ""
month_time_entry = ""
day_time_entry = ""


def change_generate_button_state(sign, tips=None, box_type=1):
    """
    改变生成按钮状态
    True - 可用
    False - 不可用
    @param sign: 是否可用标志 - Boolean
    @param tips: 提示语
    @param box_type: 1 - 信息 2 - 错误  - int
    @return: None
    """
    if sign:
        generate_btn.config(image=generate_btn_img)
        generate_btn.config(state="normal")
    else:
        generate_btn.config(image=processing_btn_img)
        generate_btn.config(state="disable")
    if not CommonTools.is_empty_or_none(tips):
        match box_type:
            case 1:
                tk.messagebox.showinfo("Info", f"{tips}")
            case 2:
                tk.messagebox.showerror("Error", f"{tips}")


def change_var_display_text_label(text):
    """
    更新标签变量
    @param text 文本
    @return None
    """
    global var_display_text
    var_display_text.set(text)


def my_task():
    """
    线程任务
    @return: None
    """
    wb = None
    try:
        # after 会阻塞UI线程
        window.after(0, change_generate_button_state, False)
        # ---------------
        # 获取Excel数据
        wb = ExcelFunc.get_workbook(STUDENT_DATA_EXCEL_FILE)
        student_data_sheet = wb.active
        names = ExcelFunc.get_data_from_sheet(student_data_sheet)

        # 随机点名
        random_num = random.randint(1, len(names))
        print(random_num)
        for name, num in names.items():
            time.sleep(0.1)
            window.after(0, change_var_display_text_label(name), False)
            if random_num == num:
                window.after(0, change_generate_button_state, True, f"恭喜【{name}】同学!")
                break

        # ---------------

    except Exception as e:
        # 错误提示
        window.after(0, change_generate_button_state, True, "出现了一个错误，请重试!", 2)
        # dev
        logging.exception(e)
        pass
    finally:
        # 关闭数据信息工作簿
        if wb is not None:
            ExcelFunc.close_workbook(wb)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def btn_clicked():
    try:
        global my_task_thread
        # Check thread whether alive
        if isinstance(my_task_thread, threading.Thread) and my_task_thread.is_alive():
            tk.messagebox.showerror(
                "操作异常!", "请稍等任务处理完毕!")
        else:
            # creat a thread to operate long-time task.
            my_task_thread = threading.Thread(target=my_task,
                                              args=(),
                                              name="my_task_thread")
            # start thread
            my_task_thread.start()
            # wait this thread util it completes its task.
            # excel_task_thread.join()

    except Exception as e:
        print(e)
        tk.messagebox.showerror(
            "文件格式错误!", "请查看文件信息是否有误！")
    finally:
        pass


def show_main_UI():
    """
    显示主界面
    @return: None
    """
    # 重现显示图形界面
    window.deiconify()


def on_exit_by_minimize():
    """
    退出界面，最小化至托盘
    @return: None
    """
    # 关闭界面
    window.withdraw()


def on_exit(icon: pystray.Icon):
    """
    完全退出程序
    @return:
    """
    icon.stop()
    window.destroy()


# UI thread is single thread !!! If there have a long-time task , everything of
# operation in UI thread will be blocked for a while.
def start():
    global window
    window = tk.Tk()
    logo = tk.PhotoImage(file=ASSETS_PATH / "icon.gif")
    window.call('wm', 'iconphoto', window._w, logo)
    window.title("菲姐点名器 v1.0")

    window.geometry("862x519")
    window.configure(bg="#3A7FF6")

    # 托盘右键菜单 , 并设置默认左键点击事件为右键菜单的显示主界面事件
    tray_menu = (MenuItem('显示主界面', show_main_UI, default=True), MenuItem('帮助', lambda: webbrowser.open('https://b84955189.notion.site/11f42730aa004efe981dfd271389e966?pvs=4')), Menu.SEPARATOR, MenuItem('退出', on_exit))
    # 创建最小化托盘图标 图标名，图片资源，应用名称，[菜单]
    tray_icon = pystray.Icon('tray_icon', Image.open(ASSETS_PATH / "icon.png"), "菲姐点名器", tray_menu)

    # 重新定义点击关闭按钮的处理,重新绑定为最小化至托盘事件
    window.protocol('WM_DELETE_WINDOW', on_exit_by_minimize)
    # 开启托盘线程，因为默认开启托盘与Tkinter UI界面的线程是相互阻塞的，所以单独开个线程便可UI界面与托盘同时存在
    threading.Thread(target=tray_icon.run, daemon=True).start()

    canvas = tk.Canvas(
        window, bg="#3A7FF6", height=519, width=862,
        bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
    canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

    text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
    # 时间输入控件
    # # 年
    global year_time_entry
    year_time_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    year_time_entry.place(x=100 - 20, y=137 + 25 + 150 + 15, width=40.0, height=35)
    # year_time_entry.focus()
    canvas.create_text(
        50 - 10, 137 + 40 + 150 + 15, text="年:", fill="#FFF",
        font=("Arial-BoldMT", int(13.0)), anchor="w")
    year_time_entry.delete(0, tk.END)
    year_time_entry.insert(0, str(DEFAULT_TIME.year))
    year_time_entry.config(state="disable")
    # # 月
    global month_time_entry
    month_time_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    month_time_entry.place(x=207 - 20, y=137 + 25 + 150 + 15, width=40.0, height=35)
    canvas.create_text(
        150 - 10, 137 + 40 + 150 + 15, text="月:", fill="#FFF",
        font=("Arial-BoldMT", int(13.0)), anchor="w")
    month_time_entry.delete(0, tk.END)
    month_time_entry.insert(0, str(DEFAULT_TIME.month))
    month_time_entry.config(state="disable")
    # # 日
    global day_time_entry
    day_time_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    day_time_entry.place(x=300 - 20, y=137 + 25 + 150 + 15, width=40.0, height=35)
    canvas.create_text(
        260 - 10, 137 + 40 + 150 + 15, text="日:", fill="#FFF",
        font=("Arial-BoldMT", int(13.0)), anchor="w")
    day_time_entry.delete(0, tk.END)
    day_time_entry.insert(0, str(DEFAULT_TIME.day))
    day_time_entry.config(state="disable")

    global var_display_text
    var_display_text = tk.StringVar()
    var_display_text.set("准备点名！")
    display_text_label = tk.Label(
        text="", bg="#FFF",
        fg="#3A7FF6", font=("Arial-BoldMT", int(30.0)), textvariable=var_display_text)
    display_text_label.place(x=570.5, y=190)

    title = tk.Label(
        text="高一·17班", bg="#3A7FF6",
        fg="white", font=("Arial-BoldMT", int(20.0)))
    title.place(x=27.0, y=120.0)

    info_text = tk.Label(
        text="有人风雨夜行，有人梦里点灯。\n"
             "哪怕前方泥泞不堪，\n"
             "也愿你风雨兼程。",
        bg="#3A7FF6", fg="white", justify="left",
        font=("Georgia", int(16.0)))

    info_text.place(x=27.0, y=200.0)

    know_more_university = tk.Label(
        text="Click here for help information.",
        bg="#3A7FF6", fg="white", cursor="hand2")
    know_more_university.place(x=27, y=400)
    know_more_university.bind('<Button-1>', lambda event: webbrowser.open_new_tab('"https://b84955189.notion.site'
                                                                                  '/11f42730aa004efe981dfd271389e966?pvs=4"'))

    # Author
    author_info = tk.Label(
        text="© LKING.ICU",
        bg="#3A7FF6", fg="white", cursor="hand2")
    author_info.place(x=27, y=425)
    author_info.bind('<Button-1>', lambda event: webbrowser.open_new_tab('https://www.lking.icu'))
    global generate_btn
    global generate_btn_img
    global processing_btn_img
    generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
    processing_btn_img = tk.PhotoImage(file=ASSETS_PATH / "processing.png")
    generate_btn = tk.Button(
        image=generate_btn_img, borderwidth=0, highlightthickness=0,
        command=btn_clicked, relief="flat")
    generate_btn.place(x=557, y=280, width=180, height=55)
    window.resizable(False, False)
    window.mainloop()
