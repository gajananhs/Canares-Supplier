# Canares Supplier Portal (PWA)

Installable supplier portal loaded with the Canares Supplier Master (347 suppliers). No dummy data.

## Features
- Supplier login (User ID = supplier code, e.g. SUP-002). Each supplier sees only their own data.
- Dashboard: total PO received, pending, delivered and completed.
- GIN (gate inward) and GRN (goods receipt with quality result) linked to POs.
- Invoice status showing GIN, GRN, Quality and payment (cleared / on hold / paid).
- Admin (Canares): add or import POs, GIN, GRN and invoices, browse suppliers, post announcements.

## Status definitions
- Pending: GIN qty is less than PO qty.
- Delivered: GIN qty >= PO qty (includes completed).
- Completed: delivered, GRN accepted qty >= PO qty and quality passed.
- Invoice payment: Cleared for payment only when GIN received, GRN posted and quality passed; otherwise On hold.

## Logins
- Suppliers: see `Supplier_Login_Credentials.xlsx` (provided separately, do NOT commit it to the repo).
- Admin: User ID `ADMIN`, password `Canares@Admin2026`. Change it: compute the SHA-256 of a new password and replace `ADMIN_H` in `index.html`.

## Files
- `index.html` app; `suppliers.json` supplier master with password hashes; `transactions.json` PO/GIN/GRN/invoice data; `sw.js`, `manifest.webmanifest`, `icons/`; `.github/workflows/pages.yml` GitHub Pages deploy.

## Workflow for data
1. Log in as ADMIN, go to Import / Export, download the template, fill sheets PO, GIN, GRN, Invoice, import.
2. Click Export transactions.json and replace that file in the repo. Push. Suppliers then see the new data.

## Important limits
This is a static site. Data is in files, so anyone who opens the site files can read all supplier and transaction data, and logins are checked in the browser. Use it for a pilot only. For production use a backend (for example Supabase or Firebase) with server-side authentication.

## Deploy
Push to `main`, then Settings > Pages > Source: GitHub Actions. Local test: `python3 -m http.server 8080`.
