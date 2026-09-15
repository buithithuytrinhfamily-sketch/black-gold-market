# Black Gold Market free resource expansion

The published site remains plain HTML/CSS/JavaScript on GitHub Pages, branch `main`, root directory. No package installation or server is needed for publishing.

## Editing the new resources

- `content/academy.tsv`: original lesson content. Seven pipe-separated fields per row.
- `content/glossary.tsv`: glossary definitions and topics.
- `content/quizzes.json`: questions, options, correct index and explanation.
- `scripts/build-portal.py`: resource page templates, navigation, tools, source attribution and route generation.
- `scripts/templates/`: shared document head and existing signup/analytics tail.
- `assets/academy.js`: local progress, quizzes, data clients, journal and widgets.
- `assets/tool-math.js`: pure calculator functions.
- `assets/academy.css`: responsive styles extending the existing portal.

Run from the repository:

```sh
python3 scripts/build-portal.py
node tests/tool-math.cjs
python3 tests/check-links.py
```

Commit both edited sources and generated HTML. GitHub Pages serves the committed files directly; it does not run this generator.

## Daily article publisher

Always pull `main` before editing and rebase on the latest remote before pushing. Do not force-push. The generator never rewrites individual `journal/*.html` articles. It adds new sitemap URLs while retaining existing entries. The homepage keeps the original journal section class and `j-grid`/`jcard` structure. Category hubs refresh their links from `/journal/` on page load; static category links remain if that request fails.

The external daily publishing script was not provided or modified. If it replaces the entire homepage or journal index from an old template, its template must be updated separately to preserve the new navigation, style links and resource sections. Appending journal cards within the existing container is compatible. Do not run this generator over another worker's uncommitted changes.

## Data and storage

TradingView embeds: charts, FX heatmap/screener, crypto heatmap, news and economic calendar. Their attribution and source links remain visible. Data availability/delay is controlled by TradingView. Failed widgets retain a source link; no synthetic prices are used as a fallback.

Frankfurter v2: daily reference conversion and an equal-weight currency-strength comparison. Publication dates are displayed. These are not intraday trading quotes.

Progress, quiz scores and practice trades use browser local storage, with explicit local-only labels. Progress and journal support export/import. Storage failures are reported. There is no website account backend, member forum, protected paid-course library or cross-device synchronization.

The existing Blueprint/VIP flows and article content remain unchanged.
