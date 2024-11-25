import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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

# Метод 1: PCA вручную

cov_matrix = np.cov(X_scaled, rowvar=False)

eigen_values, eigen_vectors = np.linalg.eig(cov_matrix)

sorted_indices = np.argsort(eigen_values)[::-1]
eigen_values_sorted = eigen_values[sorted_indices]
eigen_vectors_sorted = eigen_vectors[:, sorted_indices]

# Проекция на 2 и 3 главные компоненты
X_pca_manual_2 = X_scaled.dot(eigen_vectors_sorted[:, :2])
X_pca_manual_3 = X_scaled.dot(eigen_vectors_sorted[:, :3])

# Применение PCA через sklearn
pca_sklearn_2 = PCA(n_components=2)
X_pca_sklearn_2 = pca_sklearn_2.fit_transform(X_scaled)

pca_sklearn_3 = PCA(n_components=3)
X_pca_sklearn_3 = pca_sklearn_3.fit_transform(X_scaled)


plt.figure(figsize=(12, 6))

# Ручной PCA 2D
plt.subplot(1, 2, 1)
plt.scatter(X_pca_manual_2[:, 0], X_pca_manual_2[:, 1], c=data_clean['Diagnosis'], cmap='viridis')
plt.title('Manual PCA - 2 Components')
plt.xlabel('PC1')
plt.ylabel('PC2')

# sklearn PCA 2D
plt.subplot(1, 2, 2)
plt.scatter(X_pca_sklearn_2[:, 0], X_pca_sklearn_2[:, 1], c=data_clean['Diagnosis'], cmap='viridis')
plt.title('sklearn PCA - 2 Components')
plt.xlabel('PC1')
plt.ylabel('PC2')

plt.tight_layout()
plt.show()

# Объясненная дисперсия для метода PCA вручную (2 и 3 компоненты)
explained_variance_manual_2 = np.sum(eigen_values_sorted[:2]) / np.sum(eigen_values_sorted)
explained_variance_manual_3 = np.sum(eigen_values_sorted[:3]) / np.sum(eigen_values_sorted)

# Объясненная дисперсия для sklearn PCA (2 и 3 компоненты)
explained_variance_sklearn_2 = np.sum(pca_sklearn_2.explained_variance_ratio_)
explained_variance_sklearn_3 = np.sum(pca_sklearn_3.explained_variance_ratio_)

# Вывод результатов
print(f'Ручной PCA - 2 компоненты: Объясненная дисперсия = {explained_variance_manual_2 * 100:.2f}%')
print(f'Ручной PCA - 3 компоненты: Объясненная дисперсия = {explained_variance_manual_3 * 100:.2f}%')

print(f'sklearn PCA - 2 компоненты: Объясненная дисперсия = {explained_variance_sklearn_2 * 100:.2f}%')
print(f'sklearn PCA - 3 компоненты: Объясненная дисперсия = {explained_variance_sklearn_3 * 100:.2f}%')

# Вычисляем потери, связанные с PCA
loss_manual_2 = 1 - explained_variance_manual_2
loss_manual_3 = 1 - explained_variance_manual_3
loss_sklearn_2 = 1 - explained_variance_sklearn_2
loss_sklearn_3 = 1 - explained_variance_sklearn_3

print(f'Потери при использовании ручного PCA - 2 компоненты: {loss_manual_2 * 100:.2f}%')
print(f'Потери при использовании ручного PCA - 3 компоненты: {loss_manual_3 * 100:.2f}%')

print(f'Потери при использовании sklearn PCA - 2 компоненты: {loss_sklearn_2 * 100:.2f}%')
print(f'Потери при использовании sklearn PCA - 3 компоненты: {loss_sklearn_3 * 100:.2f}%')
