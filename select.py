import sensor, image, time
from machine import UART


# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)    # 设置为彩色模式
sensor.set_framesize(sensor.QVGA)      # 设置分辨率
sensor.skip_frames(time=2000)          # 等待摄像头稳定
sensor.set_auto_gain(False)            # 关闭自动增益
sensor.set_auto_whitebal(False)        # 关闭自动白平衡（避免颜色漂移）
clock = time.clock()
last_send_time = time.ticks_ms()  # 初始化上次发送时间为当前时间

flag_R = 0
flag_G = 0
flag_B = 0

uart = UART(1, 115200)
while(True):  # 外部循环
    if uart.any():
        data = uart.read(1)
        print(data)


        if data == b'S':
            exit_loop = False  # 标志变量，初始为 False
            flag1=0
            while(True):  # 内部循环
                img = sensor.snapshot()
                #circles = img.find_circles(threshold=2000, x_margin=20, y_margin=20,
                                           #r_margin=10, r_min=34, r_max=44, r_step=2)
                circles = img.find_circles(threshold = 2000, x_margin = 20, y_margin = 20, r_margin = 10,
                r_min = 39, r_max = 43, r_step = 5)

                if circles:
                    for c in circles:
                        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
                        #area为识别到的圆的区域，即圆的外接矩形框
                        statistics = img.get_statistics(roi=area)#像素颜色统计
                        #img.draw_circle(c.x(), c.y(), c.r(), color=(255, 0, 0))
                        if  30<statistics.l_mode()<100 and 15<statistics.a_mode()<127 and 15<statistics.b_mode()<127:#if the circle is red
                            img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
                            data = "{},{}\n".format(c.x(), c.y())  # 确保正确使用 format 方法
                            current_time = time.ticks_ms()
                            if time.ticks_diff(current_time, last_send_time) >= 400:  # 时间间隔 >= 200m 秒
                                print(data)
                                flag1+=1
                                uart.write(data)
                                last_send_time = current_time  # 更新上次发送时间
                        '''elif 34<statistics.l_mode()<100 and -64<statistics.a_mode()<-8 and -32<statistics.b_mode()<32:
                            img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
                            data = "{},{}\n".format(c.x(), c.y())  # 确保正确使用 format 方法
                            current_time = time.ticks_ms()
                            if time.ticks_diff(current_time, last_send_time) >= 200:  # 时间间隔 >= 200m 秒
                                print(data)
                                flag1+=1
                                uart.write(data)
                                last_send_time = current_time  # 更新上次发送时间'''

                        #else:
                            #img.draw_rectangle(area, color = (255, 255, 255))


                        if abs(c.x() -160) < 15 and abs(c.y() - 120) < 12:
                            print(c.x())
                            print(c.y())
                            exit_loop = True  # 标志变量置为 True
                            break  # 跳出 for 循环
                        if flag1==10:
                            exit_loop = True  # 标志变量置为 True
                            break  # 跳出 for 循环
                if exit_loop:  # 检查标志变量
                    img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
                    print(5)
                    print(data)
                    uart.write("160,120\n")
                    break  # 跳出内层 while 循环

        if data == b'Q':
            exit_loop = False  # 标志变量，初始为 False
            flag=0
            while(True):  # 内部循环
                img = sensor.snapshot()
                circles = img.find_circles(threshold = 2000, x_margin = 20, y_margin = 20, r_margin = 10,
                r_min = 39, r_max = 43, r_step = 5)
                if circles:
                    for c in circles:
                        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
                        statistics = img.get_statistics(roi=area)#像素颜色统计
                        if 30<statistics.l_mode()<100 and 15<statistics.a_mode()<127 and 15<statistics.b_mode()<127 and flag_R == 0 and c.r()>10:
                            img.draw_circle(c.x(),c.y(),c.r(),color = (255,0,0))
                            flag_R = 1
                            uart.write("1,0\n")
                            print("111")
                            flag+=1#红色
                            #time.sleep(3)

                        elif 30<statistics.l_mode()<100 and -64<statistics.a_mode()<-8 and -32<statistics.b_mode()<32 and flag_G == 0 and flag==1 and c.r()>10:
                            img.draw_circle(c.x(),c.y(),c.r(),color = (0,255,0))
                            flag_G = 1
                            uart.write("2,0\n")
                            print("222")
                            flag+=1#绿色
                            #time.sleep(3)


                        elif 0<statistics.l_mode()<100 and 0<statistics.a_mode()<40 and -80<statistics.b_mode()<-20 and flag_B == 0 and flag==2 and c.r()>10:
                            img.draw_circle(c.x(),c.y(),c.r(),color = (0,0,255))
                            flag_B = 1
                            uart.write("3,0\n")
                            print("333")
                            flag+=1
                            #time.sleep(3)


                if(flag==3):
                    exit_loop = True  # 标志变量置为 True
                    break  # 跳出 for 循环
        if data == b'R':
            exit_loop = False  # 标志变量，初始为 False
            flagR=0
            flag_R = 0;
            flag_G = 0;
            flag_B = 0;
            while(True):
                img = sensor.snapshot().lens_corr(1.8)
                circles = img.find_circles(threshold = 2000, x_margin = 20, y_margin = 20, r_margin = 10,
                r_min = 39, r_max = 43, r_step = 5)
                if circles:
                    for c in circles:
                        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
                #area为识别到的圆的区域，即圆的外接矩形框
                        statistics = img.get_statistics(roi=(c.x()-c.r(),c.y(),1,1))#像素颜色统计
                #(0,100,0,120,0,120)是红色的阈值，所以当区域内的众数（也就是最多的颜色），范围在这个阈值内，就说明是红色的圆。
                #l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。
                        if 0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and 0<statistics.b_mode()<127 and flag_R == 0:#if the circle is red
                            img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))#识别到的红色圆形用红色的圆框出来
                            flag_R = 1;
                            print("1")
                            data = "{},{}\n".format(c.x(),c.y())
                            if time.ticks_diff(current_time, last_send_time) >= 400:
                                uart.write(data)
                                flagR+=1
                                last_send_time = current_time  # 更新上次发送时间
                        if 0<statistics.l_mode()<100 and -64<statistics.a_mode()<-8 and 3<statistics.b_mode()<32 and flag_G == 0:#if the circle is green
                            img.draw_circle(c.x(), c.y(), c.r(), color = (0, 255, 0))#识别到的红色圆形用绿色的圆框出来
                            print("2")
                            flag_G = 1;
                            data = "{},{}\n".format(c.x(),c.y())
                            if time.ticks_diff(current_time, last_send_time) >= 400:
                                uart.write(data)
                                flagR+=1
                                last_send_time = current_time  # 更新上次发送时间
                        if 0<statistics.l_mode()<100 and -3<statistics.a_mode()<127 and -128<statistics.b_mode()<2 and flag_B == 0:#if the circle is blue
                            img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))#识别到的红色圆形用蓝色的圆框出来
                            flag_B = 1;
                            print("3")
                            data = "{},{}\n".format(c.x(),c.y())
                            if time.ticks_diff(current_time, last_send_time) >= 400:
                                uart.write(data)
                                flagR+=1
                                last_send_time = current_time  # 更新上次发送时间
                        if(flagR==6):
                            exit_loop = True  # 标志变量置为 True
                            break  # 跳出 for 循环
                if exit_loop:  # 检查标志变量
                    img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
                    print(5)
                    print(data)
                    uart.write("160,120\n")
                    break  # 跳出内层 while 循环








'''
  if  34<statistics.l_mode()<100 and -64<statistics.a_mode()<-8 and -32<statistics.b_mode()<32: 这个是绿色
  if  30<statistics.l_mode()<100 and 15<statistics.a_mode()<127 and 15<statistics.b_mode()<127: 这个是红色
'''





