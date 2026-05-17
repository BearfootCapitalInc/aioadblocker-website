# aioadblocker-website

Marketing website for **All-In-One Adblocker** — `aioadblocker.com`.

## Structure

```
index.html              Canonical landing page
privacy.html            Rendered privacy policy
assets/                 Image assets referenced by index.html and privacy.html
source/                 HTML sources used to render screenshot PNGs (regenerate via headless chromium)
source/policy/          Markdown sources for the policy and Chrome Store listing
```

## Deploy

Static site — drop the contents at the web root of your host.

```bash
rsync -av --delete ./ user@host:/var/www/html/aioadblocker/
```

## Regenerating screenshots

The PNGs in `assets/` are rendered from the HTML files in `source/` via headless chromium.

```bash
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=500,430 \
  --screenshot=assets/yt-before.png \
  file://$PWD/source/yt-before.html
```

Window sizes per file:
- `yt-before.html`, `yt-after.html`, `news-before.html`, `news-after.html` → `500x430`
- `six-engines.html` → `500x820`, then auto-crop white space (see note below)

The six-engines output requires post-crop with PIL to trim trailing white space:

```python
from PIL import Image
img = Image.open('assets/six-engines.png').convert('RGB')
# detect last row containing the green AIO card border, crop just below
```

## Build

No build step. Pure HTML + inline CSS + inline SVG.

## License

Proprietary — All-In-One Adblocker / BearfootCapitalInc.
