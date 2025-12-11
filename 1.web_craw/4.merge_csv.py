import os
import pandas as pd
path="web_craw/csv_data"
keyword="机械革命"
#获取所有csv文件
csv_files=os.listdir(path)
#读取所有csv文件
#合并所有csv文件
df=pd.concat([pd.read_csv(os.path.join(path,csv_file)) for csv_file in csv_files])
#保存合并后的csv文件
df.to_csv(os.path.join(path,keyword,"merged.csv"),index=False)
print("合并后的csv文件保存成功")