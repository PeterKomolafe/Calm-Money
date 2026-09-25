# Calm Money website

Astro site hosted on Netlify. Pages are static for speed and SEO; the email signup runs as a Netlify Function. Content is editable at `/admin` via Decap CMS.

## Run locally

```sh
npm install
npm run dev      # http://localhost:4321
npm run build
```

Without `EMAIL_PROVIDER` set, the signup form logs to the console in dev instead of sending anywhere.

## Where things live

| What | Where | Edit in CMS |
| --- | --- | --- |
| Hero, free guide, about, disclaimer | `src/data/site.json` | Site settings |
| Offers (price, checkout link) | `src/content/offers/*.md` | Offers |
| Testimonials | `src/content/testimonials/*.md` | Testimonials (only shown when permission is ticked) |
| Blog posts | `src/content/posts/*.md` | Blog posts |
| Colours and fonts | `src/styles/global.css` (`:root` tokens) | No |
| Signup endpoint | `src/pages/api/subscribe.ts` | No |

## Netlify setup (one time)

1. **Connect the repo** in Netlify. Build settings come from `netlify.toml`.
2. **Email provider**: in Site configuration > Environment variables, set `EMAIL_PROVIDER` to `kit` or `mailerlite` plus that provider's keys (see `.env.example`).
3. **CMS login**: create a GitHub OAuth app (callback `https://api.netlify.com/auth/done`), then add it under Netlify Site configuration > Access & security > OAuth > Install provider > GitHub. Visit `/admin` and log in with GitHub.
4. **Domain**: add your domain in Netlify and update `site` in `astro.config.mjs`.

The CMS commits to `main` (set in `public/admin/config.yml`). Each edit triggers a rebuild, live in about a minute.
