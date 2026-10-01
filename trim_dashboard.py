"""trim_dashboard.py -- deja visibles solo "Rotation map" (grafico + tabla) en el
dashboard de rrg-kit y oculta "Timeframe agreement" y "Rotation alerts" con
style="display:none" (no las borra del DOM, asi el JS sigue funcionando).

Uso: python trim_dashboard.py <entrada.html> <salida.html>

Falla con error si no encuentra alguna de las secciones: si rrg-kit cambia su
HTML, es preferible que el workflow falle y no publique una pagina mal recortada.
"""
import re
import sys

HIDE = ("Timeframe agreement", "Rotation alerts")


def trim(html: str) -> str:
    for title in HIDE:
        pat = re.compile(r'<section class="panel"(\s*)>(\s*<div class="panel-h">\s*<h2>'
                         + re.escape(title) + r'</h2>)')
        html, n = pat.subn(r'<section class="panel" style="display:none">\2', html, count=1)
        if n != 1:
            raise SystemExit(f"trim_dashboard: no se encontro la seccion '{title}'")
    if "<h2>Rotation map</h2>" not in html:
        raise SystemExit("trim_dashboard: falta la seccion 'Rotation map'")
    return html


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        out = trim(f.read())
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"recortado: {dst}")
