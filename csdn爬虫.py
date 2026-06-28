import requests
import parsel
import pdfkit

#前端模板
html='''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" >
    <title>Document</title>
</head>
<body>
  {content}
</body>
'''

url='https://blog.csdn.net/yjprolus/article/details/122129791?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522E2387362-1CE6-4795-A32D-7E878F2E9F2E%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fvipall.%2522%257D&request_id=E2387362-1CE6-4795-A32D-7E878F2E9F2E&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~vipall~first_rank_ecpm_v1~rank_v31_ecpm-1-122129791-null-null&utm_term=%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C&spm=1018.2226.3001.4187'


dic={
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}


resp=requests.get(url,headers=dic)     #响应得到回复

selector=parsel.Selector(resp.text)     #对回复的text进行提取
article=selector.css('article').get()   #css选择器 根据标签 提取数据


#print(article)

with open('aa.html',mode='w',encoding='utf-8') as f:
   f.write(html.format(content=article))


config=pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe')#pdf转换工具地址，r将二进制转换为原始字符串
pdfkit.from_file('aa.html','计算机网络资料1.pdf',configuration=config)