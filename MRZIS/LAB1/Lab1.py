import numpy as np
import matplotlib.pyplot as plt

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
reference = np.array([0, 0, 0, 1])

weights = np.random.rand(2)
bias = np.random.rand(1)

def threshold_activation(x):
    return 1 if x >= 0 else 0

threshold_activation = np.vectorize(threshold_activation)

learning_rate = 0.1
epochs = 10000

error_history = []

for epoch in range(epochs):
    error = 0
    for i in range(len(X)):
        input_data = X[i]
        net_input = np.dot(input_data, weights) + bias
        predicted_output = threshold_activation(net_input)
        error += np.sum(np.abs(reference[i] - predicted_output))
        weights += learning_rate * (reference[i] - predicted_output) * input_data
        bias += learning_rate * (reference[i] - predicted_output)
    error_history.append(error)
    if error == 0:
        break

def predict(input_data):
    for input_data_ in input_data:
        net_input = np.dot(input_data_, weights) + bias
        predicted_output = threshold_activation(net_input)
        print(f"Input: {input_data_}, Predicted Output: {predicted_output}")

predict(X)

print(f"Weights after training: {weights}")
print(f"Bias after training: {bias}")
print(f"Number of Epochs: {len(error_history)}")

xx, yy = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
zz = threshold_activation(weights[0] * xx + weights[1] * yy + bias)

plt.contourf(xx, yy, zz, levels=[-1, 0, 1], colors=('blue', 'red'), alpha=0.4)
plt.xlabel("Input Feature 1")
plt.ylabel("Input Feature 2")
plt.title("Decision Boundary")
plt.show()
