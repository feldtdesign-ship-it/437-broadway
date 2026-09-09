# 437 Broadway, foot traffic

Public data on the corner of Broadway and Canal Street, SoHo, gathered 9 September 2026.

**Live page:** https://feldtdesign-ship-it.github.io/437-broadway/

- `index.html` – the gauge. A live estimate of people entering Canal St station per minute, the day, the week, the year since 2020, weather against traffic, the camera ring, the city's own sidewalk counts, and the measured sidewalk at the door.
- `report.html` – the first, plainer field report.
- `live-wall.html` – the twelve nearest NYC DOT cameras, refreshing every 20 seconds. Open it in a browser.
- `data/` – the raw pulls: MTA hourly ridership for the Canal St complex, Open-Meteo daily weather, bus stop counts, planimetric sidewalk and curb geometry.
- `frames/` – camera frames from the evening of 9 September 2026.
- `build/` – the scripts that turn the data into the pages.

## Where the numbers come from

- MTA subway hourly ridership, station complex 623 (Canal St, N Q R W J Z 6), data.ny.gov
- NYC DOT camera network, webcams.nyctmc.org
- SoHo/NoHo Neighborhood Plan FEIS, Chapter 14 Transportation, 2021: measured sidewalk and stair counts
- SoHo Broadway Initiative: Placer.ai district figures and the Broadway and Prince counter
- NYC Planimetric Database and OpenStreetMap: sidewalk width at the door
- PLUTO: the lot, 433 to 437 Broadway
- Open-Meteo: daily weather

Nothing here counts the people passing the door itself. The page says so where it matters.
