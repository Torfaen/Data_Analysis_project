
import requests
import re
import time
import random
from DrissionPage import ChromiumPage
import json
import os
keyword="联想笔记本"
def find_title_ele(dp):
    note_text_ele = dp.ele('css:span.note-text', timeout=10)
    if note_text_ele:
        rect = note_text_ele.rect
        comment_x, comment_y = rect.midpoint
        print(f'找到title元素，坐标: ({comment_x}, {comment_y})')
        return comment_x, comment_y
    else:
        return (1000,800)

def get_id_token(json_data):
    all_id=[]
    all_xsec_token=[]
    try:
        items=json_data['data']['items']
        for item in items:
            all_id.append(item['id'])
            all_xsec_token.append(item['xsec_token'])
        return all_id,all_xsec_token
    except:
        return None,None


def pull_html(id,token):
    dp = ChromiumPage()
    # 数据获取使用监听数据包形式，一定要在执行动作之前
    html = []
    page = 1
    # 启动监听器 - 监听评论API请求
    dp.listen.start('/api/sns/web/v2/comment/page')
    #进入网页
    dp.get(f'https://www.xiaohongshu.com/explore/{id}?xsec_token={token}&xsec_source=pc_search&source=unknown')
    time.sleep(2)
    title_x, title_y = find_title_ele(dp)
    pixel_scroll=1600
    while True:
        #监听数据包
        dp.actions.move_to((title_x, title_y))
        #print(f'鼠标位置: ({dp.actions.curr_x}, {dp.actions.curr_y})')
        print(f"开始监听第{page}页数据包，最长4s")
        r=dp.listen.wait(timeout=2)
        if not r:
            print(f"r={r}没有更多数据")
            return
        #监听到了数据包
        if r:
            #记入html列表
            html.append(r.response.body)
            #cursor=r.response.body['data']['cursor']
            #print(f"cursor={cursor}")
            if not os.path.exists(f"html_data/{keyword}"):
                os.makedirs(f"html_data/{keyword}")
            with open(f"html_data/{keyword}/{id}_page{page}.json", "w", encoding="utf-8") as f:
                print(f"{id}_page{page}.json写入到路径html_data")
                json.dump(r.response.body, f, ensure_ascii=False, indent=4)
            page=page+1
            #判断是否还有更多数据
            if r.response.body['data']['has_more'] == False:
                print(f"has_more={r.response.body['data']['has_more']}，没有更多数据")
                break
            else:
                print("有更多数据")
                #下滑300像素
                dp.actions.scroll(pixel_scroll)
                print(f"下滑{pixel_scroll}像素")
        else:
            print("没有监听到数据包")
            print(f"下滑{pixel_scroll}像素")
            dp.actions.scroll(pixel_scroll)
        
def main():
    keyword="联想笔记本"
    for i in range(1,13):

        path=f"page/{keyword}/search_result_page{i}.json"
        with open(path, encoding="utf-8") as f:
            json_data = json.load(f)
            ids,xsec_tokens=get_id_token(json_data)
            #查重拉取网页
            j=1
            for id,token in zip(ids,xsec_tokens):
                #查重拉取网页
                if os.path.exists(f"html_data/{keyword}/{id}_page{j}.json"):
                    print(f"html_data/{keyword}/{id}.json已存在")
                    continue
                else:
                    pull_html(id,token)
                    j=j+1
if __name__ == "__main__":
    main()