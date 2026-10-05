# Automatic sync from canaresai.com

The portal is a static site, so it cannot call canaresai.com with a secret directly (anyone could read it).
Instead, GitHub Actions pulls the data on the server side every 30 minutes and on every push, then deploys.

## One-time setup
1. Ask the canaresai.com team for a read-only API endpoint that returns the JSON below, and an access token.
2. In the GitHub repo: Settings > Secrets and variables > Actions > New repository secret:
   - `CANARES_API_URL` (full endpoint URL)
   - `CANARES_API_TOKEN` (sent as `Authorization: Bearer <token>`)
3. Actions tab > "Deploy to GitHub Pages" > Run workflow (to test). Until the secrets exist, sync is skipped.

## Expected JSON
```
{
 "orders": [ { "no": "PO-1001", "type": "Purchase Order" | "Work Order", "supplier_code": "SUP-002",
               "supplier": "S V INDIA COATINGS", "date": "2026-10-01", "due": "2026-10-20",
               "items": [ { "code": "C1", "name": "Powder coating", "qty": 500, "rate": 25 } ] } ],
 "gin":   [ { "GIN No.": "GIN-7365", "Date": "05 Oct 2026", "Supplier": "...", "PO No.": "", "Job Work DC": "WO-1001",
              "Invoice No.": "5312", "Received Qty": 203, "Accepted Qty": 203, "Rejected Qty": 0,
              "Status": "Approved", "GRN No.": "GRN-8341", "lines": [] } ],
 "grn":   [ { "GRN No.": "GRN-8341", "Date": "05 Oct 2026", "Supplier": "...", "GIN No.": "GIN-7365",
              "Accepted Qty": 203, "Inspected By": "pramod@canares.com", "lines": [] } ]
}
```
GIN and GRN accept either the ERP column names above or short keys (`no`, `date`, `supplier`, `po`, `dc`, `inv`, `rec`, `acc`, `rej`, `st`, `grn`, `by`). If your API uses other field names, edit `scripts/sync_canares.py` (the `pick(...)` calls).

## How matching works
- A GIN belongs to an order when its PO No, or its Job Work DC (work order), equals the order number. The GRN follows its GIN.
- Supplier is matched by `supplier_code`, else by exact supplier name, else by the saved name mappings.
- Feed records replace older feed records with the same number. Records added manually or by Excel are kept.
