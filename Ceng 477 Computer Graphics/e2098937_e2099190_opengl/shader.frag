#version 410

out vec4 color;

uniform mat4 MVP; 
uniform mat4 MV; 
uniform vec4 cameraPosition;

uniform sampler2D rgbTexture;
uniform sampler2D rgbTexture1;

uniform int widthTexture;
uniform int heightTexture;

in vec2 textureCoordinate;
in vec3 vertexNormal; 
in vec3 ToLightVector; 
in vec3 ToCameraVector; 

void main() {

    vec4 texColour = texture(rgbTexture1, textureCoordinate);

    vec4 v1 = vec4(0.25,0.25,0.25,1.0);
    vec4 v2 = vec4(0.3,0.3,0.3,1.0); 
    vec4 v3 = vec4(1.0, 1.0, 1.0, 1.0);  

    vec4 diffuse = v3 * v3 * max(0, clamp(dot(vertexNormal, ToLightVector), 0, 1)); 

    vec3 H = normalize(ToLightVector + ToCameraVector);
    vec4 specular = v3 * v3 * pow(max(0, clamp(dot(vertexNormal, H), 0, 1)), 100);

    color = vec4(clamp( texColour.xyz * vec3(v2 * v1 + diffuse + specular), 0.0, 1.0), 1.0);


}
