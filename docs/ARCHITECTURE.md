Genius Academy - Architecture Firebase (admin + comptes)
==========================================================

Roles. platform_admin gere familles, comptes et acces via un espace separe admin.html. parent accede aux enfants de sa propre famille (families/{familyId}). child accede uniquement a son propre profil (childId independant de l'uid de connexion).

Fichiers de cette branche. firestore.rules contient les regles de securite (isolation par famille + claim admin). firebase.json reference les rules et les functions. functions/index.js contient les Cloud Functions createFamily, createManagedAccount, disableManagedAccount, enableManagedAccount, resetManagedPassword et deleteManagedAccount. scripts/bootstrapAdmin.js est un script local a usage unique pour donner le claim admin au premier compte. admin.html est l'interface d'administration, separee de l'app enfant et jamais liee depuis index.html.

Structure Firestore (extrait) : users/{uid} avec role, familyId, childId, displayName, status. families/{familyId} avec name, status, createdAt, createdBy. families/{familyId}/members/{uid}. families/{familyId}/children/{childId} avec displayName, avatar, level, status, linkedUid. Puis en sous-collections du child : progress/{subjectKey}, skills/{skillId}, activityEvents/{eventId}, reviews/{reviewId}, rewards/{rewardId}. Enfin adminAuditLog/{logId} pour la tracabilite des actions admin.

Etapes Firebase a faire manuellement, dans l'ordre : un, creer le projet Firebase et passer au forfait Blaze. deux, activer Authentication avec le fournisseur Email/Mot de passe. trois, creer Cloud Firestore en mode production. quatre, creer manuellement le compte admin@geniusacademy.com dans Authentication. cinq, deployer firestore.rules et functions avec la commande firebase deploy. six, executer scripts/bootstrapAdmin.js une seule fois en local. sept, renseigner la config publique Firebase dans admin.html.

Volontairement non traite dans cette phase : aucune migration des donnees localStorage de Louise ou Beatrice, et aucune modification du curriculum ni de index.html en production.
