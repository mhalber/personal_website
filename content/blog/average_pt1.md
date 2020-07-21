+++
date = "2020-07-18"
draft = false
title = "On the average pt.1 - Definition"
+++


Most people are likely familiar with the concept of an average, as we often encouter it in our everyday lives. Questions like: how much money on *average* do I spend on groceries each week, how much time on *average* do I spend in front of computer per day, etc., are very common. An average is very simple to calculate - we take some quantities, add them together, and divide the result by the number of the quantities. In mathematical notation it is:

$$
\begin{eqnarray}
\bar{a} = \frac{1}{n}\sum_{i=0}^na_i\text{,}
\label{eq:avg}
\end{eqnarray}
$$
where $a_i$ is either a scalar value or a vector, that is  $a_i \in \mathbb{R}^n$, and $n$ is the number of quantities.

An average, or a mean, is a nice little property that tells us something (albeit not that much, see [Anascombe's quartet](https://en.wikipedia.org/wiki/Anscombe's_quartet)) about our data. However, one might wonder why is the average defined as in equation $\ref{eq:avg}$? We could punt on it and simply state that the above formula is the definition of a mean, and that is the end of the discussion. Hopefully, you agree that it is not a very satisfying answer. In this post we dig a little deeper and derive the above formula.

When we think about an average, it is useful to consider it in terms of the properties that the average of some dataset posesses. Let us focus for a moment on two-dimensional case, considering a set of points. Let us assume we have a set $\mathcal{A}=\{a_1, ..., a_n\}$ of $n$ points, where each point is represented by a tuple $a_i = (x_i,y_i)$. The property of the mean point $\bar{a}$ of $\mathcal{A}$ is that it minimizes the distance between all elements of $\mathcal{A}$. Mathematically we can write that $\bar{a}$ is a minimizer of the following loss function:

$$
\DeclareMathOperator*{\argmin}{arg\\,min}
\argmin_{\bar{a}}\mathcal{L}(\bar{a}, \mathcal{A}) = \argmin_{\bar{a}}\frac{1}{2}\sum_i^n\\\|\bar{a} - a_i\\\|_2^2 \nonumber
$$

The notation of $\\| \cdot \\|_2$ is the $L_2$ norm, also known [Euclidean norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#Euclidean_norm), and it describes the length of a vector, or in other words the distance one needs to travel to get from the start of a vector to its end. As you probably have noticed, we also square the distances $\\|\bar{a} - a_i\\|_2$. One nice property of the square function $f(x)=x^2$ is that it is a convex function, which means that it has global minimum. Additionally, computing the derivative of $f(x)=x^2$ is quite easy.  We also add a scaling factor of $\frac{1}{2}$ to simplify the derivation later on. Importantly, it does not change where the minimum is.

To find $\bar{a}$ we need to take the derivative of $\mathcal{L}(\bar{a}, \mathcal{A})$ with respect to the parameters $\bar{a} = \{\bar{x}, \bar{y} \}$and set each of them to zero:
$$
\begin{align*}
\frac{ \partial \left( {1 \over 2} \sum_{i}^{n}\\|\bar{a}-a_i\\|_2^2\right)}{\partial\bar{x}} = 0 \\\\\\
\frac{ \partial \left( {1 \over 2} \sum_{i}^{n}\\|\bar{a}-a_i\\|_2^2\right)}{\partial\bar{y}} = 0
\end{align*}
$$
Let us work through the math for one of the parameters, the derivations for the other is analogous (the derivation can also be extended to any dimension).
$$
\begin{align}
\frac{\partial\left(\frac{1}{2}\sum_i^n\\|\bar{a}-a_i\\|_2^2\right)}{\partial\bar{x}} &= 0 \nonumber \\\\\\
\frac{1}{2}\sum_i^n\frac{\partial(\\|\bar{a}-a_i\\|_2^2)}{\partial\bar{x}} &= 0 && \text{// Sum rule} \nonumber\\\\\\
\frac{1}{2}\sum_i^n\frac{\partial\epsilon_i^2}{\partial\bar{x}} &= 0 && \text{// } \epsilon_i=\\|\bar{a}-a_i\\|_2 \nonumber \\\\\\
\frac{1}{2}\sum_i^n\frac{\partial\epsilon_i^2}{\partial\epsilon_i}\frac{\partial\epsilon_i}{\partial\bar{x}} &= 0 && \text{// Chain rule} \label{eq:chain}
\end{align}
$$

At this point, by the chain rule, we have two derivatives to work out here, $\frac{\partial\epsilon_i^2}{\partial\epsilon_i}$ and $\frac{\partial\epsilon_i}{\partial\bar{x}}$. Let us work them out one by one. First one is easy enough:
$$
\frac{\partial\epsilon_i^2}{\partial\epsilon_i} = 2\epsilon_i \nonumber
$$
Moving onto the second part, which is slightly more involved: 

$$
\begin{align*}
\frac{\partial{\epsilon_i}}{\partial\bar{x}}&=\frac{\partial\\|\bar{a}-a_i\\|_2}{\partial{\bar{x}}} \\\\\\
\frac{\partial{\epsilon_i}}{\partial\bar{x}}&=\frac{\partial(\sqrt{(\bar{x}-x_i)^2+(\bar{y}-y_i)^2})}{\partial{\bar{x}}} && \text{// from definition of the } L_2\text{ norm} \\\\\\
&=\frac{\partial t^\frac{1}{2}}{\partial\bar{x}} && \text{// }t=(\bar{x}-x_i)^2+(\bar{y}-y_i)^2 \text{ and } t^{\frac{1}{2}} = \sqrt{t} \\\\\\
&=\frac{\partial t^\frac{1}{2}}{\partial t}\frac{\partial t}{\partial\bar{x}} && \text{// Chain rule}\\\\\\
&=\frac{1}{2}t^{-\frac{1}{2}}\left( \frac{\partial (\bar{x}-x_i)^2}{\partial\bar{x}} + \frac{\partial (\bar{y}-y_i)^2}{\partial\bar{x}} \right) && \text{// Power rule and Sum rule} \\\\\\
&=\frac{1}{2\epsilon_i}\frac{\partial{\bar{x}^2-2\bar{x}x_i+x_i^2}}{\partial{\bar{x}}} && \text{// } t^{-\frac{1}{2}} = \frac{1}{\sqrt{(\bar{x}-x_i)^2+(\bar{y}-y_i)^2}} = \frac{1}{\epsilon_i} \\\\\\
&=\frac{1}{2\epsilon_i}(2\bar{x}-2x_i) \\\\\\
&=\frac{1}{2\epsilon_i}2(\bar{x}-x_i) \\\\\\
&=\frac{\bar{x}-x_i}{\epsilon_i}
\end{align*}
$$


That was a bit more work, but hopefully you can see that we just went through some basic transformations. Note that we are for a moment assuming that $\epsilon_i \neq 0$. If we plug both expressions back into the equation $\ref{eq:chain}$. we can find the formula for $\bar{x}$:
$$
\begin{align*}
\frac{1}{2}\sum_i^n\frac{\partial\epsilon_i^2}{\partial\epsilon_i}\frac{\partial\epsilon_i}{\partial\bar{x}} &= 0 \\\\\\
\frac{1}{2}\sum_i^n2\epsilon_i\frac{\bar{x}-x_i}{\epsilon_i} &= 0\\\\\\
\sum_i^n(\bar{x}-x_i) &= 0 \\\\\\
n\bar{x} -\sum_i^nx_i &= 0 \\\\\\
\bar{x} &= \frac{1}{n}\sum_i^nx_i
\end{align*}
$$

We have arrived at expression for the first coordinate of $\bar{a}$. As mentioned before, similar derivation can be done for $\bar{y}$. Given that the operations like addition and scalar multiplication are defined for both scalars and vectors, we have shown that the average of points in the set $\mathcal{A}$ is equal to the minimizer of the sum of squared distances:
$$
\DeclareMathOperator*{\argmin}{arg\\,min}
\argmin_{\bar{a}}\mathcal{L}(\bar{a}, \mathcal{A}) = \argmin_{\bar{a}}\frac{1}{2}\sum_i^n\\|\bar{a} - a_i\\|_2^2 = \frac{1}{n}\sum_i^na_i
$$
To finish off, and to add at least one figure to this post, below we show the average of two dimensional point set:

![Test](mean.png#center)

Hopefully this post can be useful to someone. Questions? Comments? Found errors? Feel free to hit me up on twitter [@maciejhalber](https://twitter.com/maciejhalber)!

Credits: The visualization above is **highly** inspired by the excellent visualizations in the companion video of the paper ["A General and Adaptive Robust Loss Function"](https://www.youtube.com/watch?v=BmNKbnF69eY) by Jonathan T. Barron.	