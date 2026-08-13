# Computer Use Shopify Runbook

## Purpose

Use `computer-use:computer-use` for the fixed Finest Sculpture Shopify UI.
This preserves each operator's own authorized Chrome login without storing or
transferring credentials.

## Browser rules

1. Control Google Chrome only after explicit Action 2 approval.
2. Reuse the operator's existing Shopify login.
3. Never inspect cookies, local storage, profile files, password managers,
   access tokens, or hidden browser state.
4. After every navigation or UI-changing action, request fresh app state before
   using element indices again.
5. If Shopify shows login, password, or 2FA, ask the operator to complete it and
   then continue in the same task.

## Fixed URLs

- Storefront: `https://finestsculpture.com/`
- Shopify articles: `https://admin.shopify.com/store/c4055d-2/content/articles`
- Target blog: `News`

## Preflight

1. Confirm review approval and whether the final state is draft or published.
2. Confirm bundle validation passes.
3. Confirm exactly six local images exist.
4. Confirm at least two distinct verified product URLs exist in HTML and metadata.
5. Open the fixed articles route in the signed-in Chrome.
6. Confirm the visible store is FINEST SCULPTURE / `c4055d-2` before editing.

## Upload sequence

1. Open Blog posts and choose Add blog post.
2. Fill the reviewed title.
3. Switch the body editor to HTML only when necessary and insert validated safe HTML.
4. Upload all six images through Shopify's supported media UI.
5. Ensure final body references Shopify-hosted image URLs and preserves order and alt text.
6. Fill excerpt, author, restrained tags, target blog `News`, SEO title, meta description, and handle.
7. For draft approval, keep unpublished. For explicit publication approval, set published visibility.
8. Save, reopen the same article, and compare persisted values with metadata.
9. Open Shopify preview and inspect title, layout, six images, links, Sources, five-question FAQ, tags, and SEO.

Do not edit products, collections, themes, navigation, apps, domains, users,
billing, or unrelated articles.

## Publication and verification

Publication is authorized only by an explicit phrase such as `审核通过并发布`,
`确认发布`, `发布这篇文章`, or `上传并发布` for the reviewed bundle.

After publishing:

1. Open the public article URL.
2. Confirm all six images load and alt text is present.
3. Confirm product anchors are black and underlined.
4. Click every counted product anchor and verify destination product title and URL.
5. Confirm Sources immediately precedes the final five-question FAQ.
6. Open the storefront homepage and verify `Our Latest Blog Post` shows the new article.
7. Record admin, preview, public, product, and homepage results in the completion report.

If the homepage card is missing, compare the article blog with `News` and report
the mismatch. Theme changes require separate explicit authorization.
