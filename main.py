# -*- coding: utf-8 -*-
import json
import time

from PIL import ImageChops

from process.ScreenCapture import ScreenCapture
from process.OCR import OCR
from process.Query import Query


def isSame(imgA, imgB):
    if imgA is None or imgB is None:
        return False
    diff = ImageChops.difference(imgA, imgB)
    if diff.getbbox():
        return False
    return True


def getOCRConfig():
    with open("./config.json", "r", encoding="utf-8") as fp:
        return json.load(fp)


if __name__ == "__main__":
    config = getOCRConfig()

    sc = ScreenCapture()
    ocr = OCR(config["APP_ID"], config["API_KEY"], config["SECRET_KEY"])
    query = Query()

    quesImg, answImg = None, None

    while True:
        tmpQuesImg, tmpAnswImg = sc.run()
        if not isSame(quesImg, tmpQuesImg):
            quesImg, answImg = tmpQuesImg, tmpAnswImg
            ques, answ = ocr.run(quesImg, answImg)
            freq, rightAnswer, hint = query.run(ques, answ)
            print("问题: {}".format(ques))
            print("正确答案: {}".format(rightAnswer))
            freqText = ''
            for index in range(len(freq)):
                freqText += (answ[index] + ' :' + str(round(100 * freq[index], 1)) + '%    ')
            print('概率: {}'.format(freqText))
            print('依据: {}'.format(hint))
            print()
            print('-----------------')
        time.sleep(0.8)
            
            
