# Evaluating the Reliability of Shapley Value Estimates: An Interval-Based Approach

This repository contains the code associated to paper "Evaluating the Reliability of Shapley Value Estimates: An Interval-Based Approach" published at "2024 KDD Workshop on Human-Interpretable AI".

Extension with Neural approaches: https://ieeexplore.ieee.org/abstract/document/10584436 (code will be released soon!)

## Available Methods

**Reformulated** Interval Shapley Like Values:
- Reformulated Exact
- Reformulated Unbiased KernelSHAP
- Reformulated KernelSHAP
- Reformulated Monte Carlo

**Improved** Interval Shapley Like Values:
- Improved Exact
- Improved Unbiased KernelSHAP
- Improved KernelSHAP
- Improved Monte Carlo

## Available Metrics
- L2 distance on Mean point
- L2 distance on Interval Width
- Euclidean Distance between Intervals
- Computational Time

## Available Visualizations
- **BarPlot**: global or local
- **Coefficient of Variation**: global or local
- **TimeFeature**: computational times for different number of features dataset


## Example
The [example_isv](example_isv.ipynb) shows how to import different modelus to benchmark and visually compare ISLVs methods. 


## References

- Orginal implementation of Exact: [SHAP](https://github.com/shap/shap)
- Orgianl implementation of ShapleyRegression: [ShapReg](https://github.com/iancovert/shapley-regression)
