# 目录

<!-- TOC -->

- [1. 用户手册](#1-用户手册)
    - [1.1. 启动与退出](#11-启动与退出)
    - [1.2. 加载策略](#12-加载策略)
    - [1.3. 比赛](#13-比赛)
    - [1.4. 回放](#14-回放)
    - [1.5. 设置](#15-设置)
    - [1.6. 更多信息](#16-更多信息)
- [2. 策略服务器](#2-策略服务器)
    - [2.0. remarks](#20-remarks)
    - [2.1. 通讯协议](#21-通讯协议)
        - [2.1.1. 目前已定义的消息类型包括：](#211-目前已定义的消息类型包括)
        - [2.1.2. 数据对象的类型](#212-数据对象的类型)
    - [2.2. TODO](#22-todo)
- [3. Referee](#3-referee)
    - [3.1. Interface](#31-interface)
    - [3.2. FIRA Middle League MiroSot Game Rules](#32-fira-middle-league-mirosot-game-rules)
        - [Law 1 : The Field and the Ball](#law-1--the-field-and-the-ball)
        - [Law 2 : The Players](#law-2--the-players)
        - [Laws 3 & 4](#laws-3--4)
        - [Law 5 : Game Duration](#law-5--game-duration)
        - [Law 6 : Game Commencement](#law-6--game-commencement)
        - [Law 7 : Method of Scoring](#law-7--method-of-scoring)
        - [Law 8 : Fouls](#law-8--fouls)
        - [Law 9 : Play Interruptions](#law-9--play-interruptions)
        - [Law 10 : Free Kick](#law-10--free-kick)
        - [Law 11 : Penalty-Kick](#law-11--penalty-kick)
        - [Law 12 : Goal Kick](#law-12--goal-kick)
        - [Law 13 : Free-Ball](#law-13--free-ball)

<!-- /TOC -->

# 1. 用户手册

感谢使用 **SimuSot5v5 v3.0**。本文档将帮助你学会使用平台。

## 1.1. 启动与退出

安装程序后，双击快捷方式启动程序，弹出主界面。

在主界面中，点击 `Exit` 退出程序。

## 1.2. 加载策略

在主界面中，点击 `Settings` ，设置界面上方有蓝色的`Blue`标签和黄色的`Yellow`标签。在 `Blue`后的文本框中输入蓝方策略名，在 `Yellow`后的文本框中输入黄方策略名（例如：如果你是蓝方，你的策略是 *Strategy.dll*，在 `Blue`后的文本框中输入 *Strategy.dll*），点击`Load` 。

## 1.3. 比赛

在主界面中，点击 `Game`开始正式比赛。

记分牌在比赛界面的右下角。

鼠标左键暂停/继续比赛

鼠标右键或按下`Esc`键暂停比赛，进入比赛菜单。在比赛菜单中，点击`Exit` 返回主界面，点击`Replay`进入回放界面，点击`Resume`返回比赛。 你也可以选择再次点击鼠标右键或按下`Esc`键返回比赛。

## 1.4. 回放

回放界面回放你上一次退出回放到这一次进入回放的比赛过程。

回访进度条在比赛场地下方，并显示`当前拍数/总拍数`。你可以通过拖动进度条调节回放的位置。

你也可以选择自动回放。点击`播放/暂停`控制自动回放。

正放时，点击一次`快进` 播放速度加快为2倍，点击一次`快退` 播放速度减慢为0.5倍。最大播放速度是8倍速。以最慢速正放，点击一次`快退` 变为倒放。

倒放时，点击一次`快进` 播放速度减慢为0.5倍，点击一次`快进` 播放速度加快为2倍。最大播放速度是8倍速。以最慢速倒放，点击一次`快进` 变为正放。

如果你想恢复原始回放状态，点击`播放/暂停`，回到单倍速正放。

按下`Esc`键暂停回放，进入回放菜单。在回放菜单中，点击`Exit` 返回主界面，点击`Back to Game`进入比赛界面，点击`Resume`返回回放。 你也可以选择再次按下`Esc`键返回回放。

## 1.5. 设置

在主界面中，点击 `Settings`进入设置界面。

## 1.6. 更多信息

我们会努力解决你的更多疑问。请通过以下方式联系我们：

- 主页： npu5v5.cn
- 邮件： <npu5v5@163.com>

**SimuSot5v5**将因为你的建议变得更好。


# 2. 策略服务器
 此版本策略服务器支持多次使用。策略服务器进程在加载一个dll策略之后，支持释放掉该dll，并重新在此进程中加载一个dll，避免了平台每次加载策略都需要等待策略服务器长时间的启动。
### 2.0.1. remarks
- 策略服务器可能崩溃，之后需要重新启动
- 在命令行参数中可以指定策略服务器的日志文件以及日志级别

## 2.1. 通讯协议
 服务器（*策略服务器*）与客户端（*比如模拟平台*）之间的通讯，传输层上使用UDP/TCP协议，并使用UTF8编码的Json对象作为数据的载体。

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

### 2.1.1. 目前已定义的消息类型包括：

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

### 2.1.2. 数据对象的类型

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

## 2.2. TODO
- [ ] 数据流加密




# 3. Referee
- This is the computer referee module for judging the ongoing situations.
- 
## 3.1. Interface
- Environment
    - This is a parameter used in all DLL interface.
        ``` c++
        typedef struct
        {
            Robot[] home;
            OpponentRobot[] opp;
            Ball currentBall;
            int gameState;
            int whosBall;
        } Environment;
        ```
    - Implement of Robot
        ``` c++
        typedef struct
        {
            Vector3D pos;
            double rotation;
            double velocityLeft;
            double velocityRight;
        } Robot;
        ```
    - Implement of OpponentRobot
        ``` c++
        typedef struct
        {
            Vector3D pos;
            double rotation;
        } OpponentRobot;
        ```
    - Implement of Ball
        ``` c++
        typedef struct
        {
            Vector3D pos;
        } Ball;
        ```
    - Implement of Vector3D
        ``` c++
        typedef struct
        {
            float x;
            float y;
            float z;
        } Vector3D;
        ```
    - Implement of GameState
        - Change only when the referee judges a goal or foul.
        - GameState can have 6 values.
            - 0 = Normal Match
            - 1 = Free Ball Top
            - 2 = Free Ball Bottom
            - 3 = Place Kick
            - 4 = Plenalty kick
            - 5 = Goal kick
    - Implement of WhosBall
        - Change only when the referee judges a goal or foul.
        - WhosBall can have 2 values.
            - 0 = Blue team is Offensive side.
            - 1 = Yellow team is Offensive side.
- Create
    - Called when the DLL is first loaded.
    - DLL interface
        ``` c++
        extern "C" __declspec(dllexport) void Create ( Environment *env )
        ```
- Destory
    - Called when the DLL is released.
    - DLL interface
        ``` c++
        extern "C" __declspec(dllexport) void Destroy ( Environment *env )
        ```
- Strategy
    - Platform running a shot called once.
    - DLL interface
        ``` c++
        extern "C" __declspec(dllexport) void Strategy ( Environment *env )
        ```
- Placement
    - When a goal or foul is made, the game will be paused and placed, and than the function will be called once.
    - DLL interface
        ``` c++
        extern "C" __declspec(dllexport) void Placement ( Environment *env )
        ```


## 3.2. FIRA Middle League MiroSot Game Rules
- These rules have been taken from the Mirosot rules for Robot Soccer. They have been re-printed under the acceptable usage for educational purposes clause.

### 3.2.1. Law 1 : The Field and the Ball
1. Playground dimensions

    > A black (non-reflective) wooden rectangular playground 220cm X 180cm in size with 5cm high and 2.5cm thick white side-walls will be used. The topsides of the side-walls shall be black in color with the walls painted in white (side view). Solid 7cm X 7cm isosceles triangles shall be fixed at the four corners of the playground to avoid the ball getting cornered. The surface texture of the board will be that of a ping pong table.

2. Markings on the playground (Appendix 1)

    > The field of play shall be marked as shown in Appendix 1. The center circle will have a radius of 25cm.

    > The arc, which is part of the penalty area, will be 25cm along the goal line and 5cm perpendicular to it.

    > The major lines/arcs (centerline, goal area borderlines and the center circle) will be white in color and 3mm in thick. The free ball (Law 13) robot positions (circles) shall be marked in gray color.

3. The goal

    > The goal shall be 40cm wide. Posts and nets shall not be provided at the goal.

4. The goal line and goal area

    > The goal line is the line just in front of the goal, which is 40cm long.

    > The goal areas (The region A of Appendix 1) shall comprise of the area contained by the rectangle (sized 50cm X 15cm in front of the goal).

5. The penalty area

    > The penalty areas (The region B of Appendix 1) shall comprise of areas contained by the rectangle (sized 80cm X 35cm in front of the goal) and the attached arc (25cm in parallel to the goal line and 5cm perpendicular to it).

6. The ball

    > An orange golf ball shall be used as the ball, with 42.7mm diameter and 46g weight.

7. The filed location

    > The field shall be indoors.

8. The lighting condition

    > The lighting condition in the competition site shall be fixed around 1,000 Lux.

### 3.2.2. Law 2 : The Players
1. The overall system

    > A match shall be played by two teams, each consisting of five robots. One of the robots can be the goalkeeper (Law 2.(b).2). Three human team members, a "manager", a "coach" and a "trainer" shall only be allowed on stage.

2. The robots

    1. The size of each robot shall be limited to 7.5cm X 7.5cm X 7.5cm. The height of the RF communication antenna will not be considered in deciding a robot's size.

        - The topside of a robot must not be colored in orange. A color patch either blue or yellow, as assigned by the organizers, will identify the robots in a team. All the robots must have (at least) a 3.5cm X 3.5cm solid region of their team color patch, blue or yellow, visible on their top. A team's identification color will change from game to game, and the team color patch used should be detachable. When assigned with one of the 2-team colors (blue or yellow), the robots must not have any visible patches of those colors used by an opponent team.

        > Note : The teams are recommended to prepare a minimum of 10 different color patches, other than blue and yellow, for individual robot identification

        - To enable infrared sensing a robot's sides should be colored light, except at regions necessarily used for robot functionality, such as those for sensors, wheels and the ball catching mechanism. The robots should wear uniforms and the size of which shall be limited to 8cm X 8cm X 8cm.

    2. A robot within its own goal area (Law 1.(d).) shall be considered as the "goalkeeper". The goalkeeper robot shall be allowed to catch or hold the ball only when it is inside its own goal area or penalty area.

    3. Each robot must be fully independent, with powering and motoring mechanisms self-contained. Only wireless communication shall be allowed for all kinds of interactions between the host computer and a robot.

    4. The robots are allowed to equip with arms, legs, etc., but they must comply with the size restrictions (Law 2.(b).1) even after the appendages fully expanded. None of the robots, except the single designated goalkeeper, shall be allowed to catch or hold the ball such that more than 30% of the ball is out of view either from the top or from the sides (Appendix 2).

    5. While a match is in progress, at any time the referee whistles the human operator should stop all robots using the communication between the robots and the host computer.

3. Substitutions

    > Two substitutes shall be permitted while a game is in progress. At half time, unlimited substitutions can be made. When a substitution is desired while the game is in progress, the concerned team manager should call 'time-out' to notify the referee, and the referee will stop the game at an appropriate moment. The game will restart, with all the robots and the ball placed at the same positions as they were occupying at the time of interrupting the game.

4. Time-out

    > The human operator can call for 'time-out' to notify the referee. Each team will be entitled for two time-outs in a game and each shall be of 2 minutes duration.

### 3.2.3. Laws 3 & 4 
 Laws 3 & 4 have been omitted due to their covering of the computer system information that can control the physical robots and the vision system that is used for the physical robots.

### 3.2.4. Law 5 : Game Duration
1. The duration of a game shall be two equal periods of 5 minutes each, with a half time interval for 10 minutes. An official timekeeper will pause the clock during substitutions, while transporting an injured robot from the field, during time-out and during such situations that deem to be right as per the discretion of the timekeeper.

2. If a team is not ready to resume the game after the half time, additional 5 minutes shall be allowed. Even after the allowed additional time if such a team is not ready to continue the game, that team will be disqualified from the game.

### 3.2.5. Law 6 : Game Commencement
1. Before the commencement of a game, either the team color (blue/yellow) or the ball shall be decided by the toss of a coin. The team that wins the toss shall be allowed to choose either their robot's identification color (blue/yellow) or the ball. The team who receives the ball shall be allowed to opt for their carrier frequency band as well.

2. At the commencement of the game, the attacking team will be allowed to position their robots freely in their own area and within the center circle. Then the defending team can place their robots freely in their own area except within the center circle.

 At the beginning of the first and second halves, and after a goal has been scored, the ball should be kept within the center circle and the ball should be kicked or passed towards the team's own side. With a signal from the referee, the game shall be started and all robots may move freely.

3. At the beginning of the game or after a goal has been scored, the game shall be commenced/continued, with the positions of the robots as described in Law 6.2.

4. After the half time, the teams have to change their sides.

### 3.2.6. Law 7 : Method of Scoring
1. The winner

    > A goal shall be scored when the whole of the ball passes over the goal line. The winner of a game shall be decided on the basis of the number of goals scored.

2. The tiebreaker
    > In the event of a tie after the second half, the winner will be decided by the sudden death scheme. The game will be continued after a 5 minutes break, for a maximum period of three minutes. The team managing to score the first goal will be declared as the winner. If the tie persists even after the extra 3 minutes game, the winner shall be decided through penalty-kicks. Each team shall take three penalty-kicks, which differs from Law 11 as only a kicker and a goalkeeper shall be allowed on the playground. The goalkeeper should be kept within its goal area and the positions of the kicker and of the ball shall be the same as per the Law 11.  After the referee's whistle, the goalkeeper may come out of the goal area. In case of a tie even after the three-time penalty-kicks, additional penalty-kicks shall be allowed one-by-one, until the winner can be decided. All penalty-kicks shall be taken by a single robot and shall commence with the referee's whistle. A penalty-kick will be completed, when any one of the following happens:

    1. The goalkeeper catches the ball with its appendages (if any) in the goal area.

    2. The ball comes out of goal area.

    3. Thirty (30) seconds pass after the referee's whistle.

### 3.2.7. Law 8 : Fouls
 A foul will be called for in the following cases.

1. Colliding with a robot of the opposite team, either intentionally or otherwise: the referee will call such fouls that directly affect the play of the game or that appear to have potential to harm the opponent robot. When a defender robot intentionally pushes an opponent robot, a free kick will be given to the opposite team. It is permitted to push the ball and an opponent player backwards provided the pushing player is always in contact with the ball.

2. It is permitted to push the goalkeeper robot in the goal area, if the ball is between the pushing robot and the goalkeeper. However, pushing the goalkeeper into the goal along with the ball is not allowed. If an attacking robot pushes the goalkeeper along with the ball into the goal or when the opponent robot pushes the goalkeeper directly then the referee shall call goal kick as goalkeeper charging.

3. Attacking with more than one robot in the goal area of the opposite team shall be penalized by a goal kick to be taken by the team of the goalkeeper. A robot is considered to be in the goal area if it is more than 50% inside, as judged by the referee.

4. Defending with more than one robot in the goal area shall be penalized by a penalty-kick. (A robot is considered to be in the goal area if it is more than 50% inside, as judged by the referee.) An exception to this is the situation when the additional robot in the goal area in not there for defense or if it does not directly affect the play of the game. The referee shall judge the penalty-kick situation when the additional robot in the goal area is not there for defense or if it does not directly affect the play of the game. The referee shall judge the penalty-kick situation.

5. It is referred to as handling, as judged by the referee, when a robot other than the goalkeeper catches the ball. It is also considered as handling, if a robot firmly attaches itself to the ball such a way that no other robot is allowed to manipulate the ball.

6. The goalkeeper robot should kick out the ball from its goal area (Law 1.(d).) within 10 seconds. The failure to do so will be penalized by giving a penalty kick to the opposite team.

7. Giving a goal kick to the team of the goalkeeper will penalize the intentional blocking of a goalkeeper in its goal area.

8. Only the referee and one of the human members of a team (manager, coach or trainer) shall be allowed to touch the robots. The award of a penalty-kick shall penalize touching the robots without the referee's permission.

9. Defending with more than three robots in the penalty area shall be penalized by a penalty-kick. (A robot is considered to be in the goal area if it is more than 50% inside, as judged by the referee.)

### 3.2.8. Law 9 : Play Interruptions
 The play shall be interrupted and relocation of robots shall be done by a human operator, only when:

1. A robot has to be changed.

2. A robot has fallen in such a way as to block the goal.

3. A goal is scored or a foul occurs.

4. Referee calls goal kick (Law 12) or free-ball (Law 13).

### 3.2.9. Law 10 : Free Kick
 NULL

### 3.2.10. Law 11 : Penalty-Kick
 A penalty-kick will be called under the following situations.

1. Defending with more than one robot in a goal area (Law 8.4.).

2. Failure on the part of a goalkeeper to kick out the ball from its goal area within 10 seconds (Law 8.6.).

3. When any one of the human members touches the robots without the referee's permission, while the game is in progress (Law 8.8.).

4. Defending with more than three robots in a penalty area (Law 8.9.).

    > When the referee calls a penalty-kick, the ball will be placed at the relevant penalty kick position (PK) on the playground (Appendix 1). The robot taking the kick shall be placed behind the ball. While facing a penalty kick one of the sides of the goalkeeper must be in touch with the goal line. The goalkeeper may be oriented in any direction. Other robots shall be placed freely within the other side of the half-line, but the attacking team will get preference in positioning their robots. The game shall restart normally (all robots shall start moving freely) after the referee's whistle. The robot taking the penalty-kick may kick or dribble the ball.

### 3.2.11. Law 12 : Goal Kick
 A goal kick will be called under the following situations.

1. When an attacking robot pushes the goalkeeper in its goal area, the referee shall call goal kick as goalkeeper charging (Law 8.2.).

2. Attacking with more than one robot in the goal area of the opposite team shall be penalized by a goal kick to be taken by the opposite team (Law 8.3.).

3. When an opponent robot intentionally blocks the goalkeeper in its goal area (Law 8.7.).

4. When the goalkeeper catches the ball with its appendages (if any) in its own goal area.

5. When a stalemate occurs in the goal area for 10 seconds.

    > During goal kick only the goalkeeper will be allowed within the penalty area and the ball can be placed anywhere within the penalty area. Other robots of the team shall be placed outside the penalty area during goal kick. The attacking team will get preference in positioning their robots anywhere on the playground, but it must be as per Law 8.3. The defending team can then place its robots within their own side of the playground. The game shall restart with the referee's whistle.

### 3.2.12. Law 13 : Free-Ball
 Referee will call a free-ball when a stalemate occurs for 10 seconds outside the goal area.

 When a free-ball is called within any quarter of the playground, the ball will be placed at the relevant free ball position (FB) (Appendix 1). One robot per team will be placed at locations 25cm apart from the ball position in the longitudinal direction of the playground. Other robots (of both teams) can be placed freely outside the quarter where the free-ball is being called, but with the rule that, the defending team will get their preference in positioning their robots. The game shall resume when the referee gives the signal and all robots may then move freely.
