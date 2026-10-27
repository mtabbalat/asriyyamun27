# AsriyyaMUN’27

Static conference website for **March 18–20, 2027**, at the Landmark Hotel in Amman.

Theme: **Turn The Tide**.

## Structure

- `dist/` — the complete deployable website: 21 content pages, a 404 error page, styles, scripts, portraits, gallery photographs, fonts, and committee documents.
- `content.json` — the Secretary General and Head of Conference letters and theme text.
- `team.json` — the current 15-person team, roles, and portrait framing.
- `scripts/apply-content.py` — applies letter/theme content and shared navigation to the existing HTML pages.
- `scripts/apply-team.py` — updates the team cards from `team.json`.
- `scripts/serve.py` — a local preview server with the clean URLs used by the site's navigation.

The original visual design was retained from the supplied AsriyyaMUN website. The current version includes the new letters and portraits, the 2027 team, the 2026 leadership history entries, the updated dates, and the new application form.

## Launch locally

Install **Python 3.9 or newer** if it is not already installed. No npm, package installation, or build is needed to view the site.

Download this repository with **Code → Download ZIP**, extract it, and open a terminal in the extracted folder containing `README.md`, `scripts/`, and `dist/`. Alternatively, use Git:

```sh
git clone https://github.com/mtabbalat/asriyyamun27.git
cd asriyyamun27
```

On macOS or Linux, start the server:

```sh
python3 scripts/serve.py
```

On Windows, use:

```powershell
py scripts/serve.py
```

Open **http://127.0.0.1:8000** in a browser and leave the terminal running. Press **Ctrl+C** in the terminal to stop the server. If port 8000 is busy, append `--port 8080` to the command and open http://127.0.0.1:8080 instead.

Use this preview server rather than double-clicking an HTML file: it serves the root-relative assets and clean page URLs such as `/about`, `/team`, and `/letter-from-the-hoc`. It only listens on your own computer; running it does not publish the site online.

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

The site is ready to deploy as static files. Publish **`dist/` as the web root**, not the repository root. Keep all subfolders, including `_next`, `images`, `gallery-2022`, and `files`. No database, backend, secrets, npm installation, or build step is required.

### Cloudflare Pages

Import this GitHub repository into a new **Pages** project with these settings:

| Setting | Value |
| --- | --- |
| Repository | `mtabbalat/asriyyamun27` |
| Production branch | `main` |
| Framework preset | None |
| Root directory | Leave blank (repository root) |
| Build command | `exit 0` |
| Build output directory | `dist` |

Cloudflare Pages serves the existing clean URLs such as `/about` and `/forums/security-council` directly from their HTML files. The included `404.html` gives missing pages a proper error page instead of silently displaying the homepage. Select **Save and Deploy** when you are ready to make the site public. Future pushes to `main` will update the connected deployment.

References: [Cloudflare static HTML deployment](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) and [route matching](https://developers.cloudflare.com/pages/configuration/serving-pages/).

### Other static hosts

Use `dist` as the publish/output directory and enable clean URL resolution (`/about` → `/about.html`). Assets use root-relative URLs, so host the site at a domain root, for example `https://your-site.example/`. A GitHub Pages project URL with an `/asriyyamun27/` prefix needs base-path changes; uploading the repository to GitHub alone does not enable hosting.

After deployment, check the homepage, both letters, the team portraits, the conference history, a committee page and its downloads, and the 2022 gallery.

## Links and forms

- Instagram: <https://www.instagram.com/asriyyamun27/>
- Delegate application: <https://forms.gle/PbDKQKTDjiZgJEY48>
- The contact form opens the visitor's email application, addressed to `info@asriyyamun.net`; it does not send mail through a server.

Conference images, branding, and supplied documents remain subject to their respective owners' rights. No new redistribution license is granted by this repository.
