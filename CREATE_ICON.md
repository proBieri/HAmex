# Icon für HAmex erstellen

## ⚠️ Wichtig: HACS benötigt PNG-Dateien

HACS unterstützt **nur PNG-Dateien**, keine SVG!

## Schnelle Lösung: Online PNG erstellen

### Option 1: Icon Generator verwenden

1. Besuche: https://www.favicon-generator.org/
2. Lade ein Bild hoch oder erstelle eines
3. Generiere verschiedene Größen
4. Lade `icon-256x256.png` herunter
5. Benenne um zu `icon.png`
6. Kopiere nach `custom_components/hamex/assets/icon.png`

### Option 2: Canva (kostenlos, kein Account nötig)

1. Gehe zu: https://www.canva.com/create/icons/
2. Wähle "256 x 256 px" Template
3. Gestalte dein Icon:
   - Orange Hintergrund (`#FF9800`)
   - Tank/Ölfass Symbol
   - "MEX" Text
4. Download als PNG
5. Speichere als `icon.png` in `custom_components/hamex/assets/`

### Option 3: Material Design Icon umwandeln

1. Besuche: https://materialdesignicons.com/
2. Suche nach "oil", "tank", "gauge" oder "propane-tank"
3. Download als PNG (256x256)
4. Färbe mit Online-Tool ein: https://onlinepngtools.com/change-png-color
5. Speichere als `icon.png`

### Option 4: KI-Generator (empfohlen für professionelle Ergebnisse)

**DALL-E Prompt:**
```
App icon for oil tank monitoring.
Minimalist design showing an oil barrel with a fill level gauge.
Orange and blue color scheme.
Flat design, modern, clean.
256x256 pixels, PNG format.
```

**Alternative Tools:**
- https://www.bing.com/create (Microsoft Designer, kostenlos)
- https://designer.microsoft.com/image-creator (DALL-E 3)

## Dateien die du brauchst

```
custom_components/hamex/assets/
├── icon.png          (256x256px) - PFLICHT für HACS
├── icon@2x.png       (512x512px) - Optional, bessere Qualität
├── logo.png          (420x200px) - Optional, für Detail-Seite
└── logo@2x.png       (840x400px) - Optional, Retina Display
```

## Nach dem Erstellen

1. Platziere `icon.png` in `custom_components/hamex/assets/`
2. Committe die Datei:
   ```bash
   git add custom_components/hamex/assets/icon.png
   git commit -m "Add HACS icon"
   git push
   ```

3. HACS wird das Icon automatisch erkennen!

## Design-Tipps

### Gutes Icon erkennt man an:
- ✅ Erkennbar in 24x24px (klein)
- ✅ Klare Formen, nicht zu detailliert
- ✅ Guter Kontrast
- ✅ Einzigartiges Design
- ✅ Bezug zum Thema (Öl, Tank, Sensor)

### Zu vermeiden:
- ❌ Zu viele Details
- ❌ Dünne Linien
- ❌ Kleiner Text
- ❌ Komplexe Farbverläufe
- ❌ Fotorealismus

## Farbschema für HAmex

```
Primär:   #FF9800  (Orange - Heizöl)
Sekundär: #FFC107  (Gelb - Warm)
Akzent:   #2196F3  (Blau - Technologie)
Dark:     #E65100  (Dunkelorange)
```

## Einfaches Icon ohne Tools

Wenn du schnell ein einfaches Icon brauchst:

1. Erstelle einen Screenshot von einem passenden Material Design Icon
2. Öffne https://www.iloveimg.com/resize-image/resize-png
3. Resize zu 256x256px
4. Speichere als `icon.png`

**Empfohlene Icons:**
- `mdi:oil-temperature` - Öl-Symbol
- `mdi:gauge` - Füllstandsanzeige
- `mdi:propane-tank` - Tank-Symbol
- `mdi:gauge-empty` bis `mdi:gauge-full` - Füllstände
