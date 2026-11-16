"""Genera la web del borrador del Reglamento del CEUZ.

Uso: python herramientas/construir.py [CARPETA_DEL_REGLAMENTO]

Si se indica la carpeta donde se genera el borrador (la que tiene contenido.py y generar.py),
primero copia de ella a fuentes/ el PDF, la estructura, la comparativa y el programa del reparto.
Después escribe:
  datos/reglamento.json        índice del buscador (buscar/)
  comparador/index.html        comparativa 2017 -> borrador
  pdf/<nombre>.pdf             el borrador en PDF
  reparto/reparto.py           programa del anexo
  drupal/reglamento-borrador.html   cuerpo de la página de Drupal (formato HTML filtrado)
"""
import html
import json
import os
import re
import shutil
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# --- Configuración -----------------------------------------------------------------------
WEB = "https://ceuz.unizar.es"
PAGINA = f"{WEB}/reglamento/borrador"                 # página de Drupal (sin enlazar)
PAGES = "https://coestuz.github.io/reglamento"
DOC_COMENTARIOS = "https://docs.google.com/document/d/1EMKHtYhPL_eHphx2LmC_fGVW1dBST_fDWX6yPtYoRV4/edit"                                   # enlace al Google Doc para comentar
PDF = "reglamento-ceuz-borrador-1.pdf"
AVISO = ("Borrador para la Comisión Permanente. No es la versión final ni tiene valor normativo: "
         "es el texto de trabajo para preparar la propuesta que se llevará al Pleno.")
# -----------------------------------------------------------------------------------------

FUENTES = {
    "reglamento-estructura.json": "fuentes/reglamento-estructura.json",
    "comparativa-reglamento-ceuz.html": "fuentes/comparativa-reglamento-ceuz.html",
    "reglamento-ceuz.pdf": "fuentes/reglamento-ceuz.pdf",
    "reparto.py": "fuentes/reparto.py",
}


def ruta(*p):
    return os.path.join(RAIZ, *p)


def copiar_fuentes(origen):
    for nombre, destino in FUENTES.items():
        shutil.copyfile(os.path.join(origen, nombre), ruta(destino))
    print("Fuentes copiadas de", origen)


def plano(s):
    return re.sub(r"<[^>]+>", "", html.unescape(s))


def ancla(pid):
    return "ap-" + pid.replace(".", "-")


def ancla_bloque(b):
    return f"art-{b['id']}" if b["tipo"] == "articulo" else f"disp-{b['id']}"


def cabecera(b):
    return f"Art. {b['num']}. {b['titulo']}" if b["tipo"] == "articulo" else b["titulo"]


def ref(b, p):
    if b["tipo"] == "articulo":
        return f"Art. {p['id']}" if p["et"] else f"Art. {b['num']}"
    base = plano(b["titulo"]).split(".")[0]
    return f"{base}, apdo. {p['id'].split('.', 1)[1]}" if p["et"] else base


# --- Buscador: una entrada por apartado de primer nivel, con sus letras ---------------------
def entradas(est):
    out = []
    for b in est["bloques"]:
        if b["tipo"] == "capitulo":
            continue
        actual = None
        for p in b["partes"]:
            if p["nivel"] == 1:
                actual = {"doc": "nuevo", "ref": ref(b, p), "titulo": plano(cabecera(b)),
                          "url": f"{PAGINA}#{ancla(p['id']) if p['et'] else ancla_bloque(b)}",
                          "texto": (p["et"] + " " if p["et"] else "") + p["plano"]}
                out.append(actual)
            else:
                actual["texto"] += f" {p['et']} {p['plano']}"
        if b.get("codigo"):
            out[-1]["texto"] += " " + b["codigo"]
    return out


# --- Cuerpo de Drupal ---------------------------------------------------------------------
SANGRIA = {1: "", 2: ' style="margin-left:1.6em"', 3: ' style="margin-left:3.2em"'}


def cuerpo(est):
    h = []
    enlaces = [f'<a href="{PAGES}/pdf/{PDF}">Descargar el borrador en PDF</a>',
               f'<a href="{PAGES}/comparador/">Ver qué cambia respecto al de 2017</a>']
    if DOC_COMENTARIOS:
        enlaces.append(f'<a href="{DOC_COMENTARIOS}">Comentar en el documento compartido</a>')
    h.append('<div style="background:#fff6dc;border-left:4px solid #e6c35c;padding:12px 16px;margin:0 0 1.2em">'
             f'<p><strong>{html.escape(est["version"])}.</strong> {html.escape(AVISO)}</p>'
             f'<p style="margin-bottom:0">{" · ".join(enlaces)}</p></div>')
    h.append("<h2>Buscar en el texto</h2>")
    h.append(f'<iframe src="{PAGES}/buscar/" title="Buscador del Reglamento" '
             'style="border:1px solid #cfd5e2;border-radius:8px;width:100%;height:300px" loading="lazy"></iframe>')
    h.append("<h2>Texto del borrador</h2>")
    # Índice
    ind, abierto = ["<details><summary><strong>Índice</strong></summary><ul>", '<li><a href="#preambulo">Preámbulo</a></li>'], False
    for b in est["bloques"]:
        if b["tipo"] == "capitulo":
            if abierto:
                ind.append("</ul></li>")
            ind.append(f"<li>{html.escape(b['titulo'])}<ul>")
            abierto = True
        elif b["tipo"] == "articulo":
            ind.append(f'<li><a href="#{ancla_bloque(b)}">{cabecera(b)}</a></li>')
        else:
            if abierto:
                ind.append("</ul></li>")
                abierto = False
            ind.append(f'<li><a href="#{ancla_bloque(b)}">{b["titulo"]}</a></li>')
    ind.append("</ul></details>")
    h.append("".join(ind))
    # Texto
    h.append('<h2 id="preambulo" style="margin-top:2em">Preámbulo</h2>')
    h += [f"<p>{p}</p>" for p in est["preambulo"]]
    for b in est["bloques"]:
        if b["tipo"] == "capitulo":
            h.append(f'<h2 style="margin-top:2em">{html.escape(b["titulo"])}</h2>')
            continue
        h.append(f'<h3 id="{ancla_bloque(b)}" style="margin-top:1.4em">{cabecera(b)}</h3>')
        for p in b["partes"]:
            et = f"<strong>{p['et']}</strong> " if p["et"] else ""
            pid = f' id="{ancla(p["id"])}"' if p["et"] else ""
            h.append(f"<p{pid}{SANGRIA[p['nivel']]}>{et}{p['html']}</p>")
        if b.get("codigo"):
            h.append('<pre style="font-size:13px;line-height:1.4;overflow-x:auto;background:#f6f7fb;'
                     'border:1px solid #cfd5e2;border-radius:6px;padding:10px 12px">'
                     f"{html.escape(b['codigo'])}</pre>")
    return "\n".join(h) + "\n"


def main():
    if len(sys.argv) > 1:
        copiar_fuentes(sys.argv[1])
    est = json.load(open(ruta(FUENTES["reglamento-estructura.json"]), encoding="utf-8"))
    os.makedirs(ruta("datos"), exist_ok=True)
    json.dump({"version": est["version"], "entradas": entradas(est)},
              open(ruta("datos", "reglamento.json"), "w", encoding="utf-8"), ensure_ascii=False)
    shutil.copyfile(ruta(FUENTES["comparativa-reglamento-ceuz.html"]), ruta("comparador", "index.html"))
    shutil.copyfile(ruta(FUENTES["reglamento-ceuz.pdf"]), ruta("pdf", PDF))
    shutil.copyfile(ruta(FUENTES["reparto.py"]), ruta("reparto", "reparto.py"))
    open(ruta("drupal", "reglamento-borrador.html"), "w", encoding="utf-8").write(cuerpo(est))
    if "CUENTA" in PAGES:
        print("AVISO: falta poner la cuenta de GitHub en PAGES.")
    if not DOC_COMENTARIOS:
        print("AVISO: falta el enlace al Google Doc (DOC_COMENTARIOS).")
    print("Escritos datos/reglamento.json, comparador/index.html, pdf/, reparto/ y drupal/reglamento-borrador.html")


if __name__ == "__main__":
    main()
