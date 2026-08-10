/**
 * A executer UNE SEULE FOIS, sur ta machine (jamais sur GitHub Pages).
 * 1. Console Firebase > Parametres du projet > Comptes de service > Generer une nouvelle cle privee
 *    -> enregistre le fichier sous serviceAccountKey.json a la racine (NE JAMAIS le committer).
 * 2. Cree d'abord admin@geniusacademy.com manuellement dans Firebase Authentication (console),
 *    avec le mot de passe de ton choix.
 * 3. npm install firebase-admin
 * 4. node scripts/bootstrapAdmin.js
 */
const admin = require('firebase-admin');
const serviceAccount = require('../serviceAccountKey.json');
admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });

const ADMIN_EMAIL = 'admin@geniusacademy.com';

async function main() {
    const user = await admin.auth().getUserByEmail(ADMIN_EMAIL);
    await admin.auth().setCustomUserClaims(user.uid, { admin: true, role: 'platform_admin' });
    await admin.firestore().collection('users').doc(user.uid).set({
          role: 'platform_admin',
          familyId: null,
          childId: null,
          displayName: 'Administrateur Genius Academy',
          status: 'active',
          createdAt: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });
    console.log('OK claim admin defini pour', ADMIN_EMAIL, user.uid);
}

main().then(function () { process.exit(0); }).catch(function (e) { console.error(e); process.exit(1); });
