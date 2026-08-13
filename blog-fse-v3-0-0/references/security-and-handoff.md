# Security and Operator Handoff

## Included in this portable skill

- Public storefront and Shopify store identifiers.
- Target blog `News` and homepage module name.
- Content, image, SEO, product-link, validation, upload, and verification rules.
- Deterministic validation and Word-generation scripts.
- Computer Use instructions for the operator's signed-in Chrome.

## Never include or request

- Shopify passwords, API keys, Admin API tokens, custom-app secrets, cookies,
  local storage, browser profiles, password-manager entries, or 2FA recovery data.
- The owner's authenticated Chrome state.
- OpenAI API keys. The workflow uses Codex/ChatGPT product authentication and
  built-in tools available to the installed operator.

## What a new operator needs

1. Codex with this skill installed.
2. Computer Use / Chrome control enabled.
3. Their own authorized Shopify staff account for FINEST SCULPTURE.
4. One-time Shopify sign-in in their own Chrome; subsequent runs reuse it.

This is the only human setup that cannot safely be packaged. The skill never
asks the operator to configure a Shopify store, create a custom app, or paste a
Shopify/OpenAI API key.
