### Meteor tears

[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/xiaoxiaolulu/MeteorTears/blob/master/LICENSE) [![python version](https://img.shields.io/badge/python-3.4%7C3.5%7C3.6%7C3.7-blue.svg)](https://pypi.org/project/MeteorTears/) [![Build Status](https://travis-ci.org/xiaoxiaolulu/MeteorTears.svg?branch=master)](https://travis-ci.org/xiaoxiaolulu/MeteorTears) [![Coverage Status](https://coveralls.io/repos/github/xiaoxiaolulu/MeteorTears/badge.svg?branch=master)](https://coveralls.io/github/xiaoxiaolulu/MeteorTears?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/bfd93c4e2362409da23ee48826d1ad39)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xiaoxiaolulu/MeteorTears&amp;utm_campaign=Badge_Grade)


Meteor tears 一款基于python-request通过Yaml格式文件管理用例的接口测试工具


#### 项目特点如下
1.  数据管理使用Yaml文件
2.  用例编写使用Yaml文件
3.  支持上下游接口参数关联，提取
4.  接口Response返回体多字段, Type断言, len断言, 对比
5.  落库校验，支持多个字段
6.  接口录制功能(待完善)
7.  微信，邮件告警


#### 用例(示例)
```yaml
test_update_bot_baseinfo:
  relevant_parameter: [Host, Token]
  relevant_sql: [bot_profile, bot_prs]
  description: "更新机器人"
  method: post
  url: ${Host}$/api/admin/bot/botprofile/updatebotbaseinfo
  json:
    BotConfigId: 8e0b6707-bcc6-4c4c-b072-80b169003804
    Bot_Name: Null
    Bot_Gender: 女
    Bot_DayOfBirth: "2019-03-08"
    Bot_Constellation: 双鱼座
    Bot_BloodType: AB
    Bot_Birthplace: 上海-上海
    Bot_Height: 165
    Bot_Weight: 50
    Bot_Company: 骨灰级
    Bot_School: 上海有限公司
    ID: 273d8a2a-9b0e-4582-b13b-0a60f103f621
    CreateDate: ""
    UpdateDate: ""
    CreateUserId: ""
    CreateUserName: ""
    UpdateUserId": ""
    UpdateUserName: ""
  headers:
    Content-Type: application/json; charset=utf-8
    Access-Token: ${Token}$
  assert:
    Status: 1
    Data: true
  check_db:
    Bot_Name: test
    Bot_Constellation: 水瓶座
```
key                 | value               | example
------------------- | ------------------- | ----------------
url                 | 请求接口路由          | /admin/compaign/export
method              | 请求方式             | GET
params              | url地址参数          | channelId=123importId=456
data                | 请求数据             | {"name": "SEMAUTO", "categoryId": $arguments, "enabled": 1}
file                | 上传文件数据          | {file=operate_excel.save_excel(file=os.path.join(parameters.make_directory('Data', 0), 'excel\compaign_template.xlsx'),data_index=0,excel_key='落地页编号',excel_name='compaign_template_副本.xlsx')}
json                | Json类型请求         | {"name": "SEMAUTO", "categoryId": $arguments, "enabled": 1}
headers             | 请求头               | {'Authorization': 'eyJ0eXAiOiJK', 'Content-Type': 'application/json'}
timeout             | 超时时间             | timeout: 8
setUp               | 前置条件             | setUp: print('前置条件')
tearDown            | 后置条件             | tearDown: print('后置条件')
skip                | 用例跳过             | 布尔值False或者True 
assert              | 结果断言             | {"username": "NULL", "password": "123456", "auth_code": ['len', 4]}
responseType        | 验证断言结果的数据类型 | {'Response': ['type', 'dict']}
description         | 用例描述             | "新增渠道"
res_index           | 提取变量             | res_index: [RsaPublicKey, Key]
check_db            | 落库检查             |   check_db: {TenantName: TESTRLBC}
relevant_parameter  | 上下游接口关联参数     | relevant_parameter: [Host]
relevant_sql        |  需要检查的sql语句    | relevant_sql: search_all_tenant_conf
jsonDiff            | 接口自动对比          | jsonDiff: {Code:1, message: 成功}

##### 用例解耦
1. 继承临时Api文件进行用例场景组合
```text
test_api_setup001:
  relevant_parameter: [login]
  description: "member_extend_case001"
  cases: ${login}$
# Response返回体提取的参数
  res_index: [token]
```

##### 关于断言
1. 多层结果断言, 以键值对的方式写入， 断言的Key: 预期的Value
2. 返回体数据类型断言，整体返回提ResponseType：[type, dict], 断言某个Key的类型 Key: [type, str]
3. 返回结果长度断言, Key: [len, 36]
4. 断言中存在多层嵌套情况使用.进行分割取值，如：数组.索引.需要取值的key，若超出取值索引报IndexError
```text
assert: 
    code: 1
    username: Null
    password: 123456
    ResponseType: [
        type,
        dict]
    username: [
        type,
        str]
    password: [
        len,
        8]
assert_same_key:
    disCouponList.0.showPreferential: "￥200"
```

##### 落库校验
1. 用例头写入关联的sql文件 relevant_sql: [bot_profile, bot_prs]
```text
relevant_sql: [bot_profile, bot_prs]
check_db:
    Bot_Name: test
    Bot_Constellation: 水瓶座
```


#### Mysql执行语句编写
```yaml
- ChannelBudget:
    action: SELECT
    execSQL:
      - table: shopping
      - columns: ['id']
      - params: id='1'
      - desc: ORDER BY id DESC LIMIT 1
```

key          | value        | Sample
------------ | -------------| ----------------
action       | sql执行操作类 | SELECT/DELETE/INSERT/UPDATE等   
table        | 数据库表      | channel_budget
columns      | 列名          | ['channel_id'] 列表类型，支持多个值
params       | 检索条件      | id='1'
desc         | 排序          | ORDER BY ID DESC LIMIT 1


欢迎交流   QQ: 546464268(Null)
