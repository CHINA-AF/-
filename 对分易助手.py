#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作者：龙.吟


from re import findall
from time import sleep, process_time
import pyautogui
from pyperclip import copy


def find_word():
    """网页数据中使用正则表达式找出单词"""
    with open(r'网页数据.txt', 'r', encoding='utf-8') as f:
        file = f.readlines()
    txt = findall(r'<input name="hidS" id="hidS" type="hidden" value=.*?}]', str(file))
    i_list = findall(r'HistPaperID.*?Sort', str(txt))  # 找出每一个条
    word_list = []
    for i in i_list:
        a_str = ''
        b_list = findall(r'(?<=\">).*?(?=</span>)', i)  # 找出每一个单词
        for j in b_list:  # 拼接单词
            if j != '&amp;nbsp;':  # 删除空格
                a_str += j
        word_list.append(a_str.lstrip().rstrip())
    return word_list


def read_data():
    """读取数据文件"""
    with open('单词数据.txt', 'r', encoding='utf-8') as h:
        data_list = h.read().splitlines()  # 将每一行读取为元素组成列表
    data_dic = {}
    for i in range(0, len(data_list), 2):  # 将数据保存到字典中
        en = data_list[i + 1].replace(" ", "")
        cn = data_list[i].lstrip().rstrip()
        data_dic.update({en: cn})
    return data_dic


def write_down(s):
    copy(s)
    sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    sleep(0.5)


def msg_box(word, data):  # 运行并返回运行结果
    if len(word) == 0:
        return '未找到网页数据，请检查是否正常复制\n推荐使用Edge浏览器'
    try:
        i = 0
        c = []
        rid2 = pyautogui.locateCenterOnScreen('xiayiti.png')
        if rid2 is not None:  # 判断能否找到定位图
            for w in word:
                i += 1
                if w in data.keys():
                    rid1 = pyautogui.locateCenterOnScreen('shurukuang.png')
                    if rid1 is None:
                        rid1 = pyautogui.locateCenterOnScreen('shurukuang1.png')
                    pyautogui.click(rid1)
                    pyautogui.doubleClick()
                    pyautogui.click()
                    tran = data[w]
                    sleep(0.5)
                    write_down(tran)
                    pyautogui.click(rid2)
                    sleep(0.5)
                else:
                    c.append(i)
                    pyautogui.click(rid2)
            if len(c) != 0:
                return '    输入完成!\n以下题号未找到答案，请自行查找后添加到单词数据\n  ' + str(c) + '  \n    感谢使用'
            return '输入完成，如遇问题请反馈，感谢使用'
        else:
            return '请不要遮挡网页！！'
    except FileNotFoundError:  # 文件未找到
        return '文件丢失，请检查文件完整性'
    except pyautogui.FailSafeException:  # 手动中止
        return '已手动中断程序!'
    except Exception as e:  # 未知错误
        return '未知错误，请截图反馈！\n\n' + str(e)


if __name__ == '__main__':
    t1 = process_time()
    pyautogui.FAILSAFE = True  # 手动中断开启
    flg = pyautogui.confirm(title='对分易助手1.1@by龙.吟', text='点击确认开始，请确保页面没被遮挡,输入法为英文\n  如遇程序失控移动鼠标到左上角！')
    Word = find_word()
    Data = read_data()
    if flg == 'OK':  # 点击确定后执行
        msg = msg_box(Word, Data)
        t2 = process_time()
        pyautogui.alert(title='对分易助手1.1@by龙.吟', text=msg + '!\n\n运行时间：%f秒' % (t2 - t1))
