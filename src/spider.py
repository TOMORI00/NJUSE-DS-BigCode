#!/usr/bin/python
# coding:utf-8

import pandas as pd
import json
import bs4
import requests
import re

USER_AGENT = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'


class Spider(object):
    def __init__(self,path):
        self.base_url = 'https://leetcode-cn.com/'
        self.session = requests.Session()
        self.df = pd.DataFrame(columns=['questionId', 'questionTitle','content','difficulty','totalAccepted','totalSubmission','acRate','categoryTitle','likes','translatedTitle','translatedContent'])
        self.total_num = 0
        self.path = path


    def get_problems(self):
        url = self.base_url + 'api/problems/algorithms'
        html = requests.get(url).content
        soup = bs4.BeautifulSoup(html, 'html.parser')
        problem_str = soup.prettify()
        problem_dic = json.loads(problem_str)
        problem_list = problem_dic['stat_status_pairs']

        max_cnt = 1000000
        for problem in reversed(problem_list):
            if problem['paid_only']:
                continue
            elif self.total_num >= max_cnt:
                break
            else:
                self.total_num += 1
                self.get_problem_by_slug(problem['stat']['question__title_slug'])

    def get_problem_by_slug(self, slug):
        url = self.base_url + 'graphql'
        params = {
            'operationName': "getQuestionDetail",
            'variables': {'titleSlug': slug},
            'query': '''query getQuestionDetail($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionTitle
                    content
                    difficulty
                    stats
                    categoryTitle
                    likes
                    translatedTitle
                    translatedContent
                }
            }'''
        }
        json_data = json.dumps(params).encode('utf8')
        headers = {
            'User-Agent': USER_AGENT,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com/problems/' + slug
        }
        resp = self.session.post(url, data=json_data, headers=headers, timeout=10)
        content = resp.json()
        self.save(content['data']['question'])

    def run(self):
        self.get_problems()
        self.df.to_csv(self.path)


    def save(self, question):
        if int(question['questionId']) > 10000:
            return
        print(self.total_num,'finish')
        self.df.loc[self.total_num] = {
            'questionId':question['questionId'],
            'questionTitle':question['questionTitle'],
            'content':self.filter_tags(question['content']),
            'difficulty':question['difficulty'],
            'totalAccepted':eval(question['stats'])['totalAcceptedRaw'],
            'totalSubmission':eval(question['stats'])['totalSubmissionRaw'],
            'acRate':eval(question['stats'])['acRate'],
            'categoryTitle':question['categoryTitle'],
            'likes':question['likes'],
            'translatedTitle':question['translatedTitle'],
            'translatedContent':self.filter_tags(question['translatedContent'])
        }
        return

    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', '39': "'"}

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def filter_tags(self,htmlstr):
        #先过滤CDATA
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        re_br=re.compile('<br\s*?/?>')#处理换行
        re_h=re.compile('</?\w+[^>]*>')#HTML标签
        re_comment=re.compile('<!--[^>]*-->')#HTML注释
        s=re_cdata.sub('',htmlstr)#去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        s=re_br.sub('\n',s)#将br转换为换行
        s=re_h.sub('',s) #去掉HTML 标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=self.replaceCharEntity(s)#替换实体
        return s

if __name__ == '__main__':
    spider = Spider("../data/question.csv")
    spider.run()