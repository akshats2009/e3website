// Vercel serverless function: AI-powered grant matching.
// Takes a free-text description of a business/nonprofit and returns the grants
// from data/grants.json that best fit, each with a one-line reason.
//
// Requires the ANTHROPIC_API_KEY environment variable (set in the Vercel
// project settings). If it is missing, the endpoint returns 503 and the
// frontend falls back to manual filtering.

import { readFileSync } from 'node:fs';
import Anthropic from '@anthropic-ai/sdk';

// Load the grant catalog once at cold start (single source of truth shared
// with the browser, which fetches the same file).
const GRANTS = JSON.parse(
  readFileSync(new URL('../data/grants.json', import.meta.url), 'utf8'),
);

const MODEL = 'claude-opus-4-8';
const MAX_QUERY_CHARS = 1500;
const MAX_MATCHES = 6;

// Stable system prefix (instructions + catalog) — marked for prompt caching so
// repeated searches reuse it instead of re-sending the whole catalog each time.
const SYSTEM_PROMPT = [
  {
    type: 'text',
    text:
      'You are a grant-matching assistant for small businesses and nonprofits. ' +
      'Given a short description of an organization, select the grants from the ' +
      'catalog below that best fit it. Consider eligibility (small_business vs ' +
      'nonprofit vs both), category, funding amount, and current status — an ' +
      'organization usually wants grants it actually qualifies for, and open or ' +
      'rolling grants are more actionable than closed ones (but a closed grant ' +
      'that recurs annually can still be worth noting). ' +
      'Only return grants that appear in the catalog, identified by their exact ' +
      '"name". For each, give a score from 0-100 for how well it fits and a single ' +
      'concise sentence ("reason") explaining the fit in plain language addressed ' +
      'to the applicant. Return at most ' + MAX_MATCHES + ' grants, best first. ' +
      'If nothing fits well, return an empty list.\n\n' +
      'GRANT CATALOG (JSON):\n' +
      JSON.stringify(GRANTS),
    cache_control: { type: 'ephemeral' },
  },
];

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    matches: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          score: { type: 'integer' },
          reason: { type: 'string' },
        },
        required: ['name', 'score', 'reason'],
        additionalProperties: false,
      },
    },
  },
  required: ['matches'],
  additionalProperties: false,
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed.' });
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return res.status(503).json({
      error:
        'AI search is not configured yet. Browse and filter the grants below instead.',
    });
  }

  // Vercel parses JSON bodies automatically, but guard for safety.
  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  const query = (body && typeof body.query === 'string' ? body.query : '').trim();

  if (!query) {
    return res.status(400).json({ error: 'Please describe your organization.' });
  }
  if (query.length > MAX_QUERY_CHARS) {
    return res.status(400).json({
      error: `Description is too long (max ${MAX_QUERY_CHARS} characters).`,
    });
  }

  try {
    const client = new Anthropic();
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 1500,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: query }],
      output_config: { format: { type: 'json_schema', schema: RESULT_SCHEMA } },
    });

    const text = message.content.find((b) => b.type === 'text');
    const parsed = text ? JSON.parse(text.text) : { matches: [] };

    // Join the model's picks back to the full catalog entries (the model only
    // returns names + reason + score; the browser needs the full grant object).
    const byName = new Map(GRANTS.map((g) => [g.name, g]));
    const results = (parsed.matches || [])
      .map((m) => {
        const grant = byName.get(m.name);
        return grant ? { ...grant, reason: m.reason, score: m.score } : null;
      })
      .filter(Boolean)
      .sort((a, b) => (b.score || 0) - (a.score || 0))
      .slice(0, MAX_MATCHES);

    return res.status(200).json({ matches: results });
  } catch (err) {
    console.error('grant-finder error:', err);
    return res.status(502).json({
      error: 'The AI search had a problem. Try again, or use the filters below.',
    });
  }
}
