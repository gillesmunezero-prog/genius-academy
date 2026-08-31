# -*- coding: utf-8 -*-
import json, re, unicodedata, collections

BASE = "/home/user/genius-academy/curriculum"
LEVELS = ['CP','CE1','CE2','CM1','CM2','6E','5E','4E','3E']

def norm(s):
    s = s.lower()
    s = s.replace('œ', 'oe').replace('æ', 'ae')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s

def rx(p):
    return re.compile(p, re.I)

# ---------------------------------------------------------------------------
# Classification des exercices (kind) -- reprise du moteur maths/francais,
# generique (marqueurs linguistiques, pas specifiques a une matiere)
# ---------------------------------------------------------------------------
ERROR_RX = rx(r"\berreur\b|s'est trompe|a-t-il raison|a-t-elle raison|qui a raison|est-ce juste|est-ce correct|trouve l'erreur|c'est faux|se trompe|mistake|wrong|correct this")
REASONING_RX = rx(r"pourquoi|explique|justifie|demontre|prouve|compare|d'apres toi|selon toi|quelle strategie|quelle methode|comment sais-tu|comment peux-tu|why|explain|justify")
CHALLENGE_RX = rx(r"plusieurs etapes|etape par etape|d'abord.*ensuite")
APPLICATION_RX = rx(r"€|euros?\b|kilometres?|\bkm\b|litres?|grammes?|\bkg\b|budget|magasin|marche\b|jardin|famille|recette|voyage|distance|salle|entreprise|boutique|pizza|gateau|classe de|eleves|billets?|pieces de monnaie")

def classify_exercise_kind(q):
    t = norm(q)
    if ERROR_RX.search(t):
        return "error_analysis"
    if REASONING_RX.search(t):
        return "reasoning"
    if len(t.split()) > 45 or CHALLENGE_RX.search(t):
        return "challenge"
    if APPLICATION_RX.search(t):
        return "application"
    return "practice"

def compute_difficulty(level, position, title):
    idx = LEVELS.index(level)
    base = round(1 + (idx/8.0)*4)
    posf = -1 if position <= 6 else (1 if position >= 31 else 0)
    challenge = 1 if re.search(r"defi|brevet|synthese|complexe|epreuve finale|bilan|projet final", norm(title)) else 0
    val = base + posf + challenge
    return max(1, min(5, val))

def compute_duration(level, n_exercises, title):
    idx = LEVELS.index(level)
    base = [12,15,18,20,22,25,27,28,30][idx]
    adj = (n_exercises - 5) * 1
    bump = 5 if re.search(r"defi|brevet|synthese|complexe|epreuve finale|projet final", norm(title)) else 0
    val = base + adj + bump
    val = max(10, min(45, val))
    return int(round(val / 5.0) * 5)

def classify(rules, title, fallback_module, fallback_skill, overrides=None):
    t = norm(title)
    if overrides and t in overrides:
        module, skills = overrides[t]
        return module, list(skills)
    for pattern, module, skills in rules:
        if pattern.search(t):
            return module, list(skills)
    return fallback_module, [fallback_skill]

def enrich_file(subj, rules, fallback_module, fallback_skill, overrides=None, title_overrides_content=None):
    path = f"{BASE}/{subj}.json"
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    stats = collections.Counter()
    module_counts = collections.Counter()
    skill_counts = collections.Counter()
    kind_counts = collections.Counter()
    lessons_no_application = []
    lessons_no_reasoning = []

    for lvl in LEVELS:
        lessons = data['niveaux'][lvl]
        for pos, lesson in enumerate(lessons, 1):
            # optional content patch (used only for the anglais-6E duplicate fix)
            if title_overrides_content and lesson.get('id') in title_overrides_content:
                lesson.update(title_overrides_content[lesson['id']])

            title = lesson['title']
            module, skills = classify(rules, title, fallback_module, fallback_skill, overrides)
            difficulty = compute_difficulty(lvl, pos, title)
            duration = compute_duration(lvl, len(lesson.get('exercises', [])), title)

            new_lesson = {}
            new_lesson['id'] = lesson['id']
            new_lesson['title'] = lesson['title']
            new_lesson['emoji'] = lesson['emoji']
            new_lesson['badge'] = lesson['badge']
            new_lesson['module'] = module
            new_lesson['chapter'] = title
            new_lesson['skills'] = skills
            new_lesson['difficulty'] = difficulty
            new_lesson['duration'] = duration
            new_lesson['cours'] = lesson['cours']
            new_lesson['example'] = lesson['example']

            new_exercises = []
            has_application = False
            has_reasoning = False
            for ex in lesson.get('exercises', []):
                ex = dict(ex)
                kind = classify_exercise_kind(ex.get('q',''))
                kind_counts[kind] += 1
                if kind == 'application':
                    has_application = True
                if kind in ('reasoning','error_analysis','challenge'):
                    has_reasoning = True
                new_ex = {}
                for k,v in ex.items():
                    new_ex[k] = v
                    if k == 'type':
                        new_ex['kind'] = kind
                if 'kind' not in new_ex:
                    new_ex['kind'] = kind
                new_exercises.append(new_ex)
            new_lesson['exercises'] = new_exercises

            if not has_application:
                lessons_no_application.append(f"{lesson['id']} ({lvl} #{pos:02d}) - {title}")
            if not has_reasoning:
                lessons_no_reasoning.append(f"{lesson['id']} ({lvl} #{pos:02d}) - {title}")

            module_counts[module] += 1
            for s in skills:
                skill_counts[s] += 1
            stats['lessons'] += 1

            lessons[pos-1] = new_lesson

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return dict(
        n_lessons=stats['lessons'], module_counts=module_counts, skill_counts=skill_counts,
        kind_counts=kind_counts, lessons_no_application=lessons_no_application,
        lessons_no_reasoning=lessons_no_reasoning,
    )
