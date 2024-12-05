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


uart = UART(1, 115200)
while(True):  # 外部循环
    if uart.any():
        data = uart.read(1)
        print(data)
        if data == b'Q':
            exit_loop = False  # 标志变量，初始为 False

            while(True):  # 内部循环
                img = sensor.snapshot()
                circles = img.find_circles(threshold=2000, x_margin=20, y_margin=20,
                                           r_margin=10, r_min=34, r_max=44, r_step=2)
                if circles:
                    for c in circles:
                        img.draw_circle(c.x(), c.y(), c.r(), color=(255, 0, 0))
                        data = "{},{}\n".format(c.x(), c.y())  # 确保正确使用 format 方法
                        print(data)
                        uart.write(data)
                        if abs(c.x() -160) < 15 and abs(c.y() - 120) < 15:
                            exit_loop = True  # 标志变量置为 True
                            break  # 跳出 for 循环
                if exit_loop:  # 检查标志变量
                    print(5)
                    break  # 跳出内层 while 循环

