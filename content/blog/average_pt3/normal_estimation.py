import numpy as np
from PIL import Image, ImageDraw


def estimate_normal(points, idx, n_neighbors):
  idx = 0
  q = X[idx,:]
  dists_and_inds = []
  for i in range(X.shape[0]):
    x = X[i, :]
    dist = np.linalg.norm( x - q )
    dists_and_inds.append((dist, i))

  dists_and_inds.sort()
  Q_ind = [ x[1] for x in dists_and_inds[0:5] ]
  Q = X[Q_ind, :]
  Q_cov = Q.T@Q
  eig_vals, eig_vecs = np.linalg.eig(Q_cov)
  eig_inds = eig_vals.argsort()[::-1]
  eig_vals = eig_vals[eig_inds]
  eig_vecs = eig_vecs[eig_inds]
  normal = eig_vecs[-1,:]

domain_size = 512

X1 = np.concatenate( ( [np.linspace(-0.9, 0.9, 10)], [np.ones(10)]), axis=0 ).T
X2 = np.concatenate( ( [np.linspace(-0.9, 0.9, 10)], [-1*np.ones(10)]), axis=0 ).T
X3 = np.concatenate( ( [np.ones(10)], [np.linspace(-0.9, 0.9, 10)]), axis=0 ).T
X4 = np.concatenate( ( [-1*np.ones(10)], [np.linspace(-0.9, 0.9, 10)]), axis=0 ).T

X = np.concatenate( (X1, X2, X3, X4) )

N1 = np.concatenate( ( [np.zeros(10)], [np.ones(10)]), axis=0 ).T
N2 = np.concatenate( ( [np.zeros(10)], [-1*np.ones(10)]), axis=0 ).T
N3 = np.concatenate( ( [np.ones(10)], [np.zeros(10)]), axis=0 ).T
N4 = np.concatenate( ( [-1*np.ones(10)], [np.zeros(10)]), axis=0 ).T

N = np.concatenate( (N1, N2, N3, N4) )


idx = 0
q = X[idx,:]
dists_and_inds = []
for i in range(X.shape[0]):
  x = X[i, :]
  dist = np.linalg.norm( x - q )
  dists_and_inds.append((dist, i))

dists_and_inds.sort()
Q_ind = [ x[1] for x in dists_and_inds[0:5] ]
Q = X[Q_ind, :]
Q_cov = Q.T@Q
eig_vals, eig_vecs = np.linalg.eig(Q_cov)
eig_inds = eig_vals.argsort()[::-1]
eig_vals = eig_vals[eig_inds]
eig_vecs = eig_vecs[eig_inds]
normal = eig_vecs[-1,:]


canvas = Image.new('RGB', (domain_size, domain_size), color = 'white')

d = ImageDraw.Draw(canvas)
theta = 1.0
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])

for i in range(N.shape[0]):
  x = X[i, :]
  n = N[i, :]
  x = 100*R@x + np.array([256,256])
  n = R@(50*n)
  d.line([x[0], x[1], x[0]+n[0], x[1]+n[1]], fill='blue', width=4)
  d.ellipse([x[0]-5, x[1]-5, x[0]+5, x[1]+5], fill='gray', outline='black', width=2)

x = 100*R@q + np.array([256,256])
n = R@(50*normal)
d.line([x[0], x[1], x[0]+n[0], x[1]+n[1]], fill='red', width=2)

canvas.show()