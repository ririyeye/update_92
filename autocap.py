from PIL import ImageGrab
from time import sleep
import math
import operator
from functools import reduce
import pyautogui
# 配合usb总线抓包工具使用
# 检测屏幕左上角图像变化 没有变化的时候 移动到中间按f5

#检测像素图像变化
def checkimg_same(img0 , img1):
    histogram1 = img0.histogram()
    histogram2 = img1.histogram()

    # 获取 histogram 列表中的数据，
    differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))/len(histogram1))
    
    # differ的值为0，则表示图片相同，如果differ越大，则表示图片差异越大
    print('differ:',differ)
    if differ == 0:
        return True
    else:
        return False

# 屏幕中间按下f5
def auto_click():
    pyautogui.leftClick(x=1920/2,y=1080/2)
    pyautogui.keyDown('f5')

if __name__ == "__main__":
    lastimg = ImageGrab.grab(bbox=(0, 0, 200, 200))
    while 1 :
        sleep(2)
        capimg = ImageGrab.grab(bbox=(0, 0, 200, 200))
        ret = checkimg_same(lastimg, capimg)

        if ret == True:
            break

        lastimg = capimg
    
    auto_click()
    






