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
    // As the member agreed to be named: full name, first name or initials
    name: z.string(),
    descriptor: z.string().optional(),
    // The goal they came in with, matching the calculator goals
    goal: z.enum(['debt', 'secure', 'wealth']).optional(),
    before: z.string().optional(), // questionnaire Q12: how they felt before joining
    now: z.string(), // Q12: how they feel now
    moment: z.string().optional(), // Q6 or Q10: a specific change
    // Placeholders show until real answers arrive; remove them before launch
    placeholder: z.boolean().default(false),
    // Only publish testimonials the member has given written permission to use
    permission_confirmed: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { posts, offers, testimonials };
