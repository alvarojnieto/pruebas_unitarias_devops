import pytest
from src.descuentos import (aplicar_descuento, calcular_descuento,
    calcular_precio_final, descuento_por_volumen,
    descuento_cumulativo, descuento_apilado)


def test_aplicar_descuento_del_20_por_ciento():
    # Arrange
    precio, porcentaje = 100, 20
    # Act
    resultado = aplicar_descuento(precio, porcentaje)
    # Assert
    assert resultado == 80


def test_aplicar_descuento_con_precio_negativo_lanza_error():
    # Arrange
    precio, porcentaje = -10, 10
    # Act / Assert
    with pytest.raises(ValueError):
        aplicar_descuento(precio, porcentaje)


def test_aplicar_descuento_con_porcentaje_mayor_a_100_lanza_error():
    # Arrange
    precio, porcentaje = 100, 101
    # Act / Assert
    with pytest.raises(ValueError):
        aplicar_descuento(precio, porcentaje)


def test_calcular_descuento_devuelve_el_monto():
    # Arrange
    precio, porcentaje = 200, 15
    # Act
    resultado = calcular_descuento(precio, porcentaje)
    # Assert
    assert resultado == 30


def test_calcular_descuento_con_precio_negativo_lanza_error():
    # Arrange
    precio, porcentaje = -10, 10
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_descuento(precio, porcentaje)


def test_calcular_descuento_con_porcentaje_negativo_lanza_error():
    # Arrange
    precio, porcentaje = 100, -5
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_descuento(precio, porcentaje)


def test_calcular_precio_final_aplica_impuesto_sobre_precio_descontado():   # BUG 3
    # Arrange
    precio, impuesto, descuento = 100, 10, 20
    # Act
    resultado = calcular_precio_final(precio, impuesto, descuento)
    # Assert
    assert resultado == pytest.approx(88)   # 80 + 10% de 80


def test_calcular_precio_final_con_precio_negativo_lanza_error():
    # Arrange
    precio, impuesto, descuento = -10, 5, 0
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_precio_final(precio, impuesto, descuento)


def test_calcular_precio_final_con_impuesto_negativo_lanza_error():
    # Arrange
    precio, impuesto, descuento = 100, -5, 10
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_precio_final(precio, impuesto, descuento)


def test_calcular_precio_final_con_descuento_mayor_a_100_lanza_error():
    # Arrange
    precio, impuesto, descuento = 100, 5, 101
    # Act / Assert
    with pytest.raises(ValueError):
        calcular_precio_final(precio, impuesto, descuento)


def test_descuento_por_volumen_con_9_unidades_no_tiene_descuento():
    # Arrange
    cantidad, precio_unitario = 9, 10
    # Act
    resultado = descuento_por_volumen(cantidad, precio_unitario)
    # Assert
    assert resultado == pytest.approx(90)


def test_descuento_por_volumen_con_10_unidades_aplica_5_por_ciento():
    # Arrange
    cantidad, precio_unitario = 10, 10
    # Act
    resultado = descuento_por_volumen(cantidad, precio_unitario)
    # Assert
    assert resultado == pytest.approx(95)


def test_descuento_por_volumen_con_20_unidades_aplica_10_por_ciento():
    # Arrange
    cantidad, precio_unitario = 20, 10
    # Act
    resultado = descuento_por_volumen(cantidad, precio_unitario)
    # Assert
    assert resultado == pytest.approx(180)


def test_descuento_por_volumen_con_50_unidades_aplica_15_por_ciento():
    # Arrange
    cantidad, precio_unitario = 50, 10
    # Act
    resultado = descuento_por_volumen(cantidad, precio_unitario)
    # Assert
    assert resultado == pytest.approx(425)


def test_descuento_por_volumen_con_100_unidades_aplica_20_por_ciento():
    # Arrange
    cantidad, precio_unitario = 100, 10
    # Act
    resultado = descuento_por_volumen(cantidad, precio_unitario)
    # Assert
    assert resultado == pytest.approx(800)


def test_descuento_por_volumen_con_cantidad_negativa_lanza_error():
    # Arrange
    cantidad, precio_unitario = -1, 10
    # Act / Assert
    with pytest.raises(ValueError):
        descuento_por_volumen(cantidad, precio_unitario)


def test_descuento_por_volumen_con_precio_unitario_negativo_lanza_error():
    # Arrange
    cantidad, precio_unitario = 5, -1
    # Act / Assert
    with pytest.raises(ValueError):
        descuento_por_volumen(cantidad, precio_unitario)


def test_descuento_cumulativo_con_dos_descuentos_de_10():
    # Arrange
    precio, descuentos = 100, [10, 10]
    # Act
    resultado = descuento_cumulativo(precio, descuentos)
    # Assert
    assert resultado == pytest.approx(81)


def test_descuento_cumulativo_con_lista_vacia_devuelve_el_precio():
    # Arrange
    precio, descuentos = 100, []
    # Act
    resultado = descuento_cumulativo(precio, descuentos)
    # Assert
    assert resultado == 100


def test_descuento_cumulativo_con_descuento_invalido_lanza_error():
    # Arrange
    precio, descuentos = 100, [101]
    # Act / Assert
    with pytest.raises(ValueError):
        descuento_cumulativo(precio, descuentos)


def test_descuento_cumulativo_con_precio_negativo_lanza_error():
    # Arrange
    precio, descuentos = -10, [10]
    # Act / Assert
    with pytest.raises(ValueError):
        descuento_cumulativo(precio, descuentos)


def test_descuento_apilado_que_excede_100_se_limita_a_100():   # BUG 4
    # Arrange
    precio, descuentos = 100, [60, 50]
    # Act
    resultado = descuento_apilado(precio, descuentos)
    # Assert
    assert resultado == 0


def test_descuento_apilado_con_lista_vacia_devuelve_el_precio():
    # Arrange
    precio, descuentos = 100, []
    # Act
    resultado = descuento_apilado(precio, descuentos)
    # Assert
    assert resultado == 100


def test_descuento_apilado_con_precio_negativo_lanza_error():
    # Arrange
    precio, descuentos = -10, [10]
    # Act / Assert
    with pytest.raises(ValueError):
        descuento_apilado(precio, descuentos)