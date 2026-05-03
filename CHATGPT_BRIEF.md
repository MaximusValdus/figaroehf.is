# Figaro ehf — Design Brief for ChatGPT

Paste this into a fresh ChatGPT conversation to bootstrap design work. Iterate from there: ask for new section mockups, image prompts, copy variations, etc. When you have something you like, share with Claude in Cowork to implement in HTML.

---

You are designing a marketing website for **Figaro ehf**, a boutique financial consulting firm in Reykjavík, Iceland, owned by Valdimar Hilmarsson.

## Brand aesthetic

**Editorial finance.** Think Financial Times weekend supplement, the annual report of an old European bank, Bloomberg Markets, Condé Nast Traveler. Restrained, classical, considered. Not a SaaS startup. Not consumer-app cheerful. Trust is built in typography, whitespace, and restraint — not in flourish.

## Color palette (use these exact hex codes)

- **Navy primary** `#00324B` — headings, CTAs, wordmark
- **Navy deep** `#001932` — dark bands, footer, deep backgrounds
- **Paper** `#FAFAF7` — primary background (never pure white)
- **Paper alt** `#F4F5F2` — alternate section bands
- **Brass** `#A37E2C` (primary), `#C49A47` (lighter), `#D4B16A` (lightest) — numerals, decorative accents, key figures, icon glyphs
- **Sage** `#5C8480` — used very sparingly for positive data
- **Ink** `#0F1A24` (primary text), `#2B3C4D` (secondary), `#6C7985` (muted)

Do not use brass for primary CTAs or body text — only as a decorative accent.

## Typography

- **Display / headings:** Source Serif 4 (regular weight 400). Classical transitional serif.
- **Body / UI:** Instrument Sans (regular 400, medium 500).
- Numerals (figures, tables): Instrument Sans with `tabular-nums` feature, or IBM Plex Mono.
- Sentence case for ALL headings and buttons. Lowercase `ehf` always — never `Ehf` or `EHF` in running text.

## Layout patterns

**Service card:**
1. Hero image at top, 16:10 aspect ratio, full-bleed
2. Brass-colored icon (Lucide style) inside a 48 px navy-700 circle, hanging at the bottom edge of the image (overlapping)
3. Brass numeral (01, 02, 03) in Source Serif 4, ~32 px, color `#A37E2C`
4. Heading in Source Serif 4 regular, ~24 px
5. Body description in Instrument Sans, ~15 px
6. Tinted paper-100 box at the bottom labeled `ALGENG VERKEFNI` (small letter-spaced eyebrow, navy color), with bullet list using brass chevron arrows (›)

**Header:** paper-50 background, 1 px hairline border below, sentence-case nav, navy CTA button on the right.

**Footer:** deep navy `#001932` background, paper-50 text, three columns (Starfsemi / Stofan / Tengiliðir), small kt./Reykjavík bottom strip.

**Brand flourish:** A single 48 px brass horizontal rule under the hero, once per page maximum.

## Tone of voice (Icelandic)

- Confident, direct, professional. No hedging.
- No exclamation marks. No emoji. Em dashes (—) welcome.
- Damodaran-aligned financial terminology: *verðmat*, *sjóðstreymisgreining*, *WACC*, *betastuðull*, *eiginfjárhlutfall*.
- "Við" as collective voice (even though Figaro is solo practice).
- Icelandic must read as Icelandic — no calques from English.
- Short, structured sentences. Trust the reader. Tight copy beats long copy.

## The firm's three service areas

1. **Greiningar og verðmöt** — Við vinnum fjárhagsgreiningar, viðskiptaáætlanir og verðmöt fyrir eigendur, stjórnir, kaupendur og fjárfesta. Greiningin byggir á skýrum forsendum, íslenskum markaðsaðstæðum og raunhæfu mati á rekstri, sjóðstreymi og virði fyrirtækja.
   - Algeng verkefni: Söluferli og fyrirtækjamat · Mat fyrir kaup eða samruna · Viðskiptaáætlun vegna fjármögnunar

2. **Fjármögnun** — Við styðjum fyrirtæki og eigendur í fjármögnunarferlum, hvort sem um er að ræða eiginfjármögnun, lánsfjármögnun eða blandaða fjármögnun. Aðstoðin getur náð frá undirbúningi og fjárfestakynningum til samskipta við banka, sjóði og fjárfesta.
   - Algeng verkefni: Fyrirtæki í fjármögnunarferli · Eigendur í viðræðum við banka eða fjárfesta · Endurfjármögnun eða endurskipulagning skulda

3. **Miðlun** — Figaro aðstoðar innlenda og erlenda aðila við að byggja upp tengsl á íslenskum fjármálamarkaði. Þjónustan felur meðal annars í sér markaðsinnsýn, kynningar, fundi og eftirfylgni gagnvart fagfjárfestum og stofnanafjárfestum.
   - Algeng verkefni: Innlend fyrirtæki sem leita erlendra fjármögnunaraðila · Erlendir aðilar með áhuga á íslenskum markaði · Sjóðastýringaraðilar sem vilja kynna sig fyrir íslenskum stofnanafjárfestum

## Hero (home page)

- Eyebrow: `FIGARO EHF · REYKJAVÍK`
- Display: `Fjármálaráðgjöf.`
- Lede (italic): `Ráðgjöf, greiningar og verðmöt, og tenging við alþjóðlegt fjármálaumhverfi.`
- CTAs: `Hafa samband` (filled navy) + `Lesa um nálgun okkar →` (text link)
- Brass 48 px rule below CTAs
- Meta strip with two columns: ÞJÓNUSTA: `Greiningar · Fjármögnun · Miðlun` | SAMSTARFSAÐILAR: `Guinness Global Investors`

## Other pages still to design

- **Um Figaro** — about page. Sections: Bakgrunnur (Valdimar's background, MBA at Háskóli Íslands), Aðferðafræði (Damodaran, Icelandic parameters), Sjálfstæði (no commissions, conclusions are Figaro's alone). Plus meta strip on the right (Stofnað 2013, Eigandi, Menntun, Staðsetning, Tungumál).
- **Guinness Global Investors** — dedicated partner page. Two fund cards (Global Equity Income, Global Innovators) with descriptions and ISINs, performance table (NAV, YTD, 1 yr, 3 yr in EUR), Guinness logo.
- **Hafa samband** — contact form + meta sidebar (email `valdimar@figaroehf.is`, location Reykjavík, languages Icelandic/English).

## Imagery style

- Editorial finance photography. Cinematic, low-light, considered composition.
- Tonally consistent across the set: same lighting, similar color grade, similar depth of field.
- Deep navy + warm paper tones lean dominant.
- Avoid: smiling people in suits, exaggerated diversity stock, generic SaaS imagery, bright/neon colors, cartoon illustrations.

**Image generation prompt template** (paste into DALL-E / GPT-4o image gen):
```
Editorial finance photography, deep navy and warm-paper tones, cinematic lighting, [SUBJECT]. Style: Bloomberg Markets meets Condé Nast Traveler. Restrained, considered composition. No people. 16:10 ratio.
```

Service-card subjects that work:
- **Card 01 (Greiningar):** magnifying glass on financial charts and printouts, calculator visible, warm desk lighting
- **Card 02 (Fjármögnun):** empty modern boardroom at dusk, view of Reykjavík harbour or mountains through window, laptop and documents on long dark table
- **Card 03 (Miðlun):** dark globe with glowing brass arcs connecting Iceland to London, New York, and other financial centers, night-side of earth visible

## What I want from you

- Visual mockups of additional sections in the same style as the home page (Um Figaro, Guinness page, Contact page)
- Image prompts I can use to generate matching imagery
- Copy variations where they could be sharper
- Suggestions for editorial photography that elevates the brand

## What I do NOT want

- SaaS startup vibes
- Stock-photo people (smiling, in suits, generic diversity casts)
- Bright or neon colors
- Cartoon illustrations
- Marketing-speak ("we're excited", "world-class", "revolutionary")
- Long padded copy
- Exclamation marks or emoji

---

Reference: full brand documentation lives in the Figaro-brand folder of the project (README.md, colors_and_type.css). Ask if you need anything more specific.
