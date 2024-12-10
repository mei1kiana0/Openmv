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
                        if( 0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and -128<statistics.b_mode()<0)or (0<statistics.l_mode()<100 and -128<statistics.a_mode()<0 and 0<statistics.b_mode()<127)or(0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and 0<statistics.b_mode()<127):
                            img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))#识别到的红色圆形用红色的圆框出来
                            data = "{},{}\n".format(c.x(), c.y())  # 确保正确使用 format 方法
                            current_time = time.ticks_ms()
                            if time.ticks_diff(current_time, last_send_time) >= 200:  # 时间间隔 >= 200m 秒
                                print(data)
                                uart.write(data)
                                last_send_time = current_time  # 更新上次发送时间

                        else:
                            img.draw_rectangle(area, color = (255, 255, 255))


                        if abs(c.x() -160) < 10 and abs(c.y() - 120) < 10:
                            exit_loop = True  # 标志变量置为 True
                            break  # 跳出 for 循环
                if exit_loop:  # 检查标志变量
                    print(5)
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
                        if 0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and 0<statistics.b_mode()<127 and flag_R == 0:
                            img.draw_circle(c.x(),c.y(),c.r(),color = (255,0,0))
                            flag_R = 1
                            uart.write("1,0\n")
                            flag+=1
                            break
                        elif 0<statistics.l_mode()<100 and -128<statistics.a_mode()<0 and 0<statistics.b_mode()<127 and flag_G == 0:
                            img.draw_circle(c.x(),c.y(),c.r(),color = (0,255,0))
                            flag_G = 1
                            uart.write("2,0\n")
                            flag+=1
                            break
                        elif 0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and -128<statistics.b_mode()<0 and flag_B == 0:
                            img.draw_circle(c.x(),c.y(),c.r(),color = (0,0,255))
                            flag_B = 1
                            uart.write("3,0\n")
                            flag+=1
                            break
                if(flag==3):
                    exit_loop = True  # 标志变量置为 True
                    break  # 跳出 for 循环















