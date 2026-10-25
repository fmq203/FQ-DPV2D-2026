# tools/lint.py
"""
Lint del brain (solo lectura). Desde brain/:
    python3 tools/lint.py
Chequea: wikilinks rotos, páginas fuera de wiki/index.md, frontmatter
incompleto, nombres que no son kebab-case y largo de AGENTS.md.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ("title:", "type:", "sources:", "updated:")
TYPES = {"requisito", "clase", "motor", "diseno", "entrega", "estado"}


def main():
    os.chdir(ROOT)
    md = [p for p in glob.glob("**/*.md", recursive=True) if not p.startswith(("raw/", "juego/"))]
    slugs = {os.path.basename(p)[:-3] for p in md}
    index = open("wiki/index.md", encoding="utf-8").read()
    problems = []

    for p in md:
        text = open(p, encoding="utf-8").read()
        # Los wikilinks dentro de `código` son ejemplos, no enlaces.
        for link in re.findall(r"\[\[([^\]]+)\]\]", re.sub(r"`[^`]*`", "", text)):
            if link not in slugs:
                problems.append(f"link roto: {p} -> [[{link}]]")
        slug = os.path.basename(p)[:-3]
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) and slug not in ("AGENTS", "MEMORY", "LEARNINGS"):
            problems.append(f"nombre no kebab-case: {p}")
        if p.startswith("wiki/") and slug not in ("index", "log"):
            head = text.split("---")[1] if text.startswith("---") else ""
            for field in REQUIRED:
                if field not in head:
                    problems.append(f"frontmatter sin '{field}': {p}")
            m = re.search(r"type: (\S+)", head)
            if m and m.group(1) not in TYPES:
                problems.append(f"type desconocido '{m.group(1)}': {p}")
            if f"[[{slug}]]" not in index:
                problems.append(f"fuera de index.md: {p}")

    n = len(open("AGENTS.md", encoding="utf-8").read().splitlines())
    if n > 200:
        problems.append(f"AGENTS.md tiene {n} líneas (> 200)")

    for line in problems:
        print(line)
    print(f"{len(md)} páginas, {len(problems)} problemas")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
