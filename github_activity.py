"""First-party, build-time GitHub activity snapshot. No browser token or third-party embeds."""
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import os
import re
from urllib.request import Request, urlopen

URL = 'https://github.com/users/Lucifer-Newstar/contributions'
PROFILE = 'https://github.com/Lucifer-Newstar'
CACHE = Path(__file__).parent / 'data' / 'github-activity.json'

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tips = {}
        self.tip = None
        self.heading = False
        self.heading_text = ''
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip':
            self.tip = a.get('for')
        if tag == 'h2' and a.get('id') == 'js-contribution-activity-description':
            self.heading = True
    def handle_data(self, value):
        if self.tip:
            self.tips[self.tip] = self.tips.get(self.tip, '') + value
        if self.heading:
            self.heading_text += value
    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.tip = None
        if tag == 'h2':
            self.heading = False
    def result(self):
        days = []
        for key, cell in self.cells.items():
            tip = self.tips.get(key, '').strip()
            count = re.match(r'([\d,]+) contributions?\b', tip)
            if count:
                cell['count'] = int(count.group(1).replace(',', ''))
            elif tip.startswith('No contributions'):
                cell['count'] = 0
            else:
                raise ValueError('Unknown GitHub day count format')
            days.append(cell)
        days.sort(key=lambda d: d['date'])
        validate(days)
        heading = re.search(r'([\d,]+)\s+contributions', self.heading_text)
        if not heading or int(heading.group(1).replace(',', '')) != sum(d['count'] for d in days):
            raise ValueError('GitHub calendar total mismatch')
        return days

def validate(days):
    if not 365 <= len(days) <= 371:
        raise ValueError('Unexpected calendar length')
    previous = None
    for day in days:
        current = date.fromisoformat(day['date'])
        if previous and current != previous + timedelta(days=1):
            raise ValueError('Non-contiguous contribution calendar')
        if not 0 <= day['level'] <= 4 or not 0 <= day['count'] <= 100000:
            raise ValueError('Invalid contribution count or level')
        previous = current


def snapshot():
    try:
        if os.environ.get('GITHUB_ACTIVITY_OFFLINE') == '1':
            raise OSError('Offline build requested')
        request = Request(URL, headers={'User-Agent': 'Portfolio-static-build/1.0', 'Accept': 'text/html'})
        with urlopen(request, timeout=10) as response:
            markup = response.read(2_000_000).decode('utf-8')
        parser = CalendarParser()
        parser.feed(markup)
        days = parser.result()
        today = datetime.now(timezone.utc).date()
        if not today - timedelta(days=1) <= date.fromisoformat(days[-1]['date']) <= today + timedelta(days=1):
            raise ValueError('Unexpected current calendar endpoint')
        result = {'source': URL, 'fetched_at': datetime.now(timezone.utc).isoformat(), 'days': days}
        CACHE.parent.mkdir(exist_ok=True)
        tmp = CACHE.with_suffix('.tmp')
        tmp.write_text(json.dumps(result, indent=2) + '\n')
        tmp.replace(CACHE)
        return result, False
    except Exception as exc:
        print('GitHub activity refresh unavailable; keeping dated snapshot:', type(exc).__name__)
        if CACHE.exists():
            result = json.loads(CACHE.read_text())
            validate(result['days'])
            return result, True
        return None, True


def render_activity():
    data, fallback = snapshot()
    if not data:
        return '<section id="github-activity"><div class="wrap"><h2>GitHub activity</h2><p>Activity snapshot unavailable. <a href="'+PROFILE+'">View my GitHub profile ↗</a></p></div></section>'
    days = data['days']
    end = date.fromisoformat(days[-1]['date'])
    start = end - timedelta(days=364)
    year = [d for d in days if d['date'] >= start.isoformat()]
    total = sum(d['count'] for d in year)
    active = sum(d['count'] > 0 for d in year)
    anchor = date.fromisoformat(days[0]['date'])
    anchor -= timedelta(days=(anchor.weekday()+1)%7)
    weeks = ((end-anchor).days//7)+1
    width = 34+weeks*12
    rects = []
    months = []
    previous_month = None
    for d in days:
        day = date.fromisoformat(d['date'])
        if day < start:
            continue
        column = (day-anchor).days//7
        row = (day.weekday()+1)%7
        x, y = 30+column*12, 28+row*12
        desc = day.strftime('%d %b %Y')+': '+str(d['count'])+' contribution'+('' if d['count']==1 else 's')
        rects.append(f'<rect class="gh-day gh-l{d["level"]}" x="{x}" y="{y}" width="9" height="9" rx="2"><title>{escape(desc)}</title></rect>')
        if day.month != previous_month:
            # Skip the partial first month label when it would collide with next month.
            if day.day <= 7:
                months.append(f'<text x="{x}" y="14">{day.strftime("%b")}</text>')
            previous_month = day.month
    checked = datetime.fromisoformat(data['fetched_at']).astimezone(timezone(timedelta(hours=5, minutes=30))).strftime('%d %b %Y, %H:%M IST')
    range_text = start.strftime('%d %b %Y')+' – '+end.strftime('%d %b %Y')
    status = 'Refresh unavailable · showing saved snapshot' if fallback else 'Updated at build time'
    svg = f'<svg class="gh-chart" viewBox="0 0 {width} 120" role="img" aria-labelledby="gh-chart-title gh-chart-desc"><title id="gh-chart-title">GitHub activity, last 365 days</title><desc id="gh-chart-desc">{range_text}. {total:,} contributions on {active} active days. Each square is one day; stronger shades indicate more activity.</desc>'+''.join(months)+'<text x="0" y="48">Mon</text><text x="0" y="72">Wed</text><text x="0" y="96">Fri</text>'+''.join(rects)+'</svg>'
    return f'''<section id="github-activity"><div class="wrap">
  <div class="gh-card reveal">
    <div class="gh-top"><span class="gh-path"><i aria-hidden="true"></i> github / Lucifer-Newstar</span><a href="{PROFILE}" target="_blank" rel="noopener">View profile ↗</a></div>
    <div class="gh-overview"><div><p class="eyebrow">building in the open</p><h2>GitHub activity</h2><p class="gh-range">{range_text}</p></div><div class="gh-stats"><div><b>{total:,}</b><span>contributions</span></div><div><b>{active}</b><span>active days</span></div></div></div>
    <div class="gh-scroll" tabindex="0" role="region" aria-label="Full-year GitHub contribution calendar, scroll horizontally to explore">{svg}</div>
    <div class="gh-key"><span class="gh-mobile-hint">Swipe to explore the full year ← →</span><span class="gh-legend">Less <i class="gh-l0"></i><i class="gh-l1"></i><i class="gh-l2"></i><i class="gh-l3"></i><i class="gh-l4"></i> More</span></div>
    <div class="gh-foot"><span>Snapshot · {checked}</span><span>{status}</span></div>
    <p class="gh-note">Counts visible on GitHub, including any anonymized private contributions.</p>
  </div>
</div></section>'''
