// dlltest.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"

#include <iostream>
#include "Platform.h"
#include <windows.h>
#include <fstream>
using namespace std;

#define DllExport __declspec(dllexport)

int PlayTime;

FILE *f;

extern "C" DllExport void Create(Environment *env)
{
	fopen_s(&f, "D:\\123.txt", "w");
}

extern "C" DllExport void Strategy(Environment *env)
{
	PlayTime++;

	env->home[0].velocityLeft = 0;
	env->home[0].velocityRight = 100;

	if (f != NULL) {
		for (int i = 0; i < 5; i++) {
			fprintf(f, "%lf %lf\n", env->home[i].pos.x, env->home[i].pos.y);
		}
		fprintf(f, "\n");
	}
}

extern "C" DllExport void Placement(Environment *env)
{
	//env->currentBall.pos.x = env->currentBall.pos.y = 233;
}

extern "C" DllExport void Destroy(Environment *env) { }
