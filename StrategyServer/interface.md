# 策略服务器v1.1
此版本策略服务器支持多次使用。策略服务器进程在加载一个dll策略之后，支持释放掉该dll，并重新在此进程中加载一个dll，避免了平台每次加载策略都需要等待策略服务器长时间的启动。
### remarks
- 策略服务器可能崩溃，之后需要重新启动
- 在命令行参数中可以指定策略服务器的日志文件以及日志级别

## 通讯协议
服务器（*策略服务器*）与客户端（*比如模拟平台*）之间的通讯，传输层上使用UDP协议，并使用UTF8编码的Json对象作为数据的载体。

基本的数据格式如下

```json
{
    "type": {str},
    "data": {dataobject}
}
```
每个如上的`json`对象称为一个`Message（消息）对象`，其中：
- `type`字段表示消息类型，均为字符串类型；
- `data`字段表示消息附带的数据，目前[所支持的对象类型](#数据对象的类型)见下；
- 任何数据必须有`type`字段，而`data`字段为可选字段；

每次独立的请求以客户端发起，并以服务器的回应结束。如果服务器没有需要回应的数据，则回应`fin`消息；如果发生错误，则回应`error`消息。

### 目前已定义的消息类型包括：

| 消息类型 | 描述 |data对象类型|能否作为请求？|
| :--- | :----- | ------ | ------ |
|true|逻辑真|null|N|
|false|逻辑假|null|N|
|wheelinfo|包含轮速信息|wheelinfo|N|
|placementinfo|包含摆位信息|placementinfo|N|
|ping|ping消息，等待对端的pong消息|null|Y|
|pong|pong消息，作为对对端ping消息的回应|null|N|
|load|加载dll策略|file|Y|
|free|释放当前策略|null|Y|
|create|调用dll中`Create`函数，带有环境信息|env|Y|
|strategy|调用dll中`Strategy`函数，带有环境信息|env|Y|
|placement|调用dll中`Formation`函数，带有环境信息|env|Y|
|destroy|调用dll中`Destroy`函数，带有环境信息|env|Y|
|exit|退出策略服务器|null|Y|
|error|错误|error|N|
|fin|本次请求无错误完成|null|N|

在上表中，

- `消息类型`列指`Message对象`中的`type`字段的值，均为小写；
- `能否作为请求？`表示该消息类型能否作为请求主动发起。为`N`表示该消息一般作为对一个请求的返回消息，而不表示主动发起动作；
- `data对象类型`的定义如下

### 数据对象的类型

- **null**

  该类型为空类型，字段为`null`则可以不存在；

- **file**

  ```json
  {
      "filename": {str}
  }
  ```

  表示一个文件，可以包含相对路径或绝对路径

- **vector3d**

  ```json
  {
      "x": {float},
      "y": {float},
      "z": {float}
  }
  ```

  表示一个三维向量

- **robot**

  ```json
  {
      "pos": {vector3d},
      "rotation": {float},
      "velocityLeft": {float},
      "velocityRight": {float}
  }
  ```

  表示一个己方机器人

- **opp_robot**

  ```json
  {
      "pos": {vector},
      "rotation": {float}
  }
  ```

  表示一个敌方机器人

- **ball**

  ```json
  {
      "pos": {vector3d}
  }
  ```

  表示一个球

- **env**

  ```json
  {
      "home": []{robot[5]},
      "opp": []{opp_robot[5]},
      "currentBall": {ball},
      "gameState": {int},
      "whosBall": {int}
  }
  ```

  表示一个场地环境信息

- **wheel**

  ```json
  {
      "velocityLeft": {float},
      "velocityRight": {float}
  }
  ```

  表示一个机器人的轮速信息

- **wheelinfo**

  ```json
  {
      "wheels": []{wheel[5]}
  }
  ```

  表示一组机器人的轮速信息

- **placement**

  ```json
  {
      "robot": []{robot[5]},
      "ball": {ball}
  }
  ```

  表示一个摆位的状态信息

- **error**

  ```json
  {
      "errcode": {int},
      "errdesc": {string}
  }
  ```

------

## TODO
- [ ] 数据流加密
