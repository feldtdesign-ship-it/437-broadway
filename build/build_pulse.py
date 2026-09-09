import json, os, base64, datetime, collections
S = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(S, n)))
ok = lambda n: os.path.exists(os.path.join(S, n)) and os.path.getsize(os.path.join(S, n)) > 10

# hourly by dow (summer 2026)
days = collections.Counter()
d = datetime.date(2026, 6, 1)
while d <= datetime.date(2026, 8, 31):
    days[(d.weekday() + 1) % 7] += 1
    d += datetime.timedelta(days=1)
hourly = {dw: [0.0] * 24 for dw in range(7)}
for x in J('mta_hourly.json'):
    hourly[int(x['dow'])][int(x['hr'])] = round(float(x['riders']) / days[int(x['dow'])], 1)

# months 2025-01 .. 2026-08
months = [[r['month'][:7], float(r['riders'])] for r in J('mta_2025.json')]
months = [m for m in months if '2025-01' <= m[0] <= '2026-08']

# history 2020-2024
hist = []
if ok('mta_hist.json'):
    try:
        hist = [[r['month'][:7], float(r['riders'])] for r in J('mta_hist.json')]
        hist = [h for h in hist if h[0] < '2025-01']
    except Exception as e:
        print('hist skipped:', e)

# daily + weather
daily = []
if ok('mta_daily.json'):
    try:
        w = J('weather.json')['daily']
        wx = {t: (w['temperature_2m_max'][i], w['precipitation_sum'][i] or 0.0, w['snowfall_sum'][i] or 0.0) for i, t in enumerate(w['time'])}
        for r in J('mta_daily.json'):
            dt = r['day'][:10]
            if dt in wx and '2025-01-01' <= dt <= '2026-08-31':
                t, p, s = wx[dt]
                if t is None: continue
                daily.append([dt, round(float(r['riders'])), round(t, 1), round(p, 2), round(s, 2)])
    except Exception as e:
        print('daily skipped:', e)

# frames
frames = []
stamps = ['6:14:39 pm', '6:14:59 pm', '6:15:19 pm', '6:15:39 pm', '6:15:59 pm', '6:16:19 pm']
for i in range(1, 7):
    fp = os.path.join(S, 'frames', f'f{i}.jpg')
    if os.path.exists(fp):
        frames.append({'src': 'data:image/jpeg;base64,' + base64.b64encode(open(fp, 'rb').read()).decode(), 't': 'Wed 9 Sep 2026 ' + stamps[i-1] + ' · facing south'})

ring=[]
RING=[(0,'Facing south down Broadway. The Canal crosswalk in the foreground.','Usable'),
      (3,'Facing west along Canal toward Broadway. Chinatown side of the corridor.','Corridor'),
      (4,'Facing east along Canal toward Broadway. Tribeca side of the corridor.','Corridor'),
      (2,'Facing south down Lafayette, the parallel street one block east.','Context'),
      (1,'Facing north, lens fogged. The one camera that could look down the block.','Fogged')]
rj={c['i']:c for c in json.load(open(os.path.join(S,'ring','ring.json')))}
for i,desc,tag in RING:
    c=rj[i]; fp=os.path.join(S,c['file'])
    if os.path.exists(fp):
        ring.append({'name':c['name'],'dist':c['dist'],'id':c['id'],'desc':desc,'tag':tag,'src':'data:image/jpeg;base64,'+base64.b64encode(open(fp,'rb').read()).decode()})
data = {'ring': ring, 'hourly': hourly, 'months': months, 'hist': hist, 'daily': daily, 'frames': frames}
tpl = open(os.path.join(S, 'pulse_template.html')).read()
out = tpl.replace('__DATA__', json.dumps(data, separators=(',', ':')))
open(os.path.join(S, 'canal-broadway-pulse.html'), 'w').write(out)
print(f"built: months={len(months)} hist={len(hist)} daily={len(daily)} frames={len(frames)} size={len(out)//1024}KB")
