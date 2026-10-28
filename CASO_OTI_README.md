# Caso OTI: Análisis de Method Resolution Order (MRO) en Herencia Múltiple

## Contexto del Problema

La Oficina de Tecnologías de la Información (OTI) de la UNSCH desarrolla un sistema de matrícula para el semestre 2026-II. Dos estudiantes en **idéntica situación** fueron cobrados **montos distintos** por el sistema:

- **Luis Huamaní Cárdenas** pagó: **S/ 60.00**
- **Rosa Ccahuana Prado** pagó: **S/ 45.00**

**Situación idéntica:**
- Becarios por violencia sociopolítica
- Índice académico desaprobatorio
- Matriculados fuera de fecha

**Causa:** Dos programadores diseñaron jerarquías de herencia con órdenes distintos, resultando en diferencias en el **Method Resolution Order (MRO)**.

## Preguntas a Resolver

### 1. ¿Qué clases están involucradas y qué tipo de relación existe entre ellas?

**Clases:**
- `Matrícula`: clase base, costo S/ 60.00
- `BecaViolencia`: paga la mitad del monto (÷ 2)
- `ÍndiceDesaprobatorio`: recargo de S/ 15.00
- `MatrículaExtemporánea`: recargo de S/ 15.00

**Tipo de relación:** Herencia lineal cooperativa con `super()`, donde cada clase hereda de la anterior y reutiliza el cálculo de su clase padre.

### 2. ¿En qué orden Python resolvería el cálculo en cada versión?

#### Versión 1 (Programador A): Beca → Desaprobatorio → Extemporánea

```
MRO: MatrículaExtemporáneasV1 → ÍndiceDesaprobatorioV1 → BecaViolenciaV1 → MatrículaV1 → object

Cálculo:
  60.00 (base)
  ÷ 2    = 30.00 (beca aplicada PRIMERO)
  + 15   = 45.00 (índice desaprobatorio)
  + 15   = 60.00 (matrícula extemporánea)

TOTAL: S/ 60.00
```

#### Versión 2 (Programador B): Desaprobatorio → Extemporánea → Beca

```
MRO: BecaViolenciaV2 → MatrículaExtemporáneasV2 → ÍndiceDesaprobatorioV2 → MatrículaV2 → object

Cálculo:
  60.00 (base)
  + 15   = 75.00 (índice desaprobatorio)
  + 15   = 90.00 (matrícula extemporánea)
  ÷ 2    = 45.00 (beca aplicada AL FINAL)

TOTAL: S/ 45.00
```

### 3. ¿Cuánto pagó cada estudiante?

- **Luis Huamaní (Versión 1):** S/ 60.00
- **Rosa Ccahuana (Versión 2):** S/ 45.00
- **Diferencia:** S/ 15.00

### 4. ¿Causa de la diferencia? ¿Por qué ninguno cometió error de sintaxis?

**CAUSA PRECISA:**

La diferencia depende de **CUÁNDO se aplica la beca (÷ 2)**:

- **Versión 1:** Beca se aplica al monto base → 60 ÷ 2 = 30, luego +15 +15 = **60**
- **Versión 2:** Beca se aplica después de recargos → (60 + 15 + 15) ÷ 2 = **45**

**¿Por qué ninguno cometió error de sintaxis?**

Ambos códigos son **sintácticamente válidos** en Python. El problema es **SEMÁNTICO**:

- El `super()` hace que el orden de ejecución sea **OCULTO** en la definición de las clases
- Python lo resuelve usando **MRO (Method Resolution Order)**, que sigue el algoritmo C3 Linearization
- El MRO depende del **orden en que se heredan las clases**
- Dos órdenes diferentes = dos MROs diferentes = dos resultados diferentes

**Conclusión:** El comportamiento sorprendente no es un bug de Python, es una característica de la herencia cooperativa con `super()`. Los dos programadores no se equivocaron en sintaxis, pero obtuvieron resultados diferentes por una razón **oculta** en la definición de clases.

### 5. ¿Qué pasa si se combina la matrícula general con una especialización escribiendo primero la general?

```python
class CombinacionMala(MatrículaBase, BecaViolencia):
    pass
```

**RESULTADO:**
```
TypeError: Cannot create a consistent method resolution order (MRO) 
for bases MatrículaBase, BecaViolencia
```

**EXPLICACIÓN:**

- `BecaViolencia` ya hereda de `MatrículaBase`
- Intentar `class X(MatrículaBase, BecaViolencia)` es **REDUNDANTE**
- `MatrículaBase` aparece dos veces en la jerarquía
- Python no puede crear un MRO consistente
- Esto previene errores silenciosos pero revela malas decisiones de diseño

### 6. Rediseño Propuesto

**Problema con el diseño actual:**
- El orden es OCULTO en la jerarquía de clases
- No se puede cambiar el orden sin reescribir jerarquías
- El comportamiento depende de un detalle que no es obvio

**Solución: Patrón de Modificadores Explícitos**

En lugar de herencia múltiple con `super()`, usar **composición** con una lista de modificadores:

```python
class Modificador:
    def aplicar(self, costo):
        raise NotImplementedError

class ModExtemporanea(Modificador):
    def aplicar(self, costo):
        return costo + 15.0

class ModDesaprobatorio(Modificador):
    def aplicar(self, costo):
        return costo + 15.0

class ModBecaViolencia(Modificador):
    def aplicar(self, costo):
        return costo / 2.0

class Estudiante:
    def __init__(self, nombre, modificadores):
        self.nombre = nombre
        self.modificadores = modificadores  # ORDEN EXPLÍCITO
    
    def calcular_costo(self):
        costo = 60.0
        for mod in self.modificadores:
            costo = mod.aplicar(costo)
        return costo

# CADA ESTUDIANTE DEFINE SU PROPIO ORDEN
luis = Estudiante("Luis", [
    ModDesaprobatorio(),
    ModExtemporanea(),
    ModBecaViolencia()  # Beca al final → S/ 45.00
])

rosa = Estudiante("Rosa", [
    ModBecaViolencia(),     # Beca al inicio → S/ 60.00
    ModDesaprobatorio(),
    ModExtemporanea()
])
```

**VENTAJAS:**

1. **Orden EXPLÍCITO:** visible en el constructor, no oculto en la jerarquía
2. **Flexible por estudiante:** cada uno define su propio orden sin reescribir clases
3. **Auditable:** revisa la lista de modificadores → entiendes el cálculo
4. **Sin sorpresas de MRO:** `super()` no oculta el comportamiento
5. **Testeable:** cada modificador es una función pura
6. **Mantenible:** agregar nuevos modificadores es trivial
7. **Control total:** la OTI puede decidir el orden por estudiante, o establecer un estándar

## Archivos Incluidos

- **`caso_oti_completo.py`**: Código ejecutable con ambas versiones, análisis de MRO, y solución con patrón de modificadores
- **`Caso_OTI_Análisis.docx`**: Documento Word con colores y formato profesional

## Cómo Ejecutar

```bash
python3 caso_oti_completo.py
```

**Salida esperada:**
- Análisis de MRO de ambas versiones
- Cálculos paso a paso
- Demostración del error de combinación
- Ejemplo de solución con modificadores explícitos

## Verificación

```bash
# Verificar que el código ejecuta sin errores
python3 -m py_compile caso_oti_completo.py

# Ejecutar y capturar salida
python3 caso_oti_completo.py > salida.txt
```

## Respuestas Resumidas (Checklist)

- **Pregunta 1:** Clases identificadas, tipo de relación: herencia lineal cooperativa
- **Pregunta 2:** MRO de cada versión determinado, orden de ejecución explicado
- **Pregunta 3:** Costos calculados: Luis S/ 60, Rosa S/ 45
- **Pregunta 4:** Causa explicada (cuándo se aplica beca), ninguno tiene error sintáctico
- **Pregunta 5:** Error de MRO demostrado y explicado
- **Pregunta 6:** Rediseño propuesto con patrón de modificadores implementado

## Conceptos Clave Aprendidos

- **Method Resolution Order (MRO):** Orden en que Python busca métodos en una jerarquía
- **super():** Llamada cooperativa a método de clase padre
- **C3 Linearization:** Algoritmo que Python usa para calcular el MRO
- **Herencia múltiple:** Peligros y cómo evitarlos
- **Patrón Modificador:** Alternativa flexible a herencia compleja
- **Composición sobre herencia:** Principio de diseño de software

---

**Nota:** Este caso es un ejemplo clásico en la enseñanza de Python sobre las complejidades de la herencia múltiple y por qué la composición es frecuentemente preferible.
