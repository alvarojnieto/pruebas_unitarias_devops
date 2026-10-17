from src.csv_parser import (parse_csv_line, leer_csv_como_lista,
    csv_a_diccionarios, validar_csv, extraer_columna)

def test_leer_csv_como_lista_parsea_filas():    
    contenido = "nombre,edad\nAlvaro,26\nLuisa,23\n"    
    filas = leer_csv_como_lista(contenido)    
    assert len(filas) == 3

def test_parse_csv_line_respeta_coma_dentro_de_comillas():    
    linea = 'a,"b,c",d'    
    resultado = parse_csv_line(linea)    
    assert resultado == ["a", "b,c", "d"]


def test_csv_a_diccionarios_con_fila_de_menos_columnas():  
    contenido = "a,b,c\n1,2"    
    resultado = csv_a_diccionarios(contenido)    
    assert resultado == [{"a": "1", "b": "2", "c": ""}]


def test_validar_csv_con_columnas_inconsistentes_es_falso():    
    contenido = "a,b\n1,2,3"    
    resultado = validar_csv(contenido)    
    assert resultado is False


def test_extraer_columna_con_fila_corta_rellena_vacio():    
    contenido = "a,b\n1"    
    resultado = extraer_columna(contenido, 1)    
    assert resultado == ["b", ""]