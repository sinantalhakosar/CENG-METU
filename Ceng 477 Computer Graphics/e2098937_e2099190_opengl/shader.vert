#version 410

layout(location = 0) in vec3 position;

uniform mat4 MVP;
uniform mat4 MV;
uniform mat4 inverseTransposeV;
uniform vec4 cameraPosition;
uniform vec4 lightPosition;
uniform float heightFactor;

uniform sampler2D rgbTexture;
uniform sampler2D rgbTexture1;

uniform int widthTexture;
uniform int heightTexture;


out vec2 textureCoordinate;
out vec3 vertexNormal;
out vec3 ToLightVector;
out vec3 ToCameraVector;


void main(){
    textureCoordinate = vec2((widthTexture - position.x) / widthTexture, (heightTexture - position.z) / heightTexture);
    vec4 textureColour = texture(rgbTexture, textureCoordinate);
    float y = heightFactor * textureColour.r;
    vec4 vect = vec4(position.x, y,position.z, 1);

    vec4 tmpTextureColour;

    int neighcount = 0;
    int tricount = 0;
    vec4 v0 = vec4(0,0,0,1);
    vec4 v1 = vec4(0,0,0,1);
    vec4 v2 = vec4(0,0,0,1);
    vec4 v3 = vec4(0,0,0,1);
    vec4 v4 = vec4(0,0,0,1);
    vec4 v5 = vec4(0,0,0,1);

    if(vect.x == 0 && vect.y == 0){
        neighcount = 3;
        tricount = 2;

        v0 = vec4(vect.x, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x + 1, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x + 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;
    }
    else if(vect.x == widthTexture && vect.z == heightTexture){
        neighcount = 3;
        tricount = 2;

        v0 = vec4(vect.x, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x - 1, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x - 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;
    }
    else if(vect.x == widthTexture && vect.z == 0){
        neighcount = 2;
        tricount = 1;

        v0 = vec4(vect.x - 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

    }
    else if(vect.x == 0 && vect.z == heightTexture){
        neighcount = 2;
        tricount = 1;

        v0 = vec4(vect.x + 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;
    }
    else if(vect.x == 0){
        neighcount = 4;
        tricount = 3;

        v0 = vec4(vect.x, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x + 1, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x + 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;

        v3 = vec4(vect.x, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v3.x)/widthTexture, (heightTexture- v3.z) / heightTexture));
        v3.y = heightFactor * tmpTextureColour.r;

    }
    else if(vect.x == widthTexture){
        neighcount = 4;
        tricount = 3;

        v0 = vec4(vect.x, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x - 1, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x - 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;

        v3 = vec4(vect.x, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v3.x)/widthTexture, (heightTexture- v3.z) / heightTexture));
        v3.y = heightFactor * tmpTextureColour.r;
    }
    else if(vect.z == 0){
        neighcount = 4;
        tricount = 3;

        v0 = vec4(vect.x - 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x + 1, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;

        v3 = vec4(vect.x + 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v3.x)/widthTexture, (heightTexture- v3.z) / heightTexture));
        v3.y = heightFactor * tmpTextureColour.r;

    }
    else if(vect.z == heightTexture){
        neighcount = 4;
        tricount = 3;

        v0 = vec4(vect.x + 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x - 1, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;

        v3 = vec4(vect.x - 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v3.x)/widthTexture, (heightTexture- v3.z) / heightTexture));
        v3.y = heightFactor * tmpTextureColour.r;
    }
    else{
        v0 = vec4(vect.x - 1, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v0.x)/widthTexture, (heightTexture- v0.z) / heightTexture));
        v0.y = heightFactor * tmpTextureColour.r;

        v1 = vec4(vect.x - 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v1.x)/widthTexture, (heightTexture- v1.z) / heightTexture));
        v1.y = heightFactor * tmpTextureColour.r;

        v2 = vec4(vect.x, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v2.x)/widthTexture, (heightTexture- v2.z) / heightTexture));
        v2.y = heightFactor * tmpTextureColour.r;

        v3 = vec4(vect.x + 1, 0, vect.z + 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v3.x)/widthTexture, (heightTexture- v3.z) / heightTexture));
        v3.y = heightFactor * tmpTextureColour.r;

        v4 = vec4(vect.x + 1, 0, vect.z, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v4.x)/widthTexture, (heightTexture- v4.z) / heightTexture));
        v4.y = heightFactor * tmpTextureColour.r;

        v5 = vec4(vect.x, 0, vect.z - 1, 1);
        tmpTextureColour = texture(rgbTexture, vec2((widthTexture - v5.x)/widthTexture, (heightTexture- v5.z) / heightTexture));
        v5.y = heightFactor * tmpTextureColour.r;

    }
    vec3 norm = vec3(0,0,0);
    norm = norm +  cross(vec3(v0-vect), vec3(v1-vect));
    norm = norm +  cross(vec3(v1-vect), vec3(v2-vect));

   if(tricount > 2){
        norm = norm +  cross(vec3(v2-vect), vec3(v3-vect));
    }
    if(tricount > 3){
        norm = norm +  cross(vec3(v3-vect), vec3(v4-vect));
    }
    if(tricount > 4){
        norm = norm +  cross(vec3(v4-vect), vec3(v5-vect));
        norm = norm +  cross(vec3(v5-vect), vec3(v0-vect));
    }


    norm = normalize(norm);
    vertexNormal = normalize(vec3( transpose(inverse(MV)) * vec4(norm,0) ));

    ToLightVector = normalize(vec3(MV * vec4(lightPosition.xyz - vect.xyz,0)));
    ToCameraVector = normalize(vec3(MV * vec4(cameraPosition.xyz - vect.xyz,0)));

    gl_Position = MVP * vect;
}