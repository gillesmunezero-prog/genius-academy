#!/usr/bin/env python3
"""Validation globale de tout le curriculum Genius Academy (11 matieres, CP a 3e).

Verifie pour chaque matiere :
- le meme nombre de lecons par niveau (9 niveaux CP..3E), conforme au nombre attendu
- IDs uniques (par matiere)
- JSON valide
- module / chapter / skills / difficulty / duration presents et valides a 100%
- kind present sur 100% des exercices, valeur dans l'ensemble autorise
- aucune regression par rapport aux fichiers de production d'origine (baseline) :
  id/title/cours/example/exercises[].{type,q,answer,exp,choices} inchanges,
  sauf patch de contenu explicitement autorise (ex: anglais-6E-20)

Usage:
    python3 validate_all_curriculum.py
"""
import json, sys, collections, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRICULUM = os.path.join(BASE, "curriculum")
BASELINE = os.path.join(CURRICULUM, "_production_backups")

LEVELS = ['CP','CE1','CE2','CM1','CM2','6E','5E','4E','3E']
EXPECTED = {
    'maths': 36, 'francais': 36, 'anglais': 30, 'lecture': 30, 'sciences': 24,
    'histoire': 18, 'geographie': 18, 'informatique': 18, 'echecs': 18,
    'arts': 18, 'viepratique': 12,
}
VALID_KINDS = {'practice','application','reasoning','error_analysis','challenge'}
REQUIRED_KEYS = ['id','title','emoji','badge','module','chapter','skills','difficulty','duration','cours','example','exercises']

# Content explicitly authorized to change (patched on purpose, not a regression)
ALLOWED_CONTENT_CHANGES = {'anglais-6E-20'}

def fail(msg, errors):
    errors.append(msg)

def baseline_path(subj):
    return os.path.join(BASELINE, f'{subj}_ORIGINAL.json')

def validate_subject(subj, errors):
    path = os.path.join(CURRICULUM, f'{subj}.json')
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        fail(f"[{subj}] JSON invalide : {e}", errors)
        return None

    expected_n = EXPECTED[subj]
    niveaux = data.get('niveaux', {})
    total = 0
    all_ids = []
    module_counts = collections.Counter()
    skill_counts = collections.Counter()
    kind_counts = collections.Counter()

    for lvl in LEVELS:
        arr = niveaux.get(lvl)
        if arr is None:
            fail(f"[{subj}] niveau '{lvl}' absent", errors)
            continue
        if len(arr) != expected_n:
            fail(f"[{subj}] niveau '{lvl}' a {len(arr)} lecons (attendu {expected_n})", errors)
        total += len(arr)
        for pos, l in enumerate(arr, 1):
            lid = l.get('id')
            if not lid:
                fail(f"[{subj}] {lvl} #{pos} sans id", errors)
            else:
                all_ids.append(lid)
            for k in REQUIRED_KEYS:
                if k not in l:
                    fail(f"[{subj}] {lid} : champ '{k}' manquant", errors)
            if l.get('module'):
                module_counts[l['module']] += 1
            else:
                fail(f"[{subj}] {lid} : module vide", errors)
            if not l.get('chapter'):
                fail(f"[{subj}] {lid} : chapter vide", errors)
            skills = l.get('skills') or []
            if not skills:
                fail(f"[{subj}] {lid} : skills vide", errors)
            for s in skills:
                skill_counts[s] += 1
            diff = l.get('difficulty')
            if not isinstance(diff, int) or not (1 <= diff <= 5):
                fail(f"[{subj}] {lid} : difficulty invalide ({diff!r})", errors)
            dur = l.get('duration')
            if not isinstance(dur, int) or not (5 <= dur <= 60):
                fail(f"[{subj}] {lid} : duration invalide ({dur!r})", errors)
            exs = l.get('exercises') or []
            if len(exs) < 2:
                fail(f"[{subj}] {lid} : seulement {len(exs)} exercices", errors)
            for e in exs:
                for req in ('type','q','answer','exp'):
                    if req not in e or e[req] in (None, ''):
                        fail(f"[{subj}] {lid} : exercice sans '{req}' valide", errors)
                kind = e.get('kind')
                if kind not in VALID_KINDS:
                    fail(f"[{subj}] {lid} : kind invalide ({kind!r})", errors)
                else:
                    kind_counts[kind] += 1
                if e.get('type') == 'qcm' and not e.get('choices'):
                    fail(f"[{subj}] {lid} : qcm sans choices", errors)

    dup = [i for i,c in collections.Counter(all_ids).items() if c > 1]
    if dup:
        fail(f"[{subj}] IDs dupliques : {dup}", errors)

    # comparaison a la baseline production
    bpath = baseline_path(subj)
    if os.path.exists(bpath):
        base = json.load(open(bpath, encoding='utf-8'))
        for lvl in LEVELS:
            newarr = {l['id']: l for l in niveaux.get(lvl, [])}
            basearr = {l['id']: l for l in base['niveaux'].get(lvl, [])}
            missing = set(basearr) - set(newarr)
            if missing:
                fail(f"[{subj}] {lvl} : lecons disparues vs production : {missing}", errors)
            for lid, bl in basearr.items():
                if lid in ALLOWED_CONTENT_CHANGES:
                    continue
                nl = newarr.get(lid)
                if not nl:
                    continue
                for immut in ('id','title','cours','example'):
                    if nl.get(immut) != bl.get(immut):
                        fail(f"[{subj}] {lid} : champ '{immut}' modifie vs production", errors)
                bex, nex = bl.get('exercises', []), nl.get('exercises', [])
                if len(bex) != len(nex):
                    fail(f"[{subj}] {lid} : nombre d'exercices change ({len(bex)} -> {len(nex)})", errors)
                else:
                    for be, ne in zip(bex, nex):
                        for k in ('type','q','answer','exp'):
                            if be.get(k) != ne.get(k):
                                fail(f"[{subj}] {lid} : exercice '{k}' modifie vs production", errors)
                        if be.get('choices') != ne.get('choices'):
                            fail(f"[{subj}] {lid} : choices modifiees vs production", errors)
    else:
        fail(f"[{subj}] pas de baseline de production trouvee pour comparaison ({bpath})", errors)

    return dict(total=total, module_counts=module_counts, skill_counts=skill_counts, kind_counts=kind_counts)

def main():
    errors = []
    results = {}
    for subj in EXPECTED:
        results[subj] = validate_subject(subj, errors)

    print("="*78)
    print("VALIDATION GLOBALE - GENIUS ACADEMY (11 matieres)")
    print("="*78)
    grand_total = 0
    for subj, r in results.items():
        if r is None:
            continue
        grand_total += r['total']
        print(f"\n-- {subj.upper()} --")
        print(f"  Total lecons : {r['total']} (attendu {EXPECTED[subj]*9})")
        print(f"  Modules : {dict(r['module_counts'])}")
        print(f"  Competences distinctes : {len(r['skill_counts'])}")
        print(f"  Kind : {dict(r['kind_counts'])}")

    print(f"\n-- TOTAL GENIUS ACADEMY : {grand_total} lecons --")

    print(f"\n-- ANOMALIES ({len(errors)}) --")
    if not errors:
        print("  Aucune anomalie detectee.")
    else:
        for e in errors[:200]:
            print("  - " + e)
        if len(errors) > 200:
            print(f"  ... et {len(errors)-200} de plus")

    print("\n" + "="*78)
    if errors:
        print(f"RESULTAT : ECHEC ({len(errors)} anomalie(s))")
        sys.exit(1)
    else:
        print(f"RESULTAT : OK - {grand_total} lecons valides, aucune regression detectee")
        sys.exit(0)

if __name__ == '__main__':
    main()
