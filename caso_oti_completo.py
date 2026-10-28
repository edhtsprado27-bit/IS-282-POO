"""
===============================================================================
CASO OTI: ANÁLISIS COMPLETO DE METHOD RESOLUTION ORDER (MRO)
===============================================================================
"""

print("=" * 80)
print("VERSIÓN 1: PROGRAMADOR A (Beca → Desaprobatorio → Extemporánea)")
print("=" * 80)

# ====== VERSIÓN 1: Beca primero ======
class MatrículaV1:
    """Base: S/ 60.00"""
    def calcular_costo(self):
        return 60.0

class BecaViolenciaV1(MatrículaV1):
    """Beca: paga mitad del monto actual"""
    def calcular_costo(self):
        return super().calcular_costo() / 2

class ÍndiceDesaprobatorioV1(BecaViolenciaV1):
    """Recargo: +S/ 15.00 por índice desaprobatorio"""
    def calcular_costo(self):
        return super().calcular_costo() + 15.0

class MatrículaExtemporáneasV1(ÍndiceDesaprobatorioV1):
    """Recargo: +S/ 15.00 por matrícula extemporánea"""
    def calcular_costo(self):
        return super().calcular_costo() + 15.0

# Mostrar MRO
print("\n1. METHOD RESOLUTION ORDER (MRO):")
print("   ", [c.__name__ for c in MatrículaExtemporáneasV1.__mro__])

# Cálculo paso a paso
print("\n2. CÁLCULO PASO A PASO:")
luis_v1 = MatrículaExtemporáneasV1()
print("   Base:                         S/ 60.00")
print("   ÷ 2 (Beca Violencia)       =  S/ 30.00")
print("   + 15 (Índice Desaprobatorio) = S/ 45.00")
print("   + 15 (Matrícula Extemporánea)= S/ 60.00")
print(f"\n   TOTAL VERSIÓN 1: S/ {luis_v1.calcular_costo():.2f}")

print("\n" + "=" * 80)
print("VERSIÓN 2: PROGRAMADOR B (Desaprobatorio → Extemporánea → Beca)")
print("=" * 80)

# ====== VERSIÓN 2: Beca al final ======
class MatrículaV2:
    """Base: S/ 60.00"""
    def calcular_costo(self):
        return 60.0

class ÍndiceDesaprobatorioV2(MatrículaV2):
    """Recargo: +S/ 15.00 por índice desaprobatorio"""
    def calcular_costo(self):
        return super().calcular_costo() + 15.0

class MatrículaExtemporáneasV2(ÍndiceDesaprobatorioV2):
    """Recargo: +S/ 15.00 por matrícula extemporánea"""
    def calcular_costo(self):
        return super().calcular_costo() + 15.0

class BecaViolenciaV2(MatrículaExtemporáneasV2):
    """Beca: paga mitad del monto actual"""
    def calcular_costo(self):
        return super().calcular_costo() / 2

# Mostrar MRO
print("\n1. METHOD RESOLUTION ORDER (MRO):")
print("   ", [c.__name__ for c in BecaViolenciaV2.__mro__])

# Cálculo paso a paso
print("\n2. CÁLCULO PASO A PASO:")
rosa_v2 = BecaViolenciaV2()
print("   Base:                         S/ 60.00")
print("   + 15 (Índice Desaprobatorio) = S/ 75.00")
print("   + 15 (Matrícula Extemporánea)= S/ 90.00")
print("   ÷ 2 (Beca Violencia)       =  S/ 45.00")
print(f"\n   TOTAL VERSIÓN 2: S/ {rosa_v2.calcular_costo():.2f}")

print("\n" + "=" * 80)
print("ANÁLISIS DE RESULTADOS")
print("=" * 80)

costo_v1 = luis_v1.calcular_costo()
costo_v2 = rosa_v2.calcular_costo()
diferencia = abs(costo_v1 - costo_v2)

print(f"\nLuis Huamaní (Versión 1):  S/ {costo_v1:.2f}")
print(f"Rosa Ccahuana (Versión 2): S/ {costo_v2:.2f}")
print(f"\nDIFERENCIA: S/ {diferencia:.2f}")

print("\nAMBOS ESTUDIANTES EN IDÉNTICA SITUACIÓN:")
print("Becarios por violencia sociopolítica")
print("Índice académico desaprobatorio")
print("Matriculados fuera de fecha")

print("\n PROBLEMA:")
print("   El monto depende del ORDEN DE HERENCIA, no de la situación del estudiante.")
print("   El super() hace que el orden sea OCULTO en la definición de clases.")
print("   Python resuelve el orden usando MRO (Method Resolution Order).")

print("\nCONCLUSIÓN:")
print("   Ningún programador cometió ERROR DE SINTAXIS.")
print("   Ambos códigos son válidos en Python.")
print("   El problema es SEMÁNTICO: herencia lineal + super() = comportamiento sorprendente.")

print("\n" + "=" * 80)
print("INTENTO: Combinar base con especializaciones")
print("=" * 80)

class MatrículaIntento:
    def calcular_costo(self):
        return 60.0

class BecaIntento(MatrículaIntento):
    def calcular_costo(self):
        return super().calcular_costo() / 2

try:
    class CombinacionMala(MatrículaIntento, BecaIntento):
        pass
except TypeError as e:
    print(f"\n TypeError: {e}")
    print("\nEXPLICACIÓN:")
    print("  BecaIntento ya hereda de MatrículaIntento.")
    print("  class X(MatrículaIntento, BecaIntento) es REDUNDANTE.")
    print("  Python no puede crear MRO consistente (MatrículaIntento aparece dos veces).")
    print("  Esto previene errores silenciosos pero revela malas decisiones de diseño.")

print("\n" + "=" * 80)
print("SOLUCIÓN: PATRÓN DE MODIFICADORES EXPLÍCITOS")
print("=" * 80)

print("\nEn lugar de herencia compleja con super(), usar COMPOSICIÓN:")
print("Cada modificador es independiente.")
print("El orden se define explícitamente en una lista.")
print("Cada estudiante puede tener su propio orden.\n")

class Modificador:
    """Base: interfaz para modificadores"""
    def aplicar(self, costo):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

class ModExtemporanea(Modificador):
    def aplicar(self, costo):
        return costo + 15.0
    def __repr__(self):
        return "Extemporánea(+15)"

class ModDesaprobatorio(Modificador):
    def aplicar(self, costo):
        return costo + 15.0
    def __repr__(self):
        return "Desaprobatorio(+15)"

class ModBecaViolencia(Modificador):
    def aplicar(self, costo):
        return costo / 2.0
    def __repr__(self):
        return "Beca(÷2)"

class Estudiante:
    """Estudiante con base y lista de modificadores en orden explícito"""
    def __init__(self, nombre, dni, modificadores):
        self.nombre = nombre
        self.dni = dni
        self.modificadores = modificadores

    def calcular_costo(self):
        costo = 60.0
        for mod in self.modificadores:
            costo = mod.aplicar(costo)
        return costo

    def reporte(self):
        costo = 60.0
        print(f"\n{self.nombre} ({self.dni}):")
        print(f"  Base: S/ {costo:.2f}")
        for mod in self.modificadores:
            costo = mod.aplicar(costo)
            print(f"  Aplicando {mod}: S/ {costo:.2f}")
        print(f"  TOTAL: S/ {costo:.2f}")
        return costo

# Caso 1: Luis con beca al FINAL (como Versión 2)
luis = Estudiante(
    "Luis Huamaní Cárdenas",
    "12345678",
    [ModDesaprobatorio(), ModExtemporanea(), ModBecaViolencia()]
)

# Caso 2: Rosa con beca al INICIO (como Versión 1)
rosa = Estudiante(
    "Rosa Ccahuana Prado",
    "87654321",
    [ModBecaViolencia(), ModDesaprobatorio(), ModExtemporanea()]
)

# Caso 3: Ejemplo de orden diferente
juan = Estudiante(
    "Juan Pérez",
    "11111111",
    [ModExtemporanea(), ModBecaViolencia(), ModDesaprobatorio()]
)

print("\n--- ESTUDIANTE 1: Luis (Beca al final) ---")
costo_luis = luis.reporte()

print("\n--- ESTUDIANTE 2: Rosa (Beca al inicio) ---")
costo_rosa = rosa.reporte()

print("\n--- ESTUDIANTE 3: Juan (Otro orden) ---")
costo_juan = juan.reporte()

print("\n" + "=" * 80)
print("VENTAJAS DEL NUEVO DISEÑO")
print("=" * 80)
print("""
1. El ORDEN es EXPLÍCITO: visible en el constructor, no oculto en la jerarquía.

2. FLEXIBLE por estudiante: cada uno puede tener su propio orden sin reescribir clases.

3. AUDITABLE: revisa la lista de modificadores → entiendes el cálculo.

4. Sin sorpresas de MRO: super() no oculta el comportamiento.

5. TESTEABLE: cada modificador es una función pura (entrada → salida).

6. MANTENIBLE: agregar nuevos modificadores no requiere reescribir jerarquías.

7. La OTI puede decidir:
   - Un estándar único para todos
   - Permitir que el estudiante elija el orden
   - Auditar quién está en cuál orden
   - Cambiar el orden sin recompilación
""")

print("\n" + "=" * 80)
print("RESUMEN")
print("=" * 80)
print(f"""
PREGUNTA 1: Clases y relación
  Clases: Matrícula(base), BecaViolencia, ÍndiceDesaprobatorio, MatrículaExtemporánea
  Relación: Herencia lineal cooperativa con super()

PREGUNTA 2: MRO y costos
  V1: MatrículaExtemporáneasV1 → ... → MatrículaV1 → object  |  Costo: S/ {costo_v1:.2f}
  V2: BecaViolenciaV2 → ... → MatrículaV2 → object           |  Costo: S/ {costo_v2:.2f}

PREGUNTA 3: Causa de la diferencia
  ¿Cuándo aplica la beca (÷2)?
    V1: Al inicio → 60÷2=30, +30+30 = 60
    V2: Al final → (60+30) ÷2 = 45
  Ninguno cometió error de sintaxis. El problema es semántico (orden hidden en MRO).

PREGUNTA 4: Error al combinar base con especializaciones
  TypeError: Cannot create a consistent method resolution order (MRO)
  Causa: MatrículaBase aparece dos veces en la jerarquía (redundancia).

PREGUNTA 5: Rediseño propuesto
  Patrón de Modificadores Explícitos:
  - Orden en la lista, no en la jerarquía
  - Cada estudiante define su propio orden
  - Código más legible, testeable y mantenible
  - La OTI tiene control total sobre el cálculo
""")

print("\n" + "=" * 80)
print("FIN DEL ANÁLISIS")
print("=" * 80)
