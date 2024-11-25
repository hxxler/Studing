import numpy as np

np.random.seed(0)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) 
y = np.array([0, 1, 1, 0]) 

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

input_neurons = X.shape[1]  
hidden_neurons = 4 
output_neurons = 1 
learning_rate = 0.1  

weights_input_hidden = np.random.uniform(size=(input_neurons, hidden_neurons))
weights_hidden_output = np.random.uniform(size=(hidden_neurons, output_neurons))


epochs = 10000  

for epoch in range(epochs):

    hidden_input = np.dot(X, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)
    output_input = np.dot(hidden_output, weights_hidden_output)
    predicted_output = sigmoid(output_input)

    error = y.reshape(-1, 1) - predicted_output
    
    output_error = error * sigmoid_derivative(predicted_output)
    hidden_layer_error = output_error.dot(weights_hidden_output.T) * sigmoid_derivative(hidden_output)

    weights_hidden_output += hidden_output.T.dot(output_error) * learning_rate
    weights_input_hidden += X.T.dot(hidden_layer_error) * learning_rate

test_input = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
predicted_output = sigmoid(np.dot(sigmoid(np.dot(test_input, weights_input_hidden)), weights_hidden_output))

print("Предсказанные значения для входных данных XOR:")
print(predicted_output.ravel())