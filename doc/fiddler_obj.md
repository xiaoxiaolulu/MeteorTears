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


### CustomRules文件(接口录制V.1.0.0)
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


### 注意事项
录制的接口采用不同的文件管理用例,  同时在不同的case层进行遍历, 但运行逻辑与报告生成方式与手动编写用例同
