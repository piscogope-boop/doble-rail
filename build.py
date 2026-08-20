"""Construye la web PÚBLICA a partir de la versión genérica.

Las páginas se escriben en formato artifact (sin doctype/head/body: se los pone
el wrapper de Claude al publicar). Para servirlas como web y como PWA hay que
envolverlas y engancharles manifest, iconos y service worker.

  origen   doble-rail-generico/index.html   ← genérica, sin datos personales
  destino  doble-rail-web/index.html        ← repo público

La versión personal vive en doble-rail-personal/ y NO se publica aquí: va solo
al artifact privado de Claude.

Uso:  python build.py
"""
from pathlib import Path
import sys

BASE = Path.home() / "Documents/idiomas"
SRC = BASE / "doble-rail-generico/index.html"
DST = BASE / "doble-rail-web/index.html"

# Si alguno de estos aparece en el origen, el repo es público y hay fuga.
PROHIBIDO = [
    "199.458", "my sister work", "Espanyol", "espagnol",
    "Ginebra", "errores-activos", "Anki FR", "Anki EN",
    "ingles gramática", "EXPRESIONES NATIVAS", "rev. 20 ago",
    "Francés A0", "Inglés B1+", "Meta de diciembre",
]

HEAD_TOP = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Método para estudiar dos idiomas en paralelo: los dos todos los días, separados por un corte real, con un solo motor cada vez.">
<meta name="theme-color" content="#F1F3F7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#10131A" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Doble Raíl">
"""

TAIL = """
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {});
  });
}
</script>
</body>
</html>
"""


def main():
    src = SRC.read_text(encoding="utf-8")

    fugas = [t for t in PROHIBIDO if t in src]
    if fugas:
        print("ABORTADO: el origen lleva datos personales y el repo es público.")
        for t in fugas:
            print(f"  - {t!r}")
        sys.exit(1)

    marker = "</style>"
    if marker not in src:
        sys.exit("No encuentro </style>; ¿cambió la estructura de la página?")

    head_part, body_part = src.split(marker, 1)
    out = HEAD_TOP + head_part + marker + "\n</head>\n<body>" + body_part.rstrip() + TAIL
    DST.write_text(out, encoding="utf-8")
    print(f"OK  {DST}  ({len(out)} caracteres)  sin datos personales")


if __name__ == "__main__":
    main()
