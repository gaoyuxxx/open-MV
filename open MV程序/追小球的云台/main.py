import sensor, image, time

from pid import PID #从pid里导入PID
from pyb import Servo #从pyd库里导入Servo

pan_servo=Servo(1) #定义底盘舵机
tilt_servo=Servo(2) #翘起舵机

#舵机校准
pan_servo.calibration(500,2500,500)
tilt_servo.calibration(500,2500,500)

red_threshold  = (13, 49, 18, 61, 6, 47) #红色颜色阈值

pan_pid = PID(p=0.07, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID   pid参数一般调整P即可
tilt_pid = PID(p=0.05, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
#pan_pid = PID(p=0.1, i=0, imax=90)#在线调试使用这个PID
#tilt_pid = PID(p=0.1, i=0, imax=90)#在线调试使用这个PID

#常规的sensor的设置
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.彩图
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.分辨率大小
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.颜色识别需要关掉白平衡
clock = time.clock() # Tracks FPS.

#寻找最大色块的函数，用以追踪
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob


while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.截取一张图片

    blobs = img.find_blobs([red_threshold]) #调用颜色识别的函数（识别红色阈值）
    if blobs: #如果找到红色色块
        max_blob = find_max(blobs)  #找到最大色块
        pan_error = max_blob.cx()-img.width()/2   #底盘舵机计算x方向与中心误差
        tilt_error = max_blob.cy()-img.height()/2  #翘起舵机计算y方向与中心误差

        print("pan_error: ", pan_error)

        #在寻找最大色块周围用矩形框框出来
        img.draw_rectangle(max_blob.rect()) # rect矩形
        img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy形心

        #pid参数
        pan_output=pan_pid.get_pid(pan_error,1)/2
        tilt_output=tilt_pid.get_pid(tilt_error,1)
        print("pan_output",pan_output)
        #控制舵机跟踪中心坐标
        pan_servo.angle(pan_servo.angle()+pan_output) #底盘舵机角度
        tilt_servo.angle(tilt_servo.angle()-tilt_output) #翘起舵机角度
