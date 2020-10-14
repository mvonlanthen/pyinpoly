# pyinpoly
Compute whether a given point in the plane lies inside, outside, or on the boundary of a polygon. This package use the [ray casting algorithm](https://en.wikipedia.org/wiki/Point_in_polygon). To imporve execution speed, the algorithm is written in Rust. The pure Python version is also available, mostly for benchmark purposes.

## Examples
Toy example
```python
import numpy as np
import matplotlib.pyplot as plt
import pyinpoly

polygon = np.array([
    [1,-1], [1,1], [-0.5,1], [-1,0], [-1,-1], [1,-1],
]).astype(float)

points = np.array([
    [0, 0], [0,2], [2,0], [1,0], [0,1], [-2,0], [-0.75,1], [-1,1], [0,-1], 
    [-1,0], [-1,-1], [1,-1], [-1,-0.5]
]).astype(float)

# pure Python version
isin_py = pyinpoly.pts_in_polygon_py(points, polygon, include_edges=True)

# Rust based version
isin_rs = pyinpoly.pts_in_polygon(points, polygon, include_edges=True, parallel=True)

# let's plot the results of both function
fig = plt.figure(figsize=[8,12])
ax = fig.add_subplot(211)
ax.plot(polygon[:,0], polygon[:,1], 'v-', ms=5)
ax.plot(points[isin_py,0], points[isin_py,1] , 'o', c='green', label='inside')
ax.plot(points[~isin_py,0], points[~isin_py,1] , 'o', c='red', label='outside')
ax.grid()
ax.legend(loc='upper left')
t = ax.set_title('Pure Python algorithm', fontsize=14)

ax = fig.add_subplot(212)
ax.plot(polygon[:,0], polygon[:,1], 'v-', ms=5)
ax.plot(points[isin_rs,0], points[isin_rs,1] , 'o', c='green', label='inside')
ax.plot(points[~isin_rs,0], points[~isin_rs,1] , 'o', c='red', label='outside')
ax.grid()
ax.legend(loc='upper left')
t = ax.set_title('Rust based algorithm', fontsize=14)
```

Benchmark example
```python
import numpy as np
import pyinpoly

# parameters
nb_polygon_pts = 10 
nb_points = 1_000_000

# creare a random polygon and a random list of points
polygon = 4*(np.random.rand(nb_polygon_pts+1,2)-0.5)
polygon[-1] = polygon[0]
points = 4*(np.random.rand(nb_points,2)-0.5)

tic = time.time()
isin_py = pyinpoly.pts_in_polygon_py(points, polygon, include_edges=True)
toc = time.time()
print('Python exec time: {:.06f}s'.format(toc-tic))

tic = time.time()
isin_rs = pyinpoly.pts_in_polygon(points, polygon, include_edges=True, parallel=True)
toc = time.time()
print('Rust exec time (parallel): {:.06f}s'.format(toc-tic))

tic = time.time()
isin_rs = pyinpoly.pts_in_polygon(points, polygon, include_edges=True, parallel=False)
toc = time.time()
print('Rust exec time (serial):   {:.06f}s'.format(toc-tic))
```

## Installation

### Install with Python wheel
1. Download the latest wheel here
2. install with
```bash
pip install pyinpoly-0.4.0-cp38-cp38-manylinux1_x86_64.whl
```

### compile the wheel
1. download and install the [Rust Programming Language](https://www.rust-lang.org/). The Rust compiler is included in the installer.
2. install `maturin`, which is used to compile the Rust library into a python package
    ```bash
    pip install maturin
    ```
2. Clone this repository.
3. inside the cloned repository, compile the Rust library with
    ```bash
    maturin develop --release
    maturin build --release
    ```
4. The command generate a wheel in `target/wheel`, which can be installed with 
    ```bash
    pip install target/wheel/pyinpoly-0.4.0-cp38-cp38-manylinux1_x86_64.whl
    ```