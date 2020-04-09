from bs4 import BeautifulSoup
import requests
import time


def download_image(image_number):
    # 拿到Archillect网站的url模版
    # 创建变量n，将n的初始值赋值为1，并放到url结尾
    # 创建变量r，将r赋值为通过requests包返回的相应内容 (成功即为:"<Response [200]>")
    r = requests.get("https://archillect.com/" + image_number)

    # 创建变量image_html，将image_html赋值为通过requests包content方法返回的html代码,并用bs4美化
    image_html = BeautifulSoup(r.content, "lxml")

    # 在html代码中找到图片id，利用图片id和bs4的find方法找到image的代码行
    # 创建变量image_link，将image_link赋值为：利用bs4包的get方法找到image代码行中的src，也就是源图片链接
    image_link = image_html.find(id="ii").get("src")

    # 创建一个变量image，将image赋值为通过requests包的get方法返回的图片数据
    image = requests.get(image_link).content

    # 用切片方法拿到image_link结尾的最后四个字符（.png, .gif  [-4:]）
    # image_name是图片名称
    image_name = image_number + image_link[-4:]
    # 并进行with open write操作，下载图片
    with open("images/" + image_name, "wb") as f:
        f.write(image)

    print("已成功下载" + image_name)

    return image_name


def weibo_upload(image_name):
    # 微博的api
    url = "https://api.weibo.com/2/statuses/share.json"

    payload = {
        "access_token": "2.00UNgkiH3dxuNE100c227e36rOWlGB",
        "status": "test http://www.weibo.com/",  # 微博内容，一定加个人账号的微博安全地址
    }
    files = {
        "pic": open("images" + image_name, "rb"),
    }

    requests.post(url, data=payload, files=files)
    print("已成功上传" + image_name)
    with open("image_history.txt", "wb") as f:
        f.write(image_name)


def main():
    while True:
        with open("image_history.txt", "rb") as f:
            image_number = f.read()[:-4]
            print("获得image_number为" + image_number)

        # 将image_number传入download_image函数，返回image_name
        image_name = download_image(image_number)
        # image_name传到weibo_upload方法中
        weibo_upload(image_name)

        # 每次上传后睡眠30分钟，首先测试半分钟
        time.sleep(30)


if __name__ == "__main__":
    main()
