# -*- coding: utf-8 -*-
import sys, shutil, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = "/home/user/genius-academy/curriculum"
BACKUPS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "curriculum", "_production_backups")

SUBJECTS = ['anglais','lecture','sciences','histoire','geographie','informatique','echecs','arts','viepratique']
for s in SUBJECTS:
    shutil.copy(f"{BACKUPS}/{s}_ORIGINAL.json", f"{BASE}/{s}.json")

from enrich_others import enrich_file
from rules_others import (
    RULES_ECHECS, FALLBACK_ECHECS, RULES_INFORMATIQUE, FALLBACK_INFORMATIQUE,
    RULES_ARTS, FALLBACK_ARTS, RULES_VIEPRATIQUE, FALLBACK_VIEPRATIQUE,
    RULES_GEOGRAPHIE, FALLBACK_GEOGRAPHIE, RULES_HISTOIRE, FALLBACK_HISTOIRE,
    RULES_SCIENCES, FALLBACK_SCIENCES, RULES_LECTURE, FALLBACK_LECTURE,
    RULES_ANGLAIS, FALLBACK_ANGLAIS, ANGLAIS_DUP_OVERRIDE,
)
from anglais_6e20_patch import ANGLAIS_6E20_PATCH

PLAN = [
    ('anglais', RULES_ANGLAIS, FALLBACK_ANGLAIS, ANGLAIS_DUP_OVERRIDE, ANGLAIS_6E20_PATCH),
    ('lecture', RULES_LECTURE, FALLBACK_LECTURE, None, None),
    ('sciences', RULES_SCIENCES, FALLBACK_SCIENCES, None, None),
    ('histoire', RULES_HISTOIRE, FALLBACK_HISTOIRE, None, None),
    ('geographie', RULES_GEOGRAPHIE, FALLBACK_GEOGRAPHIE, None, None),
    ('informatique', RULES_INFORMATIQUE, FALLBACK_INFORMATIQUE, None, None),
    ('echecs', RULES_ECHECS, FALLBACK_ECHECS, None, None),
    ('arts', RULES_ARTS, FALLBACK_ARTS, None, None),
    ('viepratique', RULES_VIEPRATIQUE, FALLBACK_VIEPRATIQUE, None, None),
]

all_results = {}
for subj, rules, (fb_mod, fb_skill), overrides, content_patch in PLAN:
    res = enrich_file(subj, rules, fb_mod, fb_skill, overrides=overrides, title_overrides_content=content_patch)
    all_results[subj] = res
    print(f"\n===== {subj.upper()} =====")
    print("n_lessons:", res['n_lessons'])
    print("modules:", dict(res['module_counts']))
    print("nb competences distinctes:", len(res['skill_counts']))
    print("kind counts:", dict(res['kind_counts']))
    print("lecons sans application:", len(res['lessons_no_application']))
    print("lecons sans raisonnement:", len(res['lessons_no_reasoning']))

import pickle
pickle.dump(all_results, open("/tmp/claude-0/-home-user-genius-academy/d3aa5776-654b-5ae3-9836-fd0600e157d1/scratchpad/enrich_others_results.pkl","wb"))
