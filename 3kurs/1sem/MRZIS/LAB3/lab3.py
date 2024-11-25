import numpy as np
import matplotlib.pyplot as plt
import time

np.random.seed(42)
X = np.random.uniform(low=-10, high=10, size=(1000, 1))
noise = np.random.normal(0, 5, size=(1000, 1))
y = 2 * X - 3 + noise
y = np.where(y > 0, 1, 0) 

noise_points = 50
X_noise = np.random.uniform(low=-10, high=10, size=(noise_points, 1))
y_noise = np.random.choice([0, 1], size=(noise_points, 1), p=[0.5, 0.5])
X = np.vstack([X, X_noise])
y = np.concatenate([y, y_noise])

split_index = int(0.8 * len(X))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

def adaptive_learning_rate(t, X):
    return 1 / (1 + np.sum(X**2))

def predict(X, weights):
    return 1 / (1 + np.exp(-(np.dot(X, weights))))

def train(X, y, epochs=100, learning_rate=0.01):
    weights = np.zeros((X.shape[1], 1))
    history = []
    for epoch in range(epochs):
        for i in range(len(X)):
            prediction = predict(X[i], weights)
            gradient = (y[i] - prediction) * prediction * (1 - prediction) * X[i][:, np.newaxis]
            weights += learning_rate / (1 + np.sum(X[i]**2)) * gradient
        loss = -np.mean(y * np.log(predict(X, weights)) + (1 - y) * np.log(1 - predict(X, weights)))
        history.append(loss)
    return weights, history

start_time = time.time()
weights, history = train(X_train, y_train, epochs=100)
training_time_adaptive_lr_custom = time.time() - start_time

plt.plot(range(1, len(history)+1), history, label='Training Loss')
plt.title('Training Loss over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

def predict_binary(X, weights):
    return np.where(predict(X, weights) > 0.5, 1, 0)

y_pred_binary = predict_binary(X_test, weights)

def calculate_accuracy(y_true, y_pred):
    correct_predictions = np.sum(y_true == y_pred)
    total_samples = len(y_true)
    accuracy = correct_predictions / total_samples
    return accuracy

test_accuracy_adaptive_lr_custom = calculate_accuracy(y_test, y_pred_binary)

print("Adaptive Learning Rate (Custom Model) Results:")
print("Test Accuracy:", test_accuracy_adaptive_lr_custom)
print("Training Time:", training_time_adaptive_lr_custom)
