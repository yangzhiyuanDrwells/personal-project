# -*- codeing = utf-8 -*-
# @Author :$����Զ
# @Time :2021/2/3 16:39
# @File :finance.py
# @software: PyCharm
# 1.�ɹ���ȡ���е�html��ҳ�����Ҷ�ǰ����html�����õ������ź͹��棬����ֻ��Ҫ���ÿ����վ��getData(i)����������������getData�б�
# 2.���getData2-getData(4) getData3������Ҫ��ȡ�µ���ҳ���ܵõ�
# 3.�����޽������������ʽ��ȡcookie����get_cookie������askURLStrengthen��������װcookieģ����������� ���ϲƾ���ѧ���׶�����ó�״�ѧ
# 4.����excel����п�Ⱥͳ�����
# 5.ѧϰSelenium+PhantomJS��ȡ��̬��ҳ���Ի�ȡ���� �׶�����ó�״�ѧ ��ҳԴ��

# �����˱����excel���п�


import re
import xlwt  # ����excel����
import urllib
import datetime  # ��ȡ��ǰ��ݣ�Ҫ�Ż��߹���ֻ�ṩ�������ڣ���Ҫ�������
import pickle  # ����html�ļ�
from bs4 import BeautifulSoup  # ��ҳ��������ȡ����
from selenium import webdriver
import urllib.request, urllib.error  # ָ��url����ȡ��ҳ����

finance_url = [
    "http://www.cufe.edu.cn/",  # ����ƾ���ѧ
    "http://www.nufe.edu.cn/",  # �Ͼ��ƾ���ѧ������# http://jwc.nufe.edu.cn/��
    "http://www.jxufe.edu.cn/",  # �����ƾ���ѧ
    "https://www.sdufe.edu.cn/",  # ɽ���ƾ���ѧ
    "http://www.shufe.edu.cn/",  # �Ϻ��ƾ���ѧ------�Է���������һ�����ʻ�ը
    "https://www.zuel.edu.cn/",  # ���ϲƾ�������ѧ
    "http://www.btbu.edu.cn/",  # �������̴�ѧ
    "http://www.sxufe.edu.cn/",  # ɽ���ƾ���ѧ
    "http://www.dufe.edu.cn/",  # �����ƾ���ѧ
    "http://www.tjufe.edu.cn/",  # ���ƾ���ѧ
    "https://www.heuet.edu.cn/",  # �ӱ���ó��ѧ
    "https://www.swufe.edu.cn/",  # ���ϲƾ���ѧ
    "https://www.ctbu.edu.cn/",  # ����ƾ����̴�ѧ
    "http://www.uibe.edu.cn/",  # ���⾭��ó�״�ѧ
    "https://www.hrbcu.edu.cn/",  # ��������ҵ��ѧ
    "https://www.tjcu.edu.cn/",  # �����ҵ��ѧ
    "https://www.zufe.edu.cn/",  # �㽭�ƾ���ѧ
    "http://news.zjgsu.edu.cn/18/",
    # �㽭���̴�ѧ---------��ҳ(http://www.hzic.edu.cn/)�з�������Ʋ����Ѿ�ʧЧ��status 404)|���ɹ���ҳ��url��http://news.zjgsu.edu.cn/18/
    "http://www.ynufe.edu.cn/index1024.htm",
    # "http://www.ynufe.edu.cn/",  # ���ϲƾ���ѧ---------ʹ�������Ҳ�޷�����url ��url--->http://www.ynufe.edu.cn/index1024.htm
    # Ҫ�ţ�http://www.ynufe.edu.cn/xwzx/index.htm  ���棺http://www.ynufe.edu.cn/xwzx/ybdt/index.htm
    "https://www.cueb.edu.cn/"  # �׶�����ó�״�ѧ---------�з�������ƣ�status 202 accepted��
]

finance_name = [
    "����ƾ���ѧ",
    "�Ͼ��ƾ���ѧ",
    "�����ƾ���ѧ",
    "ɽ���ƾ���ѧ",
    "�Ϻ��ƾ���ѧ",
    "���ϲƾ�������ѧ",  # �����õ���Ҫ�����Ӳ���ȫ��������������(У԰��Ӧ�ÿ���)---�ѽ��
    "�������̴�ѧ",  # ��ʱ����ȡ������ҳԴ��
    "ɽ���ƾ���ѧ",
    "�����ƾ���ѧ",
    "���ƾ���ѧ",
    "�ӱ���ó��ѧ",
    "���ϲƾ���ѧ",
    "����ƾ����̴�ѧ",  # �����õ���Ҫ�š��������Ӳ���ȫ��������������(У԰��Ӧ�ÿ���)---�ѽ��
    "���⾭��ó�״�ѧ",
    "��������ҵ��ѧ",
    "�����ҵ��ѧ",
    "�㽭�ƾ���ѧ",
    "�㽭���̴�ѧ",
    "���ϲƾ���ѧ",
    "�׶�����ó�״�ѧ"  # ����״̬��202����ȡ����Դ��---�ѽ��������Դ����ȡ����������Ҫѧϰ��ȡ��̬��ҳ֪ʶ
]
status = 404
Row = 0
getData = []  # getData�����б�
excel_savepath = "financeNewsAffiche.xls"
remainder = 2
timeout = 2


def main():
    global Row
    datalist = []  # ������վ�Ĺ��桢�����б�[����(�ֵ�)������]
    finance_html = []  # ������վ��htmlԴ��
    # �Ƚ���html��ҳԴ����ȡ
    # ��ȡǰ18��
    for i in range(0, len(finance_url) - remainder):
        html = askURL(finance_url[i])
        print(i, finance_name[i], status)
        # if 6 == i:
        #     html = bytes(html).decoding("utf-8")
        if 200 != status:
            finance_html.append(" ")
        else:
            finance_html.append(html)

    # ��װcookie��ȡ���remainder����ҳԴ��(��������)
    heads = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }
    for i in range(len(finance_url) - remainder, len(finance_url)):
        cookie = get_cookie(finance_url[i])
        heads['Cookie'] = cookie
        # heads['Cookie'] = cookies[i-len(finance_url)+remainder]

        html = askURLStrengthen(finance_url[i], heads)
        print(i, finance_name[i], status)

        if 200 != status:
            finance_html.append(" ")
        else:
            finance_html.append(html)

    # ����ÿ����ҳԴ��
    # for i in range(0, len(finance_url)):
    # pickle.dump(finance_html[i], open(str(i)+finance_name[i]+".html", 'wb'))

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # style_compression��ѹ����Ч��
    sheet = book.add_sheet("sheet1", cell_overwrite_ok=True)  # ��Ԫ�����ݿɸ���
    # ����excel�п�
    first_col = sheet.col(0)
    first_col.width = 256 * 20  # ����A�п��30
    sec_col = sheet.col(1)
    sec_col.width = 256 * 100
    thi_col = sheet.col(2)
    thi_col.width = 256 * 100

    # ���ݽ���
    for i in range(len(finance_html)):  #
        data = getData[i](finance_html[i])
        datalist.append(data)
        # �����excel
        sheet.write(Row, 0, finance_name[i])

        col = ("����", "Ҫ��")  # Ԫ����ӱ�ͷ
        for j in range(1, len(col) + 1):  # д���ͷ(����)
            sheet.write(Row + 0, j, col[j - 1])
        Row += 1

        affiche = data[0]  # ����
        news = data[1]  # ����
        for j in range(len(affiche)):
            # sheet.write(Row + j, 1, list(affiche.keys())[j])
            # sheet.write(Row + j, 2, list(affiche.values())[j])
            sheet.write(Row + j, 1,
                        xlwt.Formula('HYPERLINK("{}","{}")'.format(list(affiche.values())[j], list(affiche.keys())[j])))
        for j in range(len(news)):
            # sheet.write(Row + j, 3, list(news.keys())[j])
            # sheet.write(Row + j, 4, list(news.values())[j])
            sheet.write(Row + j, 2,
                        xlwt.Formula('HYPERLINK("{}","{}")'.format(list(news.values())[j], list(news.keys())[j])))
        Row += len(affiche) if len(affiche) > len(news) else len(news)
    a = datetime.datetime.now()  # �õ���ǰʱ��
    book.save(a.strftime("%Y-%m-%d-%H-%M-%S_") + excel_savepath)
    # ���˱���Ϊexcel����ʹ��Flask��������ݿ��ӻ���������Ѻã�excel������Ϊ���ݱ���


# �õ�ִ��url����ҳ��Ϣ�����ӳ�ʱ���ƣ�
def askURL(url):
    global status
    # ͷ����Ϣ �����û���������αװ�����������ҳ
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36"}
    req = urllib.request.Request(url, headers=head)
    html = ""  # ��ȡ������ҳԴ��
    try:
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8")
        status = response.status
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # has attribute
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# �õ�ִ��url����ҳ��Ϣ�����Ľ��棨���ӳ�ʱ���ƣ�
def askURLStrengthen(url, head={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36"}):
    global status
    # ͷ����Ϣ �����û���������αװ�����������ҳ

    req = urllib.request.Request(url, headers=head)
    html = ""  # ��ȡ������ҳԴ��
    try:
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8")
        status = response.status
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # has attribute
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


"""
# ʹ��CookieJar��ȡcookieֵ
def get_cookie(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12513.400'
    }

    cookie = cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12513.400')]
    resp = opener.open(url)

    cookieStr = ''
    for item in cookie:
        cookieStr = cookieStr + item.name + '=' + item.value + ';'
    return cookieStr
"""


# ����selenium+phantomjs�޽������������ʽ������վ���ٻ�ȡcookieֵ
def get_cookie(url):
    # �������������
    driver = webdriver.PhantomJS()
    # ��ҳ��
    driver.get(url)
    # ��ȡcookie�б�
    cookie_list = driver.get_cookies()
    # ��ʽ����ӡcookie
    # print(cookie_list)
    cookieStr = ''
    for cookie in cookie_list:
        cookieStr = cookieStr + cookie['name'] + "=" + cookie['value'] + ';'
    return cookieStr


def replaceAll(str):  # �滻���пո񡢻س������з�
    str = str.replace("\r", "")
    str = str.replace("\n", "")
    str = str.replace(" ", "")
    return str


# ����ƾ���ѧ
# getData0������ʽģʽ����
ul_xxywList_a_href0 = re.compile('<a href="(.*?)" target="_blank" title=".*?">.*?</a>')  # ����������ʽ�õ��Ľ������(.*?)����Ķ���
ul_xxywList_a_title0 = re.compile('<a href=".*?" target="_blank" title="(.*?)">.*?</a>')
div_gg_a_href0 = re.compile('<a class="fl" href="(.*?)" title=".*?"><b>.*?</b></a>')
div_gg_a_title0 = re.compile('<a class="fl" href=".*?" title="(.*?)"><b>.*?</b></a>')  # <a.*?title="(.*?)".*?</a>


def getData0(html):  # ��������
    soup = BeautifulSoup(html, "html.parser")  # ʹ��html.parser����������html�ĵ��γ����νṹ����
    affiche = {}  # ����
    news = {}  # ����

    # Ҫ��λ��class=xxywList��ul��
    ul_xxywList = soup.select("ul[class='xxywList']")
    ul_xxywList = str(ul_xxywList)
    news_url = re.findall(ul_xxywList_a_href0, ul_xxywList)
    news_title = re.findall(ul_xxywList_a_title0, ul_xxywList)

    for i in range(len(news_url)):
        news[news_title[i]] = news_url[i]
    # print(news)

    # ����λ��class=gg��div��
    # ÿ���»�ȡ��url��Ҫǰ׺��ӣ�"http://www.cufe.edu.cn/"
    div_gg = soup.select("div[class='gg']")
    div_gg = str(div_gg)
    affiche_url = re.findall(div_gg_a_href0, div_gg)
    affiche_title = re.findall(div_gg_a_title0, div_gg)
    for i in range(len(affiche_url)):
        affiche[affiche_title[i]] = "http://www.cufe.edu.cn/" + affiche_url[i]
    # print(affiche)
    return [affiche, news]


getData.append(getData0)

# �Ͼ��ƾ���ѧ
# getData1������ʽģʽ����
div_frhomegonggao_a_href1 = re.compile('<a class="fl" href="(.*?)">.*?</a>')
div_frhomegonggao_a_title1 = re.compile('<a class="fl" href=".*?">(.*?)</a>')
div_swiper_wrapper_a_href1 = re.compile('<a href="(.*?)">.*?</a>')
div_swiper_wrapper_a_title1 = re.compile('<a href=".*?">(.*?)</a>')


def getData1(html):  # ��������
    soup = BeautifulSoup(html, "html.parser")  # ʹ��html.parser����������html�ĵ��γ����νṹ����
    affiche = {}  # ����
    news = {}  # ����

    # Ҫ��λ��class="frhome-gonggao"��div��
    div_frhomegonggao = soup.select("div[class='fr home-gonggao']")
    div_frhomegonggao = str(div_frhomegonggao)
    news_url = re.findall(div_frhomegonggao_a_href1, div_frhomegonggao)
    news_title = re.findall(div_frhomegonggao_a_title1, div_frhomegonggao)

    # ÿ���»�ȡ��url��Ҫǰ׺��ӣ�"http://www.nufe.edu.cn/"
    for i in range(len(news_url)):
        news[news_title[i]] = "http://www.nufe.edu.cn/" + news_url[i]
    # print(news)

    # ����λ��class="parBd"��div�еĵ�һ��class="swiper-wrapper"��div��

    div_swiper_wrapper = soup.body.select("div[class='swiper-wrapper']")
    div_swiper_wrapper = str(div_swiper_wrapper[0])
    affiche_url = re.findall(div_swiper_wrapper_a_href1, div_swiper_wrapper)
    affiche_title = re.findall(div_swiper_wrapper_a_title1, div_swiper_wrapper)
    for i in range(len(affiche_url)):
        affiche[affiche_title[i]] = "http://www.nufe.edu.cn/" + affiche_url[i]
    # print(affiche)
    return [affiche, news]


getData.append(getData1)

# �����ƾ���ѧ
# getData2������ʽģʽ����
ul_ul2_a_href2 = re.compile('<a href="(.*?)" target="_blank">.*?</a>', re.S)
ul_ul2_a_title2 = re.compile('<p>(.*?)</p>')
ul_ul2_a_title_time2 = re.compile('<span>(.*?)</span>')
ul_two_leftrl_a_href2 = re.compile('<a href="(.*?)" target="_blank">.*?</a>')
ul_two_leftrl_a_title2 = re.compile('<a href=".*?" target="_blank">(.*?)</a>')
ul_two_leftrl_a_title_time2 = re.compile('<span style="float:right; color:#999999; font-size:12px;">(.*?)</span>')


def getData2(html):  # ��������
    soup = BeautifulSoup(html, "html.parser")  # ʹ��html.parser����������html�ĵ��γ����νṹ����
    affiche = {}  # ����
    news = {}  # ����
    # Ҫ��λ��class="ul2"��ul��
    ul_ul2 = soup.select("ul[class='ul2']")
    ul_ul2 = str(ul_ul2)
    news_url = re.findall(ul_ul2_a_href2, ul_ul2)
    news_title = re.findall(ul_ul2_a_title2, ul_ul2)
    news_time = re.findall(ul_ul2_a_title_time2, ul_ul2)
    for i in range(len(news_url)):
        news[news_title[i] + "----" + news_time[i]] = news_url[i]

    # ����̫��ͨ����ҳ�޷���ȡ����Ҫͨ��url:http://news.jxufe.edu.cn/news-list-xinxigonggao.html��ȡ
    html_affiche = askURL("http://news.jxufe.edu.cn/news-list-xinxigonggao.html")
    soup = BeautifulSoup(html_affiche, "html.parser")
    ul_two_leftrl = soup.select("div[class='two_leftrl']")
    ul_two_leftrl = str(ul_two_leftrl)
    affiche_url = re.findall(ul_two_leftrl_a_href2, ul_two_leftrl)
    affiche_title = re.findall(ul_two_leftrl_a_title2, ul_two_leftrl)
    affiche_time = re.findall(ul_two_leftrl_a_title_time2, ul_two_leftrl)
    for i in range(len(affiche_url)):
        affiche[affiche_title[i] + "----" + affiche_time[i]] = affiche_url[i]
    return [affiche, news]


getData.append(getData2)

# ɽ���ƾ���ѧ
# getData3������ʽģʽ����
news_url_a_href3 = re.compile('<a href="(.*?)" target="_blank" title=".*?">.*?</a>')
news_url_a_title3 = re.compile('<a href=".*?" target="_blank" title="(.*?)">.*?</a>')
news_url_a_title_time3 = re.compile('<span class="gray-3 fr">(.*?)</span>')
ul_style_affiche_a_href3 = re.compile('<a href="(.*?)" target="_blank" title=".*?">')
ul_style_affiche_a_title3 = re.compile('<a href=".*?" target="_blank" title="(.*?)">')
ul_style_affiche_a_title_time3 = re.compile('<span class="gray-3 fr">(.*?)</span>')


def getData3(html):  # ��������
    soup = BeautifulSoup(html, "html.parser")  # ʹ��html.parser����������html�ĵ��γ����νṹ����
    affiche = {}  # ����
    news = {}  # ����