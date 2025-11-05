# HAmex - Home Assistant Integration für Heizoel24 MEX

Diese Integration ermöglicht es, Daten vom Heizoel24 MEX Dashboard in Home Assistant zu integrieren und Ihre Heizöltanks zu überwachen.

## Features

Die Integration erstellt automatisch folgende Sensoren **für jeden MEX-Tank**:

- **Füllstand** (%) - Aktueller Füllstand in Prozent
- **Volumen** (Liter) - Aktuelle Füllmenge in Litern
- **Batterie** (%) - Batteriestand des MEX-Sensors
- **Verbrauch** (L/Tag) - Durchschnittlicher täglicher Verbrauch
- **Reichweite** (Tage) - Geschätzte verbleibende Tage bis Tank leer

Zusätzliche Sensoren:
- **Heizöl Preis Vergleich** - Preisänderung im Vergleich zu gestern
- **Heizöl Preis Prognose** - Preisprognose

Alle Sensoren enthalten zusätzliche Attribute mit detaillierten Informationen wie Tankname, maximales Volumen, Jahresverbrauch, letzter Messung, etc.

## Installation

### HACS (empfohlen)

1. Öffnen Sie HACS in Home Assistant
2. Gehen Sie zu "Integrations"
3. Klicken Sie auf die drei Punkte oben rechts und wählen Sie "Custom repositories"
4. Fügen Sie diese Repository-URL hinzu
5. Installieren Sie "HAmex"
6. Starten Sie Home Assistant neu

### Manuelle Installation

1. Kopieren Sie den gesamten Ordner `custom_components/hamex` in Ihr Home Assistant `custom_components` Verzeichnis
   - Pfad: `<config_dir>/custom_components/hamex/`
2. Starten Sie Home Assistant neu

## Konfiguration

1. Gehen Sie zu "Einstellungen" → "Geräte & Dienste"
2. Klicken Sie auf "+ Integration hinzufügen"
3. Suchen Sie nach "HAmex"
4. Geben Sie Ihre Heizoel24 Zugangsdaten ein:
   - **Benutzername**: Ihre E-Mail-Adresse bei Heizoel24
   - **Passwort**: Ihr Heizoel24-Passwort

Die Integration verwendet Cookie-basierte Authentifizierung und erstellt automatisch alle verfügbaren Sensoren.

## Technische Details

### Authentifizierung

Die Integration nutzt die offizielle Heizoel24 Web-API mit Cookie-basierter Session-Verwaltung:
- Login erfolgt über `https://www.heizoel24.de/api/account/anmelden`
- Session-Cookies werden automatisch verwaltet
- Bei Ablauf erfolgt automatische Re-Authentifizierung

### API-Endpunkte

- **Login**: `https://www.heizoel24.de/api/account/anmelden`
- **Dashboard**: `https://www.heizoel24.de/api/customer/mex/dashboard/get`

### Update-Intervall

Standard: **300 Sekunden (5 Minuten)**

## Anpassung

### Update-Intervall ändern

Das Standard-Update-Intervall beträgt 300 Sekunden (5 Minuten). Um dies zu ändern, bearbeiten Sie die Datei `const.py`:

```python
UPDATE_INTERVAL = 300  # Sekunden
```

### Sensor-Namen anpassen

Die Sensoren werden automatisch aus den API-Daten erstellt. Um die Sensor-Konfiguration anzupassen, bearbeiten Sie die Datei `sensor.py`.

## Debugging

Um Debug-Logs zu aktivieren, fügen Sie folgendes zu Ihrer `configuration.yaml` hinzu:

```yaml
logger:
  default: info
  logs:
    custom_components.hamex: debug
```

## Support

Bei Problemen oder Fragen erstellen Sie bitte ein Issue auf GitHub.

## Lizenz

MIT License
