# Analysis membership setup

Status: production project xgfkqwnfiguknpetxgcv is connected; schema installed and anonymous access checks passed. Enrollment remains closed. Production SMTP, owner account, content publication and authenticated acceptance checks are still pending. There is no paid article body in this repository. Local PostgreSQL policy tests and mocked browser contracts are not a live Supabase acceptance test.

## Connect the owner's project

1. Create a Supabase project owned by Black Gold Market. Keep its database password and all secret/service-role keys out of this public repository.
2. Run `supabase/migrations/202609150001_membership.sql` once using the project's SQL Editor. The migration creates tables, row access policies, and admin-only functions. Enrollment starts closed.
3. Enable email/password authentication with email confirmation. Set Site URL to `https://blackgoldmarket.us`; allow `https://blackgoldmarket.us/account/` as the confirmation/recovery redirect. Configure production SMTP for confirmation and recovery delivery. Supabase's default email service is limited and not a production mail setup.
4. Put only Project URL and **publishable key** in `assets/member-config.json`. No service-role or secret key is needed in the browser.
5. Register and verify the owner's account at `/account/`. Identify its UUID in Supabase Authentication. Grant admin through the SQL Editor (never through user-editable metadata):

```sql
insert into bgm_private.admins(user_id) values ('OWNER_AUTH_UUID');
```

6. Sign in at `/membership/admin/`. Add original articles with public previews and full plain-text bodies; publish after review. Paid text must go only into the protected database, never GitHub HTML/JSON/assets.
7. Review the USDT TRC20 receiving address in `bgm_orders.wallet` against the owner's wallet. It was copied from the existing `/vip/` page: `TVF22a1qKYLHXWV6FUSgRAT1hKEGLfJm22`. A QR was intentionally not copied because the existing page reuses an image across different networks. Monthly amount: 29 USDT; annual: 204 USDT. The site denominates membership in USD and accepts these fixed USDT amounts; no automatic debit or live exchange quote.
8. Before opening, verify production signup/confirmation, reset password, ordinary vs admin access, rejected orders, approval, early renewal, expiration and published/draft article access with controlled test accounts. Record test orders without sending money, review only designated test orders, and remove test memberships/orders before launch. Do not approve a real customer's payment without checking the blockchain transaction.
9. Publish at least one complete premium article and clarify customer service/refund terms before accepting payments. Only after these checks, enable enrollment:

```sql
update public.bgm_settings set enrollment_open=true where id=true;
```

To stop new orders, set the flag false. Existing created orders can still submit their transaction for review; existing members keep their paid access. Announce payment instructions accordingly.

## Daily operation

- Pending payments: `/membership/admin/`. Inspect Tronscan manually for successful transfer of the real USDT TRC20 token, receiving address, full net amount, confirmations, and correspondence to the submitting customer. Transaction ID possession alone does not prove ownership. Review notes are visible to the customer.
- Approval adds one calendar month or year from the later of current expiry or approval time. Approval and extension occur in one transaction; duplicate review fails. Expiry is checked by database policies on every article body request, without a scheduled task.
- Renewal is manual; no recurring charge and no email reminder service is implemented.
- Edit an article by loading it from the admin list. Uncheck Publish to remove it from public listings. Full text is rendered as plain text, not executable HTML.
- For exceptional access revocation, an authorized operator can update `bgm_memberships.expires_at` in the Supabase dashboard. There is no customer-side write permission.
- Lesson progress stays browser-local and is not synchronized to membership accounts.
- Account deletion and data requests are handled by the owner via the contact route. Preserve financial records according to the owner's applicable obligations; choose a retention policy before launch.

## Validation

Run from repository root:

```sh
python3 scripts/build-portal.py
python3 tests/check-links.py
node --check assets/membership.js
NODE_PATH=/path/to/test-only/node_modules node tests/membership-db.cjs
PLAYWRIGHT_PATH=/path/to/playwright node tests/membership-browser.cjs
```

Database test dependency: `@electric-sql/pglite`, installed outside this public site. Browser tests expect a local server on port 8765 and use mocked Supabase responses. Actual hosted configuration, SMTP delivery and real network payments remain to be checked after connection.

Vendor client: `@supabase/supabase-js@2.102.0`, downloaded from its jsDelivr UMD distribution. Public reference: https://supabase.com/docs/guides/auth/passwords and https://supabase.com/docs/guides/database/postgres/row-level-security.
