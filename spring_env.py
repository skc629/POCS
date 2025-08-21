#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
import warnings
import urllib3
from multiprocessing.dummy import Pool

# 关闭警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# 定义全局变量

PATH = '/env'
THREADS = 30  # 调整线程数


def check(domain):
    url = domain + PATH
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        'Accept': '*/*',
        'Connection': 'close'
    }
    try:
        response = requests.get(url, headers=headers, timeout=3, verify=False)
        if response.status_code == 200 and 'profiles' in response.text:
            print(f'[*] {url} 存在漏洞')
        # else:
        #     print(f'[-] {url} 不存在漏洞')
    except requests.exceptions.RequestException as e:
        # 可以选择忽略连接错误或超时，或者打印调试信息
        # print(f'[!] {url} 请求失败: {str(e)}')
        pass
    except Exception as e:
        # 其他异常，打印调试信息
        # print(f'[!] {url} 发生错误: {str(e)}')
        pass


def main():
    urls = []
    with open('links.txt', 'r') as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue
            if domain.startswith('http://') or domain.startswith('https://'):
                urls.append(domain)
            else:
                urls.append(f'http://{domain}')

    print(f'开始扫描，共 {len(urls)} 个URL')
    pool = Pool(THREADS)
    pool.map(check, urls)
    pool.close()
    pool.join()
    print('扫描完成')


if __name__ == '__main__':
    main()