+++
date = "2020-07-20"
draft = false
title = "On the average pt.2 - Robust average"
+++

In the [previous post]({{< ref "/blog/average_pt1.md" >}}) we derived the formula for the average and we showed that the average is a quantity that minimizes the sum of squared distances. Calculating the mean is extremely easy, as we have a closed form formula to do so.

However, as you might expect, there is no silver bullet. While the arithmetic mean has many useful properties, one if its biggest drawbacks is its sensitivity to outliers. Consider the dataset below - we have data consisting of a number of points that is mostly concentrated around a single position, with few outliers concentrated at another location:

![](calculated_mean.png#center)

Ideally, we would like our estimate (calculated mean in the figure above) to be close to the true mean. To achieve this our estimation procedure should somehow be able to ignore the outlier points. Luckily, since outlier data points are common when dealing with real-world data, people have developed a whole myriad of techniques to deal with such situations. One of these techniques involves the use of "robust" error function, that is error functions that are somewhat robust to the outliers.

To understand the intuition behind the robust error (or loss) functions, let us start by looking at the sum of squares function we analyzed in the [part 1]({{< ref "/blog/average_pt1.md" >}}) (for clarity, and without the loss of generality, we can omit the $\frac{1}{2}$ factor):

$$
\DeclareMathOperator*{\argmin}{arg\\,min}
\argmin_{\bar{a}}\mathcal{L}(\bar{a}, \mathcal{A}) = \argmin_{\bar{a}}\sum_i^n\\|\bar{a} - a_i\\|_2^2 \nonumber
$$

Let's rewrite the above equation with $\epsilon_i = \\|\bar{a} - a_i\\|_2$:

$$
\DeclareMathOperator*{\argmin}{arg\\,min}
\argmin_{\bar{a}}\mathcal{L}(\bar{a}, \mathcal{A}) = \argmin_{\bar{a}}\sum_i^n\epsilon_i^2 \nonumber
$$

We refer to the $\epsilon_i$ as the residual. By writing our loss function in the above form, it hopefully becomes clear that the squaring of the residual was just a choice that we made, as the function can be equivalently written as:

$$
\DeclareMathOperator*{\argmin}{arg\\,min}
\argmin_{\bar{a}}\mathcal{L}(\bar{a}, \mathcal{A}) = \argmin_{\bar{a}}\sum_i^n\rho(\epsilon_i) \nonumber \text{,}
$$
with $\rho(x) = x^2$. Immediately, a question emerges: what happens if we replace the square function with some other function? An example of a robust error function is the Pseudo-Huber loss, defined as $\rho_{huber}(x, \sigma) = \sigma^2\left(\sqrt{1 + (\frac{x}{\sigma})^2} - 1\right)$. The formula might look a little intimidating, however the plot of Pseudo-Huber function reveals that it is simply a function that approximates quadratic ($x^2$) near the origin and underestimates absolute value linear function everywhere else. The parameter $\sigma$ controls how quickly does this function grows (i.e. slope of the linear part).

![](functions.png#center)

To find the minimum of the Pseudo-Huber based loss function, let us follow the usual recipe of taking the derivative of a function with respect to the parameters and setting it equal to zero:

$$
\begin{align}
\frac{\partial L(\bar{a}, \mathcal{A})}{\partial \bar{x}} &= 0 \nonumber \\\\\\
\frac{\partial \sum_i^n\rho_{huber}(\epsilon_i, \sigma)}{\partial \bar{x}} &= 0 \nonumber \\\\\\
\sum_i^n \frac{\partial \rho_{huber}(\epsilon_i, \sigma)}{\partial \bar{x}} &= 0 &\text{ // Sum Rule} \nonumber  \\\\\\
\sum_i^n \frac{\partial \rho_{huber}(\epsilon_i, \sigma)}{\partial \epsilon_i} \frac{\partial \epsilon_i}{\partial \bar{x}} &= 0 &\text{ // Chain Rule} \nonumber
\end{align}
$$

As in part 1 we have split out derivative into two terms. Previously, we have shown in that:
$$
\frac{\partial \epsilon_i}{\partial \bar{x}} = \frac{\bar{x}-x_i}{\epsilon_i}
$$

What is then left to do is to calculate the $\frac{\partial \rho_{huber}(\epsilon_i, \sigma)}{\partial \epsilon_i}$:

$$
\begin{align*}
\frac{\partial \rho_{huber}(\epsilon_i, \sigma)}{\partial \epsilon_i} &= \frac{ \partial\left(\sigma^2\left(\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2} - 1\right)\right)}{\partial \epsilon_i} \\\\\\
&= \frac{ \partial\left(\sigma^2\left(\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}\right)\right)}{\partial \epsilon_i} &\text{ // Sum rule, }\sigma^2\text{ does not depend on }\bar{x}\\\\\\
&= \sigma^2\frac{ \partial\left(\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}\right)}{\partial \epsilon_i} \\\\\\
&= \sigma^2\frac{ \partial\sqrt{t}}{\partial t}\frac{\partial t}{\partial \epsilon_i} &\text{ // }t = 1 + \left(\frac{\epsilon_i}{\sigma}\right)^2 \\\\\\
&= \frac{1}{2}\sigma^2t^{-\frac{1}{2}}\frac{\partial (1 + (\frac{\epsilon_i}{\sigma})^2)}{\partial \epsilon_i} &\text{ // Power Rule}\\\\\\
&= \frac{1}{2}\sigma^2t^{-\frac{1}{2}}\frac{\partial (\frac{\epsilon_i}{\sigma})^2}{\partial \epsilon_i} &\text{ // Sum Rule, } 1\text{ does not depend on }\epsilon_i\\\\\\
&= \frac{1}{2}\sigma^2t^{-\frac{1}{2}}\frac{2\epsilon_i}{\sigma^2} \\\\\\
&= \frac{\epsilon_i}{\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}}
\end{align*}
$$

Putting the two together back into the derivative of the loss function:

$$
\begin{align*}
\frac{\partial L(\bar{a}, \mathcal{A})}{\partial \bar{x}} &= \sum_i^n \frac{\partial \rho_{huber}(\epsilon_i, \sigma)}{\partial \epsilon_i} \frac{\partial \epsilon_i}{\partial \bar{x}} \\\\\\ 
&= \sum_i^n\frac{\partial \rho_{huber}(\epsilon_i, \sigma)}{\partial \epsilon_i}\frac{1}{\epsilon_i}\left(\bar{x}-x_i\right) \\\\\\
&= \sum_i^n\frac{\epsilon_i}{\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}}\frac{1}{\epsilon_i}\left(\bar{x}-x_i\right) \\\\\\
&= \sum_i^n\frac{1}{\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}}(\bar{x}-x_i) = 0
\end{align*}
$$

Sadly, unlike when $\rho(x) = x^2$, the above formula still contains $\epsilon_i$. As such we can no longer isolate the value for $\bar{x}$ in a closed form. Instead, to find the robust estimate of the mean, we need to use an iterative approach. In this post we will use a variant of ["Iteratively Reweighted Least Squares" (IRLS)](https://en.wikipedia.org/wiki/Iteratively_reweighted_least_squares) technique. Let us write $w_i = 1/\left({\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}}\right)$, and let us further assume for a moment that the $\epsilon_i$ is not a function of $\bar{x}$. This means that we can keep the term $w_i$ fixed, which allows us to write the formula for the variable we are interested in:

$$
\begin{align}
\sum_i^nw_i(\bar{x}-x_i) &= 0 \nonumber \\\\\\
\sum_i^nw_i\bar{x} - \sum_i^nw_ix_i &= 0 \nonumber \\\\\\
\bar{x}\sum_i^nw_i &= \sum_i^nw_ix_i \nonumber \\\\\\
\bar{x} &= \frac{\sum_i^nw_ix_i}{\sum_i^nw_i}
\end{align}
$$

As you likely recognize, this is the formula for the weighted average! The weights need now to be chosen to discount the outliers that have been "skewing" the average estimate. Obviously initially we do not know what are the weights, but we also have a formula for those - $w_i = 1/\left({\sqrt{1 + (\frac{\epsilon_i}{\sigma})^2}}\right)$! With this we can design an algorithm to compute both the weights and the estimate of the mean iteratively:

$$
\begin{align*}
& \text{set all weights }w_i\text{ to }1 \\\\\\
& \textbf{Repeat }\text{until convergence:} \\\\\\
& \text{--- calculate }x^* = \frac{\sum_i^nw_ix_i}{\sum_i^nw_i} \\\\\\ 
& \text{--- calculate residuals } \epsilon_i = \\|x^* - x_i\\|_2 \\\\\\
& \text{--- calculate weights } w_i = \frac{1}{\epsilon_i}\frac{\partial \rho(\epsilon_i)}{\partial \epsilon_i} 
\end{align*}
$$

In the above recipe we write the general form of the $w_i$ for the IRLS framework, so that it can be adjusted to support any robust function, like Tukey's weights, Geman-McClure, etc. A good overview of different loss functions can be found in a paper by Black and Rangarajan[^black95], pages 41-48. Note that a single iteration of the above procedure will simply give us a regular mean, i.e. $x^* = \bar{x}$. However, as we run the algorithm multiple times, the resulting mean estimate is much closer to the true mean:

<!-- ![](robust_mean.png#center) -->
<img src='robust_mean_000.png#center' id="image"></img>
<div style="width:40%; margin: 0 auto; text-align:center;">
<input style="width:100%" type="range" id="iter_count" name="iter_count" min="0" max="9" value="0">
</div>

<script>
var slider = document.getElementById("iter_count");
var image = document.getElementById("image");
image.src = 'robust_mean_000.png#center';
slider.oninput = function() {
  image.src = 'robust_mean_00' + this.value + '.png#center';
}
</script> 

Before we end, it is important to underline why these function lead to discounting of the outliers. Hopefully this also clarifies how the robust functions were designed. If we consider our optimization procedure, the weights are defined as:
$$
w_i = \frac{1}{\epsilon_i}\frac{\partial \rho(\epsilon_i)}{\partial \epsilon_i}
$$
This means that the weights are proportional to the derivative of a function applied to our residuals. If we plot the derivative of the square function and Pseudo-Huber loss, it is clear to see that square function will result in high contributions from large errors, as the derivative of the square is a linear function. Conversely, with Pseudo-Huber loss we can see that large errors have a constant contribution, no matter how large the error gets.

![](derivatives.png#center)

To finish this post off, note that all the techniques that are shown here generalize to robust linear regression, where the residual takes the form of:
$$
\epsilon_i = y_i - f(x_i),
$$
with linear function $f$. I should most likely write down the derivation for this problem as well, but the reasoning is very similar.

I also need to point out that all of the information in this post is well known in statistics. If you wish to find out more, I'd recommend reading up on M-Estimators in statistics, and on IRLS in general. Also there is under-appreciated and somewhat now-forgotten piece of work by Michael Black and Rangarajan. Lastly, more recently Jon Barron has published a wonderful paper[^barron19] that introduced a general robust loss function - definitely give it a read!

Comments, questions? Message me on [twitter](https://twitter.com/maciejhalber)

[^barron19]: [A General and Adaptive Robust Loss Function](https://arxiv.org/abs/1701.03077); Jon Barron; CVPR 2019
[^black95]: [On the Unification of Line Processes, Outlier Rejection, and Robust Statistics with Applications in Early Vision](https://www.cise.ufl.edu/~anand/pdf/ijcv.pdf); Michael J. Black and Anand Rangarajan; IJCV 1995