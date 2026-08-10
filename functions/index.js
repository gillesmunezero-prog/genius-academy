const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();

function assertIsAdmin(context) {
    if (!context.auth || context.auth.token.admin !== true) {
          throw new functions.https.HttpsError('permission-denied', 'Admin only.');
    }
}

async function logAudit(adminUid, action, targetUid, details) {
    await db.collection('adminAuditLog').add({
          adminUid: adminUid,
          action: action,
          targetUid: targetUid || null,
          details: details || {},
          timestamp: admin.firestore.FieldValue.serverTimestamp()
    });
}

exports.createFamily = functions.https.onCall(async (data, context) => {
    assertIsAdmin(context);
    const name = (data.name || '').trim();
    if (!name) throw new functions.https.HttpsError('invalid-argument', 'name required');
    const ref = data.requestedId
      ? db.collection('families').doc(data.requestedId)
          : db.collection('families').doc();
    await ref.create({
          name: name,
          status: 'active',
          createdAt: admin.firestore.FieldValue.serverTimestamp(),
          createdBy: context.auth.uid
    });
    await logAudit(context.auth.uid, 'family_created', null, { familyId: ref.id, name: name });
    return { familyId: ref.id, name: name };
});

exports.createManagedAccount = functions.https.onCall(async (data, context) => {
    assertIsAdmin(context);
    const email = data.email;
    const password = data.password;
    const role = data.role;
    const familyId = data.familyId;
    const displayName = data.displayName;
    const childProfile = data.childProfile;

                                                        if (!email || !password || !role || !familyId) {
                                                              throw new functions.https.HttpsError('invalid-argument', 'email, password, role, familyId requis');
                                                        }
    if (['parent', 'child', 'platform_admin'].indexOf(role) === -1) {
          throw new functions.https.HttpsError('invalid-argument', 'role invalide');
    }
    const familySnap = await db.collection('families').doc(familyId).get();
    if (!familySnap.exists) throw new functions.https.HttpsError('not-found', 'famille inconnue');

                                                        const userRecord = await admin.auth().createUser({
                                                              email: email,
                                                              password: password,
                                                              displayName: displayName || email
                                                        });

                                                        const claims = role === 'platform_admin' ? { admin: true, role: role } : { role: role };
    await admin.auth().setCustomUserClaims(userRecord.uid, claims);

                                                        var childId = null;
    if (role === 'child') {
          const childRef = db.collection('families').doc(familyId).collection('children').doc();
          childId = childRef.id;
          await childRef.set({
                  displayName: displayName || email,
                  avatar: (childProfile && childProfile.avatar) || '🦄',
                  level: (childProfile && childProfile.level) || '7',
                  status: 'active',
                  createdAt: admin.firestore.FieldValue.serverTimestamp(),
                  linkedUid: userRecord.uid
          });
    }

                                                        await db.collection('users').doc(userRecord.uid).set({
                                                              role: role,
                                                              familyId: familyId,
                                                              childId: childId,
                                                              displayName: displayName || email,
                                                              status: 'active',
                                                              createdAt: admin.firestore.FieldValue.serverTimestamp(),
                                                              createdBy: context.auth.uid
                                                        });

                                                        await db.collection('families').doc(familyId).collection('members').doc(userRecord.uid).set({
                                                              role: role,
                                                              displayName: displayName || email,
                                                              status: 'active'
                                                        });

                                                        await logAudit(context.auth.uid, 'account_created', userRecord.uid, { role: role, familyId: familyId, email: email });
    return { uid: userRecord.uid, childId: childId };
});

exports.disableManagedAccount = functions.https.onCall(async (data, context) => {
      assertIsAdmin(context);
      await admin.auth().updateUser(data.uid, { disabled: true });
      await db.collection('users').doc(data.uid).update({ status: 'disabled' });
      await logAudit(context.auth.uid, 'account_disabled', data.uid);
      return { ok: true };
});

exports.enableManagedAccount = functions.https.onCall(async (data, context) => {
      assertIsAdmin(context);
      await admin.auth().updateUser(data.uid, { disabled: false });
      await db.collection('users').doc(data.uid).update({ status: 'active' });
      await logAudit(context.auth.uid, 'account_enabled', data.uid);
      return { ok: true };
});

exports.resetManagedPassword = functions.https.onCall(async (data, context) => {
      assertIsAdmin(context);
      if (!data.newPassword || data.newPassword.length < 6) {
              throw new functions.https.HttpsError('invalid-argument', 'mot de passe trop court');
      }
      await admin.auth().updateUser(data.uid, { password: data.newPassword });
      await logAudit(context.auth.uid, 'password_reset', data.uid);
      return { ok: true };
});

exports.deleteManagedAccount = functions.https.onCall(async (data, context) => {
      assertIsAdmin(context);
      if (data.confirm !== true) {
              throw new functions.https.HttpsError('failed-precondition', 'confirm=true requis');
      }
      await admin.auth().deleteUser(data.uid);
      await db.collection('users').doc(data.uid).update({ status: 'deleted' });
      await logAudit(context.auth.uid, 'account_deleted', data.uid);
      return { ok: true };
});

