+++
date = "2017-03-01"
draft = false
title = "OpenGL Gradient Background"
+++

First of all, hello to my new blog :) I've made a bunch of blog-writing attempts
in the past, with a little-to-no success. So let's hope this time it works out!

In this short article, I'll describe a neat little function that allows you to have
a gradient backgrounds in your OpenGL applications, like the snazzy 3D apps 
(Blender pictured below) do these days.

![BlenderViewport](gradient_blender.jpg#center)

Our goal is to create a single function, working very much like the glClearColor,
but rather than a single color it should be to accept arguments for colors at 
the top and bottom of the window. I'll only present how to create linear 
gradients, but extending this technique to other gradients should be simple. Thus
we can declare our function simply as:
~~~~~~~~~~~~~~~~
void mygl_GradientBackground( float top_r, float top_g, float top_b, float top_a,
                              float bot_r, float bot_g, float bot_b, float bot_a );
~~~~~~~~~~~~~~~~

To achieve the gradient background effect we will render a full-screen triangle and 
then use fragment shader to render linear gradient before all of the other graphics 
calls happen. 

Note that I am assuming some familiarity with OpenGL - I do not explain
terms like [VAO](https://www.khronos.org/opengl/wiki/Vertex_Specification#Vertex_Array_Object), 
[VBO](https://www.khronos.org/opengl/wiki/Vertex_Specification#Vertex_Buffer_Object), etc. 
There is a plenty of great resources on learning basic OpenGL online. If you are 
a complete OpenGL begginer, I'd suggest reading through [learnopengl.com](https://learnopengl.com) tutorials.

## Theory

The main trick of this technique, comes from a [Morgan McGuire](https://www.cs.williams.edu/~morgan/) [tweet and a follow up discussion](https://twitter.com/CasualEffects/status/705750628849590273). Supposedly 
following line will produce a fullscreen triangle, without us uploading any
vertex data! We only need to call __glDrawArrays(GL_TRIANGLES, 0, 3)__ on the CPU side. 

~~~~~~~~~~~~~~~~
gl_Position = vec4(gl_VertexID >> 1, gl_VertexID & 1, 0.0, 0.5) * 4 - 1
~~~~~~~~~~~~~~~~

Let's spend some time to analyze what this little line is doing.
First of all, __gl_Position__ is an internal OpenGl variable describing vertex's 
position which will be pushed down the pipeline. __gl_VertexID__ is a variable
related to the  __glDrawArrays__ call. In [documentation](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/gl_VertexID.xhtml) 
we can read:
>
gl_VertexID is a vertex language input variable that holds an integer index for the vertex. The index is implicitly generated by glDrawArrays 
>
This means that when calling __glDrawArrays__ each instance of vertex shader 
will have a different __gl_VertexID__. To get indices {0, 1, 2}, we simply call 
__glDrawArrays(GL_TRIANGLES, 0, 3)__ - and cool thing is that this will work
even without a Vertex Buffer Object bound! This means we can skip defining 
geometry on CPU side, generating positions in vertex shader instead! Knowing
this, it is not hard to calculate generated positions by hand:

|    gl_VertexID   |     x        |        y
|:-------------: | :-----------:  | :-------------:
|         0        |  0 >> 1 → 0 |    0 & 1 → 0 
|         1        |  1 >> 1 → 0 |    1 & 1 → 1 
|         2        |  2 >> 1 → 1 |    2 & 1 → 0

Thus our vertex locations are (0, 0, 0), (0, 1, 0), (1, 0, 0). Why do we need
the rest of opertations though(multiplications and substraction)? There are two
reasons: First, we want our triangle to cover entire screen, not just half. Second,
we want to write positions in Normalized Device Coordinates, which range from (-1,-1) to (1,1). 
To illustrate what the transformation do:

<div style="text-align:center;"> <img src="positions_diag.png"> </div>

As you can see in (a) the initial triangle is not exactly what we need.
We need to enlarge it and translate it to (-1, -1). The factor of 4 comes
from the triangle similarity - it is going to be the smallest triangle
that covers entire screen. I've added the red numbers in (b) to better illustrate this.

## Code

Let's start with gpu side of things. We have most of the pieces of a vertex shader.
For this purpose I have modified the vertex shader slightly, to also automatically
generate uv coordinates. Note that these range from (0,0) to (1,1). We can get 
this by remapping the range of __gl_Position.xy__ which we know will be from
(-1,-1) to (1,1);
~~~~~~~~~~~~~~~~
out vec2 v_uv;

void main()
{
  uint idx = gl_VertexID;
  gl_Positions = vec4( idx & 1, idx >> 1, 0.0, 0.5 ) * 4.0 - 1.0;
  v_uv = vec2( gl_Position.xy * 0.5 + 0.5 );
}
~~~~~~~~~~~~~~~~

Fragment shader itself is very simple. We take the colors provided by the user
and do linear blend between the two, based on __uv.y__
~~~~~~~~~~~~~~~~
uniform vec4 top_color;
uniform vec4 bot_color;
in vec2 v_uv;

out vec4 frag_color;
void main()
{
  frag_color = bot_color * (1 - uv.y) + top_color * uv.y;
}
~~~~~~~~~~~~~~~~

Now that we know how the shaders look like, let's build the function! We
want user to only provide colors - so we are responsible for setting up the 
shaders, vertex array objects and passing everything correctly to OpenGL.

~~~~~~~~~~~~~~~~
#define STR(x) #x
void mygl_GradientBackground( float top_r, float top_g, float top_b, float top_a,
                              float bot_r, float bot_g, float bot_b, float bot_a )
{
  glDisable(GL_DEPTH_TEST);

  static GLuint background_vao = 0;
  static GLuint background_shader = 0;
  
  if (background_vao == 0)
  {
    glGenVertexArrays(1, &background_vao);
  
    char* vs_src = (char*) STR
    (
      #version 330 core
      out vec2 v_ub;
      void main()
      {
        uint idx = gl_VertexID;
        gl_Positions = vec4( idx & 1, idx >> 1, 0.0, 0.5 ) * 4.0 - 1.0;
        v_uv = vec2( gl_Position.xy * 0.5 + 0.5 );
      }
    );

    char* fs_src = (char*) STR
    (
      #version 330 core
      uniform vec4 top_color;
      uniform vec4 bot_color;
      in vec2 v_uv;
      out vec4 frag_color;

      void main()
      {
        frag_color = bot_color * (1 - uv.y) + top_color * uv.y;
      }
    );
    GLuint vs_id, fs_id;
    vs_id = glCreateShader( GL_VERTEX_SHADER );
    fs_id = glCreateShader( GL_FRAGMENT_SHADER );
    glShaderSource(vs_id, 1, vs_src, NULL);
    glShaderSource(fs_id, 1, fs_src, NULL);
    glCompileShader(vs_id);
    glCompileShader(fs_id);
    background_shader = glCreateProgram();
    glAttachShader( background_shader, vs_id );
    glAttachShader( background_shader, fs_id );
    glLinkProgram(  background_shader );
    glDetachShader( background_shader, fs_id );
    glDetachShader( background_shader, vs_id );
    glDeleteShader( fs_id );
    glDeleteShader( vs_id );
  }

  glUseProgram( background_shader );
  GLuint top_color_loc = glGetUniformLocation( backgorund_shader, "top_color" );
  GLuint bot_color_loc = glGetUniformLocation( backgorund_shader, "bot_color" );
  glUniform4f( top_color_loc, top_r, top_g, top_b, top_a );
  glUniform4f( bot_color_loc, bot_r, bot_g, bot_b, bot_a );
  
  glBindVertexArray( background_vao );
  glDrawArrays(GL_TRIANGLES, 0, 3);
  glBindVertexArray(0);

  glEnable(GL_DEPTH_TEST);
}
~~~~~~~~~~~~~~~~

Most of the code above is standard OpenGL boilerplate/setup code. Only "trick" 
is making the Vertex Array Object(vao) and shader program handle static, so they
persist through diffrent calls. This also causes the shader compilation to be
executed only once.

# Results

<div style="text-align:center;"> <img style="width:100%;" src="gradients_results.png"> </div>

Now we can create "pretty" gradient backgrounds! I've posted my implementation project [here](https://gist.github.com/mhalber/0a9b8a78182eb62659fc18d23fe5e94e).
Even though we have only created shaders for vertical linear graident, modifying
the code to support other form of gradients should not be very hard. Also
note that once you have the full-screen triangle, the world is your oyster, and
you are all set to do the [fragment-shader](http://www.iquilezles.org/www/material/nvscene2008/rwwtt.pdf) [magic](https://www.shadertoy.com)!


