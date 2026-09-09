import base64, json, os, html

S = os.path.dirname(os.path.abspath(__file__))
def b64(name):
    with open(os.path.join(S, name), 'rb') as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

canal = b64('canal_broadway_2.jpg')
grand = b64('grand_broadway_2.jpg')
broome = b64('broome_lafayette.jpg')

# ---- optional MTA chart ----
chart_html = ""
mta_path = os.path.join(S, 'mta_2025.json')
if os.path.exists(mta_path) and os.path.getsize(mta_path) > 10:
    try:
        rows = json.load(open(mta_path))
        pts = [(r['month'][:7], float(r['riders'])) for r in rows if r.get('riders')]
        pts = [p for p in pts if p[0] >= '2025-01']
        # drop a partial current month
        if pts and pts[-1][0] == '2026-09':
            pts = pts[:-1]
        if len(pts) >= 6:
            W, H = 720, 260
            padl, padr, padt, padb = 56, 12, 16, 40
            n = len(pts)
            mx = max(v for _, v in pts)
            step = 500000
            top = ((int(mx) // step) + 1) * step
            bw = (W - padl - padr) / n
            bars = []
            labels = []
            for i, (m, v) in enumerate(pts):
                x = padl + i * bw
                h = (H - padt - padb) * v / top
                y = H - padb - h
                cls = "bar" if m[5:] not in ('12', '01', '02') else "bar winter"
                bars.append(f'<rect class="{cls}" x="{x+2:.1f}" y="{y:.1f}" width="{bw-4:.1f}" height="{h:.1f}"/>')
                mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m[5:])-1]
                labels.append(f'<text class="ax" x="{x+bw/2:.1f}" y="{H-padb+16}" text-anchor="middle">{mon[0]}</text>')
                if m[5:] == '01' or m == pts[0][0]:
                    labels.append(f'<text class="ax" x="{x+2:.1f}" y="{H-padb+32}" text-anchor="start">{m[:4]}</text>')
            grid = []
            for g in range(0, top+1, step):
                y = H - padb - (H - padt - padb) * g / top
                grid.append(f'<line class="grid" x1="{padl}" x2="{W-padr}" y1="{y:.1f}" y2="{y:.1f}"/>')
                grid.append(f'<text class="ax" x="{padl-6}" y="{y+4:.1f}" text-anchor="end">{g/1e6:.1f}M</text>')
            lo = min(pts, key=lambda p: p[1]); hi = max(pts, key=lambda p: p[1])
            chart_html = f'''
<section>
  <h2>Seasonal proxy: Canal St subway complex</h2>
  <p>The Canal St station complex (J, N, Q, R, W, Z, 6) has its entrances at Broadway, Lafayette and Centre. Its monthly turnstile entries are the closest free, multi-year signal for how busy this corner is through the year. Winter months are shaded.</p>
  <figure class="chart">
    <svg viewBox="0 0 {W} {H}" role="img" aria-label="Monthly subway entries at Canal St">
      {''.join(grid)}
      {''.join(bars)}
      {''.join(labels)}
    </svg>
    <figcaption>Monthly entries, Canal St complex (station id 623). Peak <b>{hi[0]}</b> at {hi[1]/1e6:.2f}M, low <b>{lo[0]}</b> at {lo[1]/1e6:.2f}M. Source: MTA hourly ridership, data.ny.gov.</figcaption>
  </figure>
  <p class="note">A station count is not a sidewalk count. It says when the neighbourhood is busy, not how many people pass this door.</p>
</section>'''
    except Exception as e:
        chart_html = f'<section><h2>Seasonal proxy</h2><p class="note">Subway ridership chart could not be built: {html.escape(str(e))}</p></section>'
else:
    chart_html = '''
<section>
  <h2>Seasonal proxy: Canal St subway complex</h2>
  <p class="note">The MTA turnstile query for the Canal St complex had not returned when this page was built. It is the best free multi-year signal for seasonality at this corner and can be added on the next pass.</p>
</section>'''

page = f'''<title>437 Broadway Foot Traffic</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Public+Sans:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{
  --paper:#F1F2EE; --ink:#16191A; --ink-2:#4A5250; --muted:#7A827E; --rule:#D6D9D3;
  --panel:#E7E9E3; --accent:#1F6B45; --accent-ink:#FFFFFF; --amber:#B8860B; --amber-bg:#F7EBC7;
  --bar:#2E7D4F; --bar-winter:#9DB9A8;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --paper:#131615; --ink:#E8EAE5; --ink-2:#B5BBB6; --muted:#8A928D; --rule:#2C312E;
    --panel:#1C201E; --accent:#5FB27F; --accent-ink:#0E1411; --amber:#E0B54A; --amber-bg:#2A2410;
    --bar:#5FB27F; --bar-winter:#3D5A49;
  }}
}}
:root[data-theme="dark"]{{
  --paper:#131615; --ink:#E8EAE5; --ink-2:#B5BBB6; --muted:#8A928D; --rule:#2C312E;
  --panel:#1C201E; --accent:#5FB27F; --accent-ink:#0E1411; --amber:#E0B54A; --amber-bg:#2A2410;
  --bar:#5FB27F; --bar-winter:#3D5A49;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Public Sans",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.55}}
main{{max-width:760px;margin:0 auto;padding:40px 24px 72px;display:flex;flex-direction:column;gap:40px}}
h1,h2,h3{{font-family:"Barlow Condensed","Arial Narrow",Impact,sans-serif;text-wrap:balance;margin:0;line-height:1.05}}
h1{{font-size:56px;font-weight:700;letter-spacing:-.01em}}
h2{{font-size:30px;font-weight:600;margin-bottom:12px;padding-top:6px;border-top:2px solid var(--ink)}}
h3{{font-size:20px;font-weight:600}}
p{{margin:0 0 12px;max-width:66ch}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}}
header .meta{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:13px;color:var(--ink-2);margin-top:14px;display:flex;flex-wrap:wrap;gap:6px 22px}}
.verdict{{background:var(--panel);border-left:6px solid var(--accent);padding:18px 22px;display:flex;flex-direction:column;gap:8px}}
.verdict p{{margin:0}}
.verdict .lead{{font-size:19px;font-weight:600;line-height:1.35}}
.warn{{background:var(--amber-bg);border-left:6px solid var(--amber);padding:14px 18px;margin:0}}
.warn b{{color:var(--ink)}}
.cams{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-top:14px}}
.cam{{display:flex;flex-direction:column;gap:8px}}
.cam img{{width:100%;aspect-ratio:352/240;object-fit:cover;display:block;border:1px solid var(--rule);background:#000}}
.cam .cap{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--ink-2);line-height:1.45}}
.cam .cap b{{color:var(--ink);font-weight:500}}
.pill{{display:inline-block;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;border-radius:3px;background:var(--accent);color:var(--accent-ink)}}
.pill.no{{background:var(--amber);color:#1a1400}}
.pill.dim{{background:var(--rule);color:var(--ink-2)}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:10px}}
th{{text-align:left;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500;padding:8px 10px 8px 0;border-bottom:1px solid var(--ink)}}
td{{padding:10px 10px 10px 0;border-bottom:1px solid var(--rule);vertical-align:top}}
td.num{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;white-space:nowrap}}
.tablewrap{{overflow-x:auto}}
.plan{{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-direction:column;gap:14px}}
.plan li{{display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:start}}
.plan .n{{font-family:"Barlow Condensed",sans-serif;font-size:26px;font-weight:700;color:var(--accent);line-height:1;padding-top:2px}}
.plan b{{display:block;margin-bottom:2px}}
.plan p{{margin:0;color:var(--ink-2);font-size:15px}}
.block{{margin-top:14px;background:var(--panel);padding:10px}}
.block svg{{width:100%;height:auto;display:block}}
.block .st{{stroke:var(--rule);stroke-width:14;fill:none}}
.block .lbl{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11px;fill:var(--ink-2)}}
.block .bld{{fill:var(--accent)}}
.block .cone{{fill:var(--accent);opacity:.22}}
.block .cone.bad{{fill:var(--amber)}}
.block .camdot{{fill:var(--ink)}}
figure{{margin:0}}
.chart svg{{width:100%;height:auto;display:block}}
.chart .grid{{stroke:var(--rule);stroke-width:1}}
.chart .bar{{fill:var(--bar)}}
.chart .bar.winter{{fill:var(--bar-winter)}}
.chart .ax{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11px;fill:var(--muted)}}
figcaption{{font-size:13.5px;color:var(--ink-2);margin-top:8px}}
.note{{font-size:14px;color:var(--ink-2);font-style:italic}}
.src{{font-size:13px;color:var(--muted);line-height:1.6}}
.src a{{color:var(--ink-2)}}
a{{color:var(--accent)}}
a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
@media (max-width:520px){{h1{{font-size:42px}}}}
</style>
<main>
<header>
  <div class="eyebrow">Foot traffic reconnaissance · 9 Sep 2026</div>
  <h1>437 Broadway</h1>
  <div class="meta">
    <span>West side of Broadway, between Howard St and Grand St</span>
    <span>SoHo / Canal, Manhattan 10013</span>
    <span>40.7202 N, 74.0014 W</span>
  </div>
</header>

<div class="verdict">
  <p class="lead">Two public DOT cameras sit within 110 m of the door. Neither shows the storefront, but the Canal St camera catches the Broadway crossing well. The city keeps no recordings, so seasonal comparison has to be bought or built from today forward.</p>
  <p>The Grand St camera is the one that could look down the block, and it is currently out of focus. The nearest official pedestrian count is in Chinatown, too far away to stand in for this block.</p>
</div>


<section>
  <h2>The numbers that exist</h2>
  <div class="tablewrap">
  <table>
    <tr><th>Figure</th><th>Value</th><th>Where it comes from</th></tr>
    <tr><td>SoHo Broadway district, daily average people present, July 2025</td><td class="num">66,900</td><td>Placer.ai, via the SoHo Broadway Initiative. District is Broadway from Canal to Houston, both sides. 437 is at its south end.</td></tr>
    <tr><td>Same figure, July 2019 / April 2020 / summer 2023</td><td class="num">49,900 / 2,600 / 54,200</td><td>Placer.ai, same series</td></tr>
    <tr><td>Sidewalk counter at Broadway &amp; Prince, change since 2023</td><td class="num">+15%</td><td>SoHo Broadway Initiative counting device, 2025</td></tr>
    <tr><td>Same counter, year on year after congestion pricing</td><td class="num">+20%</td><td>SoHo Broadway Initiative, 2025</td></tr>
    <tr><td>Canal St subway complex, entries per day, summer 2026</td><td class="num">36,300 weekday · 34,000 Sat · 27,700 Sun</td><td>MTA hourly ridership, Jun–Aug 2026. Exits are about the same again.</td></tr>
    <tr><td>Busiest hour at that station</td><td class="num">5,050 entries, weekdays 5–6 pm</td><td>MTA hourly ridership. Saturday peak is 3–4 pm at about 3,500.</td></tr>
    <tr><td>Seasonal swing at that station, 2025</td><td class="num">Feb 823k → Dec 1,126k</td><td>MTA monthly. February runs about 15% under the year's average, July to December 7 to 11% over.</td></tr>
    <tr><td>Head count in the Canal St camera frame</td><td class="num">20 to 25 people</td><td>Four frames, Wed 9 Sep 2026, 6:14 to 6:16 pm, camera facing south. Rough count from a 352 × 240 image.</td></tr>
  </table>
  </div>
  <p class="note">None of these is a count at the door. The district figure spreads over half a mile of Broadway. The station figure counts riders, not walkers. A fair working estimate for the west sidewalk at 437 is in the low tens of thousands of passers a day, with a Saturday afternoon peak of a few thousand an hour. That is an inference, not a measurement.</p>
</section>

<section>
  <h2>What the cameras see</h2>
  <p>The NYC DOT network lists 973 cameras. These are the three closest to the address, with live frames pulled at 6:05 pm today. These are pan-tilt cameras that DOT operators re-aim: the Canal St camera faced east at 6:05 pm and south by 6:15 pm.</p>
  <div class="cams">
    <div class="cam">
      <img src="{canal}" alt="Live frame from the Canal St at Broadway camera, facing east across the Canal Street crosswalk">
      <div class="cap"><b>Canal St @ Broadway</b> · 84 m south · facing east<br>Facing east: the Canal crosswalk on the Broadway line, which every north–south walker on Broadway uses. Facing south: the Broadway sidewalks below Canal. <span class="pill">Usable</span></div>
    </div>
    <div class="cam">
      <img src="{grand}" alt="Live frame from the Grand St at Broadway camera, badly out of focus, facing north">
      <div class="cap"><b>Grand St @ Broadway</b> · 108 m north · facing north<br>Points away from the block and the lens is fogged or unfocused. Would be the right camera if turned south. <span class="pill no">Not usable today</span></div>
    </div>
    <div class="cam">
      <img src="{broome}" alt="Live frame from the Broome St at Lafayette St camera, facing south down Lafayette">
      <div class="cap"><b>Broome St @ Lafayette</b> · 273 m · facing south<br>One block east on Lafayette. Not the Broadway corridor. <span class="pill dim">Context only</span></div>
    </div>
  </div>
  <div class="block" aria-hidden="true">
    <svg viewBox="0 0 720 230">
      <line class="st" x1="360" y1="10" x2="360" y2="220"/>
      <line class="st" x1="60" y1="200" x2="700" y2="200"/>
      <line class="st" x1="60" y1="40" x2="700" y2="40"/>
      <line class="st" x1="140" y1="150" x2="360" y2="150"/>
      <text class="lbl" x="372" y="26">BROADWAY</text>
      <text class="lbl" x="66" y="190">CANAL ST</text>
      <text class="lbl" x="66" y="30">GRAND ST</text>
      <text class="lbl" x="146" y="140">HOWARD ST</text>
      <polygon class="cone" points="360,200 700,150 700,230"/>
      <circle class="camdot" cx="360" cy="200" r="6"/>
      <text class="lbl" x="440" y="222">camera · facing east</text>
      <polygon class="cone bad" points="360,40 330,0 390,0"/>
      <circle class="camdot" cx="360" cy="40" r="6"/>
      <text class="lbl" x="372" y="60">camera · facing north (blurred)</text>
      <rect class="bld" x="330" y="82" width="22" height="46"/>
      <text class="lbl" x="230" y="100">437 Broadway</text>
      <text class="lbl" x="230" y="114">west side, mid-block</text>
      <text class="lbl" x="600" y="26">N ↑</text>
    </svg>
  </div>
  <p class="note">Schematic, not to scale. Cones show the direction each camera faced today.</p>
</section>

<section>
  <h2>What history exists</h2>
  <div class="tablewrap">
  <table>
    <tr><th>Source</th><th>Covers</th><th>Cost</th><th>Verdict</th></tr>
    <tr><td>NYC DOT live feed</td><td>Now only. DOT states it does not record.</td><td class="num">Free</td><td>Good from today forward, nothing backward.</td></tr>
    <tr><td>Traffic Cam Archive (third party)</td><td>Roughly the last 90 to 150 days of DOT video, 429 cameras. Coverage of this exact camera unconfirmed.</td><td class="num">Paid, per clip</td><td>Gives one summer season now.</td></tr>
    <tr><td>NYC DOT bi-annual pedestrian counts</td><td>May and September since 2007 at 114 sites. Nearest is Forsyth St at Canal, 770 m east.</td><td class="num">Free</td><td>Wrong corridor. Not a proxy for SoHo Broadway.</td></tr>
    <tr><td>Mobile-location vendors (Placer.ai, Pass_by, Unacast)</td><td>Monthly visits to this address, multi-year, with dwell and origin. Built from location pings of tens of millions of phones running apps with an opted-in location SDK, then scaled up to the population.</td><td class="num">Paid; Placer has a free login tier</td><td>Only source that answers the seasonal question for this door today.</td></tr>
  </table>
  </div>
</section>

{chart_html}

<section>
  <h2>Recommended plan</h2>
  <ol class="plan">
    <li><span class="n">1</span><div><b>Start an archive tonight.</b><p>A small scheduled job pulls a frame from the Canal St camera every 10 minutes. About 53,000 frames a year at 20 KB each, near 1 GB. Pedestrians in the crosswalk can be counted by a simple detector later, giving a season-by-season curve that is yours.</p></div></li>
    <li><span class="n">2</span><div><b>Buy the last summer from Traffic Cam Archive.</b><p>Check their map for the Canal St @ Broadway camera and pull one weekday and one Saturday per month back to June. That gives a summer baseline before the archive in step 1 has one.</p></div></li>
    <li><span class="n">3</span><div><b>Report the Grand St camera to 311.</b><p>It is the only camera that could look down the block at the storefront. A fogged lens is a maintenance ticket.</p></div></li>
    <li><span class="n">4</span><div><b>Price one vendor pull for the address.</b><p>If a lease or sales pitch needs real seasonal numbers for this door, a one-off Placer.ai report is the honest answer. Everything above is a proxy.</p></div></li>
  </ol>
</section>

<p class="warn"><b>Two assumptions.</b> "The city" was read as Manhattan. There is also a 437 Broadway in Williamsburg, Brooklyn. And the cameras are re-aimed by DOT operators through the day, so any archive will hold mixed views.</p>

<p class="src">Sources: <a href="https://webcams.nyctmc.org/">NYC DOT camera network</a> · <a href="https://data.cityofnewyork.us/Transportation/Bi-Annual-Pedestrian-Counts/cqsj-cfgu">Bi-Annual Pedestrian Counts, NYC Open Data</a> · <a href="https://newyorkcity.trafficcamarchive.com/">Traffic Cam Archive</a> · <a href="https://roadproof.com/new-york/">DOT recording policy summary</a> · <a href="https://data.ny.gov/">MTA hourly ridership, data.ny.gov</a></p>
</main>
'''
out = os.path.join(S, '437-broadway-foot-traffic.html')
open(out, 'w').write(page)
print("wrote", out, len(page)//1024, "KB; chart:", "yes" if "<rect class=\"bar" in chart_html else "no")
