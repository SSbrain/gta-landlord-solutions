# GTA Landlord Solutions

One-page site for GTA property managers and building owners.

**Live:** https://ssbrain.github.io/gta-landlord-solutions/

## Form link

The Microsoft Form is not attached yet. The placeholder lives in one place, `config.js`:

```js
window.FORM_LINK = "FORM_LINK_PLACEHOLDER";
```

When the form is ready, swap it with one command:

```bash
sed -i 's|FORM_LINK_PLACEHOLDER|https://forms.cloud.microsoft/YOUR_FORM|' config.js
```

Until then, “Tell us about your unit” scrolls to the contact section (phone and email).

## Flyer

`flyer/gta-landlord-solutions-flyer.png` (1080×1350) and `flyer/gta-landlord-solutions-flyer.pdf` (letter). Rebuild with:

```bash
python3 flyer/render_flyer.py
```

The QR code points at this website, so the form is reached through the site button.

## Contact

- Phone: 647-891-8658
- Email: besthome8658@outlook.com

Real One Realty Inc., Brokerage
