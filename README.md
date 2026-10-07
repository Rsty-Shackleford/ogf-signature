# OGF family email signatures

**Signature builder (share this link): https://rsty-shackleford.github.io/ogf-signature/**

- Logo images used by every signature: https://rsty-shackleford.github.io/ogf-signature/img/
- Source and history: https://github.com/Rsty-Shackleford/ogf-signature

One layout for everyone at OGF Manufacturing, Fearless Manufacturing and Crossroads Diesel. Each person opens the builder, picks their division, fills in the blanks, and pastes the result into their mail client. Nothing anyone types is sent anywhere; it stays in their own browser.

## Quick start for staff

1. Open the builder link above.
2. Pick your tab: **Fearless**, **Crossroads**, **Both** (you represent Fearless and Crossroads together) or **OGF**. The office number and address fill in for the division; change them if yours differ.
3. Type your name, title, mobile and email. Website is optional until the company has one.
4. Leave **Logo images** on Hosted and **Logo background** on Transparent unless the notes below give you a reason not to.
5. Click **Copy signature**, then follow the **Install it** tab for your mail client (classic Outlook, new Outlook and web, Outlook for Mac, Thunderbird, Gmail).

The three buttons:

| Button | What it copies | Use it for |
|---|---|---|
| **Copy signature** | The rendered signature, as in the preview | Outlook (all versions), Gmail, Apple Mail: paste into the signature editor |
| **Copy HTML source** | The code | Thunderbird's signature box with "Use HTML" ticked, or saving as a file |
| **Download .html** | The code, as a file | Thunderbird's "Attach the signature from a file" (works when the builder is opened from the file on disk; the hosted page cannot save files, so copy the source instead) |

If what lands in Outlook looks like code, the wrong button was used. Go back and press Copy signature.

## The four signatures

All four share one layout: the division mark on the left, a 3 px accent bar, the person's details on the right, and a footer line.

| Tab | Mark | Accent | Division line | Footer | Default office | Default address |
|---|---|---|---|---|---|---|
| Fearless | Fearless wordmark | Steel blue | Fearless Manufacturing | A DIVISION OF + OGF wordmark | (432) 631-0050 | 204 S Lincoln Ave · Odessa, TX 79761 |
| Crossroads | Crossroads badge | Orange | Crossroads Diesel | A DIVISION OF + OGF wordmark | (432) 631-0050 | 8916 W County Rd 127 · Midland, TX 79706 |
| Both | Crossroads badge over the Fearless wordmark, centred, hairline between | Steel blue | Crossroads Diesel, then Fearless Manufacturing on the next line | DIVISIONS OF + OGF wordmark | (432) 631-0050 | none |
| OGF | OGF wordmark | Steel blue | OGF Manufacturing LLC | FEARLESS MANUFACTURING · CROSSROADS DIESEL (text) | (432) 631-0050 | 8916 W County Rd 127 · Midland, TX 79706 |

The OGF and Fearless marks in the signature are the wordmark-only versions (no MANUFACTURING line). The footer OGF wordmark is deliberately small, about one and three-quarter times the height of the caps beside it, so it reads as a logotype at the end of the phrase.

## What is in this folder

This folder is the live site. It is a git checkout of the repository above; pushing to `main` updates the site within a minute.

| File | What it is |
|---|---|
| `signature-generator.html` | The builder. `index.html` is an identical copy so the site root opens it. Self-contained: works offline from a double-click, logos embedded. |
| `templates/fearless.html`, `crossroads.html`, `fearless-crossroads.html`, `ogf.html` | The same four signatures as plain HTML with `{{PLACEHOLDERS}}`, for hand editing or a server-side rollout. Office number and address are pre-filled per division. |
| `img/` | The logo PNGs every sent email links to, at 2x for high-DPI screens. Plain files are transparent; `-tile` files put the logo on a white panel (see Dark mode). `index.html` there is the listing page the folder address shows. |
| `build/build_signature.py` | Single source of truth. `PIECES` is the signature HTML, `DIVISIONS` holds each tab's mark, colours, footer and defaults. Run it to regenerate the templates and the builder. |
| `build/generator.template.html` | The builder page before the build script embeds the images and configuration. |

The vector masters are on the shared drive beside each logo, not in this repository: `ogf/logo/`, `Fearless/logo/`, `Crossroads/logo/`. Each has `logo.svg` and `logo-white.svg` (for dark backgrounds). OGF and Fearless also have `options/logo-wordmark.svg` and `logo-wordmark-white.svg` without the MANUFACTURING line; these are what the signature uses. Crossroads also has one-colour `logo-mono.svg` and `logo-mono-white.svg`; in the white one the DIESEL letters and the small triangle are cut out so the background shows through. Mail clients do not render SVG, which is why the signature uses PNGs.

## Logo images and hosting

A signature cannot carry files. The logo has to come from a web address or be embedded in the HTML.

**Hosted (default; Outlook and Gmail need it).** The PNGs in `img/` are served by GitHub Pages at `https://rsty-shackleford.github.io/ogf-signature/img/`, and the builder uses that address by default. Recipients' mail clients fetch the logo when they open the message. **Never rename, move or delete the files in `img/`, and never take the site down:** every email already sent points at them. The "Image folder" field in the builder exists for one reason, the day the logos move to a company domain; nobody else should touch it.

**Embedded (Thunderbird, Apple Mail).** The builder bakes the PNGs into the HTML as data URIs. Nothing to host; Thunderbird turns them into inline attachments on send. Gmail refuses embedded images and some Outlook versions turn them into attachments, so use Hosted for those.

The builder's preview always uses embedded copies, so it shows the logos even if the hosted files are unreachable for a moment.

**Why GitHub Pages.** Teams, SharePoint and OneDrive links need a sign-in or land on a viewer page, so a recipient outside the company sees a broken image. Drive, Dropbox and image hosts throttle or block hotlinking. A static host with direct file URLs is what signature images need, and GitHub Pages is free and reliable. The repository is public, which is fine: everything in it is already in every email sent. When the company buys its domain, add it as a custom domain in the repository's Pages settings; GitHub then redirects the old address, so older emails keep working.

## Dark mode

A signature cannot adapt to the reader's theme. Dark-mode mail clients lighten the text and leave images exactly as sent, and a pasted signature cannot carry the style rules that would swap in white logos. Two choices, under **Logo background** in the builder:

- **Transparent** (default): clean on a white message. In a dark-mode client the black OGF and Fearless wordmarks lose contrast; the Crossroads badge mostly survives.
- **White panel**: each logo on a small white panel, readable in dark mode at the cost of a visible box there.

Most people read mail on white, so Transparent is the default. The **Dark mail client** toggle in the preview simulates a dark-mode reader (text lightened, images untouched) so the two can be compared.

## Can Outlook take a URL?

No. No version of Outlook loads a signature from a web address. The route is: render the signature in a browser, copy it, paste it into Outlook's signature editor. **Copy signature** does the copying with the table, colours and logo intact. Thunderbird is the exception: it can read the signature from a file.

## Rolling it out to everyone

1. **Send the link.** Post the builder link in Teams with the quick start above. Each person does it once.
2. **Pre-fill it for them.** Open the builder from the file on disk, fill in a person's details, Download .html, and email them the file with the install steps.
3. **Server-side (Microsoft 365).** An admin creates an Exchange mail-flow rule ("Apply disclaimers") per division that appends the signature to every outgoing message. Paste the division template from `templates/` and replace the placeholders with Exchange attributes: `{{NAME}}` → `%%DisplayName%%`, `{{TITLE}}` → `%%Title%%`, `{{MOBILE}}` → `%%MobilePhone%%`, `{{OFFICE}}` → `%%PhoneNumber%%`, `{{EMAIL}}` → `%%Email%%`. This also covers phones, where Outlook only allows plain-text signatures. A disclaimer rule adds the signature at the very bottom of the message, under quoted replies; products such as Exclaimer or CodeTwo place it under the newest reply instead.

## The palette, and why it ties together

| Role | Hex | Used for |
|---|---|---|
| Ink | `#0B0C0E` | Names, the OGF and Fearless wordmarks |
| Steel | `#1F7FC4` | OGF, Fearless and Both accent bar |
| Steel, small type | `#17629B` | Titles and links on white (OGF, Fearless, Both) |
| Navy | `#0B3453` | Crossroads titles and links |
| Orange | `#FF8D2A` | Crossroads accent bar; the StrataFlow orange |
| Light blue | `#92BFD4` | Crossroads badge only |
| Mid grey | `#62666C` | Division line, address |
| Rule | `#D5D7DA` | Hairlines |

OGF and Fearless are black wordmarks, so black carries the name and the fine print. The steel blue comes from the Fearless brochures, where it was chosen to sit beside the Crossroads navy. Orange is reserved for Crossroads and matches StrataFlow. Type is Arial throughout, because a signature can only use fonts the recipient has.

## Decisions made (6 October 2026)

- **Logos vectorised.** OGF and Fearless were traced from the high-resolution originals. The Crossroads badge existed only as a 221 px PNG, so it was rebuilt: gear, bowl, shoulders, road bands, triangles and star reconstructed as geometry; CROSSROADS and DIESEL letterforms traced; MOBILE REPAIR re-set in Barlow Condensed because the original was unreadable at that size. Its orange was changed to the StrataFlow orange, `#FF8D2A`.
- **Wordmark-only marks** for OGF and Fearless in the signature, cut from the traced vectors with the tagline removed.
- **Layout rules.** No two logos side by side; the Both tab stacks Crossroads above Fearless, centred, with a hairline. The footer OGF mark is small and follows "A DIVISION OF". "Mobile Repair" is dropped from all text; the company is written as Crossroads Diesel.
- **Images are transparent** by default; the white-panel set is kept as an option for dark-mode readers.
- **Hosting.** Public GitHub repository with GitHub Pages, chosen over Teams/SharePoint (sign-in walls) and consumer hosts (hotlink limits). The image file names and address are permanent from the first email sent. Custom domain to be added when the company has one.
- **Still open.** Company website and email domain are unknown, so the Website field is blank by default.

## Editing the design

The signature HTML is written for mail clients: one table, every style inline, no CSS classes, width and height on every image, `margin:0 auto` plus `align="center"` for centred images, and `mso-line-height-rule` so Outlook honours line heights. Keep to those rules.

To change anything for all four tabs at once, edit `PIECES` or `DIVISIONS` in `build/build_signature.py`, then:

```
python3 build/build_signature.py
git add -A && git commit -m "describe the change" && git push
```

That rewrites `templates/*.html`, `signature-generator.html`, `index.html` and `img/index.html`, and the push updates the site.
