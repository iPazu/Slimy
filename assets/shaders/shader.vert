#version 130

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;

// This variable is passed to the fragment shader
out vec2 texcoord;

void main() {
  gl_Position = p3d_ProjectionMatrix * (p3d_ModelViewMatrix * p3d_Vertex);
  texcoord = p3d_MultiTexCoord0;
}