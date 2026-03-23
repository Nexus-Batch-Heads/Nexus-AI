/* ================================================
   NEXUS — Interactive Script
   Backend: Flask API (served from same origin)
================================================ */

const BACKEND_URL = '/api';

// --- Backend status check ---
async function checkBackendStatus() {
  try {
    const res = await fetch(`${BACKEND_URL}/health`);
    if (res.ok) {
      document.querySelectorAll('.backend-status').forEach(el => {
        el.classList.remove('status-offline');
        el.classList.add('status-online');
        el.title = 'Backend Connected';
      });
    }
  } catch (_) {
    document.querySelectorAll('.backend-status').forEach(el => {
      el.classList.add('status-offline');
      el.title = 'Backend Offline — using local fallback';
    });
  }
}
checkBackendStatus();

// --- Navbar scroll effect ---
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 40) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
}, { passive: true });

// --- Smooth anchor scroll ---
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// --- Scenario switcher ---
const scenarioData = {
  career: {
    question: 'Switching from software engineering to product management at a mid-size startup.',
    params: [
      { label: 'Current Experience', value: '5 years' },
      { label: 'Risk Tolerance', value: 'Moderate-High' },
      { label: 'Financial Runway', value: '8 months' }
    ],
    pathA: {
      label: 'Growth Trajectory',
      prob: '62% probability',
      timeline: [
        { time: '0–6 months', event: 'Onboarding friction, salary dip of ~15%' },
        { time: '6–18 months', event: 'Product ownership, skill acceleration' },
        { time: '18–36 months', event: 'Senior PM role, 40% comp recovery' }
      ],
      income: '+28% in 3 years',
      satisfaction: 'High',
      incomeClass: 'positive',
      satClass: 'positive'
    },
    pathB: {
      label: 'Friction Scenario',
      prob: '38% probability',
      timeline: [
        { time: '0–6 months', event: 'Role mismatch, knowledge gaps surface' },
        { time: '6–12 months', event: 'Performance review pressure, burnout risk' },
        { time: '12–18 months', event: 'Pivot back to engineering or restart search' }
      ],
      income: '-12% over 18 months',
      satisfaction: 'Low–Medium',
      incomeClass: 'negative',
      satClass: 'negative'
    },
    rec: 'Based on your profile, transitioning is advisable if you complete a product management course within 3 months of starting. Building technical PM credibility first reduces your risk scenario probability from 38% to 19%.',
    tags: ['PM Certification', 'Side Project Validation', 'Network Building']
  },
  startup: {
    question: 'Leaving a stable corporate job to launch a SaaS product in the EdTech space.',
    params: [
      { label: 'Savings Runway', value: '14 months' },
      { label: 'Risk Tolerance', value: 'High' },
      { label: 'Market Research', value: 'Moderate' }
    ],
    pathA: {
      label: 'Traction Path',
      prob: '55% probability',
      timeline: [
        { time: '0–3 months', event: 'MVP built, initial user testing complete' },
        { time: '3–9 months', event: 'First 100 paying customers, product-market fit signals' },
        { time: '9–24 months', event: 'Seed funding secured, team expansion' }
      ],
      income: 'Variable, +200% potential upside',
      satisfaction: 'Very High',
      incomeClass: 'positive',
      satClass: 'positive'
    },
    pathB: {
      label: 'Stall Scenario',
      prob: '45% probability',
      timeline: [
        { time: '0–6 months', event: 'Product development delays, budget overrun' },
        { time: '6–12 months', event: 'Low acquisition, churn above threshold' },
        { time: '12–18 months', event: 'Runway exhausted, return to employment' }
      ],
      income: '-40% over 18 months',
      satisfaction: 'Low',
      incomeClass: 'negative',
      satClass: 'negative'
    },
    rec: 'Validate with a minimum of 20 paying customers before resigning. A side-launch approach for 3 months reduces failure probability from 45% to 26% while preserving income stability.',
    tags: ['Customer Discovery', 'Side Launch First', 'Find Co-Founder']
  },
  relocation: {
    question: 'Relocating from Pune to Bangalore for a senior role at a Series B tech company.',
    params: [
      { label: 'Cost of Living Delta', value: '+35%' },
      { label: 'Career Level', value: 'Senior' },
      { label: 'Network in City', value: 'Low' }
    ],
    pathA: {
      label: 'Opportunity Path',
      prob: '70% probability',
      timeline: [
        { time: '0–3 months', event: 'Settling-in costs, social friction period' },
        { time: '3–12 months', event: 'Accelerated career growth, new network built' },
        { time: '12–30 months', event: 'Leadership visibility, 35–50% comp growth' }
      ],
      income: '+38% in 2.5 years',
      satisfaction: 'High',
      incomeClass: 'positive',
      satClass: 'positive'
    },
    pathB: {
      label: 'Isolation Risk',
      prob: '30% probability',
      timeline: [
        { time: '0–6 months', event: 'Higher cost of living erodes net savings' },
        { time: '6–12 months', event: 'Social isolation impacts performance' },
        { time: '12–18 months', event: 'Return relocation or role misalignment' }
      ],
      income: 'Neutral over 18 months',
      satisfaction: 'Medium',
      incomeClass: 'positive',
      satClass: 'negative'
    },
    rec: 'The move is strongly recommended given your career stage. Establish housing near a professional community hub and plan for at least two in-person networking events per month in the first quarter.',
    tags: ['Community Hub Living', 'Early Networking', 'Cost Buffer Planning']
  },
  investment: {
    question: 'Allocating 30% of liquid savings into a diversified equity + mutual fund portfolio over 5 years.',
    params: [
      { label: 'Horizon', value: '5 years' },
      { label: 'Risk Profile', value: 'Moderate' },
      { label: 'Current Portfolio', value: 'Fixed deposits' }
    ],
    pathA: {
      label: 'Growth Scenario',
      prob: '68% probability',
      timeline: [
        { time: '0–12 months', event: 'Portfolio establishment, 8–10% annualized returns' },
        { time: '1–3 years', event: 'Compounding effect, mid-cap exposure smooths volatility' },
        { time: '3–5 years', event: 'Target corpus reached, 2.1x capital growth' }
      ],
      income: '+2.1x in 5 years',
      satisfaction: 'High',
      incomeClass: 'positive',
      satClass: 'positive'
    },
    pathB: {
      label: 'Volatility Scenario',
      prob: '32% probability',
      timeline: [
        { time: '0–12 months', event: 'Market correction, -20% paper loss' },
        { time: '1–2 years', event: 'Panic exit triggers realized losses' },
        { time: '2–5 years', event: 'Missed recovery, 1.1x only vs 2.1x potential' }
      ],
      income: '1.1x over 5 years',
      satisfaction: 'Low',
      incomeClass: 'negative',
      satClass: 'negative'
    },
    rec: 'SIP-based monthly allocation over lump sum reduces timing risk by 44%. Avoid reviewing portfolio more than once per month. Combined large-cap + index fund allocation outperforms pure active managed in this profile.',
    tags: ['SIP Strategy', 'Index Fund Allocation', 'Annual Rebalancing']
  }
};

function setScenario(btn, key) {
  document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const d = scenarioData[key];
  if (!d) return;

  document.querySelector('.sim-detail-question').textContent = d.question;

  const paramEls = document.querySelectorAll('.sim-param label');
  paramEls.forEach((el, i) => {
    if (d.params[i]) el.textContent = d.params[i].label;
  });

  const spanEls = document.querySelectorAll('.param-slider span');
  spanEls.forEach((el, i) => {
    if (d.params[i]) el.textContent = d.params[i].value;
  });

  updateSimResults(d);
}

function updateSimResults(d) {
  const results = document.getElementById('sim-results');

  const buildTimeline = (path) => path.timeline.map(t => `
    <div class="timeline-item">
      <div class="tl-dot ${path.incomeClass === 'positive' ? 'dot-success' : 'dot-warn'}"></div>
      <div class="tl-content">
        <span class="tl-time">${t.time}</span>
        <span class="tl-event">${t.event}</span>
      </div>
    </div>`).join('');

  results.innerHTML = `
    <div class="sim-paths">
      <div class="path-card path-green">
        <div class="path-header">
          <div class="path-label">Path A — Optimal</div>
          <div class="path-prob">${d.pathA.prob}</div>
        </div>
        <div class="path-title">${d.pathA.label}</div>
        <div class="path-timeline">${buildTimeline(d.pathA)}</div>
        <div class="path-outcome">
          <div class="outcome-item">
            <span>Income Impact</span>
            <span class="outcome-val ${d.pathA.incomeClass}">${d.pathA.income}</span>
          </div>
          <div class="outcome-item">
            <span>Career Satisfaction</span>
            <span class="outcome-val ${d.pathA.satClass}">${d.pathA.satisfaction}</span>
          </div>
        </div>
      </div>
      <div class="path-card path-red">
        <div class="path-header">
          <div class="path-label">Path B — Risk</div>
          <div class="path-prob">${d.pathB.prob}</div>
        </div>
        <div class="path-title">${d.pathB.label}</div>
        <div class="path-timeline">${buildTimeline(d.pathB)}</div>
        <div class="path-outcome">
          <div class="outcome-item">
            <span>Income Impact</span>
            <span class="outcome-val ${d.pathB.incomeClass}">${d.pathB.income}</span>
          </div>
          <div class="outcome-item">
            <span>Career Satisfaction</span>
            <span class="outcome-val ${d.pathB.satClass}">${d.pathB.satisfaction}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="sim-recommendation">
      <div class="rec-title">AI Recommendation</div>
      <p class="rec-body">${d.rec}</p>
      <div class="rec-actions">
        ${d.tags.map(t => `<span class="rec-action-tag">${t}</span>`).join('')}
      </div>
    </div>`;
}

async function runSimulation() {
  const btn = document.querySelector('.btn-full');
  const original = btn.textContent;
  btn.textContent = 'Simulating...';
  btn.style.opacity = '0.7';
  btn.style.pointerEvents = 'none';

  // Determine active scenario
  const activeBtn = document.querySelector('.scenario-btn.active');
  const scenarioKey = activeBtn ? activeBtn.getAttribute('onclick').match(/'(\w+)'/)?.[1] || 'career' : 'career';

  // Read slider values
  const sliders = document.querySelectorAll('.slider');
  const params = {
    experience:       parseInt(sliders[0]?.value || 5),
    risk_tolerance:   parseInt(sliders[1]?.value || 5),
    financial_runway: parseInt(sliders[2]?.value || 5),
  };

  try {
    const res = await fetch(`${BACKEND_URL}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario: scenarioKey, params }),
    });

    if (!res.ok) throw new Error('Backend error');
    const data = await res.json();

    // Map backend response to the existing renderer
    const mapped = {
      question: data.question,
      params: [
        { label: 'Experience Level',  value: params.experience + '/10' },
        { label: 'Risk Tolerance',    value: params.risk_tolerance + '/10' },
        { label: 'Financial Runway',  value: params.financial_runway + '/10' },
      ],
      pathA: {
        label: data.pathA.label,
        prob:  data.pathA.prob,
        timeline: data.pathA.timeline,
        income:   data.pathA.income,
        satisfaction: data.pathA.satisfaction,
        incomeClass:  data.pathA.incomeClass,
        satClass:     data.pathA.satClass,
      },
      pathB: {
        label: data.pathB.label,
        prob:  data.pathB.prob,
        timeline: data.pathB.timeline,
        income:   data.pathB.income,
        satisfaction: data.pathB.satisfaction,
        incomeClass:  data.pathB.incomeClass,
        satClass:     data.pathB.satClass,
      },
      rec:  data.recommendation,
      tags: data.tags,
    };
    updateSimResults(mapped);

  } catch (err) {
    // Fallback to local data if backend is not reachable
    const localKey = document.querySelector('.scenario-btn.active')
      ?.getAttribute('onclick')?.match(/'(\w+)'/)?.[1] || 'career';
    const d = scenarioData[localKey];
    if (d) updateSimResults(d);
  }

  btn.textContent = 'Simulation Complete';
  btn.style.opacity = '1';

  const rec = document.querySelector('.sim-recommendation');
  if (rec) {
    rec.style.animation = 'none';
    rec.offsetHeight;
    rec.style.animation = 'slideIn 0.5s ease-out';
  }

  setTimeout(() => {
    btn.textContent = original;
    btn.style.pointerEvents = 'auto';
  }, 2000);
}

// --- Demo twin response map ---
const twinResponses = [
  {
    keywords: ['meeting', 'call', 'join', 'sync'],
    fn: (msg) => `Will be there. Send the agenda beforehand — want to be prepared on the key discussion points before we get into it.`
  },
  {
    keywords: ['review', 'pr', 'pull', 'code', 'feedback'],
    fn: (msg) => `On my list. Any specific sections you want me to focus on, or a full review? Also flagging any test coverage gaps if found.`
  },
  {
    keywords: ['deadline', 'deadline', 'urgent', 'asap', 'today', 'eod'],
    fn: (msg) => `Noted. What's the actual hard deadline — end of business or earlier? I'll reprioritize accordingly and flag if I need to drop something else.`
  },
  {
    keywords: ['help', 'stuck', 'issue', 'problem', 'bug', 'error'],
    fn: (msg) => `Share the error log or screenshot and I'll take a look. Also let me know which environment this is happening in — staging or prod?`
  },
  {
    keywords: ['plan', 'proposal', 'doc', 'document', 'spec', 'design'],
    fn: (msg) => `Send it over. I'll go through it and leave comments inline rather than a separate doc — easier to track that way.`
  },
  {
    keywords: ['update', 'status', 'progress', 'done', 'finished', 'complete'],
    fn: (msg) => `Almost there. Should have it wrapped up within the hour. Will ping you once it's done with a summary of what changed.`
  },
  {
    keywords: ['question', 'ask', 'wondering', 'thoughts', 'opinion', 'think'],
    fn: (msg) => `Depends on a few things — share the full context and I'll give you a proper answer rather than a half-informed one.`
  }
];

const fallbackResponses = [
  `Received. I'll get back to you with a clearer answer once I've had a chance to look into it. Give me 30 minutes.`,
  `Understood. I'll handle it — will update you once there's something concrete to share.`,
  `On it. Let me check on this and follow up shortly. Don't block on me if there's a parallel track you can take.`,
  `Noted. I'll take a look and respond with specifics rather than a generic answer — just give me a bit.`
];

function getTwinResponse(input) {
  const lower = input.toLowerCase();
  for (const rule of twinResponses) {
    if (rule.keywords.some(k => lower.includes(k))) {
      return rule.fn(input);
    }
  }
  return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
}

async function sendDemoMessage() {
  const input = document.getElementById('demo-input');
  const area  = document.getElementById('messages-area');
  const text  = input.value.trim();
  if (!text) return;

  // Render incoming message
  const inGroup = document.createElement('div');
  inGroup.className = 'msg-group';
  inGroup.innerHTML = `
    <div class="msg-label">Incoming Message</div>
    <div class="msg-bubble msg-in">${escapeHtml(text)}</div>`;
  area.appendChild(inGroup);

  // Typing indicator
  const typingGroup = document.createElement('div');
  typingGroup.className = 'msg-group';
  typingGroup.innerHTML = `
    <div class="msg-label">AI Twin <span class="generated-tag">Thinking</span></div>
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>`;
  area.appendChild(typingGroup);
  area.scrollTop = area.scrollHeight;
  input.value = '';

  let response, confidence = 94, latency = 420, source = 'rule-based';

  try {
    const res = await fetch(`${BACKEND_URL}/twin/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    if (!res.ok) throw new Error('Backend error');
    const data = await res.json();
    response   = data.response;
    confidence = data.confidence;
    latency    = data.latency_ms;
    source     = data.source;
  } catch (_) {
    // Fallback to local rule-based response if backend is unreachable
    response = getTwinResponse(text);
  }

  area.removeChild(typingGroup);

  const outGroup = document.createElement('div');
  outGroup.className = 'msg-group';
  outGroup.innerHTML = `
    <div class="msg-label">AI Twin Response <span class="generated-tag">AI</span></div>
    <div class="msg-bubble msg-out">${escapeHtml(response)}</div>
    <div class="twin-confidence" style="margin-top:8px">
      <span class="conf-label">Style Confidence</span>
      <div class="conf-bar"><div class="conf-fill" style="width:${confidence}%"></div></div>
      <span class="conf-pct">${confidence}%</span>
    </div>`;
  area.appendChild(outGroup);
  area.scrollTop = area.scrollHeight;

  // Update sidebar live stats
  const latencyEl = document.getElementById('last-latency');
  if (latencyEl) latencyEl.textContent = latency > 0 ? `${(latency/1000).toFixed(1)}s` : '< 1s';

  const apiLatencyEl = document.getElementById('api-latency');
  if (apiLatencyEl) apiLatencyEl.textContent = `Last: ${latency > 0 ? (latency/1000).toFixed(2) + 's' : '< 1s'} · ${source === 'ai' ? 'g4f AI' : 'Local Model'}`;

  const countEl = document.getElementById('msg-count');
  if (countEl) {
    const cur = parseInt(countEl.textContent.replace(/,/g, '')) || 4218;
    countEl.textContent = (cur + 1).toLocaleString();
  }
}

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// Enter key submit
document.getElementById('demo-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') sendDemoMessage();
});

// --- Intersection Observer for fade-in ---
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.feature-card, .step, .path-card, .twin-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease, border-color 0.3s ease, box-shadow 0.3s ease';
  observer.observe(el);
});

// --- Slider value label update ---
document.querySelectorAll('.slider').forEach((slider, i) => {
  slider.addEventListener('input', () => {
    const span = slider.parentElement.querySelector('span');
    const labels = [
      ['1 year', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', '8 years', '9 years', '10 years'],
      ['Very Low', 'Low', 'Low-Moderate', 'Moderate', 'Moderate', 'Moderate-High', 'High', 'High', 'Very High', 'Very High'],
      ['2 months', '3 months', '4 months', '6 months', '8 months', '10 months', '12 months', '14 months', '18 months', '24 months']
    ];
    if (labels[i] && span) {
      span.textContent = labels[i][parseInt(slider.value) - 1];
    }
  });
});
