#include <ostream>
#include "helper.h"
#include <glm/glm.hpp>
#include <glm/ext.hpp>
#include <glm/gtx/rotate_vector.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/transform.hpp>


#define SPEEDSTEP 0.25f
#define HEIGHTFACTORSTEP 0.5f
#define PITCHSTEP 0.05f
#define YAWSTEP 0.05f
#define LIGHTSTEP 5.0f

static GLFWwindow *win = NULL;

GLFWvidmode *mode;
const GLFWmonitor *monitor;
bool isFullScreen = false;

GLuint idProgramShader;
GLuint idFragmentShader;
GLuint idVertexShader;
GLuint idJpegTexture;
GLuint idJpegTexture1;

int widthTexture, heightTexture;
int imagePlaneWidth, imagePlaneHeight;
int imagePlaneWidthL, imagePlaneHeightL;

static void errorCallback(int error, const char *description) {
    fprintf(stderr, "Error: %s\n", description);
}

class FlatEarth {
public:
    glm::vec3 position;
    glm::vec3 upVector;
    glm::vec3 gazeVector;
    glm::vec3 leftVector;
    glm::vec4 lightPosition ;
    glm::mat4 modelMatrix;
    glm::mat4 viewMatrix;
    glm::mat4 projectionMatrix;
    glm::mat4 modelView;
    glm::mat4 modelViewProjection;

    float heightFactor;
    float someAngle;
    float someAspectRatio;
    float speed;
    float nearDistance;
    float farDistance;


    FlatEarth() {
        this->position = glm::vec3(widthTexture * 0.5, widthTexture * 0.1, -(widthTexture * 0.25));
        this->gazeVector = glm::vec3(0.0, 0.0, 1.0);
        this->upVector = glm::vec3(0.0, 1.0, 0.0);
        this->leftVector = glm::vec3(-1.0, 0.0, 0.0);
        this->lightPosition = glm::vec4(
                (float) widthTexture * 0.5,
               100.0,
                (float) heightTexture * 0.5,
                1);

        this->heightFactor = 10.0;
        this->someAngle = 45.0;
        this->someAspectRatio = 1;
        this->speed = 0.0;
        this->nearDistance = 0.1;
        this->farDistance = 1000.0;
    }


    void move() {
        this->position = this->position + this->speed * this->gazeVector;
        this->sendToShaders();
    }

    void reset() {
        this->position = glm::vec3(widthTexture * 0.5, widthTexture * 0.1, -(widthTexture * 0.25));
        this->gazeVector = glm::vec3(0.0, 0.0, 1.0);
        this->upVector = glm::vec3(0.0, 1.0, 0.0);
        this->leftVector = glm::vec3(1.0, 0.0, 0.0);

        this->lightPosition = glm::vec4(
                (float) widthTexture * 0.5,
               100.0,
                (float) heightTexture * 0.5,
                1);
    }

    void setPitch(bool someBoolean) {
        glm::mat4 valueOfSomeRotationAngle;
        float ovyeStep;
        if (someBoolean) {
            ovyeStep = PITCHSTEP;
        } else {
            ovyeStep = -PITCHSTEP;
        }
        valueOfSomeRotationAngle = glm::rotate(glm::radians(ovyeStep), this->leftVector);

        this->gazeVector = glm::vec3(valueOfSomeRotationAngle * glm::vec4(this->gazeVector, 1));
        this->gazeVector = glm::normalize(this->gazeVector);

        this->upVector = glm::vec3(valueOfSomeRotationAngle * glm::vec4(this->upVector, 1));
        this->upVector = glm::normalize(this->upVector);

    }

    void setYaw(bool someBoolean) {
        glm::mat4 valueOfSomeRotationAngle;
        float ovyeStep;
        if (someBoolean) {
            ovyeStep = YAWSTEP;
        } else {
            ovyeStep = -YAWSTEP;
        }
        valueOfSomeRotationAngle = glm::rotate(glm::radians(ovyeStep), this->upVector);

        this->gazeVector = glm::vec3(valueOfSomeRotationAngle * glm::vec4(this->gazeVector, 1));
        this->gazeVector = glm::normalize(this->gazeVector);

        this->leftVector = glm::vec3(valueOfSomeRotationAngle * glm::vec4(this->leftVector, 1));
        this->leftVector = glm::normalize(this->leftVector);
        
    }

     void resetSpeed() {
        this->speed = 0.0;
    }


    void changeSpeed(bool someBoolean) {
        float ovyeStep;
        if (someBoolean) {
            ovyeStep = SPEEDSTEP;
        } else {
            ovyeStep = -SPEEDSTEP;
        }
        this->speed += ovyeStep;
    }

    void movePlane(bool someBoolean) {
        int ovyeStep;
        if (someBoolean) {
            ovyeStep = 1;
        } else {
            ovyeStep = -1;
        }
        this->position.x += ovyeStep;
    }


    void changeHeight(bool someBoolean) {
        float ovyeStep;
        if (someBoolean) {
            ovyeStep = HEIGHTFACTORSTEP;
        } else {
            ovyeStep = -HEIGHTFACTORSTEP;
        }
        this->heightFactor += ovyeStep;
    }

    void changeLight(int someIntegere) {
        if (someIntegere == 0) {
            this->lightPosition.z -= LIGHTSTEP;
        } else if (someIntegere == 1) {
            this->lightPosition.z += LIGHTSTEP;
        }else if (someIntegere == 2) {
            this->lightPosition.x -= LIGHTSTEP;
        }else if (someIntegere == 3) {
            this->lightPosition.x += LIGHTSTEP;
        }else if (someIntegere == 4) {
            this->lightPosition.y -= LIGHTSTEP;
        }else if (someIntegere == 5) {
            this->lightPosition.y += LIGHTSTEP;
        }
    }

    void sendToShaders() {
        glViewport(0, 0, imagePlaneWidth, imagePlaneHeight);

        this->projectionMatrix = glm::perspective(
                this->someAngle,
                this->someAspectRatio,
                this->nearDistance,
                this->farDistance
        );

        this->viewMatrix = glm::lookAt(
                this->position,
                glm::vec3(
                        this->position.x + this->gazeVector.x * this->nearDistance,
                        this->position.y + this->gazeVector.y * this->nearDistance,
                        this->position.z + this->gazeVector.z * this->nearDistance
                ),
                this->upVector
        );

        this->modelMatrix = glm::mat4(1.0f);

        this->modelView = this->viewMatrix * this->modelMatrix;
        this->modelViewProjection = this->projectionMatrix * this->viewMatrix * this->modelMatrix;

        GLint shaderLocation = glGetUniformLocation(idProgramShader, "MV");
        glUniformMatrix4fv(shaderLocation, 1, GL_FALSE, &modelView[0][0]);

        shaderLocation = glGetUniformLocation(idProgramShader, "MVP");
        glUniformMatrix4fv(shaderLocation, 1, GL_FALSE, &modelViewProjection[0][0]);

        shaderLocation = glGetUniformLocation(idProgramShader, "lightPosition");
        glUniform4fv(shaderLocation, 1, &this->lightPosition.x);

        glm::vec4 cameraPosition4 = glm::vec4(this->position, 1);
        shaderLocation = glGetUniformLocation(idProgramShader, "cameraPosition");
        glUniform4fv(shaderLocation, 1, &cameraPosition4.x);

        shaderLocation = glGetUniformLocation(idProgramShader, "heightFactor");
        glUniform1f(shaderLocation, this->heightFactor);

        shaderLocation = glGetUniformLocation(idProgramShader, "widthTexture");
        glUniform1i(shaderLocation, widthTexture);

        shaderLocation = glGetUniformLocation(idProgramShader, "heightTexture");
        glUniform1i(shaderLocation, heightTexture);

    }
};

FlatEarth *flatEarth;
glm::vec3 *vertices;


void startRendering(int w, int h) {
    glClearColor(0, 0, 0, 1);
    glClearDepth(1.0f);
    glClearStencil(0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(3, GL_FLOAT, 0, vertices);
    glDrawArrays(GL_TRIANGLES, 0,6 * w * h);
    glDisableClientState(GL_VERTEX_ARRAY);
}

void setVData(int w, int h) {
    vertices = new glm::vec3[6 * w * h];
    glm::vec3 v1, v2, v3, v4;
    int index = -1;
    for (int i = 1; i < w; i++) {
        for (int j = 1; j < h; j++) {
            v1 = glm::vec3(i-1, 0, j-1);
            v2 = glm::vec3(i, 0, j-1);
            v3 = glm::vec3(i-1, 0, j );
            v4 = glm::vec3(i , 0, j );

            vertices[++index] = v1;
            vertices[++index] = v4;
            vertices[++index] = v2;

            vertices[++index] = v1;
            vertices[++index] = v3;
            vertices[++index] = v4;

        }
    }
}


static void keyCallback(GLFWwindow *window, int key, int scancode, int action, int mods) {
    if (action == GLFW_PRESS || action == GLFW_REPEAT) {
        switch (key) {
            case GLFW_KEY_ESCAPE:
                glfwSetWindowShouldClose(window, GLFW_TRUE);
                break;
            case GLFW_KEY_W:   
                flatEarth->setPitch(true);
                break;
            case GLFW_KEY_S:   
                flatEarth->setPitch(false);
                break;
            case GLFW_KEY_A:   
                flatEarth->setYaw(true);
                break;
            case GLFW_KEY_D:   
                flatEarth->setYaw(false);
                break;
            case GLFW_KEY_Y:   
                flatEarth->changeSpeed(true);
                break;
            case GLFW_KEY_H:   
                flatEarth->changeSpeed(false);
                break;
            case GLFW_KEY_X:   
                flatEarth->resetSpeed();
                break;
            case GLFW_KEY_R:   
                flatEarth->changeHeight(true);
                break;
            case GLFW_KEY_F:   
                flatEarth->changeHeight(false);
                break;
            case GLFW_KEY_T:   
                flatEarth->changeLight(1);
                break;
            case GLFW_KEY_G:   
                flatEarth->changeLight(0);
                break;
            case GLFW_KEY_RIGHT:   
                flatEarth->changeLight(3);
                break;
            case GLFW_KEY_LEFT:   
                flatEarth->changeLight(2);
                break;
            case GLFW_KEY_UP:   
                flatEarth->changeLight(5);
                break;
            case GLFW_KEY_DOWN:   
                flatEarth->changeLight(4);
                break;
            case GLFW_KEY_I:   
                flatEarth->reset();
                break;
            case GLFW_KEY_Q:   
                flatEarth->movePlane(true);
                break;
            case GLFW_KEY_E:   
                flatEarth->movePlane(false);
                break;
            case GLFW_KEY_P:  
                if (isFullScreen) {
                    glfwSetWindowMonitor(window, nullptr, 0, 0, imagePlaneWidthL, imagePlaneHeightL, 0);
                    isFullScreen = false;
                } else {
                    imagePlaneWidthL = imagePlaneWidth;
                    imagePlaneHeightL = imagePlaneHeight;
                    glfwSetWindowMonitor(window, const_cast<GLFWmonitor *>(monitor), 0, 0, mode->width, mode->height,
                                         mode->refreshRate);
                    isFullScreen = true;
                }

                break;
            default:
                break;
        }
    }
}

void windowSizeCallback(GLFWwindow *win, int width, int height) {
    imagePlaneWidth = width;
    imagePlaneHeight = height;
}

int main(int argc, char *argv[]) {

    if (argc != 3) {
        printf("Please provide two texture image\n");
        exit(-1);
    }

    glfwSetErrorCallback(errorCallback);

    if (!glfwInit()) {
        exit(-1);
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_COMPAT_PROFILE);

    imagePlaneWidth = 1000;
    imagePlaneHeight = 1000;
    win = glfwCreateWindow(imagePlaneWidth, imagePlaneHeight, "HW3", NULL, NULL);

    if (!win) {
        glfwTerminate();
        exit(-1);
    }
    glfwMakeContextCurrent(win);

    GLenum err = glewInit();
    if (err != GLEW_OK) {
        fprintf(stderr, "Error: %s\n", glewGetErrorString(err));

        glfwTerminate();
        exit(-1);
    }

    glfwSetKeyCallback(win, keyCallback);
    glfwSetWindowSizeCallback(win, windowSizeCallback);

    monitor = glfwGetPrimaryMonitor();
    mode = const_cast<GLFWvidmode *>(glfwGetVideoMode(const_cast<GLFWmonitor *>(monitor)));


    initShaders();
    glUseProgram(idProgramShader);
    initTexture(argv[1],argv[2], &widthTexture, &heightTexture,idProgramShader);

    setVData(widthTexture, heightTexture);

    flatEarth = new FlatEarth();
    flatEarth->sendToShaders();

    glEnable(GL_DEPTH_TEST);
    while (!glfwWindowShouldClose(win)) {

        startRendering(widthTexture, heightTexture);

        glfwSwapBuffers(win);
        glfwPollEvents();
        flatEarth->move();

    }


    glfwDestroyWindow(win);
    glfwTerminate();

    return 0;
}

