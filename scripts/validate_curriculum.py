#!/usr/bin/env python3
"""Validation du curriculum maths/francais (CP -> 3e).

Verifie :
- 36 lecons par niveau et par matiere (9 niveaux), 324+324=648
- IDs uniques
- module / chapter / skills / difficulty / duration presents et valides sur 100% des lecons
- JSON valide
- aucune lecon, exercice, reponse, correction (exp) perdue par rapport a une version de reference
  (si un chemin --baseline est fourni)
- statistiques : competences distinctes, couverture moyenne, exercices par kind,
  lecons sans exercice d'application, lecons sans exercice de raisonnement/challenge/erreur

Usage:
    python3 validate_curriculum.py curriculum/maths.json curriculum/francais.json
    python3 validate_curriculum.py curriculum/maths.json curriculum/francais.json \
        --baseline-maths /path/vers/maths_original.json \
        --baseline-francais /path/vers/francais_original.json
"""
import json, sys, argparse, collections

LEVELS = ['CP','CE1','CE2','CM1','CM2','6E','5E','4E','3E']
REQUIRED_LESSON_KEYS = ['id','title','emoji','badge','module','chapter','skills',
                         'difficulty','duration','cours','example','exercises']
VALID_KINDS = {'practice','application','reasoning','error_analysis','challenge'}

def fail(msg, errors):
    errors.append(msg)

def validate_subject(label, path, errors, warnings):
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        fail(f"[{label}] JSON invalide : {e}", errors)
        return None

    niveaux = data.get('niveaux', {})
    total = 0
    all_ids = []
    module_counts = collections.Counter()
    skill_counts = collections.Counter()
    kind_counts = collections.Counter()
    skills_per_lesson = []
    no_application = []
    no_reasoning = []

    for lvl in LEVELS:
        arr = niveaux.get(lvl)
        if arr is None:
            fail(f"[{label}] niveau '{lvl}' absent", errors)
            continue
        if len(arr) != 36:
            fail(f"[{label}] niveau '{lvl}' a {len(arr)} lecons (attendu 36)", errors)
        total += len(arr)
        for pos, l in enumerate(arr, 1):
            lid = l.get('id')
            if not lid:
                fail(f"[{label}] {lvl} #{pos} sans id", errors)
            else:
                all_ids.append(lid)
            for k in REQUIRED_LESSON_KEYS:
                if k not in l:
                    fail(f"[{label}] {lid or (lvl+'#'+str(pos))} : champ '{k}' manquant", errors)
            module = l.get('module')
            if not module:
                fail(f"[{label}] {lid} : module vide", errors)
            else:
                module_counts[module] += 1
            if not l.get('chapter'):
                fail(f"[{label}] {lid} : chapter vide", errors)
            skills = l.get('skills') or []
            if not skills:
                fail(f"[{label}] {lid} : skills vide", errors)
            skills_per_lesson.append(len(skills))
            for s in skills:
                skill_counts[s] += 1
            diff = l.get('difficulty')
            if not isinstance(diff, int) or not (1 <= diff <= 5):
                fail(f"[{label}] {lid} : difficulty invalide ({diff!r})", errors)
            dur = l.get('duration')
            if not isinstance(dur, int) or not (5 <= dur <= 60):
                fail(f"[{label}] {lid} : duration invalide ({dur!r})", errors)
            exs = l.get('exercises') or []
            if len(exs) < 3:
                fail(f"[{label}] {lid} : seulement {len(exs)} exercices", errors)
            has_app = False
            has_reason = False
            for e in exs:
                for req in ('type','q','answer','exp'):
                    if req not in e or e[req] in (None, ''):
                        fail(f"[{label}] {lid} : exercice sans '{req}' valide", errors)
                kind = e.get('kind')
                if kind not in VALID_KINDS:
                    fail(f"[{label}] {lid} : kind invalide ({kind!r})", errors)
                else:
                    kind_counts[kind] += 1
                if kind == 'application':
                    has_app = True
                if kind in ('reasoning','error_analysis','challenge'):
                    has_reason = True
                if e.get('type') == 'qcm' and not e.get('choices'):
                    fail(f"[{label}] {lid} : qcm sans choices", errors)
            if not has_app:
                no_application.append(f"{lid} ({lvl} #{pos:02d}) - {l.get('title')}")
            if not has_reason:
                no_reasoning.append(f"{lid} ({lvl} #{pos:02d}) - {l.get('title')}")

    dup = [i for i,c in collections.Counter(all_ids).items() if c > 1]
    if dup:
        fail(f"[{label}] IDs dupliques : {dup}", errors)
    if len(set(all_ids)) != total:
        fail(f"[{label}] {total - len(set(all_ids))} IDs non uniques", errors)

    return dict(
        total=total, module_counts=module_counts, skill_counts=skill_counts,
        kind_counts=kind_counts,
        avg_skills=sum(skills_per_lesson)/len(skills_per_lesson) if skills_per_lesson else 0,
        no_application=no_application, no_reasoning=no_reasoning,
        all_ids=set(all_ids),
    )

def compare_baseline(label, new_path, baseline_path, errors):
    new = json.load(open(new_path, encoding='utf-8'))
    base = json.load(open(baseline_path, encoding='utf-8'))
    for lvl in LEVELS:
        newarr = {l['id']: l for l in new['niveaux'].get(lvl, [])}
        basearr = {l['id']: l for l in base['niveaux'].get(lvl, [])}
        missing = set(basearr) - set(newarr)
        if missing:
            fail(f"[{label}] {lvl} : lecons disparues par rapport a la reference : {missing}", errors)
        for lid, bl in basearr.items():
            nl = newarr.get(lid)
            if not nl:
                continue
            for immut in ('id','title','cours','example'):
                if nl.get(immut) != bl.get(immut):
                    fail(f"[{label}] {lid} : champ '{immut}' modifie par rapport a la reference", errors)
            bex = bl.get('exercises', [])
            nex = nl.get('exercises', [])
            if len(bex) != len(nex):
                fail(f"[{label}] {lid} : nombre d'exercices change ({len(bex)} -> {len(nex)})", errors)
            else:
                for be, ne in zip(bex, nex):
                    for k in ('type','q','answer','exp'):
                        if be.get(k) != ne.get(k):
                            fail(f"[{label}] {lid} : exercice '{k}' modifie par rapport a la reference", errors)
                    if be.get('choices') != ne.get('choices'):
                        fail(f"[{label}] {lid} : choices modifiees par rapport a la reference", errors)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('maths')
    ap.add_argument('francais')
    ap.add_argument('--baseline-maths')
    ap.add_argument('--baseline-francais')
    args = ap.parse_args()

    errors = []
    warnings = []
    rm = validate_subject('MATHS', args.maths, errors, warnings)
    rf = validate_subject('FRANCAIS', args.francais, errors, warnings)

    if args.baseline_maths:
        compare_baseline('MATHS', args.maths, args.baseline_maths, errors)
    if args.baseline_francais:
        compare_baseline('FRANCAIS', args.francais, args.baseline_francais, errors)

    print("="*78)
    print("RAPPORT DE VALIDATION - CURRICULUM GENIUS ACADEMY")
    print("="*78)
    for label, r in (('MATHEMATIQUES', rm), ('FRANCAIS', rf)):
        if r is None:
            continue
        print(f"\n-- {label} --")
        print(f"  Total lecons        : {r['total']} / 324")
        print(f"  Modules             : {dict(r['module_counts'])}")
        print(f"  Competences distinctes : {len(r['skill_counts'])}")
        print(f"  Couverture moyenne skills/lecon : {r['avg_skills']:.2f}")
        print(f"  Exercices par kind  : {dict(r['kind_counts'])}")
        print(f"  Lecons sans exercice application (heuristique) : {len(r['no_application'])}")
        print(f"  Lecons sans reasoning/error_analysis/challenge (heuristique) : {len(r['no_reasoning'])}")

    if rm and rf:
        print(f"\n-- TOTAL --")
        print(f"  {rm['total']} + {rf['total']} = {rm['total']+rf['total']} / 648")

    print(f"\n-- ANOMALIES ({len(errors)}) --")
    if not errors:
        print("  Aucune anomalie detectee.")
    else:
        for e in errors:
            print("  - " + e)

    print("\n" + "="*78)
    if errors:
        print(f"RESULTAT : ECHEC ({len(errors)} anomalie(s))")
        sys.exit(1)
    else:
        print("RESULTAT : OK - 648/648 lecons valides, aucune regression detectee")
        sys.exit(0)

if __name__ == '__main__':
    main()
