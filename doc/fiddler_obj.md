# 20181221 Created By Null
### Fiddler会话保存
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

### 接口回放
1. File -》Load Archive 导入saz文件
2. Ctr + A 选择全部接口
3. 点击Replay按钮, 批量请求


### 解析saz文件or 修改CustomRules.js文件(构思与思考)
1. 解析saz文件  再批量分析接口 (待晚上和大佬讨论)
2. 改造CustomRules.js 文件批量保存txt文件，再批量分析
3. 关于Fiddler接口分析
```text
1. 去除非测试项目接口, 正则匹配
2. 接口去重判断

--- 进阶
1. 爬虫遍历保存的项目接口文档与Fiddler接口文档做diff差异化对比
```