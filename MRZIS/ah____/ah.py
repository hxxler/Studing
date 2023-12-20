import numpy as np

# Исходные данные
x1 = np.array([-4, -4, 2, 2])
x2 = np.array([-4, 2, -4, 2])
e = np.array([0, 1, 0, 1])
w1 = 0.1
w2 = 0.8
T = -0.3
alpha = 0.1

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

for epoch in range(3):
    print(f"Эпоха {epoch + 1}:")
    for i in range(len(x1)):
        S = sigmoid(w1 * x1[i] + w2 * x2[i] + T)

        E = 0.5 * (e[i] - S)**2

        w1 = w1 + alpha * (e[i] - S) * S * (1 - S) * x1[i]
        w2 = w2 + alpha * (e[i] - S) * S * (1 - S) * x2[i]
        T = T + alpha * (e[i] - S) * S * (1 - S)

        print(f"Наблюдение {i + 1}: S={S:.3f}, У={E:.4f}, w1={w1:.4f}, w2={w2:.4f}, T={T:.4f}")
    print("\n")

print("Окончательные значения:")
for i in range(len(x1)):
    S = sigmoid(w1 * x1[i] + w2 * x2[i] + T)
    E = 0.5 * (e[i] - S)**2
    print(f"Наблюдение {i + 1}: S={S:.3f}, У={E:.4f}")

print(f"Окончательные веса: w1={w1:.4f}, w2={w2:.4f}, T={T:.4f}")
