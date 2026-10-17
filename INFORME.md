# Informe: Análisis y Mejora de Pruebas Unitarias

## 1. Datos

- **Nombre:** Álvaro José Nieto Osorio
- **Grupo:** 2
- **Fecha:** 17 de octubre de 2026
- **Repositorio:** https://github.com/alvarojnieto/pruebas_unitarias_devops
- **Resumen:** 59 pruebas con estructura AAA en 3 módulos (`calculadora`, `descuentos`, `csv_parser`) y 6 bugs encontrados y corregidos.
- **Extras:** pruebas de `csv_parser` con mocking (`unittest.mock.patch`), 2 bugs corregidos en un módulo no obligatorio (`csv_parser`) y GitHub Actions ejecutando pytest en cada push.

## 2. Análisis por módulo

### 2.1 calculadora.py

Módulo de operaciones matemáticas básicas: suma, resta, multiplicación, división, potencia, raíz cuadrada, promedio, máximo, mínimo, y área y perímetro de un rectángulo.

Casos que decidí probar y por qué:

- **Casos normales** (`sumar`, `restar`, `promedio`, área y perímetro): confirman que la fórmula base es correcta antes de buscar casos raros.
- **Casos límite numéricos** (`multiplicar` por 0, `potencia` con exponente 0, `restar` con resultado negativo, `maximo` con solo negativos): son los valores donde suelen fallar las implementaciones.
- **Entradas inválidas** (`dividir` por cero, `raiz_cuadrada` de un negativo, listas vacías en `promedio`, `maximo` y `minimo`, medidas negativas en el rectángulo): el módulo promete lanzar `ValueError` y hay que comprobar que lo cumple.
- **`minimo` con `[5, 3, 8]`**: elegí una lista de solo positivos porque la implementación original inicializaba el mínimo en 0.

Recorrí las funciones una por una preguntándome qué entrada podría romperlas. Escribí una prueba por cada validación, porque son ramas que solo se ejecutan con entradas inválidas y no se prueban por accidente.

Los comentarios `# BUG` del código me señalaron `raiz_cuadrada` y `minimo` como sospechosas, y escribí las pruebas para confirmar el fallo y ver con qué entradas ocurría. En `raiz_cuadrada`, `numero ** 0.5` no falla con un negativo: devuelve un número complejo, que pasaría desapercibido en otros cálculos. En `minimo`, la función compara contra 0 en lugar de contra los elementos de la lista, así que solo una lista de positivos lo revela.

### 2.2 descuentos.py

Módulo de descuentos e impuestos: descuento simple, monto del descuento, precio final con impuesto, descuento por volumen, descuentos acumulativos y descuentos apilados.

Casos que decidí probar y por qué:

- **`aplicar_descuento` y `calcular_descuento`** con 20% y 15%: verifican la fórmula base de la que dependen las demás funciones.
- **`calcular_precio_final` con `(100, 10, 20)`**: el resultado correcto (88) se calcula a mano y permite detectar si el impuesto se aplica sobre el precio equivocado.
- **`descuento_por_volumen` con 9, 10, 20, 50 y 100 unidades**: son los bordes de cada tramo, donde aparecen los errores de `>=` contra `>`.
- **`descuento_cumulativo` con `[10, 10]`**: debe dar 81 y no 80, lo que demuestra que los descuentos se encadenan.
- **`descuento_apilado` con `[60, 50]`**: la suma excede 100%, un caso fuera de rango.
- **Validaciones** (precio, impuesto, porcentaje y cantidad negativos, porcentaje mayor a 100, listas vacías): cubren las ramas de error de cada función.

Como casi todas las funciones dependen de `aplicar_descuento`, empecé por su fórmula base con valores que puedo calcular a mano.

Los comentarios del código señalaban `calcular_precio_final` y `descuento_apilado`, y calculé a mano el resultado esperado para compararlo con el del código. En `calcular_precio_final`, con precio 100, impuesto 10% y descuento 20%, lo correcto es 88 (80 más el 10% de 80), pero la función devolvía 90 porque calculaba el impuesto sobre el precio original, contradiciendo su propio comentario de "primero el descuento, luego el impuesto". En `descuento_apilado`, una suma mayor a 100% producía el error genérico de `aplicar_descuento`, que no explica que el problema es la suma de descuentos.

### 2.3 csv_parser.py

Módulo que interpreta contenido CSV recibido **como texto** (no abre archivos): separa líneas, convierte filas a diccionarios, valida el formato, extrae y filtra columnas, y cuenta filas y columnas.

Casos que decidí probar y por qué:

- **`parse_csv_line` con `a,"b,c",d`**: una coma dentro de comillas no debe separar campos.
- **`csv_a_diccionarios` con una fila de menos columnas**: los datos reales suelen venir incompletos.
- **`validar_csv`, `extraer_columna` y `filtrar_por_columna`** con filas cortas o contenido vacío: son los casos límite de entradas incompletas.
- **`contar_filas` y `contar_columnas`**: funciones sin pruebas previas, con caso normal y vacío.
- **Mocking:** como el módulo recibe texto y no abre archivos, no hay archivos que simular. Con `unittest.mock.patch` reemplacé `parse_csv_line` dentro de `leer_csv_como_lista` y comprobé que se llama una vez por línea, probando esa función sin depender de cómo se separan los campos.

Partí de un caso normal (`nombre,edad` con dos filas) y luego busqué entradas que rompieran el análisis: contenido vacío, filas con menos columnas que la cabecera y una coma dentro de comillas.

Los comentarios del código me señalaron las funciones sospechosas y escribí las pruebas para confirmarlo. En `parse_csv_line`, la rama que detecta comillas hacía lo mismo que la otra (`linea.split(',')`), así que `a,"b,c",d` producía cuatro campos con comillas sueltas en vez de tres. En `csv_a_diccionarios`, el bucle recorría la fila y no las cabeceras, por lo que una fila corta perdía las columnas faltantes en lugar de rellenarlas con vacío.

## 3. Tabla de bugs

| # | Función | Entrada que lo revela | Resultado erróneo | Resultado esperado | Corrección aplicada |
|---|---|---|---|---|---|
| 1 | `calculadora.raiz_cuadrada` | `-16` | Número complejo (`numero ** 0.5` no falla con negativos) | `ValueError` | Validar `numero < 0` y lanzar `ValueError` antes de calcular |
| 2 | `calculadora.minimo` | `[5, 3, 8]` | `0` (no está en la lista) | `3` | Inicializar `min_val = lista[0]` en vez de `0` |
| 3 | `descuentos.calcular_precio_final` | `(100, 10, 20)` | `90` | `88` | Calcular el impuesto sobre `precio_con_descuento` y no sobre `precio` |
| 4 | `descuentos.descuento_apilado` | `(100, [60, 50])` | `ValueError` genérico de `aplicar_descuento` (la suma es 110%) | `0` (tope en 100%) | `total_descuento = min(sum(descuentos), 100)` |
| 5 | `csv_parser.parse_csv_line` | `'a,"b,c",d'` | `['a', '"b', 'c"', 'd']` | `['a', 'b,c', 'd']` | [Confirma: reemplacé el cuerpo por `next(csv.reader([linea]))`, que respeta comas dentro de comillas y comillas escapadas] |
| 6 | `csv_parser.csv_a_diccionarios` | `"a,b,c\n1,2"` | `[{'a': '1', 'b': '2'}]` (falta la clave `c`) | `[{'a': '1', 'b': '2', 'c': ''}]` | Recorrer las cabeceras en vez de la fila y rellenar con `""` |

**Decisión de diseño (bug 4):** limité el descuento total a 100% en lugar de lanzar un error, porque un descuento mayor a 100% equivale a regalar el producto y el precio nunca debe quedar negativo. La alternativa, lanzar un `ValueError` explícito, obligaba a quien llama la función a validar la suma antes de usarla.

**Decisión de diseño (bug 6):** si una fila tiene más valores que cabeceras, los sobrantes se descartan, como ya hacía el código original.

Las pruebas que revelan cada bug se commitearon antes de su corrección (`test:` y luego `fix:`), y el historial del repositorio lo muestra.

## 4. Cobertura

Comando ejecutado:

```
pytest tests/ -v --cov=src --cov-report=term-missing
```

Salida:

```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src\__init__.py                0      0   100%
src\autenticacion.py          42     42     0%   6-77
src\calculadora.py            44      2    95%   22, 32
src\conversor.py              56     56     0%   6-94
src\csv_parser.py             73      2    97%   59, 117
src\descuentos.py             58      0   100%
src\fibonacci.py              42     42     0%   6-73
src\manipulador_texto.py      93     93     0%   6-156
src\procesador_texto.py       49     49     0%   6-84
src\utils.py                  53     53     0%   6-92
src\validador.py              64     64     0%   6-117
--------------------------------------------------------
TOTAL                        574    403    30%
================================================= 59 passed in 0.33s ==================================================
```

**Lectura de los resultados:**

Los tres módulos trabajados superan la meta de 85%: `descuentos.py` llegó a 100%, `csv_parser.py` a 97% y `calculadora.py` a 95%. Con las primeras pruebas partí de 70%, 71% y 62%, y el reporte `term-missing` me mostró qué faltaba: funciones sin ninguna prueba (`restar`, `multiplicar`, `potencia`, `contar_filas`, `filtrar_por_columna`) y las ramas de validación, que solo se ejecutan con entradas inválidas. Agregué pruebas puntuales para esas líneas hasta superar el umbral.

Quedan dos líneas sin cubrir en `calculadora.py` (22 y 32) y dos en `csv_parser.py` (59 y 117). En `calculadora.py` son los `return` del caso feliz de `dividir` y `raiz_cuadrada`: probé sus errores, pero no una operación válida. En `csv_parser.py` son las comprobaciones `len(lineas) == 0` de `validar_csv` y `contar_columnas`, que son código inalcanzable: `str.split('\n')` siempre devuelve al menos un elemento y el contenido vacío ya se resuelve antes con `if not contenido_csv`.

El TOTAL es de solo 30% porque `--cov=src` mide todos los módulos de la carpeta, y los otros siete (`autenticacion`, `conversor`, `fibonacci`, `manipulador_texto`, `procesador_texto`, `utils` y `validador`) no se trabajaron en este taller, así que aparecen en 0%. Lo que importa para la meta son las filas de los tres módulos trabajados.

## 5. Reflexión final

**¿Qué NO mide la cobertura?**

La cobertura solo mide qué líneas se ejecutaron durante las pruebas, no si el resultado de esas líneas es correcto. Una línea puede estar "cubierta" porque una prueba pasó por ella, aunque esa prueba no verifique nada útil o use valores con los que el error no se nota. Por ejemplo, una prueba de `calcular_precio_final` con impuesto 0 ejecutaría toda la función y daría un resultado correcto, pero ocultaría el bug del impuesto, porque con impuesto 0 el cálculo sobre el precio original y sobre el descontado coincide. Con `minimo` pasa algo parecido: una prueba con `[3, -1, 5]` recorre todo el código y devuelve el resultado correcto (`-1`), porque la función compara contra 0 y ese caso casualmente funciona. Solo con una lista de positivos como `[5, 3, 8]` aparece el error.

Tampoco mide la calidad de los datos de entrada ni las combinaciones posibles. `parse_csv_line` tenía una rama para las comillas que hacía exactamente lo mismo que la otra (`split(',')`), así que cualquier prueba con comillas ejecutaba esa línea y la daba por cubierta, aunque el resultado fuera incorrecto. La cobertura dice "esta línea se ejecutó", no "esta línea hace lo que debe". Además, no detecta lo que el código no contempla: `leer_csv_como_lista` separa el contenido por `\n` antes de analizar cada línea, así que un campo entre comillas que contenga un salto de línea se rompería, y ninguna métrica lo señalaría, porque no falta una línea de código sino un caso que nunca se consideró.

Por último, el porcentaje puede engañar en ambos sentidos. Mis tres módulos llegaron a 95%, 97% y 100%, pero eso no prueba que no queden bugs. Y las dos líneas sin cubrir en `csv_parser.py` son código inalcanzable, así que perseguir el 100% ahí no habría mejorado la calidad de las pruebas. Para mí la cobertura sirve para encontrar qué falta probar, pero la calidad la dan los casos límite bien elegidos y las aserciones que comparan contra un resultado calculado a mano.

**¿Qué aprendí?**

Lo primero que aprendí fue a leer la firma de una función antes de probarla. Escribí una prueba de `csv_parser` con `mock_open` suponiendo que `leer_csv_como_lista` recibía la ruta de un archivo, y falló con `[['reporte.csv']]`. Ese resultado me mostró que la función recibe el texto del CSV y trataba el nombre del archivo como contenido. No era un bug del código sino una suposición mía, y me enseñó a distinguir un hallazgo real de un error de la prueba. También cambié mi idea de lo que significa una prueba en rojo: dejó de ser un fracaso y pasó a ser la evidencia del bug, y por eso separé cada `test:` de su `fix:` en commits distintos.

También aprendí Git en la práctica. Me costó configurar la cuenta correcta, corregí un commit anterior con `fixup` y `rebase` sin dejar commits sueltos en el historial, y configuré GitHub Actions para que las pruebas corran en cada push. Si repitiera el taller, probaría desde el inicio todas las funciones de cada módulo en vez de descubrir en el reporte de cobertura que `filtrar_por_columna` y `contar_filas` no tenían ninguna prueba, y escribiría los comentarios AAA desde la primera versión de cada prueba.