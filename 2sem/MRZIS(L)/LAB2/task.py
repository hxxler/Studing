import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from torch.nn import MSELoss
import numpy as np
import torch.nn as nn
import pandas as pd
import matplotlib.pyplot as plt

class AutoEncoder(nn.Module):
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 9),
            nn.LeakyReLU(),
            nn.Linear(9, encoding_dim),
            nn.LeakyReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 9),
            nn.LeakyReLU(),
            nn.Linear(9, input_dim),
            nn.LeakyReLU()
        )

    def forward(self, x):
        code = self.encoder(x)
        reconstructed = self.decoder(code)
        return reconstructed

class OjaDelta(torch.optim.Optimizer):
    def __init__(self, params, lr=0.01, delta=0.1):
        defaults = dict(lr=lr, delta=delta)
        super(OjaDelta, self).__init__(params, defaults)

    def step(self, closure=None):
        loss = None
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                d_p = p.grad.data
                lr = group['lr']
                delta = group['delta']
                p.data.add_(-lr * d_p)
                p.data.div_(torch.norm(p.data, p=2) / delta)
        return loss

class CumulativeDelta(torch.optim.Optimizer):
    def __init__(self, params, lr=0.01, alpha=0.01):
        defaults = dict(lr=lr, alpha=alpha)
        super(CumulativeDelta, self).__init__(params, defaults)
        self.prev_weight = None

    def step(self, closure=None):
        loss = None
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                   continue
            d_p = p.grad.data
            lr = group['lr']
            alpha = group['alpha']
            if self.prev_weight is not None:
                delta_eta = alpha * (p.data - self.prev_weight) / p.data
                p.data.add_(-lr * d_p)
                lr *= (1 + delta_eta)
            else:
                p.data.add_(-lr * d_p)
            self.prev_weight = p.data.clone()
            return loss

def preprocess_data(path: str, test_size=0.2, random_state=42):
    data = pd.read_csv(path)
    data["Sexybaby"] = data["Sexybaby"].map({"M": 1, "F": 0, "I": 3})
    return train_test_split(data, test_size=test_size, random_state=random_state)

def train_autoencoder(optimizer):
    X_train, X_test = preprocess_data("abalone.csv")
    X_train = torch.FloatTensor(np.array(X_train))
    X_test = torch.FloatTensor(np.array(X_test))
    train_loader = DataLoader(TensorDataset(X_train, X_train), batch_size=16, shuffle=True)
    test_loader = DataLoader(TensorDataset(X_test, X_test), batch_size=16)
    input_dim = X_train.shape[1]
    encoding_dim = 5
    model = AutoEncoder(input_dim, encoding_dim)
    criterion = nn.MSELoss()
    if optimizer == 'Oja':
        optimizer = OjaDelta(model.parameters(), lr=0.0003, delta=0.1)  # Using custom OjaDelta optimizer
    elif optimizer == 'CumulativeDelta':
        optimizer = CumulativeDelta(model.parameters(), lr=0.0003, alpha=0.01)  # Using custom CumulativeDelta optimizer
    else:
        raise ValueError("Unknown optimizer specified.")
    
    epochs = 50
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
        print(f"AE loss: {test_loss / len(test_loader)}")
    plt.plot([i for i in range(epochs)], history)
    plt.title("Loss Graph")
    plt.show()

def main():
    train_autoencoder('Oja')
    train_autoencoder('CumulativeDelta')

if __name__ == "__main__":
    main()
