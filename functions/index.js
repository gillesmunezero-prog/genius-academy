/**
 * Fonctions serveur Genius Academy.
 *
 * gradeAnswer : corrige la réponse d'un enfant (texte tapé ou transcrit à
 * l'oral) avec une vraie compréhension du sens, au lieu d'une simple
 * comparaison de mots. Remplace progressivement le moteur de correction
 * local (tolérant aux fautes mais aveugle au sens) par un jugement de fond :
 * pragmatique sur la formulation, exigeant sur le contenu.
 */

const { onCall, HttpsError } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const Anthropic = require("@anthropic-ai/sdk").default;
const { z } = require("zod");
const { zodOutputFormat } = require("@anthropic-ai/sdk/helpers/zod");

const anthropicApiKey = defineSecret("ANTHROPIC_API_KEY");

const GradeSchema = z.object({
  correct: z.boolean(),
  feedback: z.string(),
});

const SYSTEM_PROMPT = `Tu es le correcteur pédagogique de Genius Academy, une application scolaire pour des enfants de 7 à 9 ans (CE1/CM1), alignée sur le programme officiel français.

On te donne : la question posée, la réponse officielle attendue avec son explication pédagogique, et la réponse de l'enfant (tapée au clavier, écrite au stylet, ou transcrite depuis sa voix — donc parfois imprécise, mal orthographiée, ou avec des mots parasites).

Ta tâche : juge si le FOND de la réponse de l'enfant est correct, pas sa forme exacte.

Sois PRAGMATIQUE :
- Accepte toute reformulation, même très différente de la réponse officielle, du moment qu'elle montre que l'enfant a compris l'idée clé.
- Ignore les fautes d'orthographe, les hésitations orales ("euh", "ben"), les mots en trop.
- Une réponse plus précise ou plus détaillée que la réponse officielle, si elle reste exacte, est correcte.

Mais ne sois PAS indulgent :
- Refuse une réponse vague, hors-sujet, ou qui ne montre pas la compréhension attendue même si elle contient des mots de la question.
- Refuse une réponse incomplète sur le point clé de l'explication (pas juste "proche" ou "dans le bon sujet").
- Refuse une réponse qui semble juste par hasard (ex: un chiffre correct sans le raisonnement demandé, si le raisonnement était ce qu'on demandait).
- "Je ne sais pas" ou une réponse vide n'est jamais correcte.

Donne toujours un retour (feedback) court (1-2 phrases), bienveillant et encourageant, destiné directement à l'enfant, que sa réponse soit juste ou fausse. Jamais de ton sec ou moralisateur : tu es le meilleur professeur dont on se souvient toute sa vie.`;

exports.gradeAnswer = onCall(
  { secrets: [anthropicApiKey], region: "europe-west1", cors: true },
  async (request) => {
    if (!request.auth) {
      throw new HttpsError("unauthenticated", "Connexion requise.");
    }

    const { question, officialAnswer, explanation, childAnswer, subject, level } = request.data || {};
    if (!question || !officialAnswer || !childAnswer) {
      throw new HttpsError("invalid-argument", "question, officialAnswer et childAnswer sont requis.");
    }

    const client = new Anthropic({ apiKey: anthropicApiKey.value() });

    const userMessage = [
      `Matière : ${subject || "inconnue"} — Niveau : ${level || "inconnu"}`,
      `Question posée à l'enfant : ${question}`,
      `Réponse officielle attendue : ${officialAnswer}`,
      explanation ? `Explication pédagogique (pour comprendre ce qui compte vraiment) : ${explanation}` : null,
      `Réponse donnée par l'enfant : ${childAnswer}`,
    ].filter(Boolean).join("\n\n");

    const response = await client.messages.parse({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: userMessage }],
      output_config: { format: zodOutputFormat(GradeSchema), effort: "medium" },
    });

    if (!response.parsed_output) {
      throw new HttpsError("internal", "Correction impossible pour le moment, réessaie.");
    }

    return response.parsed_output;
  }
);
