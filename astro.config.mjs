// @ts-check
import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // TODO: replace with the live domain once it is connected in Netlify
  site: 'https://www.calmmoneycommunity.com',
  output: 'static',
  adapter: netlify(),
  // Checkout steps and thank-you pages stay out of the sitemap (they are noindex too)
  integrations: [sitemap({ filter: (page) => !/\/(join|thank-you)\//.test(new URL(page).pathname) })],
});
