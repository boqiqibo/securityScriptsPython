import requests


class MapAPICaller:
    def __init__(self, key):
        self.amap_key = key
        self.baidu_key = key
        self.tencent_key = key

    def amap_walking_direction(self):
        url = f"https://restapi.amap.com/v3/direction/walking?origin=116.434307,39.90909&destination=116.434446,39.90816&key={self.amap_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None

    def amap_jsapi_regeo(self):
        url = f"https://restapi.amap.com/v3/geocode/regeo?key={self.amap_key}&s=rsv3&location=116.434446,39.90816&callback=jsonp_258885_&platform=JS"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None

    def amap_miniprogram_regeo(self):
        url = f"https://restapi.amap.com/v3/geocode/regeo?key={self.amap_key}&location=117.19674%2C39.14784&extensions=all&s=rsx&platform=WXJS&appname=c589cf63f592ac13bcab35f8cd18f495&sdkversion=1.2.0&logversion=2.0"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None

    def baidu_webapi_search(self):
        url = f"https://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak={self.baidu_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None

    def baidu_webapi_ios_search(self):
        url = f"https://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak={self.baidu_key}=iPhone7%2C2&mcode=com.didapinche.taxi&os=12.5.6"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None

    def tencent_webapi_search(self):
        url = f"https://apis.map.qq.com/ws/place/v1/search?keyword=酒店&boundary=nearby(39.908491,116.374328,1000)&key={self.tencent_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None

    def batch_call(self):
        results = {
            "高德webapi": self.amap_walking_direction(),
            "高德jsapi": self.amap_jsapi_regeo(),
            "高德小程序定位": self.amap_miniprogram_regeo(),
            "百度webapi": self.baidu_webapi_search(),
            "百度webapiIOS版": self.baidu_webapi_ios_search(),
            "腾讯webapi": self.tencent_webapi_search()
        }
        return results
def print_key_and_value_length(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            print(f"Key: {key}, Value length: {value}")

if __name__ == '__main__':
    key = "key的值"
    result = MapAPICaller(key).batch_call()
    print_key_and_value_length(result)