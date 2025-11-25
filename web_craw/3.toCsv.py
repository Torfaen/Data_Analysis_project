import json
from datetime import datetime
import pandas as pd
import os
keyword="机械革命"
#获取目录所有json文件，获取评论数据
def get_comment_data(html_path):
    records=[]
    print(f'开始获取{html_path}的评论数据')
    for file in os.listdir(html_path):
        if file.endswith(".json"):
            with open(os.path.join(html_path, file), encoding="utf-8") as f:
                json_data = json.load(f)
                if json_data['code'] != 0:
                    print(f"获取数据失败，response的code值为{json_data['code']}")
                    print(f"response json 错误信息为: {json_data['msg']}")
                    continue
            comments=json_data['data']['comments']
            for c in comments:
                dt = datetime.fromtimestamp(c["create_time"] / 1000)
                record = {
                "comment_id": c["id"],
                "note_id": c["note_id"],
                "user_id": c["user_info"]["user_id"],
                "nickname": c["user_info"]["nickname"],
                "content": c["content"],
                "create_time": dt.strftime("%Y-%m-%d"),
                "like_count": int(c["like_count"]),
                "sub_count": int(c["sub_comment_count"]),
                }
                records.append(record)  # 修复：需要将 record 添加到列表中
    print(f'获取{html_path}的评论数据完成,共{len(records)}条评论数据')
    return records  # 返回包含所有评论记录的列表


def main():
#-----------toCsv部分-------------------------
    html_path="html_data_test"
    csv_path="csv_data_test"
    output_file_name="search_result_8000.csv"
    path=os.path.join(keyword,csv_path, output_file_name)
    os.makedirs(os.path.join(keyword,csv_path), exist_ok=True)
    comments=get_comment_data(html_path)
    df = pd.DataFrame(comments)
    df.to_csv(path, index=False)
    print(f'将{html_path}的评论数据保存到{path}')
    print(f'评论数据保存完成,共{len(comments)}条评论数据')
#----------------------------------------------
if __name__ == "__main__":
    main()