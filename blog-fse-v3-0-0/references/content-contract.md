# Blog—FSE—V3.0.0 Content Contract

## Publication copy

- One H1 and 5–8 decision-focused H2 sections.
- 1,200–1,500 American English words unless the operator specifies otherwise.
- Complete meaning-matched Chinese review copy, not a summary.
- Buyer's answer within the first 100 English words.
- Short paragraphs, concrete tradeoffs, and one clear recommendation.
- Practical CTA before sources and FAQ.
- `Sources and Technical References` immediately before FAQ.
- `Frequently Asked Questions` is the final H2 and contains exactly five H3 questions.
- Nothing follows FAQ.

## Research and truthfulness

- Use at least three authoritative external sources and link claims close to support.
- Prefer primary government, standards, museum, university, or technical sources.
- Distinguish verified cases, disclosed composites, and illustrations.
- Generated images are original AI design visualizations, never customer projects.
- Never invent prices, timing, grades, certifications, warranties, clients, or outcomes.

## Images

- Exactly six distinct landscape images: one hero and five section visuals.
- Every image has accurate alt text and one intended insertion point.
- No text, logos, watermarks, malformed anatomy, impossible fabrication, or fake evidence.
- Store final files under `images/` in the article bundle.

## Product internal links

- At least two distinct verified URLs on `https://finestsculpture.com/products/...`.
- Each link must resolve to a live, relevant product detail page.
- Use descriptive anchor text, never raw URLs or `click here`.
- Render each product anchor with `style="color:#111111;text-decoration:underline;"`.
- Do not insert or count same-domain collections, blogs, pages, searches, redirects, previews, admin URLs, or guessed URLs.
- Keep authority citations unchanged; they are sources, not internal links.
- Block upload when fewer than two relevant products can be verified.

## Shopify-safe HTML

Use semantic body markup only: `h2`, `h3`, `p`, `ul`, `ol`, `li`, `strong`,
`em`, `a`, `figure`, `img`, `figcaption`, `blockquote`, `table`, `thead`,
`tbody`, `tr`, `th`, `td`, `br`, and `hr` when useful. Do not include `html`,
`head`, `body`, `script`, `style`, `iframe`, `form`, `object`, `embed`,
JavaScript URLs, event handlers, or tracking code.

## SEO

- SEO title: 45–60 characters.
- Meta description: 140–160 characters.
- Handle: lowercase ASCII words separated by hyphens, no dates or local suffixes.
- Excerpt: useful 1–2 sentences, not copied verbatim from meta description.
- Tags: restrained and topical.

## Required metadata

```json
{
  "siteId": "finest-sculpture",
  "topic": "",
  "primaryKeyword": "",
  "targetWords": 1200,
  "seo": {
    "title": "",
    "metaDescription": "",
    "handle": "",
    "excerpt": "",
    "tags": []
  },
  "researchSources": [
    {"title": "", "url": "", "usedFor": ""}
  ],
  "internalLinks": [
    {"anchor": "", "url": "", "type": "commercial", "verified": true}
  ],
  "imagePlan": [
    {"file": "images/example.jpg", "purpose": "hero", "alt": "", "prompt": "", "status": "generated"}
  ],
  "review": {"status": "pending | approved", "approvedAt": ""},
  "shopify": {
    "targetBlog": "News",
    "draftCreated": false,
    "draftUrl": "",
    "previewUrl": "",
    "published": false,
    "publicUrl": ""
  },
  "validation": {"passed": false, "checkedAt": ""}
}
```
