import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const testimonials = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/testimonials' }),
  schema: z.object({
    // As the member agreed to be named: full name, first name or initials
    name: z.string(),
    // The goal they came in with, matching the calculator goals
    goal: z.enum(['debt', 'secure', 'wealth']).optional(),
    headline: z.string(), // questionnaire Q12: how they feel about money now
    before: z.string().optional(), // Q1: their situation in the weeks before joining
    tipped: z.string().optional(), // Q2: the moment they decided to join
    doubt: z.string().optional(), // Q3 and Q4: their doubts, and how they look now
    doing_now: z.string().optional(), // Q10: one thing they do now that they didn't before
    // Placeholders show until real answers arrive; remove them before launch
    placeholder: z.boolean().default(false),
    // Only publish testimonials the member has given written permission to use
    permission_confirmed: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { testimonials };
