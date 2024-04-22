import os
import re
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logging.StreamHandler().setLevel(logging.INFO)

# Welcome

def welcome():
    print('--------------------程序开始--------------------')
    print('仅供学习参考；产生任何后果由用户承担')
    print('继续使用即代表同意上述声明')
    choice = input('是否同意上述声明？ (y/n) ').lower()
    while choice not in ['y', 'n']:
        choice = input('输入无效，请重新输入是否同意上述声明？ (y/n) ').lower()
    if choice == 'y':
        return None
    else:
        input('按任意键退出...')
        exit()

welcome()

# Input and Parse URL

def inputandparseurl():
    while True:
        try:
            raw_url = input('请输入“查看详细”页网址，例如：http://jjg.spc.org.cn/resmea/standard/JJF%25201261.9-2013/?\n')
            pattern = r'http://jjg.spc.org.cn/resmea/standard/([A-Z]{3})%2520([0-9.-]{3,20})/[?]?'
            match = re.match(pattern, raw_url)
            if match:
                std_type, std_no = match.groups()
                return std_type, std_no ,raw_url
            else:
                print('输入的网址格式有误！\n标准格式为：\nhttp://jjg.spc.org.cn/resmea/standard/([A-Z]{3})%2520([0-9.-]{3,20})/[?]?.*\n而输入的格式为：')
                print(raw_url)
        except KeyboardInterrupt():
            print('程序已退出')
            exit()

std_type, std_no, raw_url = inputandparseurl()

# Generate Session

def generatesession():
    headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control' : 'max-age=0',
    'Connection' : 'keep-alive',
    'Host' : 'jjg.spc.org.cn',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }
    session = requests.session()
    session.headers.update(headers)
    response = session.get(url = f'http://jjg.spc.org.cn/resmea/view/stdonline?a100={std_type}+{std_no}&standclass=')
    return session, response

session, response = generatesession()
Myfoxit = re.findall('var enc = "([^"]*)"', response.text)
token = re.findall('var rc = "([^"]*)"', response.text)

# Get PDF Session Response

def getpdfresponse():
    url = f'http://jjg.spc.org.cn/resmea/view/onlinereading?token={token[0]}&Myfoxit={Myfoxit[0]}'
    headers = {
    'Accept' : '*/*',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control' : 'no-cache',
    'Connection' : 'keep-alive',
    'Host' : 'jjg.spc.org.cn',
    'Pragma' : 'no-cache',
    'Referer' : f'http://jjg.spc.org.cn/resmea/view/stdonline?a100={std_type}+{std_no}&standclass=',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'myfoxit' : f'{Myfoxit[0]}'
    }
    response = session.get(url, headers=headers)
    return response

# Main function
def main():
    start_time = time.time()
    with open(f'{std_type} {std_no}.pdf', 'wb') as f:
        f.write(getpdfresponse().content)
    end_time = time.time()
    if os.path.exists(f'{std_type} {std_no}.pdf'):
        print(f'下载成功 | {end_time - start_time}秒')
    else:
        print('下载失败')

main()

while True:
    try:
        choice = input('是否继续下载？ (y/n) ').lower()
        while choice not in ['y', 'n']:
            choice = input('输入无效，请重新输入是否同意上述声明？ (y/n) ').lower()
        if choice == 'y':
            std_type, std_no, raw_url = inputandparseurl()
            session, response = generatesession()
            Myfoxit = re.findall('var enc = "([^"]*)"', response.text)
            token = re.findall('var rc = "([^"]*)"', response.text)
            main()
        else:
            print('--------------------程序结束--------------------')
            logging.debug('调试日志')
            logging.info('消息日志')
            logging.warning('警告日志')
            logging.error('错误日志')
            logging.critical('严重错误日志')
            input('按任意键退出...')
            exit()
    except KeyboardInterrupt:
        breakpoint()
