import os
import requests
from bs4 import BeautifulSoup
import pdfkit


def download_images(url, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 发送GET请求获取网页内容
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找所有的图片标签
    img_tags = soup.find_all('img')

    for img in img_tags:
        # 获取图片URL
        img_url = img['src']

        # 下载图片
        response = requests.get(img_url)

        # 提取图片文件名
        img_filename = img_url.split('/')[-1]

        # 拼接保存路径
        save_path = os.path.join(output_folder, img_filename)

        # 保存图片到本地
        with open(save_path, 'wb') as f:
            f.write(response.content)


def convert_images_to_pdf(image_folder, output_pdf):
    # 获取所有图片文件
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   os.path.isfile(os.path.join(image_folder, f))]

    # 将图片文件按照文件名排序
    image_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    # 使用pdfkit将图片转换为PDF
    pdfkit.from_file(image_files, output_pdf)


if __name__ == '__main__':
    # 获取用户输入的网址
    url = input("请输入要转换的网址：")

    # 图片保存路径
    image_folder = './images'

    # 输出PDF文件路径
    output_pdf = './output.pdf'

    # 下载图片
    download_images(url, image_folder)

    # 将图片转换为PDF
    convert_images_to_pdf(image_folder, output_pdf)
