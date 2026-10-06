# OGF family email signatures

One layout for everyone at OGF Manufacturing, Fearless Manufacturing and Crossroads Diesel Mobile Repair. Each person picks their division, fills in the blanks, and pastes the result into their mail client.

## What is in this folder

| File | What it is |
|---|---|
| `signature-generator.html` | The fill-in-the-blank tool. Open it in any browser (double-click it). Works offline. Also published at the link in the note below. |
| `templates/fearless.html`, `crossroads.html`, `fearless-crossroads.html`, `ogf.html` | The same signature as plain HTML with `{{PLACEHOLDERS}}`, for anyone who would rather edit by hand or for a server-side rollout. `fearless-crossroads.html` is the combined version for people who represent both divisions. |
| `img/` | The logo PNGs the signature uses, at 2x for sharp rendering on high-DPI screens. The plain files are transparent; the `-tile` files put each logo on a white panel for people whose recipients read in dark mode (see below). |
| `build/` | `build_signature.py` is the single source of truth for the signature HTML. Edit it and run it to regenerate the templates and the generator. |

The vector masters live with each logo: `ogf/logo/logo.svg`, `Fearless/logo/logo.svg`, `Crossroads/logo/logo.svg`, each with a `logo-white.svg` for dark backgrounds. OGF and Fearless also have wordmark-only versions (no MANUFACTURING line) in their `options/` folders, and Crossroads has one-colour `logo-mono.svg` and `logo-mono-white.svg` versions. Mail clients do not render SVG, which is why the signature uses the PNGs in `img/`.

## Quick start

1. Open `signature-generator.html`.
2. Pick the division, or **Both** if you represent Fearless and Crossroads together. Both puts the two marks in one column, Fearless above Crossroads with a hairline between, uses the OGF steel-blue accent, and the footer reads "Divisions of" followed by the OGF logo. Type your name, title, phones and email.
3. Choose where the logo images come from (see below), then **Copy signature**.
4. Follow the **Install it** tab for your mail client. The tool has step-by-step instructions for classic Outlook, new Outlook and Outlook on the web, Outlook for Mac, Thunderbird and Gmail.

## About the logo images

An email signature cannot carry files the way a document does. The logo has to come from somewhere, and there are two choices:

**Hosted (recommended for Outlook and Gmail).** Upload the four PNGs from `img/` to a folder on the company website, for example `https://www.company.com/signature/`, and type that folder URL into the tool. The signature then links to `.../signature/fearless-logo.png` and so on. Recipients' mail clients download the logo when they open the message. This is how nearly every corporate signature works. Keep the file names unchanged.

**Embedded (Thunderbird, Apple Mail).** The tool bakes the PNGs into the HTML itself as data URIs. Nothing to host, and Thunderbird turns them into inline attachments on send. Gmail refuses embedded images, and some Outlook versions turn them into attachments, so use Hosted for those.

Until the images are hosted, the preview in the tool still shows the logo (the preview always uses the embedded copies).

## Dark mode

A signature cannot adapt to the reader's theme. Mail clients in dark mode lighten the text and leave images exactly as they are, and a pasted signature cannot carry the style rules that would swap in the white logos. So the images you send are the images everyone sees, on white or on dark. Two choices, both in the tool under **Logo background**:

- **Transparent** (default): clean on a white message; in a dark-mode client the black OGF and Fearless wordmarks lose contrast and the Crossroads badge mostly survives.
- **White panel**: each logo sits on a small white panel, so it stays readable in dark mode at the cost of a visible box there.

Most people read mail on white, so Transparent is the sensible default. The **Dark mail client** toggle in the preview simulates what a dark-mode reader sees, so you can compare the two before deciding.

## "Can Outlook just take a URL?"

No. Outlook has no "signature from URL" option in any version. The reliable route is: render the signature in a browser, select and copy it, paste it into Outlook's signature editor. The **Copy signature** button does the select-and-copy step for you with the table, colours and logo intact.

Thunderbird is the exception: it can read the signature from a file (**Account Settings → Attach the signature from a file instead**). Use **Download .html** with Embedded images for that.

## Rolling it out to everyone

Three options, in increasing order of effort:

1. **Send the folder.** Put this folder on the shared drive and send the quick-start steps above. Each person does it once.
2. **Pre-fill it for them.** Open the tool, fill in a person's details, click **Download .html** and email them the file with the install steps. They paste it in.
3. **Server-side (Microsoft 365).** An admin creates an Exchange mail-flow rule ("Apply disclaimers") per division that appends the signature to every outgoing message. Paste the division template from `templates/` into the rule and replace the placeholders with Exchange attributes: `{{NAME}}` → `%%DisplayName%%`, `{{TITLE}}` → `%%Title%%`, `{{MOBILE}}` → `%%MobilePhone%%`, `{{OFFICE}}` → `%%PhoneNumber%%`, `{{EMAIL}}` → `%%Email%%`. Images must be hosted. This covers phones as well, where Outlook only allows plain-text signatures. Note that a disclaimer rule adds the signature at the very bottom of the message, under quoted replies. Products such as Exclaimer or CodeTwo place it under the newest reply instead.

## The palette, and why it ties together

| Role | Hex | Used for |
|---|---|---|
| Ink | `#0B0C0E` | Names, the OGF and Fearless wordmarks |
| Steel | `#1F7FC4` | OGF and Fearless accent bar |
| Steel, small type | `#17629B` | OGF and Fearless titles and links on white |
| Navy | `#0B3453` | Crossroads titles and links |
| Orange | `#FF8D2A` | Crossroads accent bar, the same orange as the StrataFlow logo |
| Light blue | `#92BFD4` | Crossroads badge only |
| Mid grey | `#62666C` | Division line, address |
| Rule | `#D5D7DA` | Hairlines |

OGF and Fearless are black wordmarks, so black carries the name and the fine print. The steel blue is the one from the Fearless brochures, which was chosen to sit beside the Crossroads navy. Orange is reserved for Crossroads. Every signature shares the same type (Arial, because signatures can only use fonts installed on the recipient's machine), spacing and grey. Division signatures end with "A division of" in letter-spaced caps followed by the OGF logo, in the manner of the brochure page footers; the OGF signature lists its divisions there instead.

## Editing the design

The signature HTML is written for mail clients: a table, every style inline, no CSS classes, width and height on every image, and `mso-line-height-rule` so Outlook honours the line heights. Keep to those rules if you edit it.

To change the layout for all three divisions at once, edit `PIECES` in `build/build_signature.py` and run:

```
python3 build/build_signature.py
```

That rewrites `templates/*.html` and `signature-generator.html`. Change a division's colours, logo size, footer line or default address in `DIVISIONS` in the same file.
