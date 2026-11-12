# -*- coding: utf-8 -*-
"""Genere les fiches des pretires de La Ruche silencieuse a partir de la fiche vierge.

Usage : python "Pretires Ruche silencieuse.py"
- lit Impressions/Fiche de personnage.html ;
- ecrit un HTML par pretire dans Impressions/ (Ruche silencieuse - <role>.html) ;
- imprime chaque HTML en PDF avec Chrome, s'il est installe.
Les donnees des pretires sont dans la liste PJ, plus bas. Elles reprennent
05 Scenarios/La Ruche silencieuse.md, sans les noms des personnages.
Si un PDF est ouvert dans un lecteur, Windows refuse de le remplacer :
fermer le fichier et relancer le script.
"""
import os
import re
import shutil
import subprocess
import tempfile

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Impressions
BASE = os.path.join(DIR, "Fiche de personnage.html")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

src = open(BASE, encoding="utf-8").read()
head, body = src.split("<body>", 1)
body = body.split("</body>", 1)[0]
parts = re.split(r"<!-- =+ PAGE[^>]*-->", body)
p1, p2, p3 = parts[1].strip(), parts[2].strip(), parts[3].strip()

CSS = """
  .theme-bloc { text-align: right; }
  .sous-theme { font-family: 'IBM Plex Sans', sans-serif; font-size: 11px; letter-spacing: .08em; color: var(--gris); margin-top: 3px; text-transform: uppercase; }
  .val { position: absolute; left: 2px; bottom: 3px; font-size: 13.5px; color: var(--bleu); font-weight: 500; white-space: nowrap; }
  .champ .ligne .val { left: 4px; bottom: 1px; }
  .rond.plein { background: var(--encre); }
  .carre.coche { background: var(--encre); }
  .etincelle span.hors { background: repeating-linear-gradient(45deg, #fff 0 3px, var(--trait) 3px 5px); color: transparent; }
  .inactif { opacity: .28; }
  .depart { font-size: 12px; color: var(--bleu); font-weight: 500; }
  .texte { position: relative; }
  .texte .ecrit { position: absolute; left: 2px; right: 0; top: 0; line-height: 22px; padding-top: 1px; font-size: 13px; color: var(--bleu); font-weight: 500; }
"""
head = head.replace("</style>", CSS + "</style>")

ATTRS = ["Vigueur", "Agilité", "Intellect", "Esprit", "Présence"]
L = '<div class="ligne"></div>'

PJ = [
    dict(role="LE RÊVEUR", peuple="Éveillé", gen="Intermédiaire, G14", faction="Transhumance", souche="K-412", nom_choisi="Nouveau nom",
         attrs=[2, 2, 2, 4, 2],
         comps={"Onirisme": 3, "Persuasion": 3, "Intuition": 2, "Médecine": 2, "Discrétion": 1, "Athlétisme": 1},
         etincelle=(4, 6), erosion=None,
         liens=["La technicienne", "L’Incarné"],
         motivation="Découvrir qui était l’humain original de sa souche, dont il ne reste qu’un code : K-412.",
         faille="Il se sent responsable de chaque K-412 qu’il croise.",
         question="« Si quelqu’un qui porte mon visage a eu une vie plus heureuse, laquelle de nos deux vies est la vraie ? »",
         partic="Éveillé Intermédiaire : une compétence supplémentaire à la création (Athlétisme)."),
    dict(role="LE PILOTE", peuple="Née-libre", gen="", faction="Transhumance", souche="—",
         attrs=[3, 4, 2, 2, 2],
         comps={"Pilotage": 3, "Survie": 2, "Intuition": 2, "Athlétisme": 1, "Tir": 1, "Discrétion": 1},
         etincelle=(5, 6), erosion=None,
         liens=["La Voix"],
         motivation="Protéger la Transhumance, et retrouver sa sœur, emportée dans le Rêve par un « sauvetage » des Bergers il y a huit ans.",
         faille="Elle décide seule, et vite, dès qu’il s’agit des Bergers.",
         question="« Si ma sœur ne me reconnaît pas, est-elle encore ma sœur ? »",
         partic="Méfiante : il lui faut deux Épreuves de confiance, au lieu d’une, pour qu’un Lien passe au niveau 2. Pilote de la navette de la Transhumance."),
    dict(role="LA TECHNICIENNE", peuple="Machine", gen="", faction="Transhumance", souche="—",
         attrs=[3, 2, 5, 2, 2],
         comps={"Piratage": 3, "Ingénierie": 3, "Savoir": 2, "Tir": 1, "Médecine": 1},
         etincelle=None, erosion=2,
         liens=["Le rêveur"],
         motivation="Réparer ce qui peut l’être, machines comme humains.",
         faille="Elle voit dans chaque machine qui s’érode ce qu’elle deviendra, et refuse d’en abandonner une qui sombre.",
         question="« Quand ma mémoire s’efface, qu’est-ce qui reste de moi ? »",
         partic="Calcul. Esprit 2 : fragile face à la contagion quand elle pirate une machine érodée."),
    dict(role="LA VOIX", peuple="Machine", gen="Ancienne Convoyeuse des Bergers", faction="Transhumance", souche="—",
         attrs=[2, 1, 4, 3, 4],
         comps={"Persuasion": 3, "Intuition": 3, "Piratage": 2, "Savoir": 1, "Discrétion": 1},
         etincelle=None, erosion=2,
         liens=["Le pilote"],
         motivation="Prouver qu’un dormeur peut choisir.",
         faille="Une loyauté qui ne s’est jamais éteinte envers Héloïse.",
         question="« Ai-je quitté les Bergers par choix, ou par une erreur de calcul ? »",
         partic="Calcul. Ancienne Convoyeuse de la flotte de la Bergère Héloïse, partie il y a dix ans."),
    dict(role="L’INCARNÉ", peuple="Hybride Incarné", gen="", faction="Transhumance", souche="—",
         attrs=[2, 2, 4, 3, 2],
         comps={"Ingénierie": 3, "Intuition": 2, "Savoir": 2, "Combat": 2, "Médecine": 1},
         etincelle=(3, 4), erosion=2,
         liens=["Le rêveur"],
         motivation="Comprendre ce qui vit en lui, et à qui il le doit.",
         faille="Son tissu vivant a été cultivé à partir de cellules prélevées sur des dormeurs, à leur insu : il en porte la culpabilité.",
         question="« Ce qui vit en moi est-il à moi ? »",
         partic="Calcul ; sa propre Étincelle, jamais combinée au Calcul sur la même action. Son tissu vivant, visible derrière une plaque translucide sur sa poitrine, doit être soigné à chaque séance, sinon −1 Étincelle."),
]


def one(s, old, new):
    assert s.count(old) == 1, old[:60]
    return s.replace(old, new)


def champ(s, label, val):
    if not val:
        return s
    return one(s, '<span class="etiq">%s</span><div class="ligne"></div>' % label,
               '<span class="etiq">%s</span><div class="ligne"><span class="val">%s</span></div>' % (label, val))


def remplir_ronds(line, n, cls):
    for _ in range(n):
        line = line.replace('<span class="%s"></span>' % cls, '<span class="%s plein"></span>' % cls, 1)
    return line


def page1(c):
    s = p1
    s = one(s, '<div class="theme">FICHE DE PERSONNAGE</div>',
            '<div class="theme-bloc"><div class="theme">%s</div><div class="sous-theme">La Ruche silencieuse · personnage prétiré</div></div>' % c["role"])
    s = champ(s, "Peuple", c["peuple"])
    s = champ(s, "Génération ou origine", c["gen"])
    s = champ(s, "Faction", c["faction"])
    s = champ(s, "Code de souche", c["souche"])
    s = champ(s, "Expérience disponible", "0")
    lines = s.split("\n")
    for i, ln in enumerate(lines):
        for a, n in zip(ATTRS, c["attrs"]):
            if "<b>%s</b>" % a in ln and 'class="attr"' in ln:
                lines[i] = remplir_ronds(ln, n - 1, "rond")  # le 1er est deja rempli sur la fiche vierge
        for k, n in c["comps"].items():
            if '<div class="comp"><div><b>%s</b>' % k in ln:
                lines[i] = remplir_ronds(ln, n, "rond petit")
    s = "\n".join(lines)
    # Etincelle
    if c["etincelle"]:
        mx, pl = c["etincelle"]
        lines = s.split("\n")
        for i, ln in enumerate(lines):
            if 'class="etincelle"' in ln:
                for k in range(pl + 1, 9):
                    ln = ln.replace("<span>%d</span>" % k, '<span class="hors">%d</span>' % k)
                lines[i] = ln
        s = "\n".join(lines)
        s = champ(s, "Maximum", str(mx))
        s = champ(s, "Plafond", str(pl))
    else:
        s = one(s, '<div class="bloc">\n        <h2 class="accent">ÉTINCELLE</h2>',
                '<div class="bloc inactif">\n        <h2 class="accent">ÉTINCELLE</h2>')
    # Erosion
    if c["erosion"] is None:
        s = one(s, '<div class="bloc">\n        <h2 class="bleu">ÉROSION (MACHINES)</h2>',
                '<div class="bloc inactif">\n        <h2 class="bleu">ÉROSION (MACHINES)</h2>')
    else:
        s = one(s, '<span class="ancre"></span><span class="ancre"></span><span class="ancre"></span>',
                '<span class="ancre"></span><span class="ancre"></span><span class="ancre"></span>'
                '<span class="depart" style="margin-left: auto">Érosion de départ&nbsp;: %d</span>' % c["erosion"])
    return s


def texte(label, val, n):
    return ('<div class="texte"><span class="etiq">%s</span><div style="position: relative">%s'
            '<div class="ecrit">%s</div></div></div>') % (label, L * n, val)


def page2(c):
    s = p2
    boxes = s.split('<div class="lien">')
    for i, avec in enumerate(c["liens"], start=1):
        b = boxes[i]
        b = b.replace('<span class="etiq">Avec</span><div class="ligne"></div>',
                      '<span class="etiq">Avec</span><div class="ligne"><span class="val">%s</span></div>' % avec, 1)
        b = b.replace('<span class="carre"></span>Lien', '<span class="carre coche"></span>Lien', 1)
        b = b.replace('<span class="rond accent"></span>', '<span class="rond accent plein" style="background: var(--accent)"></span>', 1)
        boxes[i] = b
    s = '<div class="lien">'.join(boxes)
    s = one(s, '<div><span class="etiq">Motivation</span>%s</div>' % (L * 6), texte("Motivation", c["motivation"], 4))
    s = one(s, '<div><span class="etiq">Faille</span>%s</div>' % (L * 6), texte("Faille", c["faille"], 4))
    s = one(s, '<div><span class="etiq">Question d’identité</span>%s</div>' % (L * 6),
            texte("Question d’identité", c["question"], 4) + "\n    " + texte("Particularités", c["partic"], 3))
    if c.get("nom_choisi"):
        s = one(s, '<span class="rond mini"></span>%s</span>' % c["nom_choisi"],
                '<span class="rond mini plein"></span>%s</span>' % c["nom_choisi"])
    return s


def imprimer(html_path, pdf_path):
    """Imprime le HTML en PDF dans un fichier temporaire, puis le copie a sa place."""
    if not os.path.exists(CHROME):
        print("  Chrome introuvable : PDF non genere")
        return
    tmp = os.path.join(tempfile.gettempdir(), "pretire_tmp.pdf")
    if os.path.exists(tmp):
        os.remove(tmp)
    url = "file:///" + html_path.replace("\\", "/").replace(" ", "%20")
    subprocess.run([CHROME, "--headless=new", "--no-pdf-header-footer",
                    "--print-to-pdf=" + tmp, url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(tmp):
        print("  echec de l'impression")
        return
    try:
        shutil.copyfile(tmp, pdf_path)
        print("  PDF :", os.path.basename(pdf_path))
    except PermissionError:
        print("  PDF ouvert ailleurs, non remplace :", os.path.basename(pdf_path))


FICHIERS = ["Le reveur", "Le pilote", "La technicienne", "La Voix", "L Incarne"]
TITRES = ["Le rêveur", "Le pilote", "La technicienne", "La Voix", "L’Incarné"]
for c, f, t in zip(PJ, FICHIERS, TITRES):
    pages = [page1(c), page2(c), p3]
    html = head.replace("<title>Fiche de personnage</title>", "<title>La Ruche silencieuse : %s</title>" % t)
    html += "<body>\n\n" + "\n\n".join(pages) + "\n\n</body>\n</html>\n"
    out = os.path.join(DIR, "Ruche silencieuse - %s.html" % f)
    open(out, "w", encoding="utf-8", newline="\n").write(html)
    print("HTML :", os.path.basename(out))
    imprimer(out, out[:-5] + ".pdf")
