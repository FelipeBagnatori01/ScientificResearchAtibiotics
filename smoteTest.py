# Importações necessárias
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter

# Técnicas de balanceamento
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler, TomekLinks, EditedNearestNeighbours
from imblearn.combine import SMOTEENN, SMOTETomek
from imblearn.pipeline import Pipeline as ImbPipeline

# 1. CRIANDO DADOS DE EXEMPLO (dataset desbalanceado)
print("=== CRIANDO DATASET DESBALANCEADO ===")
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    n_clusters_per_class=1,
    weights=[0.9, 0.1],  # 90% classe 0, 10% classe 1
    random_state=42
)

print(f"Distribuição original: {Counter(y)}")

# 2. OPÇÃO 1: SMOTE + RandomUnderSampler (Pipeline)
print("\n=== OPÇÃO 1: SMOTE + RandomUnderSampler ===")
# Primeiro aplica SMOTE, depois undersampling
over = SMOTE(sampling_strategy=0.5, random_state=42)  # Aumenta classe minoritária para 50% da majoritária
under = RandomUnderSampler(sampling_strategy=0.8, random_state=42)  # Reduz classe majoritária

# Pipeline que aplica as técnicas em sequência
pipeline = ImbPipeline([
    ('over', over),
    ('under', under)
])

X_resampled1, y_resampled1 = pipeline.fit_resample(X, y)
print(f"Após SMOTE + UnderSampler: {Counter(y_resampled1)}")

# 3. OPÇÃO 2: SMOTETomek (SMOTE + Tomek Links)
print("\n=== OPÇÃO 2: SMOTETomek ===")
# Combina SMOTE com remoção de Tomek links (remove amostras ruidosas)
smote_tomek = SMOTETomek(
    sampling_strategy='auto',
    smote=SMOTE(sampling_strategy=0.7, random_state=42),
    tomek=TomekLinks(sampling_strategy='majority'),
    random_state=42
)

X_resampled2, y_resampled2 = smote_tomek.fit_resample(X, y)
print(f"Após SMOTETomek: {Counter(y_resampled2)}")

# 4. OPÇÃO 3: SMOTEENN (SMOTE + Edited Nearest Neighbours)
print("\n=== OPÇÃO 3: SMOTEENN ===")
# Combina SMOTE com ENN (remove amostras mal classificadas pelos vizinhos)
smote_enn = SMOTEENN(
    sampling_strategy='auto',
    smote=SMOTE(sampling_strategy=0.8, random_state=42),
    enn=EditedNearestNeighbours(sampling_strategy='majority'),
    random_state=42
)

X_resampled3, y_resampled3 = smote_enn.fit_resample(X, y)
print(f"Após SMOTEENN: {Counter(y_resampled3)}")

# 5. OPÇÃO 4: Controle manual das proporções
print("\n=== OPÇÃO 4: Controle Manual ===")
# Definir proporções específicas
target_majority = 5000  # Número desejado para classe majoritária
target_minority = 3000  # Número desejado para classe minoritária

# Primeiro SMOTE para aumentar a minoritária
smote_custom = SMOTE(
    sampling_strategy={1: target_minority},  # Classe 1 (minoritária) terá 3000 amostras
    random_state=42
)
X_temp, y_temp = smote_custom.fit_resample(X, y)

# Depois undersampling para reduzir a majoritária
under_custom = RandomUnderSampler(
    sampling_strategy={0: target_majority},  # Classe 0 (majoritária) terá 5000 amostras
    random_state=42
)
X_resampled4, y_resampled4 = under_custom.fit_resample(X_temp, y_temp)
print(f"Após controle manual: {Counter(y_resampled4)}")

# 6. COMPARANDO PERFORMANCE DOS MODELOS
print("\n=== COMPARANDO PERFORMANCE ===")

def avaliar_modelo(X_train, y_train, X_test, y_test, nome):
    modelo = RandomForestClassifier(random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    print(f"\n{nome}:")
    print(classification_report(y_test, y_pred))
    return modelo

# Dividir dados originais para teste
X_train_orig, X_test, y_train_orig, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Aplicar técnicas apenas no conjunto de treino
techniques = [
    (X_train_orig, y_train_orig, "Original (Desbalanceado)"),
    (X_resampled1[:int(0.8*len(X_resampled1))], y_resampled1[:int(0.8*len(y_resampled1))], "SMOTE + UnderSampler"),
    (X_resampled2[:int(0.8*len(X_resampled2))], y_resampled2[:int(0.8*len(y_resampled2))], "SMOTETomek"),
    (X_resampled3[:int(0.8*len(X_resampled3))], y_resampled3[:int(0.8*len(y_resampled3))], "SMOTEENN"),
]

# Avaliar cada técnica
for X_train, y_train, nome in techniques:
    avaliar_modelo(X_train, y_train, X_test, y_test, nome)

# 7. EXEMPLO COM DADOS REAIS (usando pandas)
print("\n=== EXEMPLO COM DATAFRAME ===")

# Criando um DataFrame de exemplo
df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
df['target'] = y

print(f"Dataset original shape: {df.shape}")
print(f"Distribuição: \n{df['target'].value_counts()}")

# Separar features e target
X_df = df.drop('target', axis=1)
y_df = df['target']

# Aplicar SMOTETomek
X_balanced, y_balanced = smote_tomek.fit_resample(X_df, y_df)

# Criar novo DataFrame balanceado
df_balanced = pd.DataFrame(X_balanced, columns=X_df.columns)
df_balanced['target'] = y_balanced

print(f"\nDataset balanceado shape: {df_balanced.shape}")
print(f"Nova distribuição: \n{df_balanced['target'].value_counts()}")

print("\n=== DICAS IMPORTANTES ===")
print("1. SMOTE + RandomUnderSampler: Mais simples e rápido")
print("2. SMOTETomek: Remove pares de Tomek (amostras muito próximas de classes diferentes)")
print("3. SMOTEENN: Remove amostras mal classificadas pelos vizinhos mais próximos")
print("4. Sempre aplicar balanceamento apenas no conjunto de treino!")
print("5. Avaliar diferentes estratégias e escolher a melhor para seu problema")