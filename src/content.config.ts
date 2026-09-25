import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    image: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const offers = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/offers' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    price: z.string(),
    cta_label: z.string().default('Book now'),
    // Stripe Payment Link, Calendly, or any checkout URL
    cta_url: z.string(),
    featured: z.boolean().default(false),
    order: z.number().default(0),
    includes: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const testimonials = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/testimonials' }),
  schema: z.object({
    name: z.string(),
    role: z.string().optional(),
    quote: z.string(),
    // Only publish testimonials the client has given written permission to use
    permission_confirmed: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { posts, offers, testimonials };
