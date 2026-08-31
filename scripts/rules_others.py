# -*- coding: utf-8 -*-
from enrich_others import rx

# ============================================================ ECHECS
RULES_ECHECS = [
    (rx(r"\bpat\b|echec perpetuel"), "Tactiques", ["echec_et_mat"]),
    (rx(r"\bmat\b|echec et mat"), "Tactiques", ["echec_et_mat","combinaison_mat"]),
    (rx(r"clouage"), "Tactiques", ["clouage"]),
    (rx(r"fourchette"), "Tactiques", ["fourchette"]),
    (rx(r"enfilade"), "Tactiques", ["enfilade"]),
    (rx(r"attaque double|attaque a la decouverte"), "Tactiques", ["attaque_double"]),
    (rx(r"sacrifice"), "Tactiques", ["sacrifice"]),
    (rx(r"combinaison"), "Tactiques", ["combinaison_mat"]),
    (rx(r"defendre|proteger (sa|une|ses) piece|defense"), "Tactiques", ["defense"]),
    (rx(r"analyser|analyse (complete|post-partie)|etudier des parties"), "Mental et compétition", ["analyse_partie"]),
    (rx(r"finale"), "Finales", ["finale_pieces"]),
    (rx(r"\ble roi\b|\bla dame\b|\bla tour\b|\ble fou\b|\ble cavalier\b|\ble pion\b(?! passe)"), "Les pièces", ["deplacement_pieces"]),
    (rx(r"valeur des pieces|valeur des pieces"), "Les pièces", ["valeur_pieces"]),
    (rx(r"roque"), "Règles et plateau", ["roque"]),
    (rx(r"echiquier|notation echiqueenne|coup special|mettre le roi en echec"), "Règles et plateau", ["plateau_notation"]),
    (rx(r"structure(s)? de pions|majorite de pions|minorite de pions|pions passes"), "Stratégie et ouverture", ["structure_pions"]),
    (rx(r"ouverture"), "Stratégie et ouverture", ["ouverture_principes","developpement"]),
    (rx(r"echange"), "Stratégie et ouverture", ["echanges"]),
    (rx(r"milieu de (jeu|partie)"), "Stratégie et ouverture", ["milieu_de_jeu"]),
    (rx(r"plan\b|strategie"), "Stratégie et ouverture", ["plan_de_partie","strategie_long_terme"]),
    (rx(r"psychologie|ethique|preparer une competition|gerer le temps|fair-play"), "Mental et compétition", ["psychologie_competition"]),
    (rx(r"pieges? classiques|reconnaitre les faiblesses|regarder toute la position"), "Stratégie et ouverture", ["plan_de_partie"]),
]
FALLBACK_ECHECS = ("Stratégie et ouverture", "plan_de_partie")

# ============================================================ INFORMATIQUE
RULES_INFORMATIQUE = [
    (rx(r"fake news|desinformation|deepfake|fausse information|information fiable|vrai ou fausse"), "Données et intelligence artificielle", ["desinformation"]),
    (rx(r"intelligence artificielle|\bia\b|robot|assistant intelligent"), "Données et intelligence artificielle", ["intelligence_artificielle"]),
    (rx(r"donnees|base(s)? de donnees|api\b|tableau"), "Données et intelligence artificielle", ["donnees"]),
    (rx(r"cybersecurite|mot de passe|hameconnage|authentification|chiffrement"), "Internet, sécurité et vie privée", ["cybersecurite","mots_de_passe"]),
    (rx(r"vie privee|identite numerique|traces numeriques|anonymat"), "Internet, sécurité et vie privée", ["vie_privee","identite_numerique"]),
    (rx(r"citoyennete numerique|ethique du numerique|enjeux de societe|reglementation"), "Internet, sécurité et vie privée", ["citoyennete_numerique"]),
    (rx(r"internet|reseaux sociaux|naviguer|en ligne|en securite"), "Internet, sécurité et vie privée", ["internet_reseaux"]),
    (rx(r"deboguer|debogage|d[ée]bugger|bugs?\b|erreur|exceptions?|traceback"), "Programmation et algorithmique", ["debogage"]),
    (rx(r"variable"), "Programmation et algorithmique", ["variables"]),
    (rx(r"boucle"), "Programmation et algorithmique", ["boucles"]),
    (rx(r"condition|elif|si\.\.\.|booleen"), "Programmation et algorithmique", ["conditions"]),
    (rx(r"\bfonctions?\b"), "Programmation et algorithmique", ["fonctions"]),
    (rx(r"classe(s)?\b|objet(s)?\b|orientee objet"), "Programmation et algorithmique", ["programmation_orientee_objet"]),
    (rx(r"liste(s)?\b|pile(s)?\b|file(s)?\b|structure(s)? de donnees"), "Programmation et algorithmique", ["structures_donnees"]),
    (rx(r"algorithm|\btri\b|recherche|complexite"), "Programmation et algorithmique", ["algorithmes"]),
    (rx(r"projet|scratch|python|programmation|programmer|sequence|instructions|pseudo-code|\bweb\b|html|css|dessin numerique|\bjeu\b|\bquiz\b|histoire interactive|application simple"), "Programmation et algorithmique", ["projet_programmation"]),
    (rx(r"materiel|ordinateur|clavier|souris|systeme d'exploitation|logiciel|ecran|stockage|codage binaire"), "Découverte du numérique", ["decouverte_materiel"]),
]
FALLBACK_INFORMATIQUE = ("Découverte du numérique", "decouverte_materiel")

# ============================================================ ARTS
RULES_ARTS = [
    (rx(r"un artiste|artiste :"), "Écoute et histoire de l'art", ["artiste_celebre","histoire_art"]),
    (rx(r"une grande oeuvre"), "Écoute et histoire de l'art", ["analyse_oeuvre","histoire_art"]),
    (rx(r"ecouter :"), "Écoute et histoire de l'art", ["ecoute_musicale"]),
    (rx(r"histoire de l'art|l'art (abstrait|contemporain|moderne|engage|du 19e|du moyen age)|grands courants|impressionnisme|epreuve d'histoire des arts|l'engagement citoyen"), "Écoute et histoire de l'art", ["histoire_art"]),
    (rx(r"analyser une oeuvre"), "Écoute et histoire de l'art", ["analyse_oeuvre"]),
    (rx(r"mon projet final|^bilan|preparer l'epreuve|presenter son travail"), "Projet créatif", ["projet_artistique"]),
    (rx(r"rythme|pulsation|tempo|mesure(s)? (composees|impaires)|swing|ostinato|anacrouse|metronome|subdiviser"), "Musique : théorie et pratique", ["rythme_pulsation"]),
    (rx(r"gamme|intervalle|accord|alteration|octave|temperament"), "Musique : théorie et pratique", ["gammes_harmonie"]),
    (rx(r"\bnote(s)?\b|portee|partition|solfege|duree(s)?"), "Musique : théorie et pratique", ["notes_solfege"]),
    (rx(r"chant|voix|chanter"), "Musique : théorie et pratique", ["chant_voix"]),
    (rx(r"instrument|orchestre|orchestration|clavier|cordes|percussion|luthier"), "Musique : théorie et pratique", ["instruments"]),
    (rx(r"compos(er|ition)|melodie|harmonie|leitmotiv|theme et variation|improvisation|transpos"), "Musique : théorie et pratique", ["composition_musicale"]),
    (rx(r"musique(s)? actuelle|electronique|rock|musique du monde|musique et societe|musique sacree|metiers de la musique"), "Écoute et histoire de l'art", ["ecoute_musicale"]),
    (rx(r"couleur"), "Arts visuels", ["couleurs"]),
    (rx(r"perspective|cadrage|composition|ligne et texture|regle des tiers|nombre d'or|symetrie et equilibre|lignes de force"), "Arts visuels", ["formes_composition"]),
    (rx(r"clair-obscur|photographie|sculpture|volume|portrait|nature morte|street art"), "Arts visuels", ["techniques_picturales"]),
    (rx(r"creer|dessin"), "Arts visuels", ["expression_creative"]),
]
FALLBACK_ARTS = ("Projet créatif", "expression_creative")

# ============================================================ VIE PRATIQUE
RULES_VIEPRATIQUE = [
    (rx(r"budget|epargne|argent|tirelire|consommation|cv et lettre|financiere"), "Éducation financière", ["education_financiere","budget_epargne"]),
    (rx(r"desinformation|reseaux sociaux et l'image|esprit critique|biais de raisonnement|information douteuse|vrai ou pas vrai|distinguer un fait|vrai, faux|verifier avant de croire|publicite"), "Esprit critique et information", ["esprit_critique","desinformation"]),
    (rx(r"stress"), "Bien-être et émotions", ["gestion_stress"]),
    (rx(r"emotion|communication non-violente|construire des relations|bon camarade|bonnes manieres|petit conflit|regle(ment)?"), "Bien-être et émotions", ["gestion_emotions","communication_relations"]),
    (rx(r"memoris|reviser|revision|apprendre par coeur|pourquoi on oublie"), "Organisation et méthode de travail", ["memorisation"]),
    (rx(r"concentr"), "Organisation et méthode de travail", ["concentration"]),
    (rx(r"sommeil|dormir|corps|se laver|premiers secours|gestes qui sauvent|securite routiere|addiction|securite\b"), "Citoyenneté, santé et sécurité", ["securite_sante"]),
    (rx(r"engager|benevolat|citoyennete|environnement"), "Citoyenneté, santé et sécurité", ["citoyennete"]),
    (rx(r"decider|choisir|decision"), "Organisation et méthode de travail", ["prise_de_decision"]),
    (rx(r"resoudre un probleme|decomposer un probleme"), "Organisation et méthode de travail", ["resolution_probleme"]),
    (rx(r"orientation|metiers"), "Organisation et méthode de travail", ["orientation_projet"]),
    (rx(r"organiser|planifier|methode de travail|prendre des notes|espace de travail|cartable|autonomie|apprendre seul|essayer tout seul|gerer son temps|journee"), "Organisation et méthode de travail", ["organisation_planification","methode_de_travail"]),
]
FALLBACK_VIEPRATIQUE = ("Organisation et méthode de travail", "methode_de_travail")

# ============================================================ GEOGRAPHIE
RULES_GEOGRAPHIE = [
    (rx(r"carte|se reperer|plan de la classe"), "Se repérer et cartographie", ["reperage_cartographie"]),
    (rx(r"continents et les oceans|decouvrir les continents"), "Se repérer et cartographie", ["continents_oceans"]),
    (rx(r"union europeenne"), "La France et l'Union européenne", ["union_europeenne"]),
    (rx(r"climat|zones? bioclimatique|risques? climatique|changement global"), "Ressources, environnement et risques", ["changement_climatique"]),
    (rx(r"agricultur|agricoles?|type(s)? d'agriculture"), "Ressources, environnement et risques", ["agriculture"]),
    (rx(r"d'ou viennent|produits (fabriques|venus)|objets qui viennent de loin"), "Le monde et la mondialisation", ["echanges_commerciaux"]),
    (rx(r"inegalites mondiales|repartir la richesse"), "Le monde et la mondialisation", ["geopolitique"]),
    (rx(r"\beau\b|fleuve|riviere|bassin versant"), "Ressources, environnement et risques", ["eau_ressource"]),
    (rx(r"ressources naturelles|energie|energetique"), "Ressources, environnement et risques", ["ressources_naturelles"]),
    (rx(r"environnement|biodiversite|developpement durable|proteger la nature|pollution"), "Ressources, environnement et risques", ["environnement_biodiversite"]),
    (rx(r"relief|risques naturels|amenagement du territoire|plat, en pente"), "Ressources, environnement et risques", ["risques_naturels"]),
    (rx(r"mondialisation"), "Le monde et la mondialisation", ["mondialisation"]),
    (rx(r"migrations?|mobilites"), "Le monde et la mondialisation", ["migrations","mobilites_transports"]),
    (rx(r"transport|echange(s)? commerc|commerce mondial|marchandises|voyager"), "Le monde et la mondialisation", ["echanges_commerciaux","mobilites_transports"]),
    (rx(r"population|demographie|densite|repartition"), "Le monde et la mondialisation", ["population_demographie"]),
    (rx(r"etudier un territoire mondial|analyse complete.*toulouse|analyser un territoire.*facade maritime"), "Le monde et la mondialisation", ["etude_de_territoire"]),
    (rx(r"etudier une region|etudier un territoire|analyser un territoire|ma region"), "La France et l'Union européenne", ["etude_de_territoire"]),
    (rx(r"campagne|rural|village"), "Habiter un territoire", ["habiter_campagne"]),
    (rx(r"ville|metropole|urbanisation|habiter|quartier|paysage"), "Habiter un territoire", ["habiter_ville"]),
    (rx(r"pays d'europe|frontiere|puissance|geopolitique|type de pays|qu'est-ce qu'un pays|etats?,? territoires"), "Le monde et la mondialisation", ["geopolitique"]),
    (rx(r"france|francais"), "La France et l'Union européenne", ["france_regions"]),
]
FALLBACK_GEOGRAPHIE = ("Habiter un territoire", "habiter_ville")

# ============================================================ HISTOIRE
RULES_HISTOIRE = [
    (rx(r"prehistoire|premiers villages|hommes des cavernes|debuts de l'humanite"), "Préhistoire et Antiquité", ["prehistoire"]),
    (rx(r"mesopotamie|egypte ancienne|ecriture apparait|premieres civilisations|hebreux|monotheisme"), "Préhistoire et Antiquité", ["civilisations_anciennes"]),
    (rx(r"grece|athenes|hellenistique|alexandre le grand|democratie athenienne|dieux grecs|recits fondateurs grecs"), "Préhistoire et Antiquité", ["monde_grec"]),
    (rx(r"rome|romain|romanisation|\bgaule\b|vercingetorix"), "Préhistoire et Antiquité", ["monde_romain"]),
    (rx(r"byzance|empire byzantin|monde musulman|\bislam\b|chine medievale|empires africains medievaux"), "Moyen Âge", ["monde_medieval_ailleurs"]),
    (rx(r"moyen age|medieval|chevalier|seigneur|feodal|clovis|charlemagne|croisade|cathedrale|peste noire|jeanne d'arc|guerre de cent ans|saint empire|papaute"), "Moyen Âge", ["moyen_age_societe"]),
    (rx(r"renaissance|leonard de vinci|grandes decouvertes|christophe colomb|grandes explorations|ameriques precolombiennes"), "Temps modernes", ["renaissance","grandes_decouvertes"]),
    (rx(r"reforme protestante|guerres de religion|henri iv|edit de nantes|lumieres"), "Temps modernes", ["temps_modernes"]),
    (rx(r"monarchie absolue|louis xiv|versailles|rois de france"), "Temps modernes", ["monarchie_absolue"]),
    (rx(r"revolution francaise|revolutions? :? ameriqu|independance des etats-unis|napoleon"), "XIXe siècle", ["revolution_francaise"]),
    (rx(r"congres de vienne|iiie republique|affaire dreyfus|colonisation|revolution industrielle|societe industrielle|vie ouvriere|traite negriere|esclavage colonial|usines et.*machines|premieres machines"), "XIXe siècle", ["revolution_industrielle","colonisation"]),
    (rx(r"premiere guerre mondiale|1914-1918"), "XXe et XXIe siècle", ["guerre_mondiale"]),
    (rx(r"entre-deux-guerres|crise des annees 1930|totalitarismes"), "XXe et XXIe siècle", ["totalitarismes"]),
    (rx(r"seconde guerre mondiale|occupation|resistance|shoah|genocide|^1945"), "XXe et XXIe siècle", ["seconde_guerre_mondiale"]),
    (rx(r"decolonisation"), "XXe et XXIe siècle", ["decolonisation"]),
    (rx(r"guerre froide|construction europeenne|cece"), "XXe et XXIe siècle", ["guerre_froide","construction_europeenne"]),
    (rx(r"ve republique|mai 1968|ive.*republique"), "XXe et XXIe siècle", ["republique_france"]),
    (rx(r"monde depuis 1945|monde depuis 1990|mondialisation|nouveaux enjeux|nouvelles conflictualites|monde d'aujourd'hui|medias, information"), "XXe et XXIe siècle", ["monde_contemporain"]),
    (rx(r"grand defi chronologique|frise chronologique|se reperer dans le temps|comparer deux epoques|chronologie|hier, aujourd'hui|notre monde et le temps|grand voyage dans le temps"), "Le temps et la méthode historique", ["reperage_temporel"]),
    (rx(r"analyser un document|etudier un temoignage|etudier une caricature|etudier une enluminure|etudier un chateau|utiliser des documents|sources de l'archeologue|traces du passe|comprendre un mythe fondateur"), "Le temps et la méthode historique", ["methode_historique"]),
]
FALLBACK_HISTOIRE = ("Le temps et la méthode historique", "reperage_temporel")

# ============================================================ SCIENCES
RULES_SCIENCES = [
    (rx(r"squelette|muscle|digestion|circulation|systeme nerveux|cinq sens|cerveau|\bsang\b|artere|veine|immunolog|anticorps|bacteries de ton intestin|antibiotique|reproduction humaine|grandir.*adolescence|\bos\b|coeur et la respiration|corps humain|bien manger|repas equilibre|groupes d'aliments|energie des aliments|nutrition"), "Corps humain et santé", ["corps_humain"]),
    (rx(r"plante|photosynthese|graine|germe|jardin, un petit monde"), "Le vivant", ["plantes_croissance"]),
    (rx(r"animal|animaux|especes disparaissent|abeille|papillon|chenille|predateur|proie|hibernation|migration|renard|poisson meurt|dauphin|huitre|habitat|herbivore|carnivore|omnivore"), "Le vivant", ["animaux_habitat"]),
    (rx(r"cellule|classification du vivant|evolution des especes|genetique|heredite|freres et soeurs ne se ressemblent"), "Le vivant", ["genetique_classification"]),
    (rx(r"ecosystemes?|chaines? alimentaires?|reseau(x)? alimentaires?|milieux? naturels?|biodiversite|espece introduite|peuplement d'un milieu"), "Écosystèmes et environnement", ["ecosystemes"]),
    (rx(r"dechets|tri des|developpement durable|environnement|carbone|pollution|eau potable|eau boueuse"), "Écosystèmes et environnement", ["environnement_biodiversite"]),
    (rx(r"electricite|circuit|ampoule|disjoncteur|tension|courant electrique|conducteur|isolant"), "Énergie, lumière et son", ["electricite_circuit"]),
    (rx(r"lumiere|ombre|miroir|optique"), "Énergie, lumière et son", ["lumiere_optique"]),
    (rx(r"\bson\b|bruit|acoustique|audition|voix aigue"), "Énergie, lumière et son", ["son_acoustique"]),
    (rx(r"energie|eolienne|chaleur"), "Énergie, lumière et son", ["energie_sources"]),
    (rx(r"matiere|solide, liquide|melange|solution|dissoudre|filtrer|separer|reaction chimique|atome|molecule|fusion|solidification|rouille|masse.*volume|densite"), "La matière", ["etats_matiere"]),
    (rx(r"force|mouvement|frottement|vitesse|pousser|tirer|freinage|pendule|objet.*tombe|flotte"), "La matière", ["forces_mouvement"]),
    (rx(r"terre|lune|soleil|planete|systeme solaire|univers|etoile|espace|\bmars\b|gravite|gravitation"), "Terre et Univers", ["terre_univers"]),
    (rx(r"climat|meteo|nuages|pluie"), "Terre et Univers", ["climat_meteo"]),
    (rx(r"roche|\bsol\b|volcan|seisme|plaque tectonique|erosion|montagne"), "Terre et Univers", ["geologie"]),
    (rx(r"cycle de l'eau|voyage de l'eau|flaque"), "Terre et Univers", ["cycle_eau"]),
    (rx(r"enquete|comment savoir|comment identifier|demarche scientifique|mesurer une force|ma petite enquete"), "Démarche scientifique et mesures", ["demarche_scientifique"]),
]
FALLBACK_SCIENCES = ("Démarche scientifique et mesures", "demarche_scientifique")

# ============================================================ LECTURE
RULES_LECTURE = [
    (rx(r"fable|conte|parabole"), "Récits et fictions", ["fable_conte","structure_recit"]),
    (rx(r"poeme|poesie"), "Poésie", ["lecture_poetique"]),
    (rx(r"theatre|dialogue"), "Théâtre et dialogues", ["lecture_theatrale"]),
    (rx(r"^lettre| lettre |correspondant"), "Correspondance", ["texte_epistolaire"]),
    (rx(r"deux .*(documents|textes|discours|memoires|versions|sources|capitaines|championnes|champions|exploratrices|freres|lanceurs|recettes)|trois (documents|sources|avis)|comparaison|photographie.*legende contestee|meme (evenement|incident|conflit|monument|lac)"), "Comparaison de documents et esprit critique", ["comparaison_documents","esprit_critique_lecture"]),
    (rx(r"rumeur|fiabilite de l'information|information qui circule|vrai remede ou fausse rumeur"), "Comparaison de documents et esprit critique", ["esprit_critique_lecture"]),
    (rx(r"graphique|tableau des"), "Comparaison de documents et esprit critique", ["lecture_graphique_tableau"]),
    (rx(r"epreuve finale"), "Comparaison de documents et esprit critique", ["comparaison_documents"]),
    (rx(r"faut-il|argumentation|debat|tribune|discours engage|poeme engage|texte satirique"), "Presse, débat et argumentation", ["texte_argumentatif"]),
    (rx(r"louis braille|louis pasteur|leonard de vinci|marie curie|nelson mandela|thomas edison"), "Textes documentaires et scientifiques", ["biographie"]),
    (rx(r"\barticle\b|interview|compte-rendu|reportage|journal de l'ecole|publicite|affiche|le metier de|opportunite ou danger|recycler|recyclage"), "Presse, débat et argumentation", ["texte_documentaire"]),
    (rx(r"points de vue|quatre points"), "Comparaison de documents et esprit critique", ["comparaison_documents"]),
    (rx(r"comment (fonctionne|pousse|respirent|naissent|vivent|se forme)|pourquoi (le|les|dort)|etude (qui|virale)|expliquee?\b|une machine fascinante"), "Textes documentaires et scientifiques", ["texte_documentaire"]),
    (rx(r"enquete|mystere|disparu(e)?|secret|alibi|accusation|temoignage"), "Récits et fictions", ["structure_recit"]),
    (rx(r"journal (de|d'un|d'une)|carnet"), "Récits et fictions", ["structure_recit"]),
]
FALLBACK_LECTURE = ("Récits et fictions", "comprehension_litterale")

# ============================================================ ANGLAIS
RULES_ANGLAIS = [
    (rx(r"\bpassive\b"), "Grammaire", ["passive_voice"]),
    (rx(r"reported speech|reported questions|reported opinions"), "Grammaire", ["reported_speech"]),
    (rx(r"relative clause"), "Grammaire", ["relative_clauses"]),
    (rx(r"conditional"), "Grammaire", ["conditionals"]),
    (rx(r"gerund"), "Grammaire", ["gerund_infinitive"]),
    (rx(r"\bfuture\b|will |going to|predictions"), "Grammaire", ["future_forms"]),
    (rx(r"present perfect"), "Grammaire", ["present_perfect"]),
    (rx(r"past perfect"), "Grammaire", ["past_perfect"]),
    (rx(r"past continuous"), "Grammaire", ["past_continuous"]),
    (rx(r"past simple|irregular.*verbs|yesterday|used to"), "Grammaire", ["past_simple"]),
    (rx(r"present continuous|simple or continuous"), "Grammaire", ["present_continuous"]),
    (rx(r"present simple|present tense|i am, you are"), "Grammaire", ["present_simple"]),
    (rx(r"modal|have to|must|should|\bcan\.\.\.|abilities"), "Grammaire", ["modal_verbs"]),
    (rx(r"comparative|superlative|comparing"), "Grammaire", ["comparatives_superlatives"]),
    (rx(r"question (word|tag)|asking (simple |correctly)|yes/no questions|indirect and polite questions|embedded and rhetorical questions"), "Grammaire", ["questions_formation"]),
    (rx(r"preposition"), "Grammaire", ["prepositions"]),
    (rx(r"pronoun|possessive case"), "Grammaire", ["pronouns"]),
    (rx(r"adjective|adverb"), "Grammaire", ["adjectives_adverbs"]),
    (rx(r"there is|there are|some and any|much, many|how many|how much"), "Grammaire", ["quantifiers"]),
    (rx(r"time clause|time expression|narrative time"), "Grammaire", ["time_expressions"]),
    (rx(r"^listening"), "Compréhension (lecture/écoute)", ["listening_comprehension"]),
    (rx(r"^reading"), "Compréhension (lecture/écoute)", ["reading_comprehension"]),
    (rx(r"^writing|writing a|writing about"), "Expression écrite", ["writing_production"]),
    (rx(r"describ"), "Expression écrite", ["describing"]),
    (rx(r"^story|storytelling"), "Expression écrite", ["storytelling"]),
    (rx(r"conversation|debat|dialogue|asking (the way|permission)|giving directions|oral exam|oral presentation|let's have a conversation"), "Expression orale et interaction", ["speaking_interaction"]),
    (rx(r"britain and the usa|school life in britain|celebrations and festivals"), "Culture et civilisation", ["civilisation_uk_usa"]),
    (rx(r"environment|media and.*technology"), "Vocabulaire", ["environment_technology"]),
    (rx(r"animals|colours|numbers|greetings|family|house|clothes|food|toys|jobs|sports|hobbies|shopping|weather|seasons|days of the week|months|my body|classroom|transport|places in|town|emotions|feelings|fruits|drinks"), "Vocabulaire", ["vocabulaire_quotidien"]),
]
FALLBACK_ANGLAIS = ("Vocabulaire", "vocabulaire_quotidien")

ANGLAIS_DUP_OVERRIDE = {
    "anglais-6E-01": ("Grammaire", ["present_simple","present_continuous"]),
    "anglais-6E-20": ("Vocabulaire", ["vocabulaire_quotidien"]),
}
