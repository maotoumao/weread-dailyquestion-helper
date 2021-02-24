# -*- coding: utf-8 -*-
import time
from functools import reduce
from urllib import request, parse
from bs4 import BeautifulSoup


class Query:

    def _getKnowledge(self, question):
        url = 'https://www.baidu.com/s?wd={}'.format(parse.quote(question))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'host': 'www.baidu.com'
        }
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        content = response.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        knowledge = soup.get_text()
        if('网络不给力，请稍后重试' in knowledge):
            time.sleep(0.5)
            print('怕不是被封了…')
            return None
        return knowledge

    def _query(self, knowledge, answers):
        freq = [knowledge.count(item) + 1 for item in answers]
        rightAnswer = None
        hint = None

        if freq.count(1) == len(answers):
            freqDict = {}
            for item in answers:
                for char in item:
                    if char not in freqDict:
                        freqDict[char] = knowledge.count(item)
            for index in range(len(answers)):
                for char in answers[index]:
                    freq[index] += freqDict[char]
            rightAnswer = answers[freq.index(max(freq))]
        else:
            rightAnswer = answers[freq.index(max(freq))]
            threshold = 50 # 前后50字符
            hintIndex = max(knowledge.index(rightAnswer), threshold)
            hint = ''.join(knowledge[hintIndex - threshold : hintIndex + threshold].split())
        
        sum = reduce(lambda a,b : a+b, freq)
        return [f / sum for f in freq], rightAnswer, hint


    def run(self, question, answers):
        knowledge = None
        while(knowledge is None):
            knowledge = self._getKnowledge(question)
        try:
            freq, rightAnswer, hint = self._query(knowledge, answers)
        except Exception as e:
            print('出现异常', e)
            freq, rightAnswer, hint = [], None, None
        return freq, rightAnswer, hint

        
