# Regresión No Lineal Múltiple: Beverage Sales vs Temperature y Promotion

# Importar bibliotecas necesarias
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.pipeline import make_pipeline

# Importar el dataset
dataset = pd.read_csv('beverage_sales.csv', encoding='latin1')

# Seleccionar las columnas relevantes
X = dataset[['Temperature (°C)', 'Promotion']]
y = dataset['Beverage Sales']

# Dividir el dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)

# Crear y entrenar modelo polinómico
poly_features = PolynomialFeatures(degree=2, include_bias=False)
model = make_pipeline(poly_features, LinearRegression())
model.fit(X_train, y_train)

# Predecir valores
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Función para graficar con líneas de regresión no lineal
def plot_regression(X, y, y_pred, title, ax):
    # Ordenar los valores para una línea suave
    sorted_idx = np.argsort(X['Temperature (°C)'])
    X_sorted = X.iloc[sorted_idx]
    y_pred_sorted = y_pred[sorted_idx]
    
    # Graficar puntos reales
    scatter = ax.scatter(X['Temperature (°C)'], y, c=X['Promotion'], cmap='coolwarm', alpha=0.7)
    
    # Graficar línea de regresión para Promoción=1
    mask_promo = X_sorted['Promotion'] == 1
    ax.plot(X_sorted['Temperature (°C)'][mask_promo], y_pred_sorted[mask_promo], 
            color='red', label='Con Promoción', linewidth=2)
    
    # Graficar línea de regresión para Promoción=0
    mask_no_promo = X_sorted['Promotion'] == 0
    ax.plot(X_sorted['Temperature (°C)'][mask_no_promo], y_pred_sorted[mask_no_promo], 
            color='blue', label='Sin Promoción', linewidth=2)
    
    ax.set_title(title)
    ax.set_xlabel('Temperatura (°C)')
    ax.set_ylabel('Ventas de Bebidas')
    ax.legend()
    plt.colorbar(scatter, ax=ax, label='Promoción (0=No, 1=Sí)')

# Crear figura con dos subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# Graficar conjunto de entrenamiento
plot_regression(X_train, y_train, y_train_pred, 'Entrenamiento: Regresión No Lineal', ax1)

# Graficar conjunto de prueba
plot_regression(X_test, y_test, y_test_pred, 'Prueba: Regresión No Lineal', ax2)

plt.tight_layout()
plt.show()

# Mostrar métricas
print(f'R² Entrenamiento: {r2_score(y_train, y_train_pred):.3f}')
print(f'R² Prueba: {r2_score(y_test, y_test_pred):.3f}')
print(f'MSE Entrenamiento: {mean_squared_error(y_train, y_train_pred):.3f}')
print(f'MSE Prueba: {mean_squared_error(y_test, y_test_pred):.3f}')

# Mostrar ecuación del modelo
feature_names = poly_features.get_feature_names_out(input_features=X.columns)
coefficients = model.named_steps['linearregression'].coef_
intercept = model.named_steps['linearregression'].intercept_

print("\nEcuación del modelo:")
print(f"Ventas = {intercept:.2f}")
for name, coef in zip(feature_names, coefficients):
    print(f" + ({coef:.2f} * {name})")