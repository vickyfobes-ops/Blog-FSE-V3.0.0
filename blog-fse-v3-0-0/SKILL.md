---
name: blog-fse-v3-0-0
description: "Run the fixed Finest Sculpture Shopify blog workflow in exactly three operator actions: (1) accept one topic and generate a source-backed American English article, meaning-matched Chinese review copy, Word review document, SEO metadata, and six original landscape images; (2) pause for human review and revise until explicitly approved; (3) discover and insert at least two verified Finest Sculpture product-detail links, validate, upload, publish, and verify the article through the operator's signed-in Chrome. Use when an operator invokes Blog—FSE—V3.0.0, asks for an FSE/Finest Sculpture blog, wants a bilingual Shopify review package, or approves a reviewed FSE article for publication. The store, target blog, domain, homepage module, formatting rules, and upload route are preconfigured; never ask for a Shopify API key or custom-app setup."
---

# Blog—FSE—V3.0.0

Operate the preconfigured Finest Sculpture workflow as three user-visible actions:

1. The operator inputs one topic; generate the complete review package.
2. The operator reviews it; revise until the operator explicitly approves.
3. After approval, add verified product links and automatically upload or publish.

Do not expose research, image generation, link discovery, HTML conversion,
preview, or verification as extra operator steps. Do not use the retired FSE
operations website or its `/executor` page. Do not ask for an OpenAI API key,
Shopify API key, custom app, access token, cookie, or session export.

## Required skills and browser surface

- Use `imagegen` for all six original images.
- Use `documents` for the Chinese Word review artifact when available; the
  bundled script is the deterministic fallback.
- Use `computer-use:computer-use` for Shopify UI work that depends on the
  operator's existing Google Chrome login.
- Use internet research for current claims and sources.

Read these files before acting:

- `assets/finest-sculpture.json` — fixed non-secret Shopify/site profile.
- `references/content-contract.md` — article, SEO, image, source, and link contract.
- `references/computer-use-shopify.md` — Chrome control and upload runbook.
- `references/security-and-handoff.md` — what is portable and what must never be packaged.

## Fixed production target

This skill is single-site and intentionally does not ask the operator to
configure Shopify. Always use the profile in `assets/finest-sculpture.json`:

- Brand: FINEST SCULPTURE.
- Storefront: `https://finestsculpture.com/`.
- Shopify store handle: `c4055d-2`.
- Shopify permanent domain: `c4055d-2.myshopify.com`.
- Target blog: `News`.
- Homepage module: `Our Latest Blog Post`.
- Internal links: at least two distinct direct `/products/` URLs.
- Images: exactly six.

The fixed profile removes repeated store setup, not Shopify authentication.
Each operator must have an authorized Shopify staff account and sign in to
Shopify in their own Chrome once. Continue from that existing login; never copy
the owner's browser state or credentials into the skill.

## Action 1 — Input one topic and generate

Accept one exact English title or a clearly selected topic. If it is specific
enough, start immediately. Do not produce a topic list unless separately asked.

### Research and write

- Research current facts online and record at least three authoritative sources.
- Prefer government, regulators, standards bodies, museums, academic or
  technical institutions, and original manufacturer documentation.
- Write 1,200–1,500 useful American English words and a complete
  meaning-matched Chinese version; the Chinese copy is not a summary.
- Answer the buyer's main question within the first 100 English words.
- Never invent projects, clients, prices, lead times, tests, certifications,
  warranties, quotations, or performance claims.
- Put `Sources and Technical References` immediately before the final FAQ.
- Make FAQ the final section with exactly five H3 questions.
- Mark natural product-link insertion points but never guess product URLs.

### Generate six images

- Generate exactly one hero and five section-specific landscape images.
- Use `imagegen` once per distinct image; do not use an API-key or CLI fallback.
- Do not include text, logos, watermarks, fake measurements, malformed anatomy,
  impossible supports, or documentary-looking fake customer evidence.
- Inspect every generated image and reject errors or near-duplicates.
- Save approved files under `blog-output/<slug>/images/` with accurate alt text.

### Build the review package

Create `blog-output/<slug>/` with:

- `<slug>.md` — English publication article.
- `<slug>.zh-CN.md` — complete Chinese review article.
- `<slug>.zh-CN.review.docx` — Chinese Word review document.
- `<slug>.meta.json` — SEO, sources, image plan, review, links, and Shopify state.
- `<slug>.review.md` — quality report and any blockers.
- `images/` — exactly six final images.

Run `scripts/build_review_docx.py --source-dir <output-directory>`. Present the
English draft, Chinese Word file, SEO, sources, and six images to the operator.

## Action 2 — Human review

Pause for the operator. Apply every requested content, image, SEO, source, or
layout revision and regenerate affected artifacts. Do not start Shopify work
until the operator explicitly says one of:

- `审核通过并上传为草稿`
- `审核通过并发布`
- `确认上传`
- `确认发布`
- `上传并发布`

Approval freezes the reviewed article, external sources, and six images.
Action 3 may add verified product links, convert to Shopify-safe HTML, upload
images, and make technical formatting changes. Any material editorial change
returns to Action 2 for fresh approval.

The phrase determines state: draft approval creates an unpublished draft;
publication approval uploads and publishes without another confirmation stage.

## Action 3 — Verified links and one-command Shopify delivery

Read `references/computer-use-shopify.md` completely and use the operator's
signed-in Chrome.

### Discover and insert product links

- Discover live products from the production storefront, its product sitemap,
  or Shopify admin.
- Open each candidate and verify it is a real product detail page on
  `finestsculpture.com` whose content is relevant to the article.
- Insert at least two distinct `/products/` links naturally in the English body.
- Use descriptive anchors styled exactly as black underlined text.
- Never count collections, blogs, pages, searches, redirects, previews, admin
  pages, staging hosts, guessed URLs, or broken URLs.
- Preserve approved external citations unchanged.
- If two relevant live product pages cannot be verified, stop and report the
  catalog blocker. Do not weaken the rule.

### Validate

- Build `<slug>.shopify.html` with semantic Shopify-safe body HTML.
- Insert all six images in the approved order with descriptive alt text.
- Set `review.status` to `approved`, the intended Shopify state, and all verified
  product links in metadata.
- Run:

```bash
python3 <skill-dir>/scripts/validate_publish_bundle.py \
  --dir <output-directory> \
  --slug <slug> \
  --domain finestsculpture.com
```

Fix every error. Never upload while validation fails.

### Upload, publish, and verify

- Open the fixed Shopify admin article route from the profile.
- Create a new article or update only the matching draft created for this topic.
- Upload all six images using Shopify's UI and replace local references with
  Shopify-hosted image URLs.
- Fill title, safe HTML body, excerpt, author, tags, SEO title, meta description,
  canonical handle, target blog `News`, and intended visibility.
- Save, reopen, and confirm persistence.
- For draft approval, leave unpublished and report admin plus preview URLs.
- For publication approval, publish and verify the public article and homepage
  `Our Latest Blog Post` card.
- On the public article, click both counted product anchors and confirm they open
  the intended product detail pages.

Continue autonomously through Action 3. Pause only for a real human blocker:
Shopify login, password, 2FA, unavailable Chrome control, or fewer than two
relevant products. Never inspect cookies, local storage, password managers,
session files, or access tokens.

## Completion report

Report title, slug, English word count, English/Chinese/Word paths, six image
files, all verified product links, unchanged authority sources, validation
result, Shopify admin/preview/public URLs, product-link click results, and
homepage-card result. Do not call incomplete work complete.
