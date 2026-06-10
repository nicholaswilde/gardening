# :seedling: Click & Grow

!!! example ""

    :material-list-status: **Status:** Inactive  

    :material-tag-text-outline: **Model:** [Smart Garden 3][1]

    :material-map-marker-outline: **Location:** Kitchen Counter  

## :clipboard: Active Pods

Think of this as the "Current State" for the device, tracking what is actively plugged into the system right now.

| Slot | Crop | Date Planted | Status |
| :--- | :--- | :--- | :--- |
| 1 | Basil | 2026-05-15 | Harvesting |
| 2 | Mini Tomato | 2026-06-01 | Sprouting |
| 3 | [Empty] | | |

## :package: Pod Inventory

| Crop / Variety | Quantity | Purchase Date | Best By | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Dwarf Pea | ? | 2025-02 | 2026-02 | |
| Mini Tomato | ? | 2025-02 | 2026-02 | |
| Peppermint | ? | 2025-02 | 2026-02 | |
| Basil | ? | 2025-02 | 2026-02 | |
| Cilantro | ? | 2025-02 | 2026-02 | |
| Chives | 0 | 2020–2024 | | Historical order. Likely depleted. |
| Parsley | 0 | 2020–2024 | | Historical order. Likely depleted. |
| Cockscomb | 0 | 2020–2024 | | Historical order. Likely depleted. |
| Red Hot Chili Pepper | 0 | 2022-02 | | Historical order. Likely depleted. |
| Red Sweet Pepper | 0 | 2025-02-18 | | Historical order. Likely depleted. |
| Wild Strawberry | 0 | 2022-06-17 | | Historical order. Likely depleted. |

## :wrench: Hardware & Maintenance

* **2026-06-09:** Initial documentation.
* **2025-05:** Procured replacement Smart Garden Plastic Cups (3 pieces).

!!! note "Maintenance Note"

    Ensure water float is checked weekly and plastic domes are removed once sprouts reach the top.

## :rocket: Planned Upgrades

!!! example ""

    :material-flask-outline: **Project:** ESP32 Water Level Telemetry 

    :material-list-status: **Status:** Planning  

    :material-connection: **Target Integration:** ESPHome / MQTT  

* **Objective:** Automate water level alerts to eliminate manual weekly float checks and push notifications directly to the dashboard.
* **Hardware Requirements:** * ESP32 microcontroller
    * Water level sensor (Researching capacitive vs. ultrasonic to avoid nutrient water corrosion)
    * Custom 3D printed low-profile enclosure
* **Implementation Notes:** The sensor will need to fit alongside the existing mechanical float without disrupting the light timer array. Once active, update the hardware table above with the deployment date.

[1]: <https://www.clickandgrow.com/products/the-smart-garden-3>
