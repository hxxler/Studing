from sklearn.neural_network import BernoulliRBM
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    X = data.drop(columns=["RiskLevel"]).values
    y = data["RiskLevel"].factorize()[0]
    return X, y

def scale_data(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

def pretrain_rbm(X_train, layer_sizes):
    rbm_models = []
    input_data = X_train

    for size in layer_sizes:
        rbm = BernoulliRBM(n_components=size, learning_rate=0.01, n_iter=10, verbose=True)
        rbm.fit(input_data)
        rbm_models.append(rbm)
        input_data = rbm.transform(input_data)  # Проекция на следующее пространство

    return rbm_models

# Создание модели с предобученными весами RBM
class MLPWithRBM(nn.Module):
    def __init__(self, input_size, layer_sizes, num_classes, rbm_models):
        super(MLPWithRBM, self).__init__()
        self.layers = nn.ModuleList()
        prev_size = input_size

        for idx, size in enumerate(layer_sizes):
            layer = nn.Linear(prev_size, size)
            if rbm_models:
                # Инициализация весов из RBM
                layer.weight.data = torch.tensor(rbm_models[idx].components_.T, dtype=torch.float32)
            self.layers.append(layer)
            prev_size = size

        self.output_layer = nn.Linear(prev_size, num_classes)

    def forward(self, x):
        for layer in self.layers:
            x = torch.relu(layer(x))
        x = self.output_layer(x)
        return x
# Основной код
def main():
    # Загрузка данных
    file_path = r'IAD/lab3/Maternal Health Risk Data Set.csv'
    X, y = load_and_preprocess_data(file_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_scaled, X_test_scaled = scale_data(X_train, X_test)

    # Преобразование данных в тензоры
    X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    # Настройка слоев
    input_size = X_train.shape[1]
    num_classes = len(np.unique(y))
    layer_sizes = [64, 32, 16, 8]

    # Предобучение с RBM
    rbm_models = pretrain_rbm(X_train_scaled, layer_sizes)

    # Создание модели с предобученными весами RBM
    model_rbm = MLPWithRBM(input_size, layer_sizes, num_classes, rbm_models)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model_rbm.parameters(), lr=0.001)

    # Обучение модели
    epochs = 500
    for epoch in range(epochs):
        model_rbm.train()
        optimizer.zero_grad()
        outputs = model_rbm(X_train_tensor)
        loss = criterion(outputs, y_train_tensor)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

    # Оценка модели
    model_rbm.eval()
    with torch.no_grad():
        y_pred = torch.argmax(model_rbm(X_test_tensor), axis=1).numpy()

    # Метрики
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    main()
