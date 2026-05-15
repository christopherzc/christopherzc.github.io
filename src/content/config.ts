import { defineCollection, z } from "astro:content";

const publications = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    authors: z.string().optional(),
    venue: z.string(),
    date: z.coerce.date(),
    paperurl: z.string().url().optional(),
    excerpt: z.string(),
    highlight: z.boolean().default(false),
    order: z.number().optional(),
  }),
});

const talks = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    venue: z.string(),
    date: z.coerce.date(),
    location: z.string().optional(),
    kind: z.string().default("Talk"),
  }),
});

const teaching = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    role: z.string(),
    course: z.string(),
    venue: z.string(),
    term: z.string(),
    date: z.coerce.date(),
    instructor: z.string().optional(),
  }),
});

export const collections = { publications, talks, teaching };
