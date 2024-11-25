import numpy as np
import matplotlib.pyplot as plt

def generate_data(num_points, a, b, c, d):
    x = np.linspace(0, 10, num_points)
    y = a * np.cos(b * x) + c * np.sin(d * x)
    return x, y

a = 0.4
b = 0.4
c = 0.08
d = 0.4
num_points = 100

x_train, y_train = generate_data(num_points, a, b, c, d)

plt.plot(x_train, y_train, label='Generated Data')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Generated Data')
plt.legend()
plt.show()

class RNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        self.W_hh = np.random.randn(hidden_size, hidden_size)
        self.W_xh = np.random.randn(hidden_size, input_size)
        self.W_hy = np.random.randn(output_size, hidden_size)
        self.b_h = np.zeros((hidden_size, 1))
        self.b_y = np.zeros((output_size, 1))

    def forward(self, inputs, h_prev):
        self.inputs = inputs
        self.h_prev = h_prev
        self.h_next = np.tanh(np.dot(self.W_xh, inputs) + np.dot(self.W_hh, h_prev) + self.b_h)
        self.output = np.dot(self.W_hy, self.h_next) + self.b_y
        return self.output, self.h_next

    def backward(self, d_output, learn_rate):
        d_h_next = np.dot(self.W_hy.T, d_output)
        d_h = (1 - self.h_next ** 2) * d_h_next
        self.W_hy -= learn_rate * np.dot(d_output, self.h_next.T)
        self.W_hh -= learn_rate * np.dot(d_h, self.h_prev.T)
        self.W_xh -= learn_rate * np.dot(d_h, self.inputs.T)
        self.b_y -= learn_rate * d_output
        self.b_h -= learn_rate * d_h
        return d_h

input_size = 1
hidden_size = 12
output_size = 1
learn_rate = 0.0005
num_epochs = 1701

rnn = RNN(input_size, hidden_size, output_size)

for epoch in range(num_epochs):
    loss = 0
    h_prev = np.zeros((hidden_size, 1))
    
    for i in range(num_points - 1):
        x = np.array([[y_train[i]]])
        y_true = np.array([[y_train[i+1]]])
        
        y_pred, h_prev = rnn.forward(x, h_prev)
        
        loss += np.square(y_pred - y_true)
        
        d_output = 2 * (y_pred - y_true)
        rnn.backward(d_output, learn_rate)
    
    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss[0][0]}')

predictions = []
h_prev = np.zeros((hidden_size, 1))
for i in range(num_points):
    # x = np.array([[x_train[i]]]).T
    x = np.array([[y_train[i]]])
    y_pred, h_prev = rnn.forward(x, h_prev)
    predictions.append(y_pred[0][0])

plt.plot(x_train, y_train, label='Generated Data')
plt.plot(x_train, predictions, label='Predictions')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Generated Data vs Predictions')
plt.legend()
plt.show()
