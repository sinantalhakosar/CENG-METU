#ifndef __HELPER__H__
#define __HELPER__H__

#include <iostream>
#include <string>
#include <fstream>
#include <jpeglib.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

extern GLuint idProgramShader;
extern GLuint idFragmentShader;
extern GLuint idVertexShader;
extern GLuint idJpegTexture;
extern GLuint idJpegTexture1;

using namespace std;

void initShaders();

GLuint initVertexShader(const string& filename);

GLuint initFragmentShader(const string& filename);

bool readDataFromFile(const string& fileName, string &data);

void initTexture(char *filename,char *filename1,int *w, int *h,GLuint idProgramShader1);

#endif
