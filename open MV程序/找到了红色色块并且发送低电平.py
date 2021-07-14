import sensor, image, time
from pyb import Pin
#设置颜色的阈值
thresholds=[(100, 0, 73, 40, 37, 127),(14, 52, 8, 126, 14, 127)]  #前面地上的果蔬的色块  后面树上的果蔬的色块

#设置感光元件的参数
sensor.reset()#初始化感光元件
sensor.set_pixformat(sensor.RGB565)#函数是设置像素模式，sensor.RGB565代表彩色，sensor.GRAYSCALE代表灰度
sensor.set_framesize(sensor.QVGA)#设置图像的大小  参数可以调整 这个参数代表着320*240
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)#颜色追踪时需要关闭自动增益
sensor.set_auto_whitebal(False)#颜色追踪时需要关闭白平衡

clock = time.clock()
p_out=Pin('P0',Pin.OUT_PP) #地上果蔬对应的识别引脚
p_out1=Pin('P1',Pin.OUT_PP) #树上果蔬对应的识别引脚
p_out.high()
p_out1.high()

while(True):
    clock.tick()
    img = sensor.snapshot()#拍摄一张照片，img为一个image对象
#image.find_blobs(thresholds, roi=Auto, x_stride=2, y_stride=1, invert=False, area_threshold=10, pixels_threshold=10, merge=False, margin=0, threshold_cb=None, merge_cb=None)
#find_blods()有很多参数 第一个参数是设置颜色阈值 同时第一个参数必须是一个列表
#第二个参数是感兴趣区就是在画面的哪个位置进行识别不设置roi默认在整个图像进行识别
#设置查找颜色的x方向上的最小宽度的像素
#设置反转阈值就是反向查找  默认不反向查找
#area_threshold设置色块的面积大小 小于这个面积被过滤掉 包含背景颜色面积
#pixels_threshold设置只包含色块的被框起来的面积大小
#margin设置是否把框框合并 多个颜色的框框是否合并
   #该函数的返回值是一个列表
    blobs=img.find_blobs([thresholds[0]],pixels_threshold=200, area_threshold=200, merge=True)
    blobs1=img.find_blobs([thresholds[1]],pixels_threshold=200, area_threshold=200, merge=True)
    if len(blobs)!=0:
        print('helloworld')
        p_out.low()
    else:
        p_out.high()
    if len(blobs1)!=0:
        print('helloworld1')
        p_out1.low()
    else:
        p_out1.high()
    for blob in blobs:
        img.draw_rectangle(blob.rect())#在图像当中画一个矩形框框
        img.draw_cross(blob.cx(),blob.cy())#在图像中画一个十字
    for blob in blobs1:
        img.draw_rectangle(blob.rect())#在图像当中画一个矩形框框
        img.draw_cross(blob.cx(),blob.cy())#在图像中画一个十字
    print(clock.fps())
