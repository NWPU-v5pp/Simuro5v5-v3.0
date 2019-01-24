#pragma once
/*
 * 平台相关的基本信息，以及平台提供的数据结构
 */
const int PLAYERS_PER_SIDE = 5;

const long FREE_BALL = 1;
const long PLACE_KICK = 2;
const long PENALTY_KICK = 3;
const long FREE_KICK = 4;
const long GOAL_KICK = 5;

// whosBall
const long ANYONES_BALL = 0;
const long BLUE_BALL = 1;
const long YELLOW_BALL = 2;

// global variables
const double FTOP = 77.2392;
const double FBOT = 6.3730;
const double GTOPY = 49.6801;
const double GBOTY = 33.9320;
const double GRIGHT = 97.3632;
const double GLEFT = 2.8748;
const double FRIGHTX = 93.4259;
const double FLEFTX = 6.8118;

typedef struct {
    double x, y, z;// x 和 y 为坐标值
} Vector3D;

typedef struct {
    long left, right, top, bottom;
} Bounds;

typedef struct {
    Vector3D pos;// 机器人坐标
    double rotation;// 机器人方向角
    double velocityLeft, velocityRight;// 机器人左右轮速度
} Robot;

typedef struct {
    Vector3D pos;// 机器人的坐标位置
    double rotation;// 机器人当前的转角
} OpponentRobot;

typedef struct {
    Vector3D pos;  // 小球的坐标位置
} Ball;

typedef struct {
    Robot home[PLAYERS_PER_SIDE];        //我方机器人数组
    OpponentRobot opp[PLAYERS_PER_SIDE];//敌方机器人数组
    Ball currentBall;               //当前小球的位置
    int gameState;                        //当前比赛的状态
    int whosBall;                        //由谁控制球
} Environment;                        //环境信息
