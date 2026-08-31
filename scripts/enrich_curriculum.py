#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enrichit curriculum/maths.json et curriculum/francais.json avec les metadonnees
module/chapter/skills/difficulty/duration (deduites du titre de chaque lecon par une
classification a base de regles) et ajoute un champ `kind` sur chaque exercice.

Idempotent : peut etre relance sans danger sur un fichier deja enrichi (les champs
sont recalcules a partir de id/title/cours/example/exercises, jamais l'inverse).
Ne modifie jamais id/title/cours/example/exercises[].{type,q,answer,exp,choices} sauf
le nettoyage de la cle erronee 'choises' quand 'choices' est deja presente.

Usage : python3 scripts/enrich_curriculum.py
Puis valider avec : python3 scripts/validate_curriculum.py curriculum/maths.json curriculum/francais.json
"""
import json, re, unicodedata, collections
import os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATHS_PATH = os.path.join(_BASE, "curriculum", "maths.json")
FR_PATH = os.path.join(_BASE, "curriculum", "francais.json")

LEVELS = ['CP','CE1','CE2','CM1','CM2','6E','5E','4E','3E']

def norm(s):
    s = s.lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s

def rx(p):
    return re.compile(p, re.I)

# ---------------------------------------------------------------------------
# MATHS : regles ordonnees (premiere correspondance gagne), puis tags bonus
# ---------------------------------------------------------------------------
MATHS_EXACT_OVERRIDES = {
    "les coins droits et les autres": ("Géométrie", ["angles","figures_planes"]),
}

MATHS_RULES = [
    (rx(r"pythagore"), "Géométrie", ["theoreme_pythagore","longueurs","raisonnement_mathematique"]),
    (rx(r"thales"), "Géométrie", ["theoreme_thales","proportionnalite","raisonnement_mathematique"]),
    (rx(r"trigonometri|cosinus"), "Géométrie", ["trigonometrie","angles","raisonnement_mathematique"]),
    (rx(r"notation scientifique|ecriture scientifique"), "Nombres et numération", ["notation_scientifique","puissances","decimaux"]),
    (rx(r"identites remarquables"), "Calcul", ["calcul_litteral","multiplication","puissances"]),
    (rx(r"calcul litteral|expressions? litterale|developper et reduire|reduire des expressions|programmes de calcul|preuves algebriques|factoriser|factoris"), "Calcul", ["calcul_litteral","raisonnement_mathematique"]),
    (rx(r"equation|inequation|systemes? et fonctions"), "Calcul", ["calcul_litteral","equations","resolution_problemes"]),
    (rx(r"fonction affine|fonction lineaire|fonctions affines|fonctions lineaires"), "Calcul", ["proportionnalite","calcul_litteral"]),
    (rx(r"\bproportionnalite\b"), "Fractions et décimaux", ["proportionnalite"]),
    (rx(r"nombres? relatifs?"), "Calcul", ["nombres_relatifs","calcul_mental"]),
    (rx(r"distributivite"), "Calcul", ["calcul_litteral","multiplication"]),
    (rx(r"puissances?( et)?( les)? puissances de 10|puissance"), "Nombres et numération", ["puissances","calcul_mental"]),
    (rx(r"vecteurs?|homothetie"), "Géométrie", ["symetrie_reperage","figures_planes"]),
    (rx(r"translation|rotation|frise"), "Géométrie", ["symetrie_reperage","figures_planes"]),
    (rx(r"symetrie"), "Géométrie", ["symetrie_reperage","figures_planes"]),
    (rx(r"repere du plan|reperage dans le plan|reperage,|coordonnees|lecture graphique"), "Géométrie", ["symetrie_reperage","raisonnement_mathematique"]),
    (rx(r"droite graduee|droite numerique"), "Nombres et numération", ["comparer_nombres","symetrie_reperage"]),
    (rx(r"solide|patron"), "Géométrie", ["solides_volumes","figures_planes"]),
    (rx(r"\bangle"), "Géométrie", ["angles","figures_planes"]),
    (rx(r"perimetre|circonference|arcs\b"), "Géométrie", ["perimetre","figures_planes"]),
    (rx(r"\baires?\b|decouvrir les aires|compter les carreaux"), "Géométrie", ["aires","figures_planes"]),
    (rx(r"volume"), "Géométrie", ["solides_volumes","aires"]),
    (rx(r"quadrilater|polygone|parallelogramme|figures? geometriques|figures? planes|constructions?|droites? parallel|droites? perpendicul"), "Géométrie", ["figures_planes","angles"]),
    (rx(r"masses?"), "Grandeurs et mesures", ["masses","conversions_mesures"]),
    (rx(r"contenances?|debits?|remplissage|liquides?"), "Grandeurs et mesures", ["contenances","conversions_mesures"]),
    (rx(r"longueurs?|distances?|echelles?"), "Grandeurs et mesures", ["longueurs","conversions_mesures"]),
    (rx(r"monnaie|euros?\b|budget|argent|centimes?|remises?|interets?"), "Grandeurs et mesures", ["monnaie","resolution_problemes"]),
    (rx(r"heure|durees?|vitesses?|fuseaux"), "Grandeurs et mesures", ["temps_durees","conversions_mesures"]),
    (rx(r"conversions?|unites? (de mesure|composees?)|changer d'unite"), "Grandeurs et mesures", ["conversions_mesures"]),
    (rx(r"pourcentages?|sur cent"), "Fractions et décimaux", ["pourcentages","proportionnalite"]),
    (rx(r"proportionnalite|autant pour|passage a l'unite|produit en croix|quatrieme proportionnelle|rapports et proportions"), "Fractions et décimaux", ["proportionnalite"]),
    (rx(r"fractions?|quotients?|parts? (differentes|qui se ressemblent)|moitie ou quart"), "Fractions et décimaux", ["fractions"]),
    (rx(r"decimaux|virgule|arrondis?"), "Fractions et décimaux", ["decimaux","estimation"]),
    (rx(r"statistiques?|donnees|graphiques?|tableaux?|pictogrammes?|moyennes?|frequences?"), "Données et probabilités", ["statistiques"]),
    (rx(r"probabilites?|chances?"), "Données et probabilités", ["probabilites"]),
    (rx(r"multiples?,? diviseurs?|facteurs premiers|pgcd"), "Nombres et numération", ["decomposer_nombres"]),
    (rx(r"multiplication|multiplier|\btables?\b"), "Calcul", ["multiplication"]),
    (rx(r"division|diviser|partage|groupement"), "Calcul", ["division"]),
    (rx(r"addition|additionner"), "Calcul", ["addition"]),
    (rx(r"soustraction|soustraire"), "Calcul", ["soustraction"]),
    (rx(r"calcul mental|automatismes?|astuces? pour calculer|calculer (plus )?vite|strategies? (de|pour) calcul|decomposer et compenser|complements? et doubles|amis de 10|doubles? et moities|bonds"), "Calcul", ["calcul_mental","calcul_reflechi"]),
    (rx(r"estim|ordre de grandeur"), "Nombres et numération", ["estimation"]),
    (rx(r"comparer|ranger|encadrer"), "Nombres et numération", ["comparer_nombres"]),
    (rx(r"decompos"), "Nombres et numération", ["decomposer_nombres"]),
    (rx(r"valeur de position|dizaines et unites|centaines,? dizaines|milliers, centaines"), "Nombres et numération", ["valeur_position"]),
    (rx(r"lire et ecrire"), "Nombres et numération", ["lire_nombres"]),
    (rx(r"defi|problemes?|resoudre|verifier"), "Résolution de problèmes", ["resolution_problemes","raisonnement_mathematique"]),
]

# ---------------------------------------------------------------------------
# FRANCAIS : cas particuliers (titres "enfantins" sans vocabulaire technique,
# verifies un par un sur le contenu reel du cours) -- controles AVANT les regles
# generiques
# ---------------------------------------------------------------------------
FR_EXACT_OVERRIDES = {
    "ce qui se passe maintenant": ("Conjugaison", ["conjugaison_present"]),
    "ce qui se passera demain": ("Conjugaison", ["conjugaison_futur"]),
    "avant, quand j'etais petit": ("Conjugaison", ["conjugaison_imparfait"]),
    "hier, j'ai fait quelque chose": ("Conjugaison", ["conjugaison_passe_compose"]),
    "des mots qui s'entendent pareil": ("Orthographe", ["homophones","orthographe"]),
    "bien ecrire les mots que je connais": ("Orthographe", ["orthographe"]),
    "les mots de la meme famille": ("Vocabulaire", ["familles_mots","vocabulaire"]),
    "des mots qui veulent dire la meme chose": ("Vocabulaire", ["synonymes_antonymes","vocabulaire"]),
    "chercher un mot dans l'ordre des lettres": ("Vocabulaire", ["dictionnaire","vocabulaire"]),
    "dire l'essentiel en une phrase": ("Compréhension", ["resume","comprehension"]),
    "condition et hypothese : les systemes en si": ("Conjugaison", ["conjugaison_autres_temps"]),
}

# ---------------------------------------------------------------------------
# FRANCAIS : regles ordonnees
# ---------------------------------------------------------------------------
FR_RULES = [
    (rx(r"dictee"), "Orthographe", ["orthographe","relecture_autocorrection"]),
    (rx(r"dictionnaire"), "Vocabulaire", ["dictionnaire","vocabulaire"]),
    (rx(r"homophones?"), "Orthographe", ["homophones","orthographe"]),
    (rx(r"orthographe"), "Orthographe", ["orthographe"]),
    (rx(r"synonym"), "Vocabulaire", ["synonymes_antonymes","vocabulaire"]),
    (rx(r"antonym|dire le contraire|mots qui disent le contraire"), "Vocabulaire", ["synonymes_antonymes","vocabulaire"]),
    (rx(r"famille|racines? savantes?|radicaux|etymolog|derivation|neologisme"), "Vocabulaire", ["familles_mots","vocabulaire"]),
    (rx(r"prefixes?|suffixes?|ajouter un morceau"), "Vocabulaire", ["prefixes_suffixes","vocabulaire"]),
    (rx(r"champ lexical|champ semantique|polysemie|connotation|denotation|contexte|deviner un mot"), "Vocabulaire", ["vocabulaire","comprehension"]),
    (rx(r"ponctuation"), "Grammaire", ["ponctuation"]),
    (rx(r"registres? de langue"), "Vocabulaire", ["vocabulaire","registres_langue"]),
    (rx(r"presente?( de l'indicatif)?\b"), "Conjugaison", ["conjugaison_present"]),
    (rx(r"imparfait"), "Conjugaison", ["conjugaison_imparfait"]),
    (rx(r"futur"), "Conjugaison", ["conjugaison_futur"]),
    (rx(r"passe compose"), "Conjugaison", ["conjugaison_passe_compose"]),
    (rx(r"subjonctif|conditionnel|plus-que-parfait|passe simple|voix passive|discours rapporte|discours indirect|concordance des temps|imperatif|choisir le bon temps"), "Conjugaison", ["conjugaison_autres_temps"]),
    (rx(r"argumenter|argumentatif|\bthese\b|dialectique|concession|donner son avis"), "Expression écrite", ["argumentation","production_ecrite"]),
    (rx(r"resum"), "Compréhension", ["resume","comprehension"]),
    (rx(r"expliqu|vulgariser|texte explicatif|dire pourquoi"), "Expression écrite", ["explication","production_ecrite"]),
    (rx(r"recit|raconter|analepse|schema narratif|action et dialogue|petite histoire"), "Expression écrite", ["recit","production_ecrite"]),
    (rx(r"description|portrait|paysage|decrire avec des mots"), "Expression écrite", ["description","production_ecrite"]),
    (rx(r"production ecrite|rediger|texte structure|texte argumente|j'ecris ma phrase tout seul"), "Expression écrite", ["production_ecrite"]),
    (rx(r"relire|corriger ma phrase|reecrire|ameliorer (un|son) texte"), "Expression écrite", ["relecture_autocorrection","production_ecrite"]),
    (rx(r"connecteurs? logiques?|petits mots qui relient"), "Grammaire", ["connecteurs_logiques"]),
    (rx(r"signes? a la fin des phrases"), "Grammaire", ["ponctuation"]),
    (rx(r"types? de phrases?|phrase affirmative|phrase negative|negation|interrogation|injonctio|averbale|emphase|impersonnel|mise en relief|donner un ordre|dire oui ou dire non|raconter, demander"), "Grammaire", ["types_phrases","construire_phrase"]),
    (rx(r"phrase complexe|propositions?|subordonnee|juxtaposition|coordination|enchassement"), "Grammaire", ["construire_phrase","types_phrases"]),
    (rx(r"construire (et enrichir )?(une |la )?phrase|phrase minimale|phrase enrichie|phrase correcte|petite phrase"), "Grammaire", ["construire_phrase"]),
    (rx(r"accord (du sujet|sujet-verbe)|sujet et mise en relief"), "Grammaire", ["accords","sujet_verbe"]),
    (rx(r"\ble sujet\b|qui fait l'action"), "Grammaire", ["sujet_verbe"]),
    (rx(r"groupe nominal|expansions? du nom|nominalisation|complement du nom|petit paquet de mots"), "Grammaire", ["groupe_nominal","accords"]),
    (rx(r"\baccord"), "Grammaire", ["accords"]),
    (rx(r"singulier|pluriel|un ou plusieurs"), "Grammaire", ["singulier_pluriel","accords"]),
    (rx(r"masculin|feminin|genre des noms|le ou la"), "Grammaire", ["masculin_feminin","accords"]),
    (rx(r"adjectifs?"), "Grammaire", ["identifier_nature_mots","accords"]),
    (rx(r"determinants?|petit mot devant le nom"), "Grammaire", ["identifier_nature_mots"]),
    (rx(r"pronoms?|il, elle, ils"), "Grammaire", ["identifier_nature_mots"]),
    (rx(r"\bnom\b|nom et l'adjectif vont ensemble"), "Grammaire", ["identifier_nature_mots"]),
    (rx(r"verbe"), "Grammaire", ["identifier_nature_mots"]),
    (rx(r"vocabulaire en contexte|comprendre (le vocabulaire|un mot)"), "Vocabulaire", ["vocabulaire","comprehension"]),
]

def classify(rules, title, fallback_module, fallback_skill, overrides=None):
    t = norm(title)
    if overrides and t in overrides:
        module, skills = overrides[t]
        return module, list(skills)
    for pattern, module, skills in rules:
        if pattern.search(t):
            return module, list(skills)
    return fallback_module, [fallback_skill]

def add_bonus_skills_maths(t, skills):
    bonus = []
    if re.search(r"probl[eè]me", t) and "resolution_problemes" not in skills:
        bonus.append("resolution_problemes")
    if re.search(r"raisonn|prouv|justifi|verifi|coherence|preuve|pourquoi", t) and "raisonnement_mathematique" not in skills:
        bonus.append("raisonnement_mathematique")
    if re.search(r"estim|arrondi|ordre de grandeur", t) and "estimation" not in skills:
        bonus.append("estimation")
    if re.search(r"conversions?|unites? composees?", t) and "conversions_mesures" not in skills:
        bonus.append("conversions_mesures")
    if re.search(r"probabilit|\bchances?\b", t) and "probabilites" not in skills:
        bonus.append("probabilites")
    return (skills + bonus)[:4]

def add_bonus_skills_fr(t, skills):
    bonus = []
    if re.search(r"raisonnement|coherence|logique", t) and "comprehension" not in skills:
        bonus.append("comprehension")
    return (skills + bonus)[:4]

def compute_difficulty(level, position, title):
    idx = LEVELS.index(level)
    base = round(1 + (idx/8.0)*4)
    posf = -1 if position <= 6 else (1 if position >= 31 else 0)
    challenge = 1 if re.search(r"defi|brevet|synthese|complexe", norm(title)) else 0
    val = base + posf + challenge
    return max(1, min(5, val))

def compute_duration(level, n_exercises, title):
    idx = LEVELS.index(level)
    base = [12,15,18,20,22,25,27,28,30][idx]
    adj = (n_exercises - 5) * 1
    bump = 5 if re.search(r"defi|brevet|synthese|complexe", norm(title)) else 0
    val = base + adj + bump
    val = max(10, min(45, val))
    return int(round(val / 5.0) * 5)

ERROR_RX = rx(r"\berreur\b|s'est trompe|a-t-il raison|a-t-elle raison|qui a raison|est-ce juste|est-ce correct|trouve l'erreur|c'est faux|se trompe")
REASONING_RX = rx(r"pourquoi|explique|justifie|demontre|prouve|compare|d'apres toi|selon toi|quelle strategie|quelle methode|comment sais-tu|comment peux-tu")
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

def enrich_file(path, rules, fallback_module, fallback_skill, bonus_fn, id_prefix_check, overrides=None):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    stats = collections.Counter()
    module_counts = collections.Counter()
    skill_counts = collections.Counter()
    kind_counts = collections.Counter()
    lessons_no_application = []
    lessons_no_reasoning = []
    fixed_choises = 0

    for lvl in LEVELS:
        lessons = data['niveaux'][lvl]
        for pos, lesson in enumerate(lessons, 1):
            title = lesson['title']
            module, skills = classify(rules, title, fallback_module, fallback_skill, overrides)
            skills = bonus_fn(norm(title), skills)
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
            has_reasoning_or_challenge = False
            for ex in lesson.get('exercises', []):
                ex = dict(ex)
                if 'choises' in ex:
                    if 'choices' in ex and ex['choices']:
                        del ex['choises']
                        fixed_choises += 1
                kind = classify_exercise_kind(ex.get('q',''))
                kind_counts[kind] += 1
                if kind == 'application':
                    has_application = True
                if kind in ('reasoning','error_analysis','challenge'):
                    has_reasoning_or_challenge = True
                # rebuild with kind inserted after 'type'
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
                lessons_no_application.append(f"{lesson['id']} ({lvl} #{pos:02d}) — {title}")
            if not has_reasoning_or_challenge:
                lessons_no_reasoning.append(f"{lesson['id']} ({lvl} #{pos:02d}) — {title}")

            module_counts[module] += 1
            for s in skills:
                skill_counts[s] += 1
            stats['lessons'] += 1

            lessons[pos-1] = new_lesson

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return dict(
        n_lessons=stats['lessons'],
        module_counts=module_counts,
        skill_counts=skill_counts,
        kind_counts=kind_counts,
        lessons_no_application=lessons_no_application,
        lessons_no_reasoning=lessons_no_reasoning,
        fixed_choises=fixed_choises,
    )

def main():
    res_m = enrich_file(MATHS_PATH, MATHS_RULES, "Résolution de problèmes", "resolution_problemes", add_bonus_skills_maths, "maths", overrides=MATHS_EXACT_OVERRIDES)
    res_f = enrich_file(FR_PATH, FR_RULES, "Grammaire", "identifier_nature_mots", add_bonus_skills_fr, "francais", overrides=FR_EXACT_OVERRIDES)

    for label, res in [("MATHS", res_m), ("FRANCAIS", res_f)]:
        print(f"\n===== {label} =====")
        print("n_lessons:", res['n_lessons'])
        print("modules:", dict(res['module_counts']))
        print("nb competences distinctes:", len(res['skill_counts']))
        print("top competences:", res['skill_counts'].most_common(15))
        print("kind counts:", dict(res['kind_counts']))
        print("lecons sans exercice application:", len(res['lessons_no_application']))
        print("lecons sans raisonnement/challenge/erreur:", len(res['lessons_no_reasoning']))
        print("choises corrigees:", res['fixed_choises'])

if __name__ == '__main__':
    main()
