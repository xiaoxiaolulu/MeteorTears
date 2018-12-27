### Meteor tears

[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/xiaoxiaolulu/MeteorTears/blob/master/LICENSE) [![python version](https://img.shields.io/badge/python-3.4%7C3.5%7C3.6%7C3.7-blue.svg)](https://pypi.org/project/MeteorTears/)


Meteor tears 一款基于python-request通过Json格式文件管理用例的接口测试工具


### 用例编写(Json文件管理)
key | value | example
------------ | -------------| ----------------
url | 请求接口路由 | /admin/compaign/export
method | 请求方式 | GET
params | url地址参数 | ?channelId=123importId=456
data | 请求数据 | {"name": "SEMAUTO", "categoryId": $arguments, "enabled": 1}
file | 上传文件数据 | {file=operate_excel.save_excel(file=os.path.join(parameters.make_directory('Data', 0), 'excel\compaign_template.xlsx'),data_index=0,excel_key='落地页编号',excel_name='compaign_template_副本.xlsx')}
json | Json类型请求 | {"name": "SEMAUTO", "categoryId": $arguments, "enabled": 1}
headers | 请求头 | {'Authorization': 'eyJ0eXAiOiJK', 'Content-Type': 'application/json'} 
assert | 结果断言 | {"username": "NULL", "password": "123456", "auth_code": ['len': 4]}
responseType | 验证断言结果的数据类型 | {'Response': ['username'：'str']}
description | 用例描述 | "新增渠道"
jsonDiff | 返回结果自动对比 | {"code":0,"message":"操作成功","data":""}


### Mysql执行语句编写讲解
```yaml
- ChannelBudget:
    action: SELECT
    execSQL:
      - table: shopping
      - columns: ['id']
      - params: id='1'
      - desc: ORDER BY id DESC LIMIT 1
    except:
      - is_table: 0
      - message: You have an error in your SQL syntax
```

key | value | Sample
------------ | -------------| ----------------
action| sql执行操作类 | SELECT/DELETE/INSERT/UPDATE等   
table| 数据库表 | channel_budget
columns| 列名 | ['channel_id'] 列表类型，支持多个值
params| 检索条件 | id='1'
desc| 排序 | ORDER BY ID DESC LIMIT 1


### 接口录制V1.0.0
```text
File -》Save -》  (a) All sessions  以saz格式文件保存所有会话 
                 (b) Selected Sessions 保存选择的会话
                            1. in ArchiveZIP ：保存为saz文件
                            2. in ArchiveZIP ：保存为saz文件
                            3. as Text (Headers only) ：仅保存头部
                 (c) Request 保存请求
                            1. Entir Request:保存整个请求信息（headers和body）
                            2. Request Body:只保存请求body部分
                 (d) Response 保存请求返回
                            1. Request Body:只保存请求body部分
                            2. Response Body:只保存返回body部分
                            3. Response Body:只保存返回body部分

返回Response结构体乱码
        点击decode 
```

#### 接口回放
1. File -》Load Archive 导入saz文件
2. Ctr + A 选择全部接口
3. 点击Replay按钮, 批量请求


#### 修改CustomRules文件
1. 找到OnBeforeResponse方法
2. 添加如下代码
```javascript
        oSession.utilDecodeResponse();
        var now = new Date();
        var ts = now.getTime();
        var filename =  'F:/MeteorTears/WorkFlow/' + ts + '_' + oSession.id + '.yaml';
        var curDate = new Date();
        var logContent = "Request url: " + oSession.url + "\r\nRequest header: " + oSession.oRequest.headers +  "\r\nRequest body: " + oSession.GetRequestBodyAsString() + "\r\nResponse code: " + oSession.responseCode + "\r\nResponse body: " + oSession.GetResponseBodyAsString() + "\r\n";
        var sw : System.IO.StreamWriter;
        if (System.IO.File.Exists(filename)){
            sw = System.IO.File.AppendText(filename);
            sw.Write(logContent);
        }
        else{
            sw = System.IO.File.CreateText(filename);
            sw.Write(logContent);
        }
        sw.Close();
        sw.Dispose();
```
3. C:\Users\56464\Documents\Fiddler2\Scripts\目录下最好先备份原文件,并命名CustomRulesBack.js
4. 录制的原始接口信息会保存在/WorkFlow/目录下
5. 录制完的接口为JSON格式文件, load_fiddler_files.py分析并生成新的迭代对象, create_workFlow_obj.py将生成新的Json格式用例文件,

--------------

欢迎交流   QQ: 546464268(Null)