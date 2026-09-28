# AsriyyaMUN’27

Static conference website for **March 18–20, 2027**, at the Landmark Hotel in Amman.

Theme: **Turn The Tide**.

## Structure

- `dist/` — the complete deployable website: 21 HTML pages, styles, scripts, portraits, gallery photographs, fonts, and committee documents.
- `content.json` — the Secretary General and Head of Conference letters and theme text.
- `team.json` — the current 15-person team, roles, and portrait framing.
- `scripts/apply-content.py` — applies letter/theme content and shared navigation to the existing HTML pages.
- `scripts/apply-team.py` — updates the team cards from `team.json`.
- `scripts/serve.py` — a local preview server with the clean URLs used by the site's navigation.

The original visual design was retained from the supplied AsriyyaMUN website. The current version includes the new letters and portraits, the 2027 team, the 2026 leadership history entries, the updated dates, and the new application form.

## Preview locally

Python 3 is sufficient; no package installation or build is needed to view the site.

```sh
python3 scripts/serve.py
```

Open `http://127.0.0.1:8000`. Use `--port 8080` to select another port.

## Edit content

The HTML in `dist/` is tracked source and is ready to deploy. For changes to letters, the theme, or the team, edit the corresponding JSON and run:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/apply-content.py
python3 scripts/apply-team.py
```

Other page content, dates, and shared links can be edited directly in the relevant HTML files. Shared header and footer content is repeated across all pages.

Team photographs use CSS crop windows over the supplied portrait sheets, keeping the original photographs unchanged while hiding the sheets' white margins and printed captions.

## Hosting

Publish `dist/` as the web root. The host must resolve clean paths such as `/about` to `/about.html`. Assets use root-relative URLs, so deployment at a domain root is expected.

GitHub repository publication alone does not enable GitHub Pages or change the live site's hosting. The source website is deployed separately through Sites; its service-specific configuration is omitted from this portable package.

## Links and forms

- Instagram: <https://www.instagram.com/asriyyamun27/>
- Delegate application: <https://forms.gle/PbDKQKTDjiZgJEY48>
- The contact form opens the visitor's email application, addressed to `info@asriyyamun.net`; it does not send mail through a server.

Conference images, branding, and supplied documents remain subject to their respective owners' rights. No new redistribution license is granted by this repository.
