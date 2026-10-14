from src.csv_parser import leer_csv_como_lista


def test_leer_csv_como_lista_parsea_filas():    
    contenido = "nombre,edad\nAlvaro,26\nLuisa,23\n"    
    filas = leer_csv_como_lista(contenido)    
    assert len(filas) == 3