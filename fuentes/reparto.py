"""Reparto de puestos del Consejo de Estudiantes entre centros (anexo del Reglamento).

Uso: python reparto.py censo.csv PUESTOS
  censo.csv: una línea por centro, «centro;estudiantes» (también vale la coma).
  PUESTOS:   puestos de los centros (60 menos los del Consejo de Gobierno).
"""
import csv, sys
from fractions import Fraction


def repartir(censo, puestos):
    if puestos < len(censo):
        sys.exit("Hay menos puestos que centros.")
    asignados = {c: 1 for c in censo}  # un puesto por centro
    orden = []  # (centro, cociente, ¿sorteo?) de cada puesto restante
    for _ in range(puestos - len(censo)):
        # Sainte-Laguë: estudiantes / (2s + 1)
        coc = {c: Fraction(censo[c], 2 * asignados[c] + 1) for c in censo}
        mejor = max(coc.values())
        # Empate: gana el centro con más estudiantes; si persiste, sorteo
        empatados = sorted((c for c in censo if coc[c] == mejor),
                           key=lambda c: -censo[c])
        gana = empatados[0]
        sorteo = len(empatados) > 1 and censo[empatados[1]] == censo[gana]
        asignados[gana] += 1
        orden.append((gana, mejor, sorteo))
    return asignados, orden


def leer(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        texto = f.read()
    sep = ";" if ";" in texto else ","
    filas = csv.reader(texto.splitlines(), delimiter=sep)
    return {c.strip(): int(n) for c, n in filas
            if c.strip() and n.strip().isdigit()}


if __name__ == "__main__":
    censo, puestos = leer(sys.argv[1]), int(sys.argv[2])
    asignados, orden = repartir(censo, puestos)
    print(f"{'Centro':<50}{'Estudiantes':>12}{'Puestos':>9}")
    for c in sorted(censo, key=lambda c: -censo[c]):
        print(f"{c:<50}{censo[c]:>12}{asignados[c]:>9}")
    print(f"{'Total':<50}{sum(censo.values()):>12}{puestos:>9}\n")
    for i, (c, q, sorteo) in enumerate(orden, len(censo) + 1):
        aviso = "  EMPATE: hay que sortear" if sorteo else ""
        print(f"Puesto {i:>2}: {c} (cociente {float(q):.2f}){aviso}")
