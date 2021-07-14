# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

import sensor, image, time, math
#引入感光元件的模块，图像，时间，数字

threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(41, 85, 24, 73, -22, 36)] # 识别色块的眼色阈值



# 设置摄像头
sensor.reset()#初始化感光元件
sensor.set_pixformat(sensor.RGB565)#设置为彩色
sensor.set_framesize(sensor.QVGA)#设置图像的大小
sensor.skip_frames(time = 2000)#跳过n张照片，在更改设置后，跳过一些帧，等待感光元件变稳定。
sensor.set_auto_gain(False) # 在使用颜色追踪时，需要关闭自动增益。
sensor.set_auto_whitebal(False) # 在使用颜色追踪时，需要关闭自动白平衡。
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

# 一直拍照
while(True):
    clock.tick()
    img = sensor.snapshot()#拍摄一张照片，img为一个image对象
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True):
    #find_blobs 找到色块
    # pixels_threshold 像素个数阈值，如果色块像素数量小于这个值，会被过滤掉，
    #area_threshold 面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
    #merge=True，那么就会有多个blob被合并到一个blob

        # These values are stable all the time.
        img.draw_rectangle(blob.rect()) #blob.rect() 返回这个色块的外框——矩形元组(x, y, w, h)
        img.draw_cross(blob.cx(), blob.cy()) #形心

    print(clock.fps())
