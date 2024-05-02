import numpy as np
import matplotlib.pyplot as plt
import time

class SingleLayerPerceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size, 1)
        self.bias = np.random.rand(1)

    def adaptive_learning_rate(self, X):
        return 1 / (1 + np.sum(X ** 2))

    def train(self, X, y, learning_rate, num_epochs, online_learning=True):
        errors = []
        start_time = time.time()

        for epoch in range(num_epochs):
            for i in range(X.shape[0]):
                output = self.predict(X[i])
                error = y[i] - output
                current_learning_rate = learning_rate * self.adaptive_learning_rate(X[i])
                self.weights += current_learning_rate * error * X[i].reshape(-1, 1)
                self.bias += current_learning_rate * error
            errors.append(np.mean((self.predict(X) - y) ** 2))

        end_time = time.time()
        training_time = end_time - start_time

        return errors, training_time

    def predict(self, x):
        return np.dot(x, self.weights) + self.bias

a = 1
b = 5
d = 0.1

np.random.seed(0)
X = np.random.rand(100, 3)
y = a * np.sin(b * X[:, 0]) + d + 0.1 * np.random.randn(100)

train_size = int(0.8 * X.shape[0])
X_train, y_train = X[:train_size, :], y[:train_size]
X_test, y_test = X[train_size:, :], y[train_size:]

X_tensor_train = X_train
y_tensor_train = y_train.reshape(-1, 1)

X_tensor_test = X_test
y_tensor_test = y_test.reshape(-1, 1)

model = SingleLayerPerceptron(input_size=3)

# Обучение сети с постоянным коэффициентом обучения (Online Learning)
errors_online_const, training_time_online_const = model.train(X_tensor_train, y_tensor_train, learning_rate=0.01, num_epochs=100, online_learning=True)

# Обучение сети с адаптивным коэффициентом обучения (Online Learning)
errors_online_adapt, training_time_online_adapt = model.train(X_tensor_train, y_tensor_train, learning_rate=0.01, num_epochs=100, online_learning=True)

# Обучение сети с постоянным коэффициентом обучения (Batch Learning)
errors_batch_const, training_time_batch_const = model.train(X_tensor_train, y_tensor_train, learning_rate=0.01, num_epochs=100, online_learning=False)

# Обучение сети с адаптивным коэффициентом обучения (Batch Learning)
errors_batch_adapt, training_time_batch_adapt = model.train(X_tensor_train, y_tensor_train, learning_rate=0.01, num_epochs=100, online_learning=False)

plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(errors_online_const, label='Online-Const')
plt.plot(errors_online_adapt, label='Online-Adapt')
plt.plot(errors_batch_const, label='Batch-Const')
plt.plot(errors_batch_adapt, label='Batch-Adapt')
plt.title('График изменения ошибок')
plt.xlabel('Эпохи')
plt.ylabel('Ошибка')
plt.legend()

plt.subplot(2, 1, 2)
y_pred_online_const = model.predict(X_tensor_test).flatten()
y_pred_online_adapt = model.predict(X_tensor_test).flatten() 
y_pred_batch_const = model.predict(X_tensor_test).flatten()  
y_pred_batch_adapt = model.predict(X_tensor_test).flatten()  

plt.plot(y_test, label='Истинные значения')
plt.plot(y_pred_online_const, label='Online-Const')
plt.plot(y_pred_online_adapt, label='Online-Adapt')  
plt.plot(y_pred_batch_const, label='Batch-Const')  
plt.plot(y_pred_batch_adapt, label='Batch-Adapt')  

plt.title('График прогноза значений')
plt.xlabel('Примеры')
plt.ylabel('Значения')
plt.legend()

plt.tight_layout()
plt.show()

print("{:<15} {:<10} {:<25} {:<15}".format("Тип обучения", "Эпохи", "Error", "Время выполнения"))
print("{:<15} {:<10} {:<25} {:<15}".format("Online-Const", len(errors_online_const), errors_online_const[-1], training_time_online_const))
print("{:<15} {:<10} {:<25} {:<15}".format("Online-Adapt", len(errors_online_adapt), errors_online_adapt[-1], training_time_online_adapt))
print("{:<15} {:<10} {:<25} {:<15}".format("Batch-Const", len(errors_batch_const), errors_batch_const[-1], training_time_batch_const))
print("{:<15} {:<10} {:<25} {:<15}".format("Batch-Adapt", len(errors_batch_adapt), errors_batch_adapt[-1], training_time_batch_adapt))
