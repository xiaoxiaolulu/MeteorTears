#### 用例编写(Yaml文件管理)
```yaml
test_get_public_key:
  # 上下游关联的参数文件名
  relevant_parameter: [Host]
  # 此接口落库的sql语句
  relevant_sql: search_all_tenant_conf
  # 测试用例名称
  description: "获取公钥"
  # 请求方式
  method: get
  # 请求路由
  url: ${Host}$/api/auth/getpublickey
  # 接口断言
  assert:
    Code: 1
  # 提取测试接口Response返回参数
  res_index: [RsaPublicKey, Key]
  # 落库校验
  check_db:
    TenantName: TESTRLBC
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


##### 关于断言
1. 多层结果断言, 以键值对的方式写入， 断言的Key: 预期的Value
2. 返回体数据类型断言，整体返回提ResponseType：[type, dict], 断言某个Key的类型 Key: [type, str]
3. 返回结果长度断言, Key: [len, 36]
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
```
