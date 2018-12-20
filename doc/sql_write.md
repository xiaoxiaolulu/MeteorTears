# Mysql执行语句编写讲解

### 示例如下：
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


### 执行

```python
@test_data_runner
def channel_budget():
    pass
```

#### 返回结果如下
```python
[DEBUG] [2018-12-10 18:12:25,227] logger.py [line:136] : 操作的数据库表为 ====> Shopping
[DEBUG] [2018-12-10 18:12:25,233] logger.py [line:136] : 执行的SQL语句为 ===> SELECT id FROM shopping WHERE id='1' ORDER BY id DESC LIMIT 1
[DEBUG] [2018-12-10 18:12:25,234] logger.py [line:136] : 执行结果为 ===> 1
```
