async function fetchJSON(url, opts){
  const res = await fetch(url, opts)
  if(!res.ok) throw new Error(`HTTP ${res.status}`)
  return await res.json()
}

function formatCurrencyBRL(value){
  try{
    return new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(value||0)
  }catch{ return `${value}` }
}

function setClock(){
  const now = new Date()
  const time = now.toLocaleTimeString('pt-BR',{hour12:false})
  const date = now.toLocaleDateString('pt-BR')
  document.getElementById('clock-time').textContent = time
  document.getElementById('clock-date').textContent = date
}
setInterval(setClock, 1000); setClock()

let revenueChart
async function renderRevenueChart(series){
  const ctx = document.getElementById('chart-revenue')
  if(!ctx) return
  const labels = (series||[]).map(p=>p.period)
  const values = (series||[]).map(p=>p.value)
  if(revenueChart){ revenueChart.destroy() }
  revenueChart = new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: 'Receita', data: values, borderColor: '#22d3ee', backgroundColor: 'rgba(34,211,238,.15)', tension: .25, fill: true }]},
    options: { plugins: { legend: { display: false }}, scales: { x: { ticks: { color: '#94a3b8'}}, y: { ticks: { color: '#94a3b8'}}}}
  })
}

async function loadOverview(){
  try{
    const period = document.getElementById('filter-period')?.value || '12m'
    const data = await fetchJSON(`/api/overview?period=${encodeURIComponent(period)}`)
    const leadsHoje = data.leads_novos?.hoje ?? 0
    document.getElementById('kpi-leads').textContent = leadsHoje
    document.getElementById('kpi-leads-meta').textContent = `${data.leads_novos?.hoje||0} / ${data.leads_novos?.semana||0} / ${data.leads_novos?.mes||0}`
    document.getElementById('kpi-processos').textContent = data.processos_novos ?? 0
    document.getElementById('kpi-prazos').textContent = data.prazos_criticos ?? 0
    document.getElementById('kpi-docs').textContent = data.documentos_pendentes ?? 0
    document.getElementById('kpi-faturamento').textContent = formatCurrencyBRL(data.faturamento_previsto || 0)
    document.getElementById('kpi-servicos').textContent = data.servicos_pm2_ativos ?? 0
    document.getElementById('kpi-alertas').textContent = (data.alertas_risco||[]).length
    await renderRevenueChart(data.revenue_series || [])
  }catch(e){ console.error('overview', e) }
}

async function loadServices(){
  try{
    const services = await fetchJSON('/api/services')
    const online = services.filter(s=>s.status==='online').length
    document.getElementById('services-count').textContent = online
    const statusDot = document.getElementById('server-status')
    statusDot.classList.remove('yellow','red'); statusDot.classList.add('green')
  }catch(e){
    const statusDot = document.getElementById('server-status')
    statusDot.classList.remove('green','yellow'); statusDot.classList.add('red')
  }
}

async function loadNotifications(){
  try{
    const data = await fetchJSON('/api/notifications')
    const wrap = document.getElementById('notifications')
    wrap.innerHTML = ''
    for(const n of data.items||[]){
      const div = document.createElement('div')
      div.className = `notice ${n.severity||''}`
      div.textContent = n.message
      wrap.appendChild(div)
    }
  }catch(e){ /* ignore */ }
}

async function showModule(key){
  const target = document.getElementById('module-details')
  target.classList.remove('hidden')
  target.innerHTML = 'Carregando...'
  try{
    const data = await fetchJSON(`/api/modules/${encodeURIComponent(key)}`)
    const metrics = data.metrics || {}
    target.innerHTML = `<h3>${key.toUpperCase()}</h3><pre>${JSON.stringify(metrics,null,2)}</pre>`
  }catch(e){
    target.innerHTML = 'Falha ao carregar módulo'
  }
}

function bindModules(){
  document.querySelectorAll('.widget[data-module]').forEach(btn=>{
    btn.addEventListener('click', ()=> showModule(btn.dataset.module))
  })
}

async function performAction(action){
  try{
    const res = await fetchJSON(`/api/actions/${encodeURIComponent(action)}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({source:'dashboard'})})
    toast(`Ação "${action}" executada`) 
  }catch(e){ toast('Falha na ação', true) }
}

function bindActions(){
  document.querySelectorAll('.actions .btn').forEach(btn=>{
    btn.addEventListener('click', ()=> performAction(btn.dataset.action))
  })
}

function toast(message, error){
  const t = document.getElementById('toast')
  t.textContent = message
  t.style.borderColor = error ? 'var(--red)' : 'var(--accent)'
  t.classList.remove('hidden')
  setTimeout(()=> t.classList.add('hidden'), 2200)
}

function bindSearch(){
  const input = document.getElementById('global-search')
  const results = document.getElementById('search-results')
  let timer
  input.addEventListener('input', ()=>{
    clearTimeout(timer)
    const q = input.value.trim()
    if(!q){ results.classList.add('hidden'); results.innerHTML=''; return }
    timer = setTimeout(async ()=>{
      try{
        const data = await fetchJSON(`/api/search?q=${encodeURIComponent(q)}`)
        const items = []
        if((data.clients||[]).length){
          items.push('<div class="group"><h4>Clientes</h4>' + data.clients.map(c=>`<div class="item">${c.nome} — ${c.email||''}</div>`).join('') + '</div>')
        }
        if((data.processes||[]).length){
          items.push('<div class="group"><h4>Processos</h4>' + data.processes.map(p=>`<div class="item">${p.Numero_Processo||''} — ${p.Cliente||''}</div>`).join('') + '</div>')
        }
        results.innerHTML = items.join('') || '<div class="group"><div class="item">Sem resultados</div></div>'
        results.classList.remove('hidden')
      }catch{ results.classList.add('hidden') }
    }, 250)
  })
}

function bindFilters(){
  const period = document.getElementById('filter-period')
  if(period){ period.addEventListener('change', loadOverview) }
  const tv = document.getElementById('btn-tv')
  if(tv){ tv.addEventListener('click', ()=> document.body.classList.toggle('tv-mode')) }
}

async function loadInsights(){
  try{
    const data = await fetchJSON('/api/insights')
    const wrap = document.getElementById('notifications')
    for(const tip of data.insights||[]){
      const div = document.createElement('div')
      div.className = 'notice info'
      div.textContent = `💡 ${tip}`
      wrap.appendChild(div)
    }
  }catch{}
}

function init(){
  bindModules(); bindActions(); bindSearch(); bindFilters();
  loadOverview(); loadServices(); loadNotifications(); loadInsights();
  setInterval(loadOverview, 20_000)
  setInterval(loadNotifications, 20_000)
}

document.addEventListener('DOMContentLoaded', init)