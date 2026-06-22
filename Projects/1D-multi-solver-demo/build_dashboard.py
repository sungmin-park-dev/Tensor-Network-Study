"""Build a standalone HTML dashboard from the standalone XXZ comparison CSVs.

Reads xxz_solver_comparison.csv, xxz_observables_comparison.csv, and
xxz_entanglement_decay.csv (all produced by the compare_xxz_*.py / verify_xxz_bethe.py
scripts) and writes reports/dashboard.html. The HTML is self-contained except for the
Chart.js CDN script tag, so it opens directly in a browser (double-click or
file://.../reports/dashboard.html) without a local server.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _linear_fit_slope(x: list[float], y: list[float]) -> float:
    n = len(x)
    x_bar = sum(x) / n
    y_bar = sum(y) / n
    num = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    den = sum((xi - x_bar) ** 2 for xi in x)
    return num / den


def _to_float(value: str) -> float | None:
    if value == "nan":
        return None
    return float(value)


def load_solver_comparison() -> dict:
    path = ROOT / "xxz_solver_comparison.csv"
    rows = list(csv.DictReader(path.open()))
    L = [int(r["L"]) for r in rows]
    e_ed = [_to_float(r["E_ED"]) for r in rows]
    e_bethe = [_to_float(r["E_Bethe"]) for r in rows]
    e_dmrg = [_to_float(r["E_DMRG"]) for r in rows]
    per_site = lambda es: [None if e is None else e / l for e, l in zip(es, L)]
    diffs = [
        abs(ed - dm) / l
        for ed, dm, l in zip(e_ed, e_dmrg, L)
        if ed is not None
    ]
    return {
        "L": L,
        "ed": per_site(e_ed),
        "bethe": per_site(e_bethe),
        "dmrg": per_site(e_dmrg),
        "max_abs_diff": max(diffs) if diffs else None,
    }


def load_observables() -> dict:
    path = ROOT / "xxz_observables_comparison.csv"
    gap_L, gap_v = [], []
    corr_delta, corr_zz, corr_xx = [], [], []
    for row in csv.reader(path.open()):
        if not row or row[0].startswith("#"):
            continue
        if row[0] == "gap":
            gap_L.append(int(row[1]))
            gap_v.append(float(row[2]))
        elif row[0] == "corr":
            corr_delta.append(float(row[1]))
            corr_zz.append(float(row[2]))
            sxsx = row[5]
            corr_xx.append(None if sxsx == "nan" else float(sxsx))
    return {
        "gap_L": gap_L,
        "gap_v": gap_v,
        "corr_delta": corr_delta,
        "corr_zz": corr_zz,
        "corr_xx": corr_xx,
    }


def load_entanglement_decay() -> dict:
    path = ROOT / "xxz_entanglement_decay.csv"
    ell, s_dmrg = [], []
    gapless_r, gapless_v, gapped_r, gapped_v = [], [], [], []
    L_ent = None
    for line in path.open():
        line = line.strip()
        if line.startswith("# entanglement L="):
            L_ent = int(line.split("L=")[1].split()[0])
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        if parts[0] == "ent":
            ell.append(int(parts[1]))
            s_dmrg.append(float(parts[3]))
        elif parts[0] == "decay":
            delta, r, v = float(parts[1]), int(parts[2]), float(parts[3])
            if abs(delta - 1.0) < 1e-9:
                gapless_r.append(r)
                gapless_v.append(v)
            elif abs(delta - 2.0) < 1e-9:
                gapped_r.append(r)
                gapped_v.append(v)

    c_fit = None
    if L_ent and len(ell) > 2:
        x = [math.log((L_ent / math.pi) * math.sin(math.pi * l / L_ent)) for l in ell]
        slope = _linear_fit_slope(x, s_dmrg)
        c_fit = 3.0 * slope

    return {
        "ell": ell,
        "s": s_dmrg,
        "gapless_r": gapless_r,
        "gapless_v": gapless_v,
        "gapped_r": gapped_r,
        "gapped_v": gapped_v,
        "c_fit": c_fit,
    }


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>XXZ 1D multi-solver dashboard</title>
<style>
  body {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; margin: 0;
         background: #fafafa; color: #1a1a1a; }}
  main {{ max-width: 980px; margin: 0 auto; padding: 2rem 1.5rem 3rem; }}
  h1 {{ font-size: 22px; font-weight: 500; margin: 0 0 4px; }}
  p.subtitle {{ color: #666; font-size: 14px; margin: 0 0 2rem; }}
  .cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 2rem; }}
  .card {{ background: #fff; border: 1px solid #e5e5e5; border-radius: 10px; padding: 1rem; }}
  .card .label {{ font-size: 12px; color: #666; margin: 0 0 4px; }}
  .card .value {{ font-size: 22px; font-weight: 500; margin: 0; }}
  .card .hint {{ font-size: 12px; color: #999; margin: 4px 0 0; }}
  .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px; }}
  .panel h2 {{ font-size: 14px; font-weight: 500; margin: 0 0 8px; }}
  .legend {{ display: flex; gap: 14px; font-size: 12px; color: #666; margin-bottom: 6px; }}
  .legend span {{ display: flex; align-items: center; gap: 4px; }}
  .swatch {{ width: 10px; height: 10px; border-radius: 2px; display: inline-block; }}
  .chart-wrap {{ position: relative; height: 240px; }}
  footer {{ margin-top: 2rem; font-size: 12px; color: #999; }}
</style>
</head>
<body>
<main>
  <h1>XXZ 1D multi-solver dashboard</h1>
  <p class="subtitle">Generated by build_dashboard.py from xxz_*_comparison.csv / xxz_entanglement_decay.csv. Heisenberg point (Jxy=1, Delta=1) unless noted.</p>

  <div class="cards">
    <div class="card">
      <p class="label">Energy agreement</p>
      <p class="value">{max_abs_diff:.1e}</p>
      <p class="hint">ED vs DMRG, per site</p>
    </div>
    <div class="card">
      <p class="label">Spin gap, L={gap_L_last}</p>
      <p class="value">{gap_v_last:.3f}</p>
      <p class="hint">closes as 1/L</p>
    </div>
    <div class="card">
      <p class="label">CFT central charge</p>
      <p class="value">c &asymp; {c_fit:.2f}</p>
      <p class="hint">expected c = 1</p>
    </div>
    <div class="card">
      <p class="label">Correlation decay</p>
      <p class="value">power law / exp</p>
      <p class="hint">gapless vs gapped</p>
    </div>
  </div>

  <div class="grid">
    <div class="panel">
      <h2>Energy per site vs chain length L</h2>
      <div class="legend">
        <span><span class="swatch" style="background:#378ADD"></span>ED</span>
        <span><span class="swatch" style="background:#1D9E75"></span>Bethe</span>
        <span><span class="swatch" style="background:#D85A30"></span>DMRG</span>
      </div>
      <div class="chart-wrap"><canvas id="chartEnergy"></canvas></div>
    </div>
    <div class="panel">
      <h2>Spin gap vs chain length L</h2>
      <div class="legend"><span><span class="swatch" style="background:#378ADD"></span>spin gap</span></div>
      <div class="chart-wrap"><canvas id="chartGap"></canvas></div>
    </div>
    <div class="panel">
      <h2>Entanglement entropy vs subsystem size l</h2>
      <div class="legend"><span><span class="swatch" style="background:#534AB7"></span>S(l)</span></div>
      <div class="chart-wrap"><canvas id="chartEntropy"></canvas></div>
    </div>
    <div class="panel">
      <h2>Transverse correlation decay (log scale)</h2>
      <div class="legend">
        <span><span class="swatch" style="background:#378ADD"></span>gapless (Delta=1)</span>
        <span><span class="swatch" style="background:#BA7517"></span>gapped (Delta=2)</span>
      </div>
      <div class="chart-wrap"><canvas id="chartDecay"></canvas></div>
    </div>
  </div>

  <footer>Source data: xxz_solver_comparison.csv, xxz_observables_comparison.csv, xxz_entanglement_decay.csv. See reports/findings.md for the full write-up.</footer>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
Chart.defaults.color = '#666';
Chart.defaults.font.size = 11;
const grid = {{ color: 'rgba(0,0,0,0.08)' }};

new Chart(document.getElementById('chartEnergy'), {{
  type: 'line',
  data: {{
    labels: {energy_L},
    datasets: [
      {{ label: 'ED', data: {energy_ed}, borderColor: '#378ADD', backgroundColor: '#378ADD', pointRadius: 4 }},
      {{ label: 'Bethe', data: {energy_bethe}, borderColor: '#1D9E75', backgroundColor: '#1D9E75', pointRadius: 3, pointStyle: 'rect', borderDash: [4,2] }},
      {{ label: 'DMRG', data: {energy_dmrg}, borderColor: '#D85A30', backgroundColor: '#D85A30', pointRadius: 3, pointStyle: 'crossRot', borderDash: [2,2] }}
    ]
  }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
    scales: {{ x: {{ title: {{ display: true, text: 'chain length L' }}, grid }},
               y: {{ title: {{ display: true, text: 'E0 / L' }}, grid }} }} }}
}});

new Chart(document.getElementById('chartGap'), {{
  type: 'line',
  data: {{ labels: {gap_L}, datasets: [{{ label: 'spin gap', data: {gap_v}, borderColor: '#378ADD', backgroundColor: '#378ADD', pointRadius: 4 }}] }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
    scales: {{ x: {{ title: {{ display: true, text: 'chain length L' }}, grid }},
               y: {{ title: {{ display: true, text: 'gap' }}, grid }} }} }}
}});

new Chart(document.getElementById('chartEntropy'), {{
  type: 'line',
  data: {{ labels: {ell}, datasets: [{{ label: 'S(l)', data: {entropy}, borderColor: '#534AB7', backgroundColor: '#534AB7', pointRadius: 2, tension: 0.3 }}] }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
    scales: {{ x: {{ title: {{ display: true, text: 'subsystem size l' }}, grid }},
               y: {{ title: {{ display: true, text: 'entropy S' }}, grid }} }} }}
}});

new Chart(document.getElementById('chartDecay'), {{
  type: 'line',
  data: {{ labels: {decay_r}, datasets: [
    {{ label: 'gapless', data: {gapless_v}, borderColor: '#378ADD', backgroundColor: '#378ADD', pointRadius: 0, borderWidth: 2 }},
    {{ label: 'gapped', data: {gapped_v}, borderColor: '#BA7517', backgroundColor: '#BA7517', pointRadius: 0, borderWidth: 2 }}
  ] }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
    scales: {{ x: {{ title: {{ display: true, text: 'distance r' }}, grid }},
               y: {{ type: 'logarithmic', title: {{ display: true, text: '|<Sx Sx>|' }}, grid }} }} }}
}});
</script>
</body>
</html>
"""


def main() -> None:
    solver = load_solver_comparison()
    obs = load_observables()
    ent = load_entanglement_decay()

    html = TEMPLATE.format(
        max_abs_diff=solver["max_abs_diff"],
        gap_L_last=obs["gap_L"][-1],
        gap_v_last=obs["gap_v"][-1],
        c_fit=ent["c_fit"],
        energy_L=json.dumps(solver["L"]),
        energy_ed=json.dumps(solver["ed"]),
        energy_bethe=json.dumps(solver["bethe"]),
        energy_dmrg=json.dumps(solver["dmrg"]),
        gap_L=json.dumps(obs["gap_L"]),
        gap_v=json.dumps(obs["gap_v"]),
        ell=json.dumps(ent["ell"]),
        entropy=json.dumps(ent["s"]),
        decay_r=json.dumps(ent["gapless_r"]),
        gapless_v=json.dumps(ent["gapless_v"]),
        gapped_v=json.dumps(ent["gapped_v"]),
    )

    out = ROOT / "reports" / "dashboard.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
