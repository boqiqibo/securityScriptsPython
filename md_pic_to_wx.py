import re
import os
import requests
import json

def get_access_token(appid, secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            print(f"获取 access_token 失败: {result}")
            return None
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

# 判断路径是否存在，并且是否是文件
def check_file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)

# 从md中获取图片路径
def get_pic_path_list(markdown_file_path):
    # 读取markdown文件内容
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # 使用正则表达式匹配所有URL地址
    # png
    pic_list = re.findall(r'!\[[^\]]*\]\(([^)]*\.png)\)', markdown_content)
    return pic_list

# 拼接路径
def join_pic_path(markdown_file_path:str, pic_path):
    # 判断相对路径还是绝对路径
    if os.path.isabs(pic_path):
        if check_file_exists(pic_path):
            return pic_path
    else:
        pic_path = os.path.join(os.path.dirname(markdown_file_path), pic_path)
        if check_file_exists(pic_path):
            return pic_path
    return None





def upload_image_to_wechat(access_token, image_path):
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    files = {'media': open(image_path, 'rb')}
    try:
        response = requests.post(url, files=files)
        result = json.loads(response.text)
        if 'url' in result:
            return result['url']
        else:
            print(f"上传失败，错误信息: {result}")
            return None
    except Exception as e:
        print(f"发生异常: {e}")
        return None




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
需要修改的三个参数
directory
appid
secret
"""
if __name__ == '__main__':
    # 指定目录，这里以当前目录为例，你可以修改为你想要的目录
    directory = r'要上传到微信平台的markdown'
    appid = "你自己的appid"
    secret = "你自己的appsecret"

    md_file_paths = get_md_file_paths(directory)
    for file_path in md_file_paths:
        pic_path_list = get_pic_path_list(file_path)
        access_token = get_access_token(appid, secret)
        print(access_token)
        image_online_json = {}
        for image_path in pic_path_list:
            img_real_path = join_pic_path(file_path, image_path)
            if img_real_path is not None:
                url = upload_image_to_wechat(access_token, img_real_path)
                image_online_json[image_path] = url
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        for old_url, new_url in image_online_json.items():
            markdown_content = markdown_content.replace(old_url, new_url)
        markdown_file_path = file_path
        with open(markdown_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)


    print("完成")
