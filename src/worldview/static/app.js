const domainFilter = document.getElementById('domainFilter');
const freeFilter = document.getElementById('freeFilter');
const refreshBtn = document.getElementById('refreshBtn');
const providersPills = document.getElementById('providersTableBody');
const telemetryBody = document.getElementById('telemetryTableBody');
const envVars = document.getElementById('envVars');
const stats = document.getElementById('stats');
const recordsEl = document.getElementById('records');
const layersEl = document.getElementById('layers');
const synthForm = document.getElementById('synthForm');
const synthResult = document.getElementById('synthResult');
const modeBtns = document.querySelectorAll('.mode-btn');
const telemetryCloud = document.getElementById('telemetryCloud');
const mgrsValue = document.getElementById('mgrsValue');
const latlonValue = document.getElementById('latlonValue');
const clockEl = document.getElementById('clock');

let activeMode = 'recorded';
let ws;

function setClock() {
  clockEl.textContent = new Date().toISOString();
}
setInterval(setClock, 1000);
setClock();

function setDomainOptions(domains) {
  const current = domainFilter.value;
  const entries = Object.keys(domains);
  domainFilter.innerHTML = '<option value="">All</option>' + entries.map((d) => `<option value="${d}">${d}</option>`).join('');
  domainFilter.value = current;
}

function renderStats(domainSummary) {
  stats.innerHTML = domainSummary.items
    .map((item) => `<span class="pill">${item.domain}: ${item.total} (${item.free_tier} free)</span>`)
    .join('');
}

function renderProviderPills(providers) {
  providersPills.innerHTML = providers
    .slice(0, 30)
    .map((p) => `<span class="pill">${p.name}</span>`)
    .join('');
}

function mgrsFromPoint(p) {
  return `${Math.abs(Math.floor(p.lat * 10)).toString().padStart(3, '0')}${p.lat >= 0 ? 'N' : 'S'} ${Math.abs(Math.floor(p.lon * 10)).toString().padStart(4, '0')}`;
}

function renderTelemetry(points) {
  telemetryBody.innerHTML = points
    .slice(0, 40)
    .map(
      (p) => `<tr>
      <td>${p.asset_id}</td>
      <td>${p.domain}</td>
      <td>${mgrsFromPoint(p)}</td>
    </tr>`
    )
    .join('');

  telemetryCloud.innerHTML = points
    .slice(0, 140)
    .map((p) => {
      const x = ((p.lon + 180) / 360) * 100;
      const y = (1 - (p.lat + 90) / 180) * 100;
      const cls = p.domain === 'gps_jam' || p.domain === 'military' ? 'ping red' : 'ping';
      return `<span class="${cls}" style="left:${x}%;top:${y}%;"></span>`;
    })
    .join('');

  const first = points[0];
  if (first) {
    mgrsValue.textContent = mgrsFromPoint(first);
    latlonValue.textContent = `${first.lat.toFixed(4)}°, ${first.lon.toFixed(4)}°`;
  }
}

function renderRecords(records) {
  recordsEl.innerHTML = records
    .map(
      (r) => `<div class="record"><strong>${r.title}</strong><br/>risk: ${r.risk_score}<br/>${r.summary}</div>`
    )
    .join('');
}

function renderLayers(config) {
  layersEl.innerHTML = config.layers
    .map((l) => `<div class="layer-card">${l.enabled ? '🟢' : '⚪'} ${l.label}<br/><small>${l.domain}</small></div>`)
    .join('');
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}

async function loadProviders() {
  const params = new URLSearchParams();
  if (domainFilter.value) params.append('domain', domainFilter.value);
  if (freeFilter.value) params.append('free_tier', freeFilter.value);
  const providersResp = await fetchJson(`/api/v1/providers?${params}`);
  setDomainOptions(providersResp.domains);
  renderProviderPills(providersResp.providers);
}

async function loadPlaybackTelemetry() {
  const defaults = await fetchJson('/api/v1/telemetry/default-window');
  const body = {
    ...defaults,
    domains: domainFilter.value ? [domainFilter.value] : defaults.domains,
  };
  const playback = await fetchJson('/api/v1/telemetry/playback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  renderTelemetry(playback.points);
}

function startLiveStream() {
  if (ws) ws.close();
  ws = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/api/v1/ws/live`);
  ws.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    renderTelemetry(payload.points);
  };
}

async function loadDashboard() {
  const [keysResp, domainSummary, featuresResp, recordsResp] = await Promise.all([
    fetchJson('/api/v1/providers/required-keys'),
    fetchJson('/api/v1/domains/summary'),
    fetchJson('/api/v1/features'),
    fetchJson('/api/v1/intelligence/records'),
  ]);

  await loadProviders();
  envVars.textContent = keysResp.env_vars.join('\n');
  renderStats(domainSummary);
  renderLayers(featuresResp);
  renderRecords(recordsResp);

  if (activeMode === 'live') {
    startLiveStream();
  } else {
    if (ws) ws.close();
    await loadPlaybackTelemetry();
  }
}

modeBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    modeBtns.forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    activeMode = btn.dataset.mode;
    loadDashboard();
  });
});

refreshBtn.addEventListener('click', loadDashboard);

domainFilter.addEventListener('change', loadDashboard);
freeFilter.addEventListener('change', loadDashboard);

synthForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    title: document.getElementById('synthTitle').value,
    source_url: document.getElementById('synthUrl').value,
    body: document.getElementById('synthBody').value,
  };
  const result = await fetchJson('/api/v1/intelligence/synthesize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  synthResult.textContent = JSON.stringify(result, null, 2);
});

window.addEventListener('DOMContentLoaded', loadDashboard);
