### 2019-06-28
1. 对测试用例数据执行前进行预处理
```示例
测试用例分层结构：
    1.其中testapi目录不会执行
    2.api文件和csase文件调用
        a.testapi
            以$<params>$方式代表入参方式
            testapi: cases\testapi\api.yaml -> [一个yaml文件对应一个api]
            入参方式: parmas_kwargs:
                        user: tary.liu
                        psw: 123456
        b.testsuite 
            testcase: cases\testcaes\case.yaml -> [一个yaml文件对应一个case文件]
            suite一般调用正向的测试cases，通过组装不同的case形成不同的测试场景
    3. 最后处理完数据后无序加载测试容器，执行逻辑运行逻辑不变
        加载数据以[{filename: {casename: casebody}}, {filename: {casename: casebody}}]
            转化成py文件对应的数据：
                filename => 文件名&类名
                casename => 用例函数名
                casebody => 用例运行装饰器处理的测试数据,包含requestbody&断言等
                
cases----------------testapi
        |
        |------------testcases
        |
        |------------testsuites
```

### 2019-06-27
1. 优化lib.public.load_cases，对测试用例数据进行分类
```示例
a.用例之间的调用以testcases: cases\testcaes\login.yaml进行调用
b.被调用的测试用例以.py函数入参形式调用 status -> TODO
    parmas_kwargs: 
        - username: tracy.liu
        - password: 546464628
    
    传统形式：<封装固定方法进行调用>
        def login(username, password):
            res = request.post(host, {user: username, psw: password}, headers)
            self.assertEqual(res.status_code: 200)
            self.assertEqual(res.json()[user], username)
    
     cases---------testcases
            |
            |------testsuites
```


### 2019-06-26
1. 修复lib.utils.recording._params(filepath)录制Get类型接口
```示例
coupon:
    assert:
        status_code: 200
    description: coupon
    headers:
        Accept: application/json;version=3.0;compress=false
        Accept-Encoding: gzip
        Connection: Keep-Alive
        Content-Type: application/json; charset=utf-8
        Host: test2-appserver.atzc.com:7065
        User-Agent: Autoyol_99:Android_27|91AB99D0EDA542DCC966AABD2A0C5BB8D30A34D40031FF9E3B9F1CA3BF
        X-Tingyun-Id: YfYbInNBhKA;c=2;r=1295516226;u=24e923be2321c04dc7b49754eae43b7f::839528A9D7D98C34
    method: GET
    relevant_parameter: []
    relevant_sql: []
    res_index: []
    skip: false
    timeout: 8
    url: https://test2-appserver.atzc.com:7065/v40/disCoupon/own?pageSize=10&pageNum=1&token=61527c61c92946d58fe1b0934e84613f&status=1&OS=ANDROID&OsVersion=27&AppVersion=99&IMEI=861438046958534&mac=B40FB38790F3&androidID=7ccde31ec3ec4990&PublicLongitude=121.409244&PublicLatitude=31.172197&publicCityCode=021&appName=atzucheApp&deviceName=V1816A&publicToken=61527c61c92946d58fe1b0934e84613f&AppChannelId=testmarket&AndroidId=7ccde31ec3ec4990&requestId=B40FB38790F31561518520965&mem_no=819209698
```

### TODO V2.5.0 测试平台前后端分离开发
1. 在已有模块完善的情况下，进行前后端分离开发


### TODO V2.0.0 测试平台，之前脚本框架稳健无特大问题的情况下研发
1. 初步使用Flask进行研发, 前后端混合开发, 初期版本只包含接口部分


### TODO V1.6.0 mock
1. 完善mock机制，使用Flask，用上下文管理器，对Json的mock文件进行mock接口服务
2. mock文件格式待构思
3. 理论上Restful，支持POST, GET, DEL, PUT等类型接口


### TODO V1.5.5  接口单接口性能待补充
1. 接口单接口测试模板类构思及完成 -> templates.locust_func, templates.locust_header, templates.locust_load_attr
2. 接口单接口测试用例编写格式模式构思及完成
3. 接口性能与接口测试用例运行方式，并行 or 单独执行， 是否使用分布式待观察
4. 测试报告Response 与 assert 部分内容颜色标记
5. 接口性能报告使用Jinjia2模板引擎渲染
6. 优化项目代码以及潜在问题


### 2019-06-25
1. 接口录制模块完善, del老版code, 新增Recording module 
```示例(注意事项逻辑未必稳定，待进一步测试)
python recording.py --r=C:\Users\56464\Desktop\Untitled.har --n=test --p=C:\Users\56464\Desktop\MeteorTears

参数：
    --r 抓包工具保存下来的录制文件路径
    --n 生成测试用例名称命名
    --p 生成测试用例保存文件路径
```


### 2019-06-24
1. 优化临时文件目录结构
```示例
现在分四层
variables---------config_params         (Host等常量配置文件目录)
            |
            |-----extract_params        (接口提取参数保存文件目录)
            |
            |-----interface_params      (Data/Json等接口参数保存文件目录)
            |
            |-----random_params         (随机参数变量保存文件目录)
```
2. setUp & tearDown涉及负责多条数据处理时，使用EnvironClean模块进行函数编程，再在yamlCase中调用数据处理函数
```示例
EnvironPreparation:
    setUp: EnvironClean.marketing_partner_operation()
```


### 2019-06-20
1. 优化wraps.cases_runner逻辑，现支持临时变量文件中的变量替换
2. 针对用例存在耦合的情况，以临时变量文件的方式继承api请求文件，以确保无论用例执行顺序如何，都能单独运行
```示例
test_api_setup001:
  relevant_parameter: [login]
  description: "member_extend_case001"
  cases: ${login}$
# Response返回体提取的参数
  res_index: [token]
```


### 2019-06-13
1. 加入Response文本对比功能，关键词json_diff
2. 优化邮件模板，新增现有测试用例统计元素
3. 优化部分文件注释
```示例
  json_diff:
    {
      "status_code": 200,
      "response_body": {
        "data": {
          "disCouponList": [
          {
            "id": "466667",
            "disName": "我不知道",
            "endDate": "2019-06-30 00:00",
            "description": "1. 满100000000减2000\n2. 有效期：2019.06.12-2019.06.30\n3. 仅抵扣租金",
            "overlaidType": "0",
            "status": "1",
            "isFirstLimit": "0",
            "showPreferential": "￥2000"
          },
          {
            "id": "466665",
            "disName": "12",
            "endDate": "2019-06-30 00:00",
            "description": "1. 满1000减200\n2. 有效期：2019.06.11-2019.06.30\n3. 仅抵扣租金",
            "overlaidType": "0",
            "status": "1",
            "isFirstLimit": "0",
            "showPreferential": "￥200"
          }
          ],
          "count": "2",
          "totalPage": "1"
        },
        "resCode": "000000",
        "resMsg": "success"
      }
    }
```


### 2019-06-12
1. 报告失败重跑htmlReport, 暂时不稳定，请暂时使用HtmlReport_back
2. 优化多层嵌套字典中存在相同Key取值的逻辑断言, 以.分割
```示例
  assert_same_key:
    disCouponList.0.showPreferential: "￥2000"
```


### 2019-06-06
1. 优化报告逻辑，新增失败重跑功能


### 2019-06-02
1. 项目结构目录调整
2. 优化Response返回结构体


### 2019-05-17
1. 优化email模板，新增测试数据统计功能
2. 优化用例格式，新增前后置条件编写


### 2019-05-16
1. 新增自动生成随机测试数据功能


### 2019-05-14
1. 新增用例跳过功能


### 2019-05-13
1. 更新断言逻辑，新增断言Response指定字段长度
2. 更新落库校验逻辑，支持多字段断言
3. 更新部分文档


### 2019-05-09
1. 修复部分参数文件&配置文件错误
2. 重构部分代码
3. 数据库操作由Mysql改为Sqlserver
4. 增加数据落库校验
5. SQL语句使用Yaml文件编写
6. TODO 代码与校验逻辑待优化，暂只支持一个字段的落库校验


### 2019-03-27
1.完成关联参数配置


### 2019-03-22
1.用例管理文件格式变更为Yaml  json.load =》yaml.load，方便contextor更优雅的实现传参方式
2.添加res_index方便动态传参，保存入临时变量文件(用例执行完自动回溯)
```text
用例中的变量名以{临时变量文件名}的方式书写
1. 用例编写文件目录cases，生成临时yaml用例文件目录caseAll, test_cases根据caseAll自动生成py用例文件，并执行
```

### 2018-12-26
1. 搭建travis-ci + coveralls
2. 使用 coverage
3. setup.py done


### 2018-12-24
1. 修改CustomRules文件代码,使Fiddler能自动保存会话进指定的目录
2. 分析录制接口文件并生成新的request的对象
3. 生成录制接口的用例数据对象, 运行逻辑采用之前的手动编写用例规则
4. 完成V1.3.0 TODO， 接口性能与用例模型待补充


### 2018-12-14
1. 完成Email模板，样式已调试完毕
2. 用例基本可跑批 
3. 查看项目代码, 使用FIXME对待完善代码就行标签注释(共计14个TODO) status -> 代码风格保持一致性，部分代码待优化美观


### V1.3.0 TODO
1. 对Fiddler进行改造使之能够完成接口录制功能，python对录制接口分析并自动运行 status -> done 逻辑变更，老版代码回溯删除


### V1.2.0 TODO
1. 使用locust库二次开发，完成接口性能测试 status -> 待研发


### V1.1.0 TODO
1. 测试模型设计并编写完毕 status -> done
2. 服务器部署, 接入Jenkins, 持续集成 status -> done


### V1.0.0 TODO
1. 项目配置层代码优化, 当前代码过于繁琐复杂 status -> done
2. 测试用例的校验器设计[Response结构体分析->返回数据类型 code等多重断言] status -> done
3. 测试模板的重新定义, 使之功能更为全面 status -> done
4. 测试阶段，编写用例测试，框架逻辑是否有所遗漏 status -> done
5. 第一版本基本用例编写功能完成 status -> done
6. 后期完善之前老代码，重构告警机制代码 status ->done


### 2018-12-13
1. 完成用例的基本运行编写
2. 生成测试报告
3. 检查当前所有代码是否符合PEP8代码规范标准


### 2018-12-12
1. 测试模板设计与编写
2. 用例生成主体逻辑
3. Json文件用例编写设计
4. Https/Http关键字模块编写
5. 代码PEP8编码规范检查并修改


### 2018-12-11 以前的日志忘写了,写一下现阶段完成的Modules
1. Xml配置文件类, 配置层基本完成
2. Mysql操作类(本次使用Yaml文件管理数据操作), 包含一个装饰器, 业务数据层基本完成
3. 数据安全模式, 一个简单加密解密类
4. fp文件操作采用以前的代码
5. Excel操作类, 支持动态参数, 沿用先前的代码
6. 多层嵌套Json解析操作类
7. 日志操作类, 依旧沿用以前的代码
8. 时间日期方法, 沿用先前代码
9. 完善了代码风格与注释
10. 明确了代码的基本分层与风格
