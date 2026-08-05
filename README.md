# figaroehf.is

Static website for Figaro ehf — Reykjavík-based financial consulting firm.
Built as a single-file HTML site using the Figaro brand system (deep navy on warm paper, EB Garamond + Instrument Sans, restrained editorial style).

## Files

```
index.html              The site (single file, all 5 sections inline)
assets/figaro-logo.png  The brand mark
README.md               This file
```

## Local preview

Open `index.html` in any browser — no build step, no server needed.

## Setting up Git (one-time)

The folder includes a broken `.git/` from earlier setup attempts. Wipe it and re-init from PowerShell or Git Bash on Windows:

```powershell
cd C:\Users\valdi\Documents\FigaroCowork\Project\figaroehf-site
Remove-Item -Recurse -Force .git
git init -b main
git config user.email "valdimar@figaroehf.is"
git config user.name "Valdimar Hilmarsson"
git add .
git commit -m "Initial commit — figaroehf.is static site"
```

## Contact form — connect Formspree

The form in `index.html` posts to a placeholder URL. Wire it up:

1. Sign up at [formspree.io](https://formspree.io) with `valdimar@figaroehf.is` (free tier: 50 submissions/month, plenty)
2. Create a new form, name it "figaroehf.is contact"
3. Copy the form ID (looks like `xrgjeoqz` or similar)
4. In `index.html`, find `https://formspree.io/f/YOUR_FORM_ID` and replace `YOUR_FORM_ID` with your real ID
5. Commit + deploy. First submission triggers a confirmation email from Formspree — confirm it once.

The honeypot anti-spam field (`_gotcha`) and subject prefix (`_subject`) are pre-wired — Formspree handles them automatically.

## Deploy options

### Option A — GitHub Pages (free, easiest)

1. Create a public GitHub repo (e.g. `figaroehf/figaroehf.is`)
2. Push:
   ```powershell
   git remote add origin https://github.com/figaroehf/figaroehf.is.git
   git push -u origin main
   ```
3. In repo Settings → Pages → Source: `main` branch, root folder. Save.
4. Wait ~30 sec. Site is live at `https://figaroehf.github.io/figaroehf.is/`.
5. To use `figaroehf.is` domain: in repo Settings → Pages → Custom domain, type `figaroehf.is`. Save.
6. At your DNS provider (where `figaroehf.is` is registered), point the apex `A` records to GitHub's IPs:
   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```
   And `CNAME www` → `figaroehf.github.io`
7. GitHub auto-issues a Let's Encrypt SSL cert within ~24h.

**Pros:** free forever, auto-deploy on push, zero server config.
**Cons:** repo must be public for the free tier. Also routed through US infrastructure.

### Option B — 1984.is (Icelandic hosting)

If you already have a 1984 hosting plan, this keeps everything Icelandic.

1. SFTP into your 1984 hosting (credentials from your 1984 control panel)
2. Upload `index.html` and `assets/` folder to the web root (typically `public_html/` or `www/`)
3. Point `figaroehf.is` DNS A-record to the 1984 server IP (in the 1984 control panel)
4. Enable Let's Encrypt SSL via 1984 control panel

**Pros:** Icelandic data sovereignty, supports a privacy-focused Icelandic provider.
**Cons:** manual upload on each change (no auto-deploy unless you set up rsync/CI).

### Updating the site

After making any text or design change to `index.html`:

**GitHub Pages:**
```powershell
git add .
git commit -m "Update: <what changed>"
git push
```
Live within ~30 sec.

**1984:** SFTP the changed files. Live immediately.

## Updating Guinness fund table

Once a month, refresh the NAV / YTD / 1 yr / 3 yr numbers from the Guinness factsheets (Y EUR Acc class):
- [Global Equity Income factsheet](https://www.guinnessgi.com/sites/default/files/factsheets/guinness-global-equity-income-fund-en.pdf)
- [Global Innovators factsheet](https://www.guinnessgi.com/sites/default/files/factsheets/guinness-global-innovators-fund-en.pdf)

The table lives in **two** files — update both:

- `guinness.html` — search for `Ávöxtun (í EUR)`. Icelandic number format: decimal **comma** (`25,3062`, `-0,6%`), date as `DD.MM.YYYY`.
- `en/guinness.html` — search for `Performance (in EUR)`. English number format: decimal **point** (`25.3062`, `-0.6%`), date as `D Mon YYYY` (e.g. `30 Apr 2026`).

In each file update: the date in the table heading, the 8 number cells (NAV / YTD / 1 ár / 3 ár per fund), the `pos`/`neg` class on each cell to match the sign, and the factsheet month in the footnote below the table. Commit, push, done.

## Adding the English version (later)

When ready, duplicate `index.html` to `en/index.html`, translate copy into editorial English, and add a language toggle in the header. The brand voice rules apply: confident, restrained, Damodaran terminology in English.

## Brand reference

Full brand system lives at `../../Figaro-brand/` — colors, type, logos, and the original UI kit.
Key tokens used in this site (already inlined in `index.html`):

- Navy: `#00324B` (primary), `#001932` (deep)
- Paper: `#FAFAF7`, `#F4F5F2`
- Brass accent: `#A37E2C`
- Type: EB Garamond (display), Instrument Sans (body)
