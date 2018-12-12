### 用例编写设计(Json文件管理)
key | value | example
------------ | -------------| ----------------
Url | 请求接口路由 | /admin/compaign/export
Method | 请求方式 | GET
UrlParams | url地址参数 | ?channelId=123importId=456
Data | 请求数据 | {"name": "SEMAUTO", "categoryId": $arguments, "enabled": 1}
File | 上传文件数据 | {file=operate_excel.save_excel(file=os.path.join(parameters.make_directory('Data', 0), 'excel\compaign_template.xlsx'),data_index=0,excel_key='落地页编号',excel_name='compaign_template_副本.xlsx')}
Json | Json类型请求 | {"name": "SEMAUTO", "categoryId": $arguments, "enabled": 1}
Headers | 请求头 | {'Authorization': 'eyJ0eXAiOiJK', 'Content-Type': 'application/json'} 
Assert | 结果断言 | {"username": "NULL", "password": "123456", "auth_code": ['len': 4]}
ResponseType | 验证断言结果的数据类型 | {'Response': ['username'：'str']
Description | 用例描述 | "新增渠道"
JsonDiff | 返回结果自动对比 | {"code":0,"message":"操作成功","data":""}