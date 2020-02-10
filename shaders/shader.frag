
#version 130

uniform sampler2D texInput;

in vec2 texcoord;

out vec4 p3d_FragColor;

void main() {
  float value = texture(texInput, texcoord).r;

  // This block is the code from applyMasks, except that texcoord is in 0..1 range.
  float distance = length(texcoord - vec2(0.5));
  float max_width = sqrt(2) * 0.5 - (5.0 / 1024.0);
  float delta = distance / max_width;
  float gradient = delta * delta;
  value -= gradient * gradient;

  if (value > 0.75) {
    p3d_FragColor = vec4(0, 0.6, 0.1, 1);
  } else if (value > 0.30) {
    p3d_FragColor = vec4(0, 0.8, 0.3, 1);
  } else if (value > 0.15) {
    p3d_FragColor = vec4(0.9, 1, 0.7, 1);
  } else {
    p3d_FragColor = vec4(0, 0.6, 1, 1);
  }

  //p3d_FragColor = vec4(value, value, value, 1);
}