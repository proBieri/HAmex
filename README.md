# HAmex - Home Assistant Integration für Heizoel24 MEX (Inoffiziell)

Diese Integration ermöglicht es, Daten vom Heizoel24 MEX Dashboard in Home Assistant zu integrieren und Ihre Heizöltanks zu überwachen.

## Features

### Geräte-Struktur

Die Integration erstellt automatisch separate **Geräte** für bessere Organisation:

#### Pro Tank (z.B. "Tank 1", "Tank 2")
Jeder physische Tank wird als eigenes Gerät angelegt mit folgenden Sensoren:
- **Füllstand** (%) - Aktueller Füllstand in Prozent
- **Volumen** (L) - Aktuelle Füllmenge in Litern
- **Batterie** (%) - Batteriestand des MEX-Sensors
- **Verbrauch** (L/Tag) - Durchschnittlicher täglicher Verbrauch
- **Reichweite** (Tage) - Geschätzte verbleibende Tage bis Tank leer

#### Virtuelles "Gesamt" Gerät
Zusammenfassung aller Tanks mit Gesamtwerten:
- **Gesamtvolumen** (L) - Summe aller Tanks
- **Gesamtfüllstand** (%) - Gewichteter Durchschnitt
- **Gesamtverbrauch** (L/Tag) - Systemverbrauch
- **Gesamtreichweite** (Tage) - Geschätzte Restdauer
- **Preis Vergleich** (%) - Preisänderung zu gestern
- **Preis Prognose** (%) - Erwartete Preisentwicklung

Alle Sensoren enthalten zusätzliche Attribute mit detaillierten Informationen.

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

Die Integration nutzt die Heizoel24 Web-API mit Cookie-basierter Session-Verwaltung:
- Login erfolgt über `https://www.heizoel24.de/api/account/anmelden`
- Session-Cookies werden automatisch verwaltet
- Bei Ablauf erfolgt automatische Re-Authentifizierung

### API-Endpunkte

- **Login**: `https://www.heizoel24.de/api/account/anmelden`
- **Dashboard**: `https://www.heizoel24.de/api/customer/mex/dashboard/get`

### Update-Intervall

Standard: **3600 Sekunden (60 Minuten)**

## Anpassung

### Update-Intervall ändern

Das Standard-Update-Intervall beträgt 3600 Sekunden (60 Minuten). Um dies zu ändern, bearbeiten Sie die Datei `const.py`:

```python
UPDATE_INTERVAL = 3600  # Sekunden
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



## Spenden

Falls sie mir einen Kaffee (oder natürlich ein paar Liter Heizöl) spenden möchten.. 

[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20me%20a%20coffee-%23ffdd00?style=flat-square&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/probieri)


## Copyright
Alle Rechte an den API's und den verwendeten Icons liegen bei https://www.heizoel24.de

## Lizenz

MIT License.
