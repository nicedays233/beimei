import numpy as np
rng = np.random.RandomState(42)
print(rng)
x: None = 10 * rng.rand(50)
print(x)
y = 2 * x - 1 + rng.randn(50)
