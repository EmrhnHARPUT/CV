import numpy as np

def f(x):
    return x**2
x = 3
h = 0.00001

dx = (f(x+h) - f(x))/h


np.random.seed(42)
X = 2 * np.random.rand(100, 1) 
y = 4 + 3 * X + np.random.randn(100, 1)  

w = 0.0
b = 0.0

learning_rate = 0.1
epochs = 1000  
N = len(X)

for epoch in range(epochs):
    y_pred = w * X + b

    dw = (2 / N) * np.sum(X * (y_pred - y))
    db = (2 / N) * np.sum(y_pred-y)

    w = w - learning_rate * dw
    b = b - learning_rate * db

print(f"Eğitim Sonucu -> Hesaplanan w: {w:.2f}, Hesaplanan b: {b:.2f}")