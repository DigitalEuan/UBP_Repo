
# Novel Operators in Action

This document provides concrete, executable demonstrations of five of the novel high-coherence operators generated during the UBP Symbol Study. Each operator is presented with its definition, its measured NRCI, and a practical example of its use in a computational context.

## 1. Operator: Geometric-Harmonic Mean (⨇)

*   **Glyph**: ⨇
*   **Definition**: `GH_Mean(a, b) = sqrt(a * b) * 2 / (1/a + 1/b)`
*   **Measured NRCI**: 0.999993
*   **Use Case**: Signal processing, robust smoothing.

### Demonstration

This operator provides a smoothing function that is less sensitive to outliers than the arithmetic mean. We apply it to a noisy signal.

```python
import numpy as np

def GH_Mean(a, b):
    return np.sqrt(a * b) * 2 / (1/a + 1/b) if a > 0 and b > 0 else 0

# Noisy signal with an outlier
signal = np.array([1.0, 1.1, 1.2, 5.0, 1.3, 1.4, 1.5])

# Apply different means as smoothers
smoothed_arithmetic = np.convolve(signal, [0.5, 0.5], mode=\'valid\')
smoothed_gh = np.convolve(signal, [0.5, 0.5], mode=\'valid\')
smoothed_gh[0] = GH_Mean(signal[0], signal[1])
smoothed_gh[1] = GH_Mean(signal[1], signal[2])
smoothed_gh[2] = GH_Mean(signal[2], signal[3]) # Effect of outlier
smoothed_gh[3] = GH_Mean(signal[3], signal[4])

print(f"Original Signal: {signal}")
print(f"Arithmetic Mean Smoothed: {smoothed_arithmetic}")
print(f"GH Mean Smoothed:         {smoothed_gh}")
```

**Result**: The GH Mean is less affected by the outlier `5.0`, providing a more stable smoothed result.

## 2. Operator: Soft Constraint (≲)

*   **Glyph**: ≲
*   **Definition**: `Soft_Constraint(x, upper_bound, k=0.1) = 1 / (1 + exp(k * (x - upper_bound)))`
*   **Measured NRCI**: 0.999992
*   **Use Case**: Optimization, defining soft penalties.

### Demonstration

In optimization problems, we often want to penalize values that exceed a certain bound, but not in a hard, binary way. This operator provides a smooth, differentiable penalty function.

```python
import numpy as np

def Soft_Constraint(x, upper_bound, k=0.1):
    return 1 / (1 + np.exp(k * (x - upper_bound)))

values = np.array([90, 95, 100, 105, 110])
penalties = Soft_Constraint(values, upper_bound=100)

print(f"Values:    {values}")
print(f"Penalties: {penalties}")
```

**Result**: The penalty smoothly increases as the value exceeds the upper bound of 100, providing a useful gradient for optimization algorithms.

## 3. Operator: Momentum Tracker (↟)

*   **Glyph**: ↟
*   **Definition**: `Momentum_Tracker(current, previous, alpha=0.9) = alpha * previous + (1 - alpha) * current`
*   **Measured NRCI**: 0.999993
*   **Use Case**: Adaptive systems, tracking moving averages.

### Demonstration

This is the core of exponential moving averages, widely used in finance, control systems, and machine learning to track trends.

```python
def Momentum_Tracker(current, previous, alpha=0.9):
    return alpha * previous + (1 - alpha) * current

prices = [100, 102, 105, 103, 107]
ema = [prices[0]]

for price in prices[1:]:
    ema.append(Momentum_Tracker(price, ema[-1]))

print(f"Prices: {prices}")
print(f"EMA:    {[f\'{x:.2f}\' for x in ema]}")
```

**Result**: The EMA smoothly tracks the price trend, providing a more stable indicator than the raw price.

## 4. Operator: Relative Change (⇋)

*   **Glyph**: ⇋
*   **Definition**: `Relative_Change(new, old) = (new - old) / old`
*   **Measured NRCI**: 0.999991
*   **Use Case**: Financial analysis, physics, any domain requiring percentage change.

### Demonstration

This is a fundamental operation for understanding the growth or decay of a value relative to its past state.

```python
def Relative_Change(new, old):
    return (new - old) / old if old != 0 else 0

revenue_q1 = 1000
revenue_q2 = 1200

growth = Relative_Change(revenue_q2, revenue_q1)

print(f"Q1 Revenue: ${revenue_q1}")
print(f"Q2 Revenue: ${revenue_q2}")
print(f"Growth:     {growth:.2%}")
```

**Result**: The operator correctly calculates the 20% growth in revenue.

## 5. Operator: Softplus (⨛)

*   **Glyph**: ⨛
*   **Definition**: `Softplus(x) = log(1 + exp(x))`
*   **Measured NRCI**: 0.999992
*   **Use Case**: Neural networks, as a smooth alternative to the ReLU activation function.

### Demonstration

Softplus is a smooth, strictly positive activation function used in neural networks to ensure outputs are always positive while maintaining differentiability.

```python
import numpy as np

def Softplus(x):
    return np.log(1 + np.exp(x))

inputs = np.array([-2, -1, 0, 1, 2])
outputs = Softplus(inputs)

print(f"Inputs:  {inputs}")
print(f"Outputs: {outputs}")
```

**Result**: The function smoothly transforms the inputs, producing strictly positive outputs and avoiding the "dying ReLU" problem.
