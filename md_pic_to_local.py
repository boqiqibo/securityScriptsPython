import re  
import os  
import requests  

def download_images(markdown_file_path):
    # 读取markdown文件内容
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # 使用正则表达式匹配所有URL地址
    urls = re.findall(r'!\[[^\]]*\]\(([^)]*\.png)\)', markdown_content)

    # 存储所有URL地址
    url_list = []
    for url in urls:
        if url.startswith('http'):
            url_list.append(url)
        
        
    # 定义要创建的文件夹名称
    folder_name = os.path.join(os.path.dirname(markdown_file_path),"picture_libs")

    # 检查文件夹是否存在
    if not os.path.exists(folder_name):
        # 如果不存在，则创建文件夹
        os.makedirs(folder_name)
        print(f"文件夹 {folder_name} 创建成功。")
    # else:
        # print(f"文件夹 {folder_name} 已存在。")

    # 下载图片到本地
    for url in url_list:
        global proxy
        if proxy:
            global proxies
            response = requests.get(url, proxies=proxies)
        else:
            response = requests.get(url)
        if response.status_code == 200:
            image_name = os.path.basename(url)[:255]  # 限制图片名字长度不超过255个字符
            image_dir = os.path.join(os.path.dirname(markdown_file_path),"picture_libs")#markdown文件目录同级下名为picture_libs的文件夹
            image_path = os.path.join(image_dir,image_name)#带绝对路径带文件名
            image_relpath = os.path.relpath(image_path,os.path.dirname(markdown_file_path))#计算相对路径
            with open(image_path, 'wb') as file:
                file.write(response.content)
                print(f"图片 {image_name} 下载成功")
                # 替换markdown文件中的URL地址，这里的image_path需要改成相对路径
                markdown_content = markdown_content.replace(url, image_relpath)
        else:
            print(f"图片 {url} 下载失败")
            continue

        # 将替换后的内容写回markdown文件
        with open(markdown_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

    



def get_md_file_paths(directory):
    url = []
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为 .md
            if file.endswith('.md'):
                # 构建文件的完整路径
                file_path = os.path.join(root, file)
                url.append(file_path)
    return url

"""
如果需要代理，
将proxy的值改为True，
并在proxies中填入代理地址
"""
proxy = False
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

"""
放在与poc的同目录下，运行即可

"""
if __name__ == '__main__':
    # 指定目录，这里以当前目录为例，你可以修改为你想要的目录
    directory = '.'
    md_file_paths = get_md_file_paths(directory)
    # for path in md_file_paths:
    #     print(path)
    for file_path in md_file_paths:
        download_images(file_path)
    print("完成")
