# Beispiel-Konfigurationen für HAmex

## Dashboard-Karte für einen Tank

Fügen Sie diese Karte zu Ihrem Home Assistant Dashboard hinzu:

```yaml
type: entities
title: Heizöl Tank R
entities:
  - entity: sensor.tank_r_fullstand
    name: Füllstand
    icon: mdi:gauge
  - entity: sensor.tank_r_volumen
    name: Volumen
    icon: mdi:oil-temperature
  - entity: sensor.tank_r_verbrauch
    name: Täglicher Verbrauch
    icon: mdi:chart-line
  - entity: sensor.tank_r_reichweite
    name: Reichweite
    icon: mdi:calendar-clock
  - entity: sensor.tank_r_batterie
    name: MEX Batterie
    icon: mdi:battery
```

## Gauge-Karte für Füllstand

```yaml
type: gauge
entity: sensor.tank_r_fullstand
name: Tank R Füllstand
min: 0
max: 100
severity:
  green: 40
  yellow: 20
  red: 0
```

## Verlaufsgraph

```yaml
type: history-graph
title: Tankfüllstand letzte 7 Tage
entities:
  - entity: sensor.tank_r_fullstand
  - entity: sensor.tank_l_fullstand
hours_to_show: 168
refresh_interval: 0
```

## Automation: Benachrichtigung bei niedrigem Füllstand

```yaml
automation:
  - alias: "Heizöl Tank niedrig"
    trigger:
      - platform: numeric_state
        entity_id: sensor.tank_r_fullstand
        below: 20
    action:
      - service: notify.notify
        data:
          title: "Heizöl Tank niedrig!"
          message: >
            Tank R hat nur noch {{ states('sensor.tank_r_fullstand') }}%
            ({{ states('sensor.tank_r_volumen') }}L).
            Geschätzte Reichweite: {{ states('sensor.tank_r_reichweite') }} Tage.
```

## Automation: Benachrichtigung bei niedriger Batterie

```yaml
automation:
  - alias: "MEX Sensor Batterie niedrig"
    trigger:
      - platform: numeric_state
        entity_id: sensor.tank_r_batterie
        below: 20
    action:
      - service: notify.notify
        data:
          title: "MEX Sensor Batterie niedrig"
          message: >
            Die Batterie des MEX Sensors (Tank R) ist bei
            {{ states('sensor.tank_r_batterie') }}%.
```

## Automation: Günstiger Heizölpreis

```yaml
automation:
  - alias: "Heizöl Preisprognose günstig"
    trigger:
      - platform: numeric_state
        entity_id: sensor.heizol_preis_prognose
        below: -2  # Prognose: Mindestens 2% günstiger
    condition:
      - condition: numeric_state
        entity_id: sensor.tank_r_fullstand
        below: 50  # Nur wenn Tank unter 50%
    action:
      - service: notify.notify
        data:
          title: "Heizöl: Günstiger Preis erwartet"
          message: >
            Die Preisprognose zeigt {{ states('sensor.heizol_preis_prognose') }}% Änderung.
            Tank R ist bei {{ states('sensor.tank_r_fullstand') }}% -
            eventuell ein guter Zeitpunkt zum Bestellen?
```

## Lovelace Dashboard (vollständig)

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # Heizöl Übersicht

  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.tank_r_fullstand
        name: Tank R
        min: 0
        max: 100
        severity:
          green: 40
          yellow: 20
          red: 0
      - type: gauge
        entity: sensor.tank_l_fullstand
        name: Tank L
        min: 0
        max: 100
        severity:
          green: 40
          yellow: 20
          red: 0

  - type: entities
    title: Tank Details
    entities:
      - type: section
        label: Tank R
      - entity: sensor.tank_r_volumen
        name: Volumen
      - entity: sensor.tank_r_verbrauch
        name: Verbrauch
      - entity: sensor.tank_r_reichweite
        name: Reichweite
      - entity: sensor.tank_r_batterie
        name: Batterie
      - type: section
        label: Tank L
      - entity: sensor.tank_l_volumen
        name: Volumen
      - entity: sensor.tank_l_verbrauch
        name: Verbrauch
      - entity: sensor.tank_l_reichweite
        name: Reichweite
      - entity: sensor.tank_l_batterie
        name: Batterie

  - type: entities
    title: Preisinformationen
    entities:
      - entity: sensor.heizol_preis_vergleich
        name: Preis vs. Gestern
      - entity: sensor.heizol_preis_prognose
        name: Preisprognose

  - type: history-graph
    title: Füllstand Verlauf
    entities:
      - entity: sensor.tank_r_fullstand
      - entity: sensor.tank_l_fullstand
    hours_to_show: 168
```

## Template-Sensor: Gesamt-Füllstand

Wenn Sie mehrere Tanks haben und den Gesamtfüllstand berechnen möchten:

```yaml
template:
  - sensor:
      - name: "Heizöl Gesamt Volumen"
        unit_of_measurement: "L"
        state: >
          {{ states('sensor.tank_r_volumen') | float(0) +
             states('sensor.tank_l_volumen') | float(0) }}
        icon: mdi:oil-temperature

      - name: "Heizöl Gesamt Füllstand"
        unit_of_measurement: "%"
        state: >
          {% set tank_r_vol = states('sensor.tank_r_volumen') | float(0) %}
          {% set tank_l_vol = states('sensor.tank_l_volumen') | float(0) %}
          {% set tank_r_max = state_attr('sensor.tank_r_fullstand', 'max_volume') | float(1000) %}
          {% set tank_l_max = state_attr('sensor.tank_l_fullstand', 'max_volume') | float(1000) %}
          {% set total_vol = tank_r_vol + tank_l_vol %}
          {% set total_max = tank_r_max + tank_l_max %}
          {{ ((total_vol / total_max * 100) | round(1)) if total_max > 0 else 0 }}
        icon: mdi:gauge
```
