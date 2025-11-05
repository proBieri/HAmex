# HAmex Branding und Icons

## HACS Icon Anforderungen

HACS benötigt folgende Bildformate für optimale Darstellung:

### 1. Icon (Quadratisch)
- **Dateiname**: `icon.png` oder `icon@2x.png`
- **Größe**: 256x256px (oder 512x512px für @2x)
- **Format**: PNG mit transparentem Hintergrund
- **Verwendung**: Wird in der HACS Integration Liste angezeigt

### 2. Logo (Optional, Rechteckig)
- **Dateiname**: `logo.png` oder `logo@2x.png`
- **Größe**: Variabel, empfohlen 420x200px
- **Format**: PNG mit transparentem Hintergrund
- **Verwendung**: Wird auf der Integration Detail-Seite angezeigt

### 3. Logo Dark Mode (Optional)
- **Dateiname**: `logo_dark.png`
- **Verwendung**: Alternative für Dark Mode

## Speicherort

Zwei Möglichkeiten:

### Option A: Im Repository (empfohlen)
```
custom_components/hamex/
├── assets/
│   ├── icon.png
│   ├── icon@2x.png
│   ├── logo.png
│   └── logo@2x.png
```

In `manifest.json` hinzufügen:
```json
{
  "version": "1.0.0"
}
```

### Option B: Externe URL
In `hacs.json` hinzufügen:
```json
{
  "name": "HAmex",
  "render_readme": true
}
```

## Design-Empfehlungen für HAmex

### Icon-Konzept
- **Ölfass/Tank Symbol** in Orange/Gelb (Heizöl-Farbe)
- **Füllstandsanzeige** (z.B. Balken oder Wellenlinie)
- **MEX-Bezug** durch moderne, technische Gestaltung
- **Minimalistisch** für gute Erkennbarkeit in kleiner Größe

### Farbschema
- **Primär**: `#FF9800` (Orange - Heizöl)
- **Sekundär**: `#FFC107` (Amber)
- **Akzent**: `#2196F3` (Blau - Technologie)
- **Dark**: `#424242`

## Tools zum Erstellen

### Online (kostenlos)
- **Figma**: https://www.figma.com
- **Canva**: https://www.canva.com
- **Pixlr**: https://pixlr.com

### KI-generiert
- **DALL-E**: https://openai.com/dall-e
- **Midjourney**: https://www.midjourney.com
- **Stable Diffusion**: Lokal oder via Websites

### Icon-Bibliotheken
- **Material Design Icons**: https://materialdesignicons.com
- **Font Awesome**: https://fontawesome.com
- **Flaticon**: https://www.flaticon.com

## Beispiel Prompt für KI-Generierung

```
Create a minimalist app icon for a home automation integration.
Theme: Oil tank monitoring system.
Elements: Oil barrel or tank with a fill level indicator.
Colors: Orange (#FF9800) and blue (#2196F3).
Style: Flat design, modern, clean, simple.
Background: Transparent or solid color.
Size: 512x512 pixels, high resolution.
```

## Temporäre Lösung: Text-basiertes Icon

Wenn noch kein Icon verfügbar ist, kannst du ein einfaches Text-Icon verwenden.
Siehe `icon_template.html` für eine SVG-Vorlage.
