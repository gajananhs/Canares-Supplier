# Canares Supplier Portal (PWA)

Installable, offline-capable supplier portal prototype: dashboard, purchase orders, ASN, FIP/FIR uploads, RFQs and invoices.

Front-end only. Data is sample data held in memory; any User ID and password work. Real login, database and ERP integration need a backend.

## Files
- `index.html` app (HTML, CSS and JS in one file)
- `manifest.webmanifest` PWA manifest
- `sw.js` service worker (offline cache)
- `icons/` app icons (192, 512, maskable 512)
- `.github/workflows/pages.yml` auto-deploy to GitHub Pages

## Deploy on GitHub Pages
1. Create a new repository and push these files to the `main` branch.
2. In the repo: **Settings > Pages > Build and deployment > Source: GitHub Actions**.
3. The workflow runs on each push. The site appears at `https://<user>.github.io/<repo>/`.

## Run locally
Service workers need http, not file://:

    python3 -m http.server 8080

Open http://localhost:8080

## Install
Open the site in Chrome or Edge and use the Install button or the address-bar install icon. On iPhone: Share > Add to Home Screen.

## Updating
After changing files, bump `CACHE` in `sw.js` (for example `canares-sp-v2`) so users get the new version.
