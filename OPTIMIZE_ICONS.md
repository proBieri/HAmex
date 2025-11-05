# Icons für Home Assistant Brands optimieren

## Problem
Deine aktuellen Icons sind **zu groß** für das Home Assistant Brands Repository:

- `icon.png`: **60KB** (max 10KB erlaubt)
- `icon@2x.png`: **165KB** (max 20KB erlaubt)

## Lösung: Online Kompression mit TinyPNG

### Schritt-für-Schritt Anleitung

1. **Öffne TinyPNG**
   - Gehe zu: https://tinypng.com/

2. **Upload icon.png**
   - Drag & Drop dein `icon.png` (256x256px)
   - Warte auf Kompression
   - Download die komprimierte Version
   - Sollte nun ~5-8KB sein

3. **Upload icon@2x.png**
   - Drag & Drop dein `icon@2x.png` (512x512px)
   - Warte auf Kompression
   - Download die komprimierte Version
   - Sollte nun ~12-18KB sein

4. **Ersetze die Dateien**
   ```bash
   # Im HAmex Projektordner
   mv ~/Downloads/icon.png icon.png
   mv ~/Downloads/icon@2x.png icon@2x.png
   ```

5. **Überprüfe die Größe**
   ```bash
   ls -lh icon*.png
   # icon.png sollte < 10KB sein
   # icon@2x.png sollte < 20KB sein
   ```

## Alternative: ImageOptim (macOS)

Wenn du macOS verwendest:

1. Download: https://imageoptim.com/
2. Installiere ImageOptim
3. Drag & Drop beide Icons in ImageOptim
4. Automatische Optimierung (kann 80% Reduktion erreichen!)

## Alternative: Online PNG Compressor

Andere gute Tools:

- **Squoosh**: https://squoosh.app/
  - Sehr gute Kontrolle über Qualität
  - WebP Support

- **CompressPNG**: https://compresspng.com/
  - Schnell und einfach

- **PNGGauntlet** (Windows): https://pnggauntlet.com/

## Prüfen der Dateigrößen

Nach der Optimierung:

```bash
cd /Users/Shared/Previously\ Relocated\ Items/Security/Data/Source/HAmex
ls -lh icon.png icon@2x.png
```

**Ziel:**
- ✅ icon.png: < 10KB (10240 bytes)
- ✅ icon@2x.png: < 20KB (20480 bytes)

## Nach der Optimierung

1. Committe die optimierten Icons:
   ```bash
   git add icon.png icon@2x.png
   git commit -m "Optimize icons for Brands repository requirements"
   git push
   ```

2. Erstelle dann den Pull Request zum Brands Repository (siehe BRANDS_PR_GUIDE.md)

## Warum ist das wichtig?

- Home Assistant Brands Repo hat **strikte Größenlimits**
- Große Icons verlangsamen Home Assistant UI
- PRs mit zu großen Icons werden **abgelehnt**
- Nach Optimierung: Gleiche Qualität, 80-90% kleinere Dateien!
