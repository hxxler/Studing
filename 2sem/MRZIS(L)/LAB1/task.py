from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import torch
import torch.nn as nn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def preprocess_data(path: str, test_size=0.2, random_state=42):
    data = pd.read_csv(path)
    data["Sexybaby"] = data["Sexybaby"].map({"M": 1, "F": 0, "I": 3})
    return train_test_split(data, test_size=0.2, random_state=42)


class AutoEncoder(nn.Module):
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            torch.nn.Linear(input_dim, 9),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(9, encoding_dim),
            torch.nn.LeakyReLU()
        )
        self.decoder = nn.Sequential(
            torch.nn.Linear(encoding_dim, 9),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(9, input_dim),
            torch.nn.LeakyReLU()
        )

    def forward(self, x):
        code = self.encoder(x)
        reconstructed = self.decoder(code)
        return reconstructed


def train_autoencoder():
    X_train, X_test = preprocess_data("abalone.csv")
    X_train = torch.FloatTensor(np.array(X_train))
    X_test = torch.FloatTensor(np.array(X_test))
    train_loader = DataLoader(TensorDataset(X_train, X_train), batch_size=16, shuffle=True)
    test_loader = DataLoader(TensorDataset(X_test, X_test), batch_size=16)
    input_dim = X_train.shape[1]
    encoding_dim = 5
    model = AutoEncoder(input_dim, encoding_dim)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0003, betas=(0.9, 0.999))
    epochs = 30
    history = []
    for epoch in range(epochs):
        running_loss = 0.0
        for data in train_loader:
            inputs, _ = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        history.append(running_loss / len(train_loader))
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {running_loss / len(train_loader)}")
    with torch.no_grad():
        test_loss = 0.0
        for data in test_loader:
            inputs, _ = data
            outputs = model(inputs)
            test_loss += criterion(outputs, inputs).item()
        print(f"ae loss: {test_loss / len(test_loader)}")
    plt.plot([i for i in range(epochs)], history)
    plt.title("График ошибки")
    plt.show()


def pca(X, n_components):
    X_centered = X - np.mean(X, axis=0)
    covariance_matrix = np.cov(X_centered, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]
    top_eigenvectors = eigenvectors[:, :n_components]
    X_pca = np.dot(X_centered, top_eigenvectors)
    X_reconstructed = np.dot(X_pca, top_eigenvectors.T)
    reconstruction_error = np.mean(np.square(X_centered - X_reconstructed))
    return X_pca, reconstruction_error


def train_pca():
    data = np.array(preprocess_data("abalone.csv")[0])
    pca_data, pca_error = pca(data, 2)
    print("pca_error", pca_error)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=np.arange(1, 3), y=np.var(pca_data, axis=0) / np.sum(np.var(pca_data, axis=0)))
    plt.title('Важность компонент')
    plt.xlabel('Компонента')
    plt.ylabel('Доля объясненной дисперсии')

    plt.show()


def main():
    train_autoencoder()
    train_pca()


if __name__ == "__main__":
    main()
