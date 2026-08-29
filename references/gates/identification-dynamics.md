# Identification, Dynamics, and Path Gates

## 7. Identifiability and inverse-problem factorization

Separate instrument/geometry, gain/noise, and target state. Determine whether observations identify the requested parameter, a product/ratio/integral, or only an equivalence class. Use known templates or analytic features for initialization before joint refinement when possible.

Low residual is insufficient. Require forward replay, perturbation sensitivity, parameter correlation/rank, holdout geometry/conditions, and an independent reconstruction or formula. When not identifiable, report a set, interval, conditional result, or required extra experiment.

## 8. Continuous dynamics, hybrid modes, and contact

When arrival, collision, threshold crossing, valve opening, failure, release, detonation, saturation, or contact changes equations, list each mode, entry condition, state update, exit condition, and invariant. Do not average mode changes into one smooth curve without an error bound.

For contact, check non-penetration, nonnegative contact force, and complementarity when relevant. For collisions and occlusion, use the full physical object, not only centers or sampled points, unless the reduction is proven safe.

## 9. Trajectory and event constraints

Endpoint feasibility does not imply path feasibility. Check first/last crossing, duration above/below threshold, continuous collision-free motion, coverage gaps, queue overflow, and constraint violation between samples. Use coarse grids only to bracket; refine event times and demonstrate step/tolerance convergence.

For segmented paths or regions, audit connections, seams, and cross-region interactions after recombination.
