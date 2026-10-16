# Navin Jairam M — portfolio site

Static site: plain HTML, CSS and JavaScript. No framework, no backend, no build tools needed to host it.

## Layout
- `site/` — the deployable folder. Upload its contents as-is.
- `build.py` + `pages.py` — regenerate the HTML pages: `python3 build.py https://your-domain/`
  (the URL is used for the canonical and Open Graph tags; `styles.css`, `script.js`, `og.png` and `assets/` are edited directly in `site/`).
- `test/site.test.js` — content and link checks: `node --test test/site.test.js`

## Notes
- Theme: `theme-init.js` sets light/dark before first paint (saved choice in localStorage, else the OS setting); the sun/moon button and the `theme light|dark` terminal command switch it.
- Background: two fixed canvases in `script.js` (DevOps motifs), ~30 fps, paused when the tab is hidden, static under reduced motion.
- Photo: `site/assets/img/navin.webp` + `navin.jpg` (600×600). Swap these two files to change it.
- The downloadable resume (`site/assets/Navin_Jairam_M_Resume.pdf`) is the copy without a phone number.

## Host it on AWS (S3 + CloudFront)
1. Create an S3 bucket (keep Block Public Access on) and upload everything inside `site/`:
   `aws s3 sync site/ s3://YOUR-BUCKET/ --delete`
2. Create a CloudFront distribution with the bucket as origin, using Origin Access Control, default root object `index.html`,
   and a custom error response that maps 404 to `/404.html`.
3. Point your domain at the distribution (Route 53 alias record + an ACM certificate in us-east-1).
4. Rebuild with your domain so the share-preview tags point at it: `python3 build.py https://your-domain/` and sync again.

Page links use `.html` file names, so they work on S3/CloudFront without any rewrite rules.
