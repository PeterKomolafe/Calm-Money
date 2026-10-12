// Deletes forecast card pictures older than 12 months, once a day (see forecast-card.mjs)
import { getStore } from '@netlify/blobs';

const KEEP_MS = 365 * 24 * 60 * 60 * 1000;

export default async () => {
  const store = getStore('forecast-cards');
  const { blobs } = await store.list();
  let deleted = 0;
  for (const { key } of blobs) {
    const found = await store.getMetadata(key);
    if (found && Date.now() - Number(found.metadata.created || 0) > KEEP_MS) { await store.delete(key); deleted++; }
  }
  console.log(`Forecast cards: ${blobs.length} kept or checked, ${deleted} deleted`);
};

export const config = { schedule: '@daily' };
