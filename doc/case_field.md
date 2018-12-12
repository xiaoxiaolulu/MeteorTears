### 用例关键字对象设计
key | value |
------------ | -------------|
UrlField | 请求接口路由 | 
MethodField | 请求方式 | 
UrlParamsField | url地址参数 |
DataField | 请求数据 | 
FileField | 上传文件数据 | 
JsonField | Json类型请求 | 
HeadersField | 请求头 | 
AssertField | 结果断言 | 
ResponseTypeField | 验证断言结果的数据类型 | 
DescriptionField | 用例描述 | 
JsonDiffField | 返回结果自动对比 | 


### test_modules
所有测试用例模型都以类的形式写入lib/public/modules.py文件中
```python
from lib.public import case_field


class AddChannel(object):
    
    url = case_field.UrlField('/admin/channel/add')
    method = case_field.MethodField('POST')
    data = case_field.DataField({
      "name": "SEMAUTO1",
      "level": 1,
      "parentId": 0,
      "categoryId": 1,
      "enabled": 1,
      "enableCaptcha": 1
    })
    headers = case_field.HeadersField({
      "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiODg5MDIiLCJ1X21peCI6IiIsInVfbmFtZSI6ImhlbGxvIiwidV90aW1lIjoxNTQwNTM1MjYzfQ.eN8ozTkSzqxIbVq4Fa2AhvTZNjozpUP_Ad5XAw6xicI"
    })
    description = case_field.DescriptionField("添加渠道数据")
```


### 自动生成Json文件的测试用例数据
在项目根目录下执行以下命令(生成用例在cases/目录下)
```python
createJsonCase -a -r

...Json文件格式的测试用例数据生成完毕, 请前往cases/目录下查看
```
