import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models


file_path = 'Exasens.csv'
data = pd.read_csv(file_path)

data_clean = data.drop([0, 1]).reset_index(drop=True)

label_encoder_diagnosis = LabelEncoder()
label_encoder_id = LabelEncoder()

data_clean['Diagnosis'] = label_encoder_diagnosis.fit_transform(data_clean['Diagnosis'].dropna())
data_clean['ID'] = label_encoder_id.fit_transform(data_clean['ID'].dropna())

data_clean = data_clean.dropna(subset=['Diagnosis', 'ID'])

np.random.seed(42)
data_clean['Feature1'] = np.random.randn(len(data_clean))
data_clean['Feature2'] = np.random.randn(len(data_clean))
data_clean['Feature3'] = np.random.randn(len(data_clean))

features = ['Feature1', 'Feature2', 'Feature3']
X = data_clean[features]

X_scaled = StandardScaler().fit_transform(X)

def build_autoencoder(n_neurons):
    input_layer = layers.Input(shape=(X_scaled.shape[1],))
    encoded = layers.Dense(n_neurons, activation='relu')(input_layer)
    decoded = layers.Dense(X_scaled.shape[1], activation='sigmoid')(encoded)
    
    autoencoder = models.Model(input_layer, decoded)
    
    encoder = models.Model(input_layer, encoded)
    
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')
    
    return autoencoder, encoder

autoencoder_2, encoder_2 = build_autoencoder(2)
autoencoder_2.fit(X_scaled, X_scaled, epochs=50, batch_size=256, shuffle=True)

# Построим автоэнкодер с тремя нейронами в среднем слое
autoencoder_3, encoder_3 = build_autoencoder(3)
autoencoder_3.fit(X_scaled, X_scaled, epochs=50, batch_size=256, shuffle=True)

# Получаем проекции данных на 2 и 3 главные компоненты (через автоэнкодер)
X_encoded_2 = encoder_2.predict(X_scaled)
X_encoded_3 = encoder_3.predict(X_scaled)

# t-SNE с двумя компонентами
tsne_2 = TSNE(n_components=2)
X_tsne_2 = tsne_2.fit_transform(X_scaled)

# t-SNE с тремя компонентами
tsne_3 = TSNE(n_components=3)
X_tsne_3 = tsne_3.fit_transform(X_scaled)

#Визуализация --------------------
plt.figure(figsize=(12, 8))

# Визуализация автоэнкодера с двумя нейронами
plt.subplot(2, 2, 1)
plt.scatter(X_encoded_2[:, 0], X_encoded_2[:, 1], c=data_clean['Diagnosis'], cmap='viridis')
plt.title('Autoencoder - 2 neurons')
plt.xlabel('Component 1')
plt.ylabel('Component 2')

# Визуализация автоэнкодера с тремя нейронами
plt.subplot(2, 2, 2)
ax = plt.axes(projection='3d')
ax.scatter(X_encoded_3[:, 0], X_encoded_3[:, 1], X_encoded_3[:, 2], c=data_clean['Diagnosis'], cmap='viridis')
ax.set_title('Autoencoder - 3 neurons')
ax.set_xlabel('Component 1')
ax.set_ylabel('Component 2')
ax.set_zlabel('Component 3')

# Визуализация t-SNE с двумя компонентами
plt.subplot(2, 2, 3)
plt.scatter(X_tsne_2[:, 0], X_tsne_2[:, 1], c=data_clean['Diagnosis'], cmap='viridis')
plt.title('t-SNE - 2 components')
plt.xlabel('Component 1')
plt.ylabel('Component 2')

# Визуализация t-SNE с тремя компонентами
plt.subplot(2, 2, 4)
ax = plt.axes(projection='3d')
ax.scatter(X_tsne_3[:, 0], X_tsne_3[:, 1], X_tsne_3[:, 2], c=data_clean['Diagnosis'], cmap='viridis')
ax.set_title('t-SNE - 3 components')
ax.set_xlabel('Component 1')
ax.set_ylabel('Component 2')
ax.set_zlabel('Component 3')

plt.tight_layout()
plt.show()