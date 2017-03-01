+++
date = "2017-03-01"
draft = true
title = "OpenGL Gradient Background"

+++
First of all, hello to my new blog. I've made a bunch of blog-writing attempts
in the past, with little-to-no success. So let's hope this time it works out!

In this short article, I'll describe a neat little function that allows you to have
a gradient backgrounds in your OpenGL applications, like the snazzy 3D apps do
these days.

<div style="text-align:center;">
<img src="gradient_blender.jpg"> &nbsp <img src="gradient_maya.jpg">
</div>

### GOAL
Our goal is to create a single function, working very much like glClearColor,
but accepting the arguments for colors at the top and bottom of the window. I'll
only present how to create linear gradients, but extending this technique to 
other gradients should be simple.
~~~~~~~~~~~~~~~~
void mygl_ClearGradient( float top_r, float top_g, float top_b, float top_a,
                         float bot_r, float bot_g, float bot_b, float bot_a );
~~~~~~~~~~~~~~~~
### APPROACH
Overall approach is to render a full-screen triangle and then use fragment
shader to render the linear gradient before all other graphics calls happen. 

### DETAILS
Describe the trick to avoid geometric data submission and just do it in the vertex
shader. Point out that this is the meat of this technique

Then describe the fragment shader

Then describe the function of the body, say that we're omitting error checks,
and that the reader will most likely implement this using their own wrapper etc.

### RESULTS  

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