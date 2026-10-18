# Navin Jairam M — portfolio

A lightweight, multi-page static portfolio built with HTML, CSS, and vanilla JavaScript. GitHub Actions builds, tests, and deploys the site to GitHub Pages.

## GitHub Pages setup

1. Push this repository to `Lucifer-Newstar/Portfolio` on the `main` branch.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
3. The workflow in `.github/workflows/pages.yml` will build and publish the `site/` directory on each push to `main`. Pull requests run the build and checks without deploying.
4. The expected project-site URL is `https://lucifer-newstar.github.io/Portfolio/`. The workflow generates canonical and social-preview URLs for the repository owner and repository name automatically.

The generated `404.html` is included in the Pages artifact; its links use the base path from the build URL (`/Portfolio/`), so it works at any depth. Links use `.html` filenames, so the site works without server-side rewrite rules. For a custom domain, update the build URL in the workflow and configure the domain under Pages settings.

**Portfolio Platform source link:** set `PORTFOLIO_PLATFORM_REPO` near the top of `build.py` to the cleaned, renamed AWS repo's name; while it is `""` the site shows "Source: private, available on request".

## Local development

```sh
python3 build.py https://lucifer-newstar.github.io/Portfolio/
node --test test/site.test.js
```

The build script generates the HTML pages into `site/`; edit `pages.py` for page content and the corresponding files in `site/` for shared CSS, JavaScript, fonts, images, and other static assets. The test suite checks page metadata, local links, accessibility landmarks, required portfolio content, and the downloadable resume. It requires Node.js, Python 3, and `pdftotext` (provided by `poppler-utils` on Ubuntu).

## Repository layout

- `.github/workflows/pages.yml` — validation and GitHub Pages deployment workflow
- `build.py`, `pages.py` — static HTML generation
- `site/` — deployable website, including `404.html`, assets, and resume
- `test/site.test.js` — generated-site regression tests
