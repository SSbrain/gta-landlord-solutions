# GTA Landlord Solutions

One-page site for GTA property managers and building owners.

The “Tell us about your unit” form is on the site at `#intake` and posts through FormSubmit. After submit, visitors go to `thanks.html`. Buttons use `config.js`:

```js
window.FORM_LINK = "#intake";
```

## Flyer

`flyer/gta-landlord-solutions-flyer.png` (1080×1350) and `flyer/gta-landlord-solutions-flyer.pdf` (letter). Rebuild with:

```bash
python3 flyer/render_flyer.py
```

Real One Realty Inc., Brokerage
