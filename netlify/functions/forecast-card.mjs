// Stores the picture of someone's money forecast card for their forecast email, and serves it back.
// The site takes the picture in the visitor's browser (src/pages/forecast-card.astro) and posts it here;
// the email shows it from /card/<id>.jpg. Pictures are kept for 12 months (forecast-card-cleanup.mjs).
// Uses Netlify Blobs, which comes with the Netlify site at no extra cost.
import { getStore } from '@netlify/blobs';

const MAX_BYTES = 1_500_000;
const ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const store = () => getStore('forecast-cards');

// Only our own pages may upload (the site itself, or a Netlify preview of it, which is served from its own address)
const ours = (req) => {
  const origin = req.headers.get('origin');
  if (!origin) return false;
  const { hostname } = new URL(origin);
  return hostname === new URL(req.url).hostname || hostname === 'www.calmmoneycommunity.com' || hostname === 'calmmoneycommunity.com';
};

const upload = async (req) => {
  if (!ours(req)) return new Response('Not allowed', { status: 403 });
  if (req.headers.get('content-type') !== 'image/jpeg') return new Response('Expected a JPEG', { status: 415 });
  const body = new Uint8Array(await req.arrayBuffer());
  if (body.length > MAX_BYTES) return new Response('Too large', { status: 413 });
  if (body[0] !== 0xff || body[1] !== 0xd8 || body[2] !== 0xff) return new Response('Expected a JPEG', { status: 415 });
  const id = crypto.randomUUID();
  await store().set(id, body, { metadata: { created: Date.now() } });
  return Response.json({ url: `${new URL(req.url).origin}/card/${id}.jpg` });
};

const serve = async (req, id) => {
  if (!ID.test(id)) return new Response('Not found', { status: 404 });
  const image = await store().get(id, { type: 'arrayBuffer' });
  if (!image) return new Response('Not found', { status: 404 });
  return new Response(image, {
    headers: { 'Content-Type': 'image/jpeg', 'Cache-Control': 'public, max-age=31536000, immutable', 'X-Robots-Tag': 'noindex' },
  });
};

export default async (req, context) => {
  if (req.method === 'POST') return upload(req);
  if (req.method === 'GET' && context.params.id) return serve(req, context.params.id.replace(/\.jpg$/, ''));
  return new Response('Not found', { status: 404 });
};

export const config = { path: ['/api/forecast-card', '/card/:id'] };
