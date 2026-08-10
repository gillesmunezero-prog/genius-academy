Mapping localStorage vers Firestore (a valider avant migration)

Cle geniusAcademyData.profiles[i].name, .avatar, .track correspond au document families/{familyId}/children/{childId} (champs displayName, avatar, level).

Cle profiles[i].stars correspond a families/{familyId}/children/{childId}/rewards (cumul recalcule a partir des evenements).

Cle profiles[i].badges correspond a families/{familyId}/children/{childId}/rewards/{rewardId}.

Cle profiles[i].progress[subject][track] correspond a families/{familyId}/children/{childId}/progress/{subjectKey}.

Cle profiles[i].subjectTrack correspond au champ track inclus dans le document progress/{subjectKey}.

Cle profiles[i].streak et lastLessonDate correspondent a families/{familyId}/children/{childId}/skills/streak (document dedie).

L'historique des lecons terminees correspond a families/{familyId}/children/{childId}/activityEvents/{eventId}, ou eventId est un UUID genere cote client pour eviter les doublons lors d'un changement d'appareil.

Aucune donnee locale ne sera supprimee pendant la migration : il s'agira d'un import additif, precede d'un export JSON automatique. La migration ne sera declenchee qu'apres validation explicite de l'environnement Firebase.
