# Icon für HAmex zum Home Assistant Brands Repository hinzufügen

## Problem
HACS zeigt keine Icons für Custom Integrations an, die nur in deinem Repository liegen.
Icons müssen zum **Home Assistant Brands Repository** hinzugefügt werden.

## Lösung: Pull Request erstellen

### Schritt 1: Brands Repository forken

1. Gehe zu: https://github.com/home-assistant/brands
2. Klicke auf **Fork** (oben rechts)
3. Erstelle einen Fork in deinem Account

### Schritt 2: Verzeichnisstruktur erstellen

Im Fork erstelle folgende Struktur:

```
brands/
└── custom_integrations/
    └── hamex/               ← Dein Domain-Name aus manifest.json
        ├── icon.png         ← 256x256px (wir haben das bereits!)
        ├── icon@2x.png      ← 512x512px (optional, wir haben das!)
        └── logo.png         ← 256x128px (optional)
```

### Schritt 3: Icon-Dateien hochladen

**Option A: Via GitHub Web Interface (einfach)**

1. Gehe zu deinem Fork
2. Navigate zu `custom_integrations/`
3. Klicke auf **Add file** → **Create new file**
4. Dateiname: `hamex/icon.png`
5. Drag & Drop dein `icon.png` aus dem HAmex Projekt
6. Wiederhole für `icon@2x.png`
7. Commit mit Nachricht: "Add hamex integration icons"

**Option B: Via Git (fortgeschritten)**

```bash
# Fork klonen
git clone https://github.com/DEIN_USERNAME/brands.git
cd brands

# Verzeichnis erstellen
mkdir -p custom_integrations/hamex

# Icons kopieren (aus HAmex Projekt)
cp /pfad/zu/HAmex/icon.png custom_integrations/hamex/
cp /pfad/zu/HAmex/icon@2x.png custom_integrations/hamex/

# Commit
git add custom_integrations/hamex/
git commit -m "Add hamex integration icons"
git push
```

### Schritt 4: Pull Request erstellen

1. Gehe zu deinem Fork auf GitHub
2. Klicke auf **Contribute** → **Open pull request**
3. Titel: `Add hamex integration icons`
4. Beschreibung:
   ```
   Add icons for the hamex custom integration.

   Integration: https://github.com/proBieri/HAmex
   Domain: hamex

   - icon.png (256x256px)
   - icon@2x.png (512x512px)
   ```
5. Klicke **Create pull request**

### Schritt 5: Warten auf Approval

- Das Home Assistant Team prüft deinen PR
- Kann 1-7 Tage dauern
- Nach Merge sind Icons in HACS sichtbar!

## Anforderungen (wichtig!)

### Dateigrößen-Limits
- **icon.png**: max 10KB (dein aktuelles ist 60KB - zu groß!)
- **icon@2x.png**: max 20KB (dein aktuelles ist 165KB - zu groß!)

### Icons optimieren

**Online Tool (empfohlen):**
https://tinypng.com/
- Lade dein icon.png hoch
- Komprimiert auf ~5-8KB
- Download und verwende die komprimierte Version

**Oder mit sips (macOS):**
```bash
cd /pfad/zu/HAmex
sips -s format png -s formatOptions 70 icon.png --out icon_optimized.png
```

## Wichtige Links

- **Brands Repository**: https://github.com/home-assistant/brands
- **Anleitung**: https://developers.home-assistant.io/blog/2020/05/08/logos-custom-integrations/
- **Beispiel PR**: Suche nach "custom_integrations" im Brands Repo

## Nach dem PR

Sobald der PR gemerged ist:
- Icons erscheinen automatisch in HACS
- Icons erscheinen in Home Assistant UI
- Keine Änderungen in deinem HAmex Repository nötig

## Temporäre Lösung (bis PR gemerged ist)

Icons in deinem Repository (wie aktuell) zeigen sich **nicht** in HACS, aber:
- Du kannst sie in der README anzeigen
- Nutzer sehen sie im GitHub Repository
- Nach Installation erscheint die Integration ohne Icon (normal für Custom Integrations)
