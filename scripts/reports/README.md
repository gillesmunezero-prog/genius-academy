# Listes "sans application" / "sans raisonnement"

Generees par `scripts/validate_curriculum.py` (fonction de classification des exercices
`kind` dans `scripts/enrich_curriculum.py`... voir aussi le rapport de session).

**Important - lire avant d'agir sur ces listes** : la classification `kind` est une
heuristique par mots-cles appliquee au texte de la question (`q`) de chaque exercice.
Elle detecte bien les situations avec un marqueur explicite (montant en euros, contexte
chiffre du quotidien pour les maths ; marqueurs de raisonnement/justification pour le
raisonnement). Elle sous-estime fortement les exercices d'application en francais, ou
« appliquer » une notion consiste le plus souvent a l'utiliser dans une phrase donnee
(pas de marqueur « vie reelle » detectable par mots-cles). Un echantillonnage manuel
sur plusieurs dizaines de lecons listees ici a confirme que la plupart ont deja un
contenu pedagogique complet et adapte (voir le rapport de session) : ces listes
signalent une absence du *marqueur heuristique*, pas necessairement une absence reelle
de contenu applicatif. A relire manuellement avant toute intervention.
