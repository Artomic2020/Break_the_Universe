import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import *

window = pyglet.window.Window(width=1280, height=720, caption="Hello Pyglet")
window.set_location(x=400, y=200)

vertex_source = """
#version 330 core
layout(location = 0) in vec2 vertices;
layout(location = 1) in vec4 colors;

out vec4 newColor;

void main()
{
    gl_Position = vec4(vertices, 0.0, 1.0);
    newColor = colors;
}
"""

fragment_source = """
#version 330 core
in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor =newColor ;
}
"""

# Compile shaders + program
vert_shader = Shader(vertex_source, "vertex")
frag_shader = Shader(fragment_source, "fragment")
program = ShaderProgram(vert_shader, frag_shader)

batch = pyglet.graphics.Batch()

# A colored triangle (NDC coordinates: -1..1)
positions = [
    -0.5, -0.5,   # left
     0.5, -0.5,   # right
     0.0,  0.5    # top
]

colors = [
    1.0, 0.0, 0.0, 1.0,   # red
    0.0, 1.0, 0.0, 1.0,   # green
    0.0, 0.0, 1.0, 1.0    # blue
]

# Add vertex list to the shader program.

program.vertex_list(
    3,
    GL_TRIANGLES,
    batch=batch,
    vertices=('f', (-0.5, -0.5, 0.5, -0.5, 0.0, 0.5)),
    colors=('Bn', (255,0,0,255, 0,250,0,255, 0,0,255,255))
)



# IMPORTANT: attribute names must match shader inputs: "vertices" and "colors"
# program.vertex_list(
#     3,
#     pyglet.gl.GL_TRIANGLES,
#     batch=batch,
#     vertices=("f", positions),
#     colors=("f", colors),
# )

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()
