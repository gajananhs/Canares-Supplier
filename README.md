# Canares Supplier Portal (PWA)

Real data loaded: 347 suppliers (Supplier Master), 327 GINs and 323 GRNs (ERP exports dated 05 Oct 2026).

## Logins
- Suppliers: User ID = supplier code (e.g. SUP-002), initial password in `Supplier_Login_Credentials.xlsx` (keep it out of the repo).
- Admin: `ADMIN` / `Canares@Admin2026`. Change by replacing `ADMIN_H` (SHA-256 of the new password) in `index.html`.
- Master records with the same company name (e.g. SUP-002 and SUP299) are treated as one supplier and see the same data.

## Admin: adding data
- Purchase Orders, GIN, GRN pages each have a green "+ Add" button with a form (required fields marked *).
- Import / Export page: upload the ERP GIN file (sheets GINs + GIN Lines), the GRN file (GRNs + GRN Lines) and the PO template (sheet PO). Select several files at once.
- Unmapped supplier names (typos in ERP) are listed on the Import / Export page; choose the right supplier and press Map.
- GIN rows without a PO No have a "Link PO" button so PO status can be tracked.

## Publishing changes to suppliers
Admin changes are stored in the admin's browser only. Click "Export transactions.json" and replace that file in the GitHub repo (Add file > Upload files). The site redeploys in about a minute.

## Status rules
- Pending: received qty (GIN tagged with the PO) is below PO qty.
- Delivered: received qty at least PO qty.
- Completed: delivered, accepted in full, GIN status Approved and GRN posted.
- Invoice quality: Approved = Passed, Partial = Partially accepted, Pending QC = Under inspection.

## Limits
Static site: all data files are readable by anyone with the site address and logins are checked in the browser. Pilot use only; production needs a backend with server-side login.
