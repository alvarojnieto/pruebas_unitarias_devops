import pytest
from src.calculadora import sumar, dividir, raiz_cuadrada, promedio, maximo, minimo


def test_sumar_positivos():
    # Arrange
    a, b = 7, 5
    # Act
    resultado = sumar(a, b)
    # Assert
    assert resultado == 12
    
def test_dividir_por_cero_lanza_error():
    with pytest.raises(ValueError):
        dividir(10, 0)

def test_raiz_cuadrada_de_negativo_lanza_error():    
    numero = -16   
    with pytest.raises(ValueError):
        raiz_cuadrada(numero)

def test_minimo_de_positivos_devuelve_el_menor():      
    lista = [5, 3, 8]    
    resultado = minimo(lista)    
    assert resultado == 3


def test_promedio_de_lista_normal():
    lista = [2, 4, 6]   
    resultado = promedio(lista)   
    assert resultado == 4


def test_promedio_de_lista_vacia_lanza_error():    
    lista = []    
    with pytest.raises(ValueError):
        promedio(lista)


def test_maximo_con_numeros_negativos():   
    lista = [-5, -2, -9]    
    resultado = maximo(lista)   
    assert resultado == -2