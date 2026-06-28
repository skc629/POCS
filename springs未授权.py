#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
import argparse
import warnings
import urllib3
import textwrap
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
            print(f'[+] {url} 存在漏洞')
        else:
            print(f'[-] {url} 不存在漏洞')
    except requests.exceptions.RequestException as e:
        # 可以选择忽略连接错误或超时，或者打印调试信息
        # print(f'[!] {url} 请求失败: {str(e)}')
        pass
    except Exception as e:
        # 其他异常，打印调试信息
        # print(f'[!] {url} 发生错误: {str(e)}')
        pass


def main():
    # 实例化一个对象 , 并添加命令行的描述信息,一般在脚本中用来介绍脚本是干嘛的
    parser = argparse.ArgumentParser(description='spring未授权检测工具',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''示例：python one.py -u http://www.baidu.com'''))

    # dest给输入值取参数名
    parser.add_argument("-u", dest="url", help="请输入的要检测的URL")
    parser.add_argument("-f", dest="file", help="请输入的要检测的URL文件")
    # parse_args将输入的值解析为python对象
    args = parser.parse_args()
    if args.url:
        if 'http' not in args.url:
            args.url=f'http://{args.url}'
        check(args.url)
    elif args.file:
        urls = []
        with open(args.file, 'r') as f:
            for line in f:
                domain = line.strip()
                if not domain:
                    continue
                if domain.startswith('http://'):
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
    banner = """ 
    .___                .___                   .__                        
  __| _/____  ___.__. __| _/____  ___.__. _____|  |   ____   ____ ______  
 / __ |\__  \<   |  |/ __ |\__  \<   |  |/  ___/  | _/ __ \_/ __ \\____ \ 
/ /_/ | / __ \\___  / /_/ | / __ \\___  |\___ \|  |_\  ___/\  ___/|  |_> >
\____ |(____  / ____\____ |(____  / ____/____  >____/\___  >\___  >   __/ 
     \/     \/\/         \/     \/\/         \/          \/     \/|__|    

    """
    print(banner)
    #函数调用
    main()