﻿# This Python file uses the following encoding: utf-8
#开发项目：AI人工语音播报提醒
#日期：2023.12.2
#作者：kkklu
#email:2039871@qq.com

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
import time,datetime
from PySide2.QtCore import qDebug
#read_xml:
#import xml.etree.ElementTree as ET
#import pandas as pd
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os
import logging
#--------------------------------------------
...
#函数名：AI语音播报
def Artificial_voice_playback_1(messages):
    try:
        logging.debug("创建语音引擎")
        # 创建语音引擎
        engine = pyttsx3.init()

        # 设置语音速度
        engine.setProperty('rate', 150)

        volume=engine.getProperty('volume')
        qDebug(f'语音音量：{volume}')
    
        # 设置语音音量
        engine.setProperty('volume', 1)

        # 定义要转换为语音的消息
        #messages = ["现在是北京时间", "现在是纽约时间"]

        # 循环播放消息
        #    while True:
        #for message in messages:
    
        # 将消息转换为语音并播放
        engine.say(messages)
        engine.runAndWait()
    except IOError:
        logging.error(IOError)
    # 等待语音播放完毕
    time.sleep(1)
        # 等待60秒后再次循环播放消息
   #    time.sleep(60)
    return

#-------------------------------------------------
#函数名：闹钟
def set_alarm(alarm_time, alarm_sound,messages):
       while True:
           time.sleep(1)
           current_time = time.strftime("%H:%M:%S") #需加上年月日，带上年月日一起判断
           if current_time == alarm_time:
               #os.system("start " + alarm_sound)
               Artificial_voice_playback_1(messages)
               break
#函数名：闹钟
def compare_time(data):
    data_tmp=list()
    data_tmp=data
    #while True:
    #time.sleep(1)
    current_date =datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d") #time.strftime("%H:%M") #需加上年月日，带上年月日一起判断
    current_time =datetime.datetime.today().strptime(datetime.datetime.today().strftime("%H:%M:%S"),"%H:%M:%S")#time.strftime("%Y/%m/%d")
    current_week=datetime.datetime.today().weekday() #datetime.datetime.strptime(datetime.datetime.today().strftime('%w'),'%w')
    qDebug(str(current_week))

    start_date=datetime.datetime.strptime(data_tmp[0][0],"%Y-%m-%d") #time.time()
    end_date=datetime.datetime.strptime(data_tmp[0][1],"%Y-%m-%d")
    alarm_time=datetime.datetime.strptime(data_tmp[0][2],"%H:%M:%S")  #应该要带%S，不然会播报60次或者一分钟
    loop=data_tmp[0][3]

        # region debug
    #qDebug(datetime.datetime.strftime("%Y-%m-%d",current_date)) #要不要加"%Y/%m/%d"？？
        # endregion
        
    for i in range(0,len(data_tmp),1):
        start_date=datetime.datetime.strptime(data_tmp[i][0],"%Y-%m-%d") #xml文件的开始日期
        end_date=datetime.datetime.strptime(data_tmp[i][1],"%Y-%m-%d")   #xml文件的结束日期
        alarm_time=datetime.datetime.strptime(data_tmp[i][2],"%H:%M:%S")   #xml文件的闹钟时间
        loop=data_tmp[i][4]
        #qDebug(loop)
        if current_date >= start_date and current_date <= end_date:
            #qDebug("当前日期在start date 和 end date之间")
            if current_time == alarm_time: 
                if loop=='每天':#
                    qDebug("当前时间处于闹钟时间")
                    #Artificial_voice_playback_1(data[i][3].__str__())
                    return i
                elif loop=='每周六':
                    if current_week==5:
                        pass
                        return i
                elif loop=='每周日':
                    if current_week==6:
                        pass
                        return i
                elif loop=='周一至周五':
                    if current_week !=5 and current_week!=6:
                        pass
                        return i
                elif loop=='每周六日':
                    if current_week ==5 or current_week == 6:
                        pass
                        return i
                    
    return -1
               #Artificial_voice_playback_1(data[i][3].__str__())
               #break

       #if compare  return True else return false


   #if __name__ == "__main__":
   #    alarm_time = input("请输入闹钟时间，格式为 'HH:MM': ")
   #    alarm_sound = input("请输入闹钟声音文件路径（如：C:/Windows/Media/alarm.wav）: ")
   #    set_alarm(alarm_time, alarm_sound)
   # return

# if__name__ == "__main__":
#     pass
