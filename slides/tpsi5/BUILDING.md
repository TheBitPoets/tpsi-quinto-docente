# Build delle slide TPSI5

Le slide sorgente restano Markdown/Marp. HTML, PDF e PPTX sono artifact derivati e non vanno modificati a mano.

## Requisiti

- Python 3.11+;
- Node.js 18+ con `npx`;
- Chrome/Chromium per PDF e PPTX.

La versione del renderer e fissata in `scripts/build_slides.py` (`@marp-team/marp-cli@4.5.0`).

## Solo controllo strutturale

```bash
python scripts/build_slides.py --check-only
```

Il controllo verifica 19 deck modulari `00..18`, corrispondenza con i moduli canonici, front matter Marp, checkpoint/Feisbuc e link nell'indice slide.

## Build completa

```bash
python scripts/build_slides.py --formats html,pdf,pptx --browser chrome
```

Output predefinito:

```text
build/tpsi5-slides/
  html/
  pdf/
  pptx/
  MANIFEST.json
  SHA256SUMS.txt
```

Per una build rapida senza browser:

```bash
python scripts/build_slides.py --formats html
```

## CI

`.github/workflows/slides.yml` esegue controllo + build HTML/PDF/PPTX e pubblica un artifact GitHub Actions chiamato `tpsi5-slides-<commit-sha>` con retention di 30 giorni.

Gli artifact sono una derivazione del delivery layer. Il curriculum resta quello del Content Pack `1.0.0 / approved`.
