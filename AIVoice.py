# This Python file uses the following encoding: utf-8
#开发项目：AI人工语音播报提醒
#日期：2023.12.2
#作者：kkklu

#性能描述：
#定时播报需要播报的语音，提醒值班员。例如：请报平安、请三台并机、请恢复正常播出....
#读取xml文件，starttime endtime message等，闹钟判断时间并播出语音
#两个UI，一个UI运行执行程序，执行完了显示执行日志；另一个设置UI，设置starttime endtime message 按星期还是每天循环，参照计划任务,保存是写入xml文件

#改进：
#1.每个函数需考虑异常处理，成功后return true
#2.要不要考虑线程
#3.在哪个程序里放进清理xml文件中过期的语音提醒

#----------------------------------------
import pyttsx3
import time

#read_xml:
#import xml.etree.ElementTree as ET
import pandas as pd
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os
#--------------------------------------------

#函数名：AI语音播报
def Artificial_voice_playback(messages):

    # 创建语音引擎
    engine = pyttsx3.init()

    # 设置语音速度
    engine.setProperty('rate', 150)

    # 设置语音音量
    engine.setProperty('volume', 0.7)

    # 定义要转换为语音的消息
    #messages = ["现在是北京时间", "现在是纽约时间"]

    # 循环播放消息
#    while True:
        for message in messages:
            # 将消息转换为语音并播放
            engine.say(message)
            engine.runAndWait()
            # 等待语音播放完毕
            time.sleep(1)
        # 等待60秒后再次循环播放消息
   #    time.sleep(60)
    return
#-------------------------------------------------
#函数名：闹钟
def set_alarm(alarm_time, alarm_sound):
       while True:
           time.sleep(1)
           current_time = time.strftime("%H:%M") #需加上年月日，带上年月日一起判断
           if current_time == alarm_time:
               #os.system("start " + alarm_sound)
               Artificial_voice_playback(messages)
               break

   #if __name__ == "__main__":
   #    alarm_time = input("请输入闹钟时间，格式为 'HH:MM': ")
   #    alarm_sound = input("请输入闹钟声音文件路径（如：C:/Windows/Media/alarm.wav）: ")
   #    set_alarm(alarm_time, alarm_sound)
    return
#----------------------------------------------------
#函数名：读取xml文件
#参考网址：https://zhuanlan.zhihu.com/p/582830847
def read_xml():
    # 读取xml字符串
    try:
        xml_data=open("config.xml").read()
    except IOError:
        print("Error:找不到文件打开！")
    else：
        root = ET.fromstring(xml_data)

        # 打开XML文件并解析 第二种打开xml方式
        #tree = ET.parse('config.xml')

        #获取根元素
        root=tree.getroot()
        data = list()
        for child in root:
            data1 = list()
            for son in child:
                data1.append(son.text)
            data.append(data1)
    ​
        df = pd.DataFrame(data, columns=['start_date', 'end_date', 'time','message'])
        print(df)
    return
#-------------------------------------------------------
# if__name__ == "__main__":
#     pass
