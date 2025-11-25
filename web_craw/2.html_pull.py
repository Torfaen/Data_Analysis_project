import requests
import json
import random
import time
import os

keyword="机械革命"
cookies_dict = json.load(open('cookies.json', 'r', encoding='utf-8'))
# 将字典格式的cookies转换为字符串格式
cookies_str = '; '.join([f'{k}={v}' for k, v in cookies_dict.items()])
headers = {
    'cookie': cookies_str,
    'referer': 'https://www.xiaohongshu.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}

def get_id_token(json_data):
    all_id=[]
    all_xsec_token=[]
    items=json_data['data']['items']
    for item in items:
        all_id.append(item['id'])
        all_xsec_token.append(item['xsec_token'])
    return all_id,all_xsec_token

def pull_html(id,xsec_token):
    #wait_time=random.randint(10, 20)
    print(f'开始处理获取{id}的数据')
    #print(f'等待{wait_time}秒')
    #time.sleep(wait_time)
    cursor=''
    page_now=1
    wait_time=1
    #原始页面，不滑动
    #https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id=689cace8000000001c00cf4c&cursor=&top_comment_id=&image_formats=jpg,webp,avif&xsec_token=ABQ5fywvpJcoh6mG7oXIpmq0wVidTt42S1z8S3uvJZaq8%3D
    #https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id=689cace8000000001c00cf4c&cursor=68b1690f000000000903a01d&top_comment_id=&image_formats=jpg,webp,avif&xsec_token=ABQ5fywvpJcoh6mG7oXIpmq0wVidTt42S1z8S3uvJZaq8%3D
    while True:
        print(f'等待{wait_time}秒，开始获取{id}的第{page_now}页评论数据')
        time.sleep(wait_time)
        try:
            url = f'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={id}&cursor={cursor}&top_comment_id=&image_formats=jpg,webp,avif&xsec_token={xsec_token}'
            response = requests.get(url=url, headers=headers)
        except Exception as e:
            print( e)
            time.sleep(20)
            continue
        
        if response.json()['code'] != 0:
            print(f"获取数据失败，response的code值为{response.json()['code']}")
            print(f"response json 错误信息为: {response.json()['msg']}")
            #停止
            
            print(f'抓取下一个帖子数据')
            time.sleep(5)
            break

        try:
           # 确保目录存在
            os.makedirs("html_data_test", exist_ok=True)
            path = os.path.join("html_data_test",f"{id}_page{page_now}.json")
            #查重有没有写过
            with open(path, "w", encoding="utf-8") as f:
                print(f"{id}_page{page_now}.json写入到路径{path}")
                f.write(response.text)
        except Exception as e:
            print(e)
            print(f"保存数据失败{e}")
            exit()

        #重设等待时间
        wait_time=random.randint(3, 5)
        if response.json()['data']['has_more']== True:
            #更新cursor
            cursor=response.json()['data']['cursor']
            #翻到下一页
            page_now=page_now+1
            continue
        #hasmore为false
        print(f"{id}没有更多评论了")
        break


#本py文件用来pull_html，数据处理
def main():
#-----------pull_html部分-------------------------
    os.makedirs("html_data", exist_ok=True)
    os.makedirs("csv_data", exist_ok=True)
    json_data=[]
    #阈值检测，重新拉取
    min_page=3
    #获取搜索页面所有搜索结果的json文件
    for i in range(1,9):
        path=f"page/{keyword}/search_result_page{i}.json"
        json_data.append(path)
    for i in range(len(json_data)):
        with open(json_data[i], encoding="utf-8") as f:
            json_data[i] = json.load(f)
            ids,xsec_tokens=get_id_token(json_data[i])
            #查重判断，如果已经拉取过，就跳过
            for id,token in zip(ids,xsec_tokens):
                #查重拉取网页
                if os.path.exists(f"html_data_test/{keyword}_{id}_page{min_page}.json"):
                    print(f"页面{id}_page已经存在且超过最少页数：{min_page}页，跳过不拉取")
                    continue
                pull_html(id,token)
#----------------------------------------------
if __name__ == "__main__":
    main()