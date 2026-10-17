from unittest.mock import patch
from src.csv_parser import (parse_csv_line, leer_csv_como_lista,
    csv_a_diccionarios, validar_csv, extraer_columna,
    filtrar_por_columna, contar_filas, contar_columnas)


def test_leer_csv_como_lista_parsea_filas():
    # Arrange
    contenido = "nombre,edad\nAlvaro,26\nLuisa,23\n"
    # Act
    filas = leer_csv_como_lista(contenido)
    # Assert
    assert len(filas) == 3
    assert filas[1] == ["Alvaro", "26"]


def test_leer_csv_como_lista_con_contenido_vacio_devuelve_lista_vacia():
    # Arrange
    contenido = ""
    # Act
    resultado = leer_csv_como_lista(contenido)
    # Assert
    assert resultado == []


def test_leer_csv_como_lista_con_parse_mockeado():   # EXTRA: mocking
    # Arrange
    contenido = "linea1\nlinea2"
    # Act
    with patch("src.csv_parser.parse_csv_line", return_value=["x"]) as falso:
        resultado = leer_csv_como_lista(contenido)
    # Assert
    assert resultado == [["x"], ["x"]]
    assert falso.call_count == 2


def test_parse_csv_line_respeta_coma_dentro_de_comillas():   # BUG 5
    # Arrange
    linea = 'a,"b,c",d'
    # Act
    resultado = parse_csv_line(linea)
    # Assert
    assert resultado == ["a", "b,c", "d"]


def test_parse_csv_line_con_linea_vacia_devuelve_lista_vacia():
    # Arrange
    linea = ""
    # Act
    resultado = parse_csv_line(linea)
    # Assert
    assert resultado == []


def test_csv_a_diccionarios_con_fila_de_menos_columnas():   # BUG 6
    # Arrange
    contenido = "a,b,c\n1,2"
    # Act
    resultado = csv_a_diccionarios(contenido)
    # Assert
    assert resultado == [{"a": "1", "b": "2", "c": ""}]


def test_csv_a_diccionarios_sin_filas_de_datos_devuelve_lista_vacia():
    # Arrange
    contenido = "a,b"
    # Act
    resultado = csv_a_diccionarios(contenido)
    # Assert
    assert resultado == []


def test_csv_a_diccionarios_con_contenido_vacio_devuelve_lista_vacia():
    # Arrange
    contenido = ""
    # Act
    resultado = csv_a_diccionarios(contenido)
    # Assert
    assert resultado == []


def test_validar_csv_con_columnas_inconsistentes_es_falso():
    # Arrange
    contenido = "a,b\n1,2,3"
    # Act
    resultado = validar_csv(contenido)
    # Assert
    assert resultado is False


def test_validar_csv_con_columnas_consistentes_es_verdadero():
    # Arrange
    contenido = "a,b\n1,2"
    # Act
    resultado = validar_csv(contenido)
    # Assert
    assert resultado is True


def test_validar_csv_con_contenido_vacio_es_falso():
    # Arrange
    contenido = ""
    # Act
    resultado = validar_csv(contenido)
    # Assert
    assert resultado is False


def test_extraer_columna_con_fila_corta_rellena_vacio():
    # Arrange
    contenido = "a,b\n1"
    # Act
    resultado = extraer_columna(contenido, 1)
    # Assert
    assert resultado == ["b", ""]


def test_extraer_columna_con_contenido_vacio_devuelve_lista_vacia():
    # Arrange
    contenido = ""
    # Act
    resultado = extraer_columna(contenido, 0)
    # Assert
    assert resultado == []


def test_filtrar_por_columna_devuelve_solo_coincidencias():
    # Arrange
    contenido = "n,c\nAna,x\nLuis,y"
    # Act
    resultado = filtrar_por_columna(contenido, 1, "x")
    # Assert
    assert resultado == [["Ana", "x"]]


def test_filtrar_por_columna_con_contenido_vacio_devuelve_lista_vacia():
    # Arrange
    contenido = ""
    # Act
    resultado = filtrar_por_columna(contenido, 0, "x")
    # Assert
    assert resultado == []


def test_contar_filas_de_csv_con_tres_lineas():
    # Arrange
    contenido = "a,b,c\n1,2,3\n4,5,6\n"
    # Act
    resultado = contar_filas(contenido)
    # Assert
    assert resultado == 3


def test_contar_filas_de_contenido_vacio_es_cero():
    # Arrange
    contenido = ""
    # Act
    resultado = contar_filas(contenido)
    # Assert
    assert resultado == 0


def test_contar_columnas_usa_la_primera_fila():
    # Arrange
    contenido = "a,b,c\n1,2,3\n"
    # Act
    resultado = contar_columnas(contenido)
    # Assert
    assert resultado == 3


def test_contar_columnas_de_contenido_vacio_es_cero():
    # Arrange
    contenido = ""
    # Act
    resultado = contar_columnas(contenido)
    # Assert
    assert resultado == 0