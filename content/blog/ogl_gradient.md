+++
date = "2017-03-01"
draft = true
title = "OpenGL Gradient Background"

+++
First of all, hello to my new blog :) I've made a bunch of blog-writing attempts
in the past, with a little-to-no success. So let's hope this time it works out!

In this short article, I'll describe a neat little function that allows you to have
a gradient backgrounds in your OpenGL applications, like the snazzy 3D apps do
these days.

<div style="text-align:center;">
<img src="gradient_blender.jpg"> &nbsp <img src="gradient_maya.jpg">
</div>

Our goal is to create a single function, working very much like glClearColor,
but accepting the arguments for colors at the top and bottom of the window. I'll
only present how to create linear gradients, but extending this technique to 
other gradients should be simple.
~~~~~~~~~~~~~~~~
void mygl_ClearGradient( float top_r, float top_g, float top_b, float top_a,
                         float bot_r, float bot_g, float bot_b, float bot_a );
~~~~~~~~~~~~~~~~

To achieve this effect we will put a full-screen triangle on the screen and then 
use fragment shader to render the linear gradient before all of the other 
graphics calls happen. 

The main trick of this technique, comes from a [Morgan McGuire](https://www.cs.williams.edu/~morgan/) [tweet and follow up discussion](https://twitter.com/CasualEffects/status/705750628849590273). Supposedly 
following line will produce a fullscreen triangle, without us uploading any
vertex data! We only need to call __glDrawArrays__ on the CPU side.

~~~~~~~~~~~~~~~~
gl_Position = vec4(gl_VertexID >> 1, gl_VertexID & 1, 0.0, 0.5) * 4 - 1
~~~~~~~~~~~~~~~~

Let's spend some time to analyze what this little line is doing.
gl_Position is an OpenGl variable describing vertex position which will be
pushed down the pipeline. Since we only want to have a full scree triangle we will
basically be writing position in Normalized Device Coordinates(NDC). Each vertex
coming from glDrawArrays call, even without any buffer bound will have an
id, and we shall use this information to generate the triangle. It is not hard
to see that

  x   | y
  :-------------:  | :-------------:
  0 >> 1 -> 0 | 0 & 1 -> 0 
  1 >> 1 -> 0 | 1 & 1 -> 1 
  2 >> 1 -> 1 | 2 & 1 -> 0


Thus our vertex locations are (0, 0, 0), (0, 1, 0), (1, 0, 0). After the rest of
the transformations we will have (-1, -1, -1), (-1, 3, -1), (3, -1, -1).

### ADD DIAGRAM

Fragment shader is trivial, simply taking our colors as uniform and rendering
them based on y position.
~~~~~~~~~~~~~~~~
Code for fragment shader
~~~~~~~~~~~~~~~~

With this in mind, let's start building our function. In the function body we will
need to first create a shader program. This is a straight-forward task
~~~~~~~~~~~~~~~~
Include code for setup of shader
~~~~~~~~~~~~~~~~
Note that this should only happen once - that's why we used static variable, which
persist between function calls in c/c++. Now let's bind our shader and
call draw function
~~~~~~~~~~~~~~~~
Include rest of the function.
~~~~~~~~~~~~~~~~
Note how we are not uploading any geometry data - this will be outomatically
generated on the GPU!

Code 

Show some different gradients.

Finish. 

<!--~~~~~~~~~~~~~~~~
int main()
{
  printf("Hello, World!");
}
~~~~~~~~~~~~~~~~

When \\(a \ne 0\\), there are two solutions to \\(ax^2 + bx + c = 0\\) and they are
\\[x = {-b \pm \sqrt{b^2-4ac} \over 2a}.\\]-->