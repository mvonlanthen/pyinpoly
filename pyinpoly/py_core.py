import numpy as np
from .pyinpoly import pts_in_polygon_rs

def pts_in_polygon(points, poly, include_edges=True, parallel=True):
    '''
    Compute which points are inside and/or on the edges of a polygon. The 
    polygon must be closed, hence the last point must be equal to the first one.

    This function calls the Rust implementation. about 10x (serial) to 40x 
    (parallel) faster than the pure Python implenetation (pts_in_polygon_py).

    Usage
    -----
    isin = pts_in_polygon(points, poly, include_edges=True, parallel=True)

    Arguments
    ---------
    points: np.array. points.shape=(N,2)
        List of N points.
    poly: np.array. poly.shape=(M+1,2)
        Corners of the polygon. Closed polygon, hence the first point must be 
        equal to the first point (no check done in the function!).
    include_edges: bool. default: True
        Defines how the points exactly on the edges should be processed. If 
        `True`, these points will be concidered inside the polygon. No epsilon! 
        A edge point is 100% on the edge, or it's not.]
    parallel: bool. default: True
        Parallel execution

    Returns
    -------
    isin: np.array of bool. isin.shape=(N,)
        True for the points inside the polygon.
    '''
    return pts_in_polygon_rs(points, poly, include_edges, parallel)

def pts_in_polygon_py(points, poly, include_edges=True):
    '''
    Compute which points are inside and/or on the edges of a polygon. The 
    polygon must be closed, hence the last point must be equal to the first one.

    This is the pure Python implentation. Use the function `pts_in_polygon` for 
    better performance (much better!!)

    Usage
    -----
    isin = pts_in_polygon_py(points, poly, include_edges=True)

    Arguments
    ---------
    points: np.array. points.shape=(N,2)
        List of N points.
    poly: np.array. poly.shape=(M+1,2)
        Corners of the polygon. Closed polygon, hence the first point must be 
        equal to the first point (no check done in the function!).
    include_edges: bool. default: True
        Defines how the points exactly on the edges should be processed. If 
        `True`, these points will be concidered inside the polygon. No epsilon! 
        A edge point is 100% on the edge, or it's not.

    Returns
    -------
    isin: np.array of bool. isin.shape=(N,)
        True for the points inside the polygon.
    '''
    # chech arguments
    if points.shape[1]!=2:
        raise ValueError(
            ('The dimension of the second axis of `points` must be equal to 2 '
             '(i.e 2D points), not {}.').format(points.shape[1])
        )
    if poly.shape[1]!=2:
        raise ValueError(
            ('The dimension of the second axis of `poly` must be equal to 2 '
             '(i.e 2D polygon), not {}.').format(poly.shape[1])
        )

    xs = points[:,0]
    ys = points[:,1]
    n = len(poly)
    is_inside = np.zeros(len(xs),bool)
    on_edge = np.zeros(len(xs),bool)
    indices = np.arange(len(xs))

    # loop through each edges defined by (p1, p2)
    p1x, p1y = poly[0]
    for i in range(1, n):
        p2x, p2y = poly[i%n]
        if p1y == p2y:
            # test if points are on horizontal edge
            bidx = (ys==p1y) & ((xs>=min(p1x, p2x)) & (xs<max(p1x, p2x)))
            on_edge[bidx] = True          
        else: # p1y!= p2y
            # select all points will horizonlta right ray crossing the segment and 
            # scompute the intersections
            c_bidx = (ys>=min(p1y, p2y)) & (ys<max(p1y, p2y))
            idx = indices[c_bidx]
            xinters = (ys[c_bidx] - p1y) * (p2x - p1x) / float(p2y - p1y) + p1x

            # point is right on the edge
            bidx = xs[c_bidx]==xinters
            on_edge[idx[bidx]] = True

            # point is to the left from current edge
            bidx = xs[c_bidx]<xinters
            is_inside[idx[bidx]] = ~is_inside[idx[bidx]]
        # go to next edge
        p1x, p1y = p2x, p2y
        
        # add the on
        if include_edges:
            is_inside[on_edge==True] = True
        else:
            is_inside[on_edge==True] = False

    return is_inside