import json
import time
from DrissionPage import ChromiumPage
import os
import hashlib

keyword = "联想笔记本"


def get_search_data():
    #启动浏览器
    dp =ChromiumPage()
    #看过的哈希值集合（用于去重）
    seen_hashes=set()
    # 数据获取使用监听数据包形式，一定要在执行动作之前
    dp.listen.start('/api/sns/web/v1/search/notes')
    # 访问网站
    dp.get('https://www.xiaohongshu.com/search_result?keyword=%25E8%2581%2594%25E6%2583%25B3%25E7%25AC%2594%25E8%25AE%25B0%25E6%259C%25AC&source=unknown')
    print('开始获取数据,等待数据包加载')
    max_Page=20
    current_Page=1
    down_pixel=500
    time_out= 3
    time_out_sum=0
    while current_Page<=max_Page:
        # 等待数据包加载
        print(f'等待第{current_Page}页数据包加载，超时时间{time_out}秒')
        print(f"当前数据包超时时长为{time_out_sum}秒")
        r=dp.listen.wait(timeout = time_out )
        if not r:
            time_out_sum = time_out_sum + time_out
            print(f'第{current_Page}页数据包加载超时，跳过当前循环')
            print(f'滚动画面，向下滑动到底')
            dp.scroll.to_bottom()
            continue
        time_out_sum=0
        # 获取响应文本的前20行
        json_data = r.response.body  
        #字典转换为字符串
        response_text = json.dumps(json_data, ensure_ascii=False)  
        #字符串取前20行，计算哈希值
        response_lines = response_text.split('\n')[:20]  
        first_20_lines = '\n'.join(response_lines)
        
        # 计算前20行的哈希值
        data_hash = hashlib.md5(first_20_lines.encode('utf-8')).hexdigest()
        
        #数据包查重（使用哈希值）
        if data_hash in seen_hashes:
            #已有数据包，跳过当前循环
            dp.scroll.to_bottom()
            print(f'已有数据包，跳过当前循环，向下滑动{down_pixel}像素')
            continue
        
        #新数据包，添加到seen_hashes查重集合
        seen_hashes.add(data_hash)
        print(f'第{current_Page}页数据包加载完成')
        # 创建page目录（如果不存在）
        page_dir = f"page/{keyword}"
        os.makedirs(page_dir, exist_ok=True)
        # 保存 JSON 数据到文件（json_data已在上面定义）
        with open(f"{page_dir}/search_result_page{current_Page}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        # 滚动画面
        current_Page+=1
        if current_Page <= max_Page:  # 最后一页不需要滚动
            print(f'滚动画面，向下滑动{down_pixel}像素')
            dp.scroll.to_bottom()
            time.sleep(2)  # 等待页面加载



#本py文件负责搜索并获取搜索结果
def main():
    get_search_data()
if __name__ == "__main__":
    main()