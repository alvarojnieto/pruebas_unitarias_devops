import pytest
from src.descuentos import (aplicar_descuento, calcular_descuento,
    calcular_precio_final)


def test_aplicar_descuento_del_20_por_ciento():    
    precio, porcentaje = 100, 20   
    resultado = aplicar_descuento(precio, porcentaje)   
    assert resultado == 80


def test_calcular_descuento_devuelve_el_monto():    
    precio, porcentaje = 200, 15    
    resultado = calcular_descuento(precio, porcentaje)    
    assert resultado == 30


def test_calcular_precio_final_aplica_impuesto_sobre_precio_descontado(): 
    precio, impuesto, descuento = 100, 10, 20    
    resultado = calcular_precio_final(precio, impuesto, descuento)   
    assert resultado == pytest.approx(88)  


