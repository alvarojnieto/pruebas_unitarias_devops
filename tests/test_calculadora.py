import pytest
from src.calculadora import (sumar, restar, multiplicar, dividir, potencia,
    raiz_cuadrada, promedio, maximo, minimo,
    calcular_area_rectangulo, calcular_perimetro_rectangulo)


def test_sumar_positivos():
    # Arrange
    a, b = 7, 5
    # Act
    resultado = sumar(a, b)
    # Assert
    assert resultado == 12


def test_restar_con_resultado_negativo():
    # Arrange
    a, b = 3, 10
    # Act
    resultado = restar(a, b)
    # Assert
    assert resultado == -7


def test_multiplicar_por_cero():
    # Arrange
    a, b = 8, 0
    # Act
    resultado = multiplicar(a, b)
    # Assert
    assert resultado == 0


def test_dividir_por_cero_lanza_error():
    # Arrange
    a, b = 10, 0
    # Act / Assert
    with pytest.raises(ValueError):
        dividir(a, b)


def test_potencia_con_exponente_cero():
    # Arrange
    base, exponente = 5, 0
    # Act
    resultado = potencia(base, exponente)
    # Assert
    assert resultado == 1


def test_raiz_cuadrada_de_negativo_lanza_error():   # BUG 1
    # Arrange
    numero = -16
    # Act / Assert
    with pytest.raises(ValueError):
        raiz_cuadrada(numero)


def test_promedio_de_lista_normal():
    # Arrange
    lista = [2, 4, 6]
    # Act
    resultado = promedio(lista)
    # Assert
    assert resultado == 4


def test_promedio_de_lista_vacia_lanza_error():
    # Arrange
    lista = []
    # Act / Assert
    with pytest.raises(ValueError):
        promedio(lista)


def test_maximo_con_numeros_negativos():
    # Arrange
    lista = [-5, -2, -9]
    # Act
    resultado = maximo(lista)
    # Assert
    assert resultado == -2


def test_maximo_de_lista_vacia_lanza_error():
    # Arrange
    lista = []
    # Act / Assert
    with pytest.raises(ValueError):
        maximo(lista)


def test_minimo_de_positivos_devuelve_el_menor():   # BUG 2
    # Arrange
    lista = [5, 3, 8]
    # Act
    resultado = minimo(lista)
    # Assert
    assert resultado == 3


def test_minimo_de_lista_vacia_lanza_error():
    # Arrange
    lista = []
    # Act / Assert
    with pytest.raises(ValueError):
        minimo(lista)


def test_area_rectangulo_de_4_por_5():
    # Arrange
    base, altura = 4, 5
    # Act
    resultado = calcular_area_rectangulo(base, altura)
    # Assert
    assert resultado == 20


def test_area_rectangulo_con_base_negativa_lanza_error():
    # Arrange
    base, altura = -1, 5
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_area_rectangulo(base, altura)


def test_perimetro_rectangulo_de_4_por_5():
    # Arrange
    base, altura = 4, 5
    # Act
    resultado = calcular_perimetro_rectangulo(base, altura)
    # Assert
    assert resultado == 18


def test_perimetro_rectangulo_con_altura_negativa_lanza_error():
    # Arrange
    base, altura = 4, -5
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_perimetro_rectangulo(base, altura)