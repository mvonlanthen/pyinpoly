// use ndarray::{ArrayD, ArrayViewD, Array1, Axis};
use numpy::{IntoPyArray, PyReadonlyArray2, PyArray1};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};
use inpolygon::pts_in_polygon;

/// Find if a list of points is inside of a polygon.
#[pymodule]
fn pyinpoly(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    // wrapper of `inpolygon::pts_in_polygon`. Python docstring below (with triple /)
    /// Compute which points are inside and/or on the edges of a polygon. The 
    /// polygon must be closed, hence the last point must be equal to the first one.
    /// 
    /// This is Rust implementation. about 10x (serial) to 40x (parallel) faster 
    /// than the pure Python implenetation (pts_in_polygon_py).
    /// 
    /// Usage
    /// -----
    /// isin = pts_in_polygon_rs(points, poly, include_edges, parallel)
    /// 
    /// Arguments
    /// ---------
    /// points: np.array. points.shape=(N,2)
    ///     List of N points.
    /// poly: np.array. poly.shape=(M+1,2)
    ///     Corners of the polygon. Closed polygon, hence the first point must be 
    ///     equal to the first point (no check done in the function!).
    /// include_edges: bool
    ///     Defines how the points exactly on the edges should be processed. If 
    ///     `True`, these points will be concidered inside the polygon. No epsilon! 
    ///     A edge point is 100% on the edge, or it's not.]
    /// parallel: bool
    ///     Parallel execution
    /// 
    /// Returns
    /// -------
    /// isin: np.array of bool. isin.shape=(N,)
    ///     True for the points inside the polygon.
    #[pyfn(m, "pts_in_polygon_rs")]
    fn pts_in_polygon_rs<'py>(
        py: Python<'py>,
        points: PyReadonlyArray2<f64>,
        polygon: PyReadonlyArray2<f64>,
        include_edges: bool,
        parallel: bool
    ) -> &'py PyArray1<bool> {
        let points = points.as_array();
        let polygon = polygon.as_array();
        let is_inside = pts_in_polygon(&points, &polygon, include_edges, parallel);
        return is_inside.into_pyarray(py);
    }

    Ok(())
}