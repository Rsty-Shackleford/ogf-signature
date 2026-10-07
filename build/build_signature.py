#!/usr/bin/env python3
"""Builds the OGF family email-signature kit.

Single source of truth for the signature HTML. Writes:
  ../templates/<division>.html   fill-in-the-blank templates ({{NAME}} etc.)
  ../signature-generator.html    self-contained generator page (logos embedded)
Run from anywhere:  python3 build_signature.py
"""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "img")
TPL = os.path.join(ROOT, "templates")

# ---------------------------------------------------------------- palette
INK, MID, SOFT, RULE = "#0b0c0e", "#62666c", "#8b8e93", "#d5d7da"
STEEL, STEEL_TEXT = "#1f7fc4", "#17629b"          # marks / small type on white
NAVY, ORANGE, LBLUE = "#0b3453", "#ff8d2a", "#92bfd4"      # orange = StrataFlow orange

DIVISIONS = {
    "fearless": dict(
        name="Fearless Manufacturing",
        logos=[("fearless-logo.png", 190, 33, "Fearless Manufacturing")],
        accent=STEEL, type=STEEL_TEXT,
        footer="A division of", footer_logo=True,
        office="(432) 631-0050", address="204 S Lincoln Ave · Odessa, TX 79761",
    ),
    "crossroads": dict(
        name="Crossroads Diesel",
        logos=[("crossroads-logo.png", 100, 102, "Crossroads Diesel")],
        accent=ORANGE, type=NAVY,
        footer="A division of", footer_logo=True,
        office="(432) 631-0050", address="8916 W County Rd 127 · Midland, TX 79706",
    ),
    # for people who represent both divisions at once: one column, Crossroads over Fearless, centred, OGF accent, "Divisions of" footer
    "both": dict(
        name=["Crossroads Diesel", "Fearless Manufacturing"],      # one line each
        logos=[("crossroads-logo.png", 84, 85, "Crossroads Diesel"),
               ("fearless-logo.png", 150, 26, "Fearless Manufacturing")],
        accent=STEEL, type=STEEL_TEXT,
        footer="Divisions of", footer_logo=True,
        office="(432) 631-0050", address="",
    ),
    "ogf": dict(
        name="OGF Manufacturing LLC",
        logos=[("ogf-logo.png", 170, 41, "OGF Manufacturing")],
        accent=STEEL, type=STEEL_TEXT,
        footer="Fearless Manufacturing · Crossroads Diesel", footer_logo=False,
        office="(432) 631-0050", address="8916 W County Rd 127 · Midland, TX 79706",
    ),
}

FONT = "font-family:Arial,Helvetica,sans-serif;"
LINE = "mso-line-height-rule:exactly;"

# Signature pieces. Every colour and font is inline because Outlook and Gmail
# strip <style> blocks. {{KEY}} placeholders are filled by the generator (JS)
# or by hand in the templates.
PIECES = {
    "outer": (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'style="border-collapse:collapse;' + FONT + '">'
        '<tr>'
        '<td valign="middle" style="padding:0 18px 0 0;vertical-align:middle;">{{LOGO}}</td>'
        '<td valign="middle" style="padding:2px 0 2px 16px;border-left:3px solid {{ACCENT}};vertical-align:middle;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
        '{{ROWS}}'
        '</table>'
        '</td>'
        '</tr>'
        '{{FOOTER}}'
        '</table>'
    ),
    "logo": (
        '<img src="{{IMG_LOGO}}" width="{{LOGO_W}}" height="{{LOGO_H}}" alt="{{DIVISION}}" '
        'style="display:block;margin:0 auto;border:0;outline:none;text-decoration:none;width:{{LOGO_W}}px;height:{{LOGO_H}}px;">'
    ),
    "logo_link": '<a href="{{WEBSITE_URL}}" style="text-decoration:none;border:0;">{{LOGO_IMG}}</a>',
    # two marks in one column, centred, a hairline between them
    "logo_stack": (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
        '{{LOGO_ROWS}}</table>'
    ),
    "logo_stack_row": '<tr><td align="center" valign="middle" style="padding:{{PAD}};text-align:center;vertical-align:middle;{{BORDER}}">{{LOGO_IMG}}</td></tr>',
    "row_name": (
        '<tr><td style="' + FONT + LINE + 'font-size:15px;line-height:19px;font-weight:bold;'
        'letter-spacing:1px;text-transform:uppercase;color:' + INK + ';padding:0;">{{NAME}}</td></tr>'
    ),
    "row_title": (
        '<tr><td style="' + FONT + LINE + 'font-size:12px;line-height:17px;font-weight:bold;'
        'color:{{TYPE}};padding:1px 0 0 0;">{{TITLE}}</td></tr>'
    ),
    "row_division": (
        '<tr><td style="' + FONT + LINE + 'font-size:12px;line-height:17px;'
        'color:' + MID + ';padding:0;">{{DIVISION}}</td></tr>'
    ),
    "row_phones": (
        '<tr><td style="' + FONT + LINE + 'font-size:12px;line-height:17px;'
        'color:' + INK + ';padding:7px 0 0 0;">{{PHONES}}</td></tr>'
    ),
    "phone_mobile": (
        '<span style="color:{{TYPE}};font-weight:bold;">M</span>&nbsp;'
        '<a href="tel:{{MOBILE_TEL}}" style="color:' + INK + ';text-decoration:none;">{{MOBILE}}</a>'
    ),
    "phone_office": (
        '<span style="color:{{TYPE}};font-weight:bold;">O</span>&nbsp;'
        '<a href="tel:{{OFFICE_TEL}}" style="color:' + INK + ';text-decoration:none;">{{OFFICE}}</a>'
    ),
    "phone_sep": '&nbsp;&nbsp;&nbsp;',
    "row_links": (
        '<tr><td style="' + FONT + LINE + 'font-size:12px;line-height:17px;'
        'color:' + INK + ';padding:0;">{{LINKS}}</td></tr>'
    ),
    "link_email": '<a href="mailto:{{EMAIL}}" style="color:{{TYPE}};text-decoration:none;">{{EMAIL}}</a>',
    "link_web": '<a href="{{WEBSITE_URL}}" style="color:{{TYPE}};text-decoration:none;">{{WEBSITE}}</a>',
    "link_sep": '<span style="color:' + SOFT + ';">&nbsp;&nbsp;·&nbsp;&nbsp;</span>',
    "row_address": (
        '<tr><td style="' + FONT + LINE + 'font-size:12px;line-height:17px;'
        'color:' + MID + ';padding:0;">{{ADDRESS}}</td></tr>'
    ),
    # Footer: "A division of" in letter-spaced caps, then the full OGF logo (with MANUFACTURING).
    "footer_logo": (
        '<tr><td colspan="2" style="padding:12px 0 0 0;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"><tr>'
        '<td valign="middle" style="' + FONT + LINE + 'font-size:9px;line-height:12px;letter-spacing:2px;'
        'text-transform:uppercase;color:' + SOFT + ';padding:0 8px 0 0;vertical-align:middle;white-space:nowrap;">{{FOOTER}}</td>'
        '<td valign="middle" style="padding:0;vertical-align:middle;">'
        '<img src="{{IMG_MARK}}" width="58" height="14" alt="OGF Manufacturing" '
        'style="display:block;border:0;width:58px;height:14px;"></td>'
        '</tr></table>'
        '</td></tr>'
    ),
    "footer_plain": (
        '<tr><td colspan="2" style="' + FONT + LINE + 'font-size:9px;line-height:12px;letter-spacing:2px;'
        'text-transform:uppercase;color:' + SOFT + ';padding:12px 0 0 0;">{{FOOTER}}</td></tr>'
    ),
}


def fill(s, **kw):
    for k, v in kw.items():
        s = s.replace("{{" + k + "}}", v)
    return s


def static_template(key):
    """Fill-in-the-blank version: every row present, person fields left as {{PLACEHOLDERS}}."""
    d = DIVISIONS[key]
    img_base = "../img/"
    imgs = []
    for fn, w, h, alt in d["logos"]:
        im = fill(PIECES["logo"], IMG_LOGO=img_base + fn, LOGO_W=str(w), LOGO_H=str(h), DIVISION=alt)
        imgs.append(fill(PIECES["logo_link"], LOGO_IMG=im))
    if len(imgs) == 1:
        logo = imgs[0]
    else:
        rows = "".join(fill(PIECES["logo_stack_row"], LOGO_IMG=im,
                            PAD=("0 0 10px 0" if i == 0 else "10px 0 0 0"),
                            BORDER=("" if i == 0 else "border-top:1px solid " + RULE + ";"))
                       for i, im in enumerate(imgs))
        logo = fill(PIECES["logo_stack"], LOGO_ROWS=rows)
    names = d["name"] if isinstance(d["name"], list) else [d["name"]]
    rows = (PIECES["row_name"] + PIECES["row_title"]
            + "".join(fill(PIECES["row_division"], DIVISION=n) for n in names)
            + fill(PIECES["row_phones"], PHONES=PIECES["phone_mobile"] + PIECES["phone_sep"] + PIECES["phone_office"])
            + fill(PIECES["row_links"], LINKS=PIECES["link_email"] + PIECES["link_sep"] + PIECES["link_web"])
            + (PIECES["row_address"] if d["address"] else ""))
    footer = PIECES["footer_logo"] if d["footer_logo"] else PIECES["footer_plain"]
    footer = fill(footer, IMG_MARK=img_base + "ogf-mark.png", FOOTER=d["footer"])
    sig = fill(PIECES["outer"], LOGO=logo, ROWS=rows, FOOTER=footer)
    sig = fill(sig, ACCENT=d["accent"], TYPE=d["type"], ADDRESS=d["address"],
               OFFICE=d["office"], OFFICE_TEL="+1" + re.sub(r"\D", "", d["office"]))
    # entities instead of raw UTF-8 so the fragment reads correctly in any editor or mail client
    sig = sig.replace("·", "&middot;")
    # pretty-ish: one tag per line for hand editing
    sig = re.sub(r"><", ">\n<", sig)
    return (
        "<!-- " + " / ".join(d["name"] if isinstance(d["name"], list) else [d["name"]]).replace("·", "&middot;") + " email signature template.\n"
        "     Replace every {{PLACEHOLDER}}. Delete a row you do not need (each <tr>...</tr> is one line of the signature).\n"
        "     Images: ../img/ paths work for Thunderbird's 'attach signature from file'. For Outlook and Gmail,\n"
        "     replace them with the hosted URLs (see README.md), or use signature-generator.html which does all of this for you. -->\n"
        + sig + "\n"
    )


def main():
    os.makedirs(TPL, exist_ok=True)
    for key in DIVISIONS:
        fn = {"both": "fearless-crossroads"}.get(key, key) + ".html"
        with open(os.path.join(TPL, fn), "w") as f:
            f.write(static_template(key))
        print("wrote templates/" + fn)

    images = {}
    for base in ["fearless-logo", "crossroads-logo", "ogf-logo", "ogf-mark"]:
        for fn in [base + ".png", base + "-tile.png"]:      # transparent, and on a white panel for dark-mode clients
            with open(os.path.join(IMG, fn), "rb") as f:
                images[fn] = "data:image/png;base64," + base64.b64encode(f.read()).decode()

    gen = open(os.path.join(HERE, "generator.template.html")).read()
    # hero band: the white vector marks, as data URIs so the page stays one file
    def svg_uri(path):
        with open(path, "rb") as f:
            return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()
    OGFROOT = os.path.dirname(ROOT)
    gen = gen.replace("/*__HERO_OGF__*/", svg_uri(os.path.join(OGFROOT, "ogf", "logo", "logo-white.svg")))
    gen = gen.replace("/*__HERO_FEARLESS__*/", svg_uri(os.path.join(OGFROOT, "Fearless", "logo", "logo-white.svg")))
    gen = gen.replace("/*__HERO_CROSSROADS__*/", svg_uri(os.path.join(OGFROOT, "Crossroads", "logo", "logo-mono-white.svg")))
    gen = gen.replace("/*__PIECES__*/", "const PIECES = " + json.dumps(PIECES) + ";")
    gen = gen.replace("/*__DIVISIONS__*/", "const DIVISIONS = " + json.dumps(DIVISIONS) + ";")
    gen = gen.replace("/*__IMAGES__*/", "const IMAGES = " + json.dumps(images) + ";")
    with open(os.path.join(ROOT, "signature-generator.html"), "w") as f:
        f.write(gen)
    with open(os.path.join(ROOT, "index.html"), "w") as f:   # same page at the site root
        f.write(gen)
    # img/index.html: the image folder address shows what is there (static hosts do not list folders)
    pngs = sorted(fn for fn in os.listdir(IMG) if fn.endswith(".png"))
    rows = "".join('<li><a href="%s"><img src="%s" alt=""><code>%s</code></a></li>' % (fn, fn, fn) for fn in pngs)
    with open(os.path.join(IMG, "index.html"), "w") as f:
        f.write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>Signature images</title><style>body{font-family:Arial,sans-serif;margin:32px;color:#0b0c0e;background:#f0f1f2}'
                'h1{font-size:20px;margin:0 0 6px}p{margin:0 0 20px;color:#62666c;max-width:60ch}ul{list-style:none;padding:0;margin:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}'
                'li a{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid #d5d7da;padding:12px 14px;text-decoration:none;color:#0b0c0e}'
                'li img{height:40px;width:auto;max-width:120px;background:repeating-conic-gradient(#e5e7ea 0 25%,#fff 0 50%) 0 0/16px 16px}code{font-size:12px}</style></head><body>'
                '<h1>OGF signature images</h1><p>These files are linked from every OGF, Fearless and Crossroads email signature. Do not rename, move or delete them. The <code>-tile</code> files are the same logos on a white panel.</p>'
                '<ul>' + rows + '</ul></body></html>')
    print("wrote signature-generator.html (%d KB)" % (len(gen) // 1024))
    # optional: a copy without the document skeleton, for hosting in a viewer that supplies its own
    out = os.environ.get("ARTIFACT_OUT")
    if out:
        art = re.sub(r"<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*", "", gen)
        art = re.sub(r'<meta (charset="utf-8"|name="viewport"[^>]*)>\n', "", art)
        art = art.replace("</head>\n<body>", "").replace("</body>\n</html>", "")
        with open(out, "w") as f:
            f.write(art)
        print("wrote", out)


if __name__ == "__main__":
    main()
