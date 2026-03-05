const domainFilter = document.getElementById('domainFilter');
const freeFilter = document.getElementById('freeFilter');
const refreshBtn = document.getElementById('refreshBtn');
const providersBody = document.getElementById('providersTableBody');
const envVars = document.getElementById('envVars');
const stats = document.getElementById('stats');

function setDomainOptions(domains) {
  const entries = Object.keys(domains);
  domainFilter.innerHTML = '<option value="">All</option>' +
    entries.map(d => `<option value="${d}">${d}</option>`).join('');
}

function renderStats(domainSummary) {
  stats.innerHTML = domainSummary.items.map(item => `
    <article class="card">
      <strong>${item.domain}</strong><br>
      total: ${item.total}<br>
      free: ${item.free_tier}<br>
      paid: ${item.paid_only}
    </article>
  `).join('');
}

function renderProviders(providers) {
  providersBody.innerHTML = providers.map(p => `
    <tr>
      <td>${p.name}</td>
      <td>${p.domain}</td>
      <td>${p.auth}</td>
      <td>${p.free_tier ? 'Yes' : 'No'}</td>
      <td>${p.env_vars.join(', ') || '-'}</td>
    </tr>
  `).join('');
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

async function loadDashboard() {
  const domain = domainFilter.value;
  const free = freeFilter.value;

  const params = new URLSearchParams();
  if (domain) params.append('domain', domain);
  if (free) params.append('free_tier', free);

  const [providersResp, keysResp, domainSummary] = await Promise.all([
    fetchJson(`/api/v1/providers?${params}`),
    fetchJson('/api/v1/providers/required-keys'),
    fetchJson('/api/v1/domains/summary'),
  ]);

  setDomainOptions(providersResp.domains);
  if (domain) domainFilter.value = domain;
  renderStats(domainSummary);
  renderProviders(providersResp.providers);
  envVars.textContent = keysResp.env_vars.join('\n');
}

refreshBtn.addEventListener('click', loadDashboard);
window.addEventListener('DOMContentLoaded', loadDashboard);
