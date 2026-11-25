# GTA Landlord Solutions

One-page site for GTA property managers and building owners.

**Live:** https://ssbrain.github.io/gta-landlord-solutions/

## Intake form

The “Tell us about your unit” form is on the site at `#intake` and posts to FormSubmit (`besthome8658@outlook.com`). After submit, visitors go to `thanks.html`.

All “Tell us about your unit” buttons use the value in `config.js`:

```js
window.FORM_LINK = "#intake";
```

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
