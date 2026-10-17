import pytest
from src.descuentos import (aplicar_descuento, calcular_descuento,
    calcular_precio_final, descuento_por_volumen,
    descuento_cumulativo, descuento_apilado)


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


def test_descuento_por_volumen_con_9_unidades_no_tiene_descuento():
    cantidad, precio_unitario = 9, 10    
    resultado = descuento_por_volumen(cantidad, precio_unitario)   
    assert resultado == pytest.approx(90)


def test_descuento_por_volumen_con_100_unidades_aplica_20_por_ciento():
    cantidad, precio_unitario = 100, 10   
    resultado = descuento_por_volumen(cantidad, precio_unitario)    
    assert resultado == pytest.approx(800)


def test_descuento_cumulativo_con_dos_descuentos_de_10():    
    precio, descuentos = 100, [10, 10]    
    resultado = descuento_cumulativo(precio, descuentos)    
    assert resultado == pytest.approx(81)


def test_descuento_apilado_que_excede_100_se_limita_a_100():    
    precio, descuentos = 100, [60, 50]    
    resultado = descuento_apilado(precio, descuentos)    
    assert resultado == 0