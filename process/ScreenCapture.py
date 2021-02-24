# -*- coding: utf-8 -*-
import win32gui, win32con
from PIL import ImageGrab

class ScreenCapture:
    def __init__(self):
        self.hwnd = win32gui.FindWindow(0, "微信读书")
        if self.hwnd == 0:
            raise Exception("没有找到'微信读书'小程序")
        self.bound = win32gui.GetWindowRect(self.hwnd)
        self.rpx = self._rpx2px(self.bound[2] - self.bound[0])

    # rpx转px
    def _rpx2px(self, base):
        ratio = base / 750
        def _rpx(rpx):
            return rpx * ratio
        return _rpx

    # 截图
    def _getCapture(self):
        img = ImageGrab.grab(self.bound)
        return img
    
    # 切割
    def _splitCapture(self, img):
        quesImg = img.crop((self.rpx(85), self.rpx(460), self.rpx(670), self.rpx(590)))
        ansImg = img.crop((self.rpx(85), self.rpx(590), self.rpx(670), self.rpx(1055)))
        return quesImg, ansImg
    
    
    def run(self):
        img = self._getCapture()
        return self._splitCapture(img)
        


        

        
        

        



