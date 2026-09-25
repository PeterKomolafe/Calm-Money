// @ts-check
import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // TODO: replace with the live domain once it is connected in Netlify
  site: 'https://calm-money.netlify.app',
  output: 'static',
  adapter: netlify(),
  integrations: [sitemap()],
});
