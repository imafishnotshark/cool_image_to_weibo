from bs4 import BeautifulSoup
import requests


# 拿到Archillect网站的url模版
# 创建变量n，将n的初始值赋值为1，并放到url结尾
# 创建变量r，将r赋值为通过requests包返回的相应内容 (成功即为:"<Response [200]>")
for number in range(1, 11):
    n = str(number)
    r = requests.get('https://archillect.com/' + n)

    # 创建变量image_html，将image_html赋值为通过requests包content方法返回的html代码,并用bs4美化
    image_html = BeautifulSoup(r.content, 'lxml')

    # 在html代码中找到图片id，利用图片id和bs4的find方法找到image的代码行
    # 创建变量image_link，将image_link赋值为：利用bs4包的get方法找到image代码行中的src，也就是源图片链接
    image_link = image_html.find(id='ii').get('src')

    # 创建一个变量image，将image赋值为通过requests包的get方法返回的图片数据
    image = requests.get(image_link).content

    # 用切片方法拿到image_link结尾的最后四个字符（[-4:]）
    # 并进行with open write操作，下载图片
    with open('images/' + n + image_link[-4:], 'wb') as f:
        f.write(image)

    print("已成功下载" + n + image_link[-4:])
