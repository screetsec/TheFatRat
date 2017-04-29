#extension GL_OES_EGL_image_external : require

precision mediump float;
uniform samplerExternalOES texUnit;
uniform float opacity;
uniform float saturation;
uniform float gamma;
varying vec2 UV;

vec3 rgb2hsl(vec3 rgb)
{
    float e = 1.0e-7;

    vec4 p = rgb.g < rgb.b ? vec4(rgb.bg, -1.0, 2.0 / 3.0) : vec4(rgb.gb, 0.0, -1.0 / 3.0);
    vec4 q = rgb.r < p.x ? vec4(p.xyw, rgb.r) : vec4(rgb.r, p.yzx);

    float v = q.x;
    float c = v - min(q.w, q.y);
    float h = abs((q.w - q.y) / (6.0 * c + e) + q.z);
    float l = v - c * 0.5;
    float s = c / (1.0 - abs(2.0 * l - 1.0) + e);
    return clamp(vec3(h, s, l), 0.0, 1.0);
}

vec3 hsl2rgb(vec3 hsl)
{
    vec3 h = vec3(hsl.x * 6.0);
    vec3 p = abs(h - vec3(3.0, 2.0, 4.0));
    vec3 q = 2.0 - p;

    vec3 rgb = clamp(vec3(p.x - 1.0, q.yz), 0.0, 1.0);
    float c = (1.0 - abs(2.0 * hsl.z - 1.0)) * hsl.y;
    return (rgb - vec3(0.5)) * c + hsl.z;
}

void main()
{
    vec4 color = texture2D(texUnit, UV);
    vec3 hsl = rgb2hsl(color.xyz);
    vec3 rgb = pow(hsl2rgb(vec3(hsl.x, hsl.y * saturation, hsl.z * opacity)), vec3(gamma));
    gl_FragColor = vec4(rgb, 1.0);
}
