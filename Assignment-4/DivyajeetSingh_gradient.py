import numpy as np
import time


X = np.arange(-20, 20, 0.1)
eps = np.random.rand(400) * 10
y = 23 * X + 43 + eps

ALPHA: float = 0.01
w: float = np.random.rand()
b: float = np.random.rand()

start_time = time.time()
for _ in range(10000):
    y_pred: np.ndarray = w * X + b
    w = w - ALPHA * np.mean((y_pred - y) * X)
    b = b - ALPHA * np.mean(y_pred - y)
end_time = time.time()

print(f"w = {w}, b = {b}")