# -*- coding: utf-8 -*-
"""Deuxieme passe (v3, haute precision) : complete `skills` uniquement quand
le TITRE de la lecon correspond a plusieurs regles distinctes du referentiel
de sa matiere. Un titre qui nomme deliberement deux notions ("fonctions et
donnees", "ville et campagne", "clouage et enfilade") en enseigne
generalement deux -- c'est un signal fiable car les titres sont courts et
rediges avec soin, contrairement au corps du texte (cours/exemples/exercices)
qui contient trop de vocabulaire ambigu (mots courants comme "son", "chaleur"
etc. qui declenchent des faux positifs quand on les cherche dans un texte
libre). Un premier essai de scan du cours pour les lecons de synthese a ete
teste et abandonne : il produisait des faux positifs verifies (ex: "son"
confondu avec le possessif "son/sa/ses"). Seul le titre est donc utilise ici.
Plafond a 3 competences. N'ajoute jamais sans correspondance de regle
explicite. Ne supprime jamais une competence deja presente. Ne touche a
aucun autre champ."""
import sys, json, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enrich_others import norm
from rules_others import (
    RULES_ECHECS, RULES_INFORMATIQUE, RULES_ARTS, RULES_VIEPRATIQUE,
    RULES_GEOGRAPHIE, RULES_HISTOIRE, RULES_SCIENCES, RULES_LECTURE, RULES_ANGLAIS,
)

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "curriculum")
LEVELS = ['CP','CE1','CE2','CM1','CM2','6E','5E','4E','3E']
CAP = 3

SUBJECT_RULES = {
    'anglais': RULES_ANGLAIS, 'lecture': RULES_LECTURE, 'sciences': RULES_SCIENCES,
    'histoire': RULES_HISTOIRE, 'geographie': RULES_GEOGRAPHIE,
    'informatique': RULES_INFORMATIQUE, 'echecs': RULES_ECHECS, 'arts': RULES_ARTS,
    'viepratique': RULES_VIEPRATIQUE,
}

def all_matches(rules, text):
    found = []
    for pattern, module, skills in rules:
        if pattern.search(text):
            for s in skills:
                if s not in found:
                    found.append(s)
    return found

report = {}
for subj, rules in SUBJECT_RULES.items():
    path = f"{BASE}/{subj}.json"
    data = json.load(open(path, encoding='utf-8'))
    stats = collections.Counter()
    dist = collections.Counter()
    changed = 0
    examples = []
    for lvl in LEVELS:
        for l in data['niveaux'][lvl]:
            original = list(l['skills'])
            title_matches = all_matches(rules, norm(l['title']))
            new_skills = list(original)
            for s in title_matches:
                if s not in new_skills and len(new_skills) < CAP:
                    new_skills.append(s)
            if new_skills != original:
                changed += 1
                examples.append((lvl, l['id'], l['title'], original, new_skills))
            l['skills'] = new_skills
            dist[len(new_skills)] += 1
            stats['n'] += 1
            stats['total_skills'] += len(new_skills)

    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    report[subj] = dict(n=stats['n'], avg=stats['total_skills']/stats['n'], dist=dict(dist),
                         changed=changed, examples=examples)
    print(f"\n===== {subj.upper()} =====")
    print(f"  n={stats['n']}  avg_skills={stats['total_skills']/stats['n']:.2f}  lecons_modifiees={changed}")
    print(f"  distribution: {dict(sorted(dist.items()))}")

