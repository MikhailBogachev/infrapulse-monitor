"use strict";

const shell = document.querySelector("#shell");
const drawer = document.querySelector("#drawer");
const modal = document.querySelector("#modal");
const demo = document.querySelector("#demo");
const toast = document.querySelector("#toast");
modal.className = demo.className = "dialog-panel";
const paths = {
  pulse: "M2 12h5l3-8 4 16 3-8h5",
  grid: "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
  monitor: "M4 4h16a2 2 0 0 1 2 2v11H2V6a2 2 0 0 1 2-2ZM8 21h8m-4-4v4",
  triangle: "M10.3 4.9 2.5 18a2 2 0 0 0 1.7 3h15.6a2 2 0 0 0 1.7-3L13.7 4.9a2 2 0 0 0-3.4 0ZM12 9v4m0 4h.01",
  bell: "M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9m-8 12a2 2 0 0 0 4 0",
  user: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z",
  settings: "M4 7h16M4 12h16M4 17h16M8 5v4m8 1v4m-6 1v4",
  check: "m5 12 4 4L19 6",
  circle: "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0Z",
  clock: "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0ZM12 6v6l4 2",
  pause: "M9 5H6v14h3zm9 0h-3v14h3z",
  play: "m7 4 14 8-14 8z",
  x: "m18 6-12 12M6 6l12 12",
  plus: "M12 5v14M5 12h14",
  refresh: "M20 7v5h-5M4 17v-5h5m-4.5-1a8 8 0 0 1 14-4L20 12M4 12l1.5 5a8 8 0 0 0 14-4",
  menu: "M4 6h16M4 12h16M4 18h16",
  right: "m9 18 6-6-6-6",
  arrow: "M5 12h14m-7-7 7 7-7 7",
  back: "M19 12H5m7-7-7 7 7 7",
  box: "m12 3 9 5v8l-9 5-9-5V8zm-9 5 9 5 9-5m-9 5v8",
  edit: "m13 6 5 5M4 20l5-1L21 7l-5-5L4 14z",
  logout: "M10 17l5-5-5-5m5 5H3m9-8h8v16h-8",
};
const statuses = {
  UP: ["ok", "check"], DOWN: ["bad", "triangle"],
  PENDING: ["warn", "clock"], PAUSED: ["neutral", "pause"],
};
const closeReasons = {
  RECOVERED: "Recovered", CONFIGURATION_CHANGED: "Configuration changed", MONITOR_DELETED: "Monitor deleted",
};
const outcomes = {
  SUCCESS: "Success", FAILURE: "Target failure", TIMEOUT: "Target timeout",
  ERROR: "Internal error", SKIPPED: "Skipped", INTERRUPTED: "Interrupted",
};
const windows = { "24h": 1, "7d": 7, "30d": 30 };
const day = 86400000;
const fixtureOwner = "owner@example.com";
const pollingScreens = new Set(["overview", "monitors", "monitor", "incidents", "incident", "notifications"]);
const now = () => Date.now();
const newSession = (generation = 0) => ({ generation: generation + 1, accessUntil: now() + 15 * 60000, renewalUntil: now() + 7 * day });
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[char]);
const glyph = (name) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"
  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${paths[name]}"/></svg>`;
const iso = (value) => new Date(value).toISOString();
const dateText = (value) => iso(value).slice(0, 16).replace("T", " ");
const stamp = (value) => value ? `<time datetime="${iso(value)}">${dateText(value)} UTC</time>` : "—";
const clockText = (value) => iso(value).slice(11, 19);
const brand = () => `<div class="brand"><span class="logo">${glyph("pulse")}</span>InfraPulse</div>`;
const pill = (label, tone, icon) => `<span class="pill ${tone}">${glyph(icon)}${escapeHtml(label)}</span>`;
const status = (name) => pill(name, ...statuses[name]);
const selected = (actual, value) => actual === value ? " selected" : "";
const checked = (value) => value ? " checked" : "";
const href = (route) => `#/${route}`;
const link = (route, label, icon, css = "") => `<a href="${href(route)}"${css ? ` class="${css}"` : ""}>${icon ? glyph(icon) : ""}${escapeHtml(label)}</a>`;
const button = (action, label, icon, css = "", attrs = "") =>
  `<button type="button" class="btn ${css}" data-action="${action}" ${attrs}>${icon ? glyph(icon) : ""}${escapeHtml(label)}</button>`;

function fixture() {
  const time = now();
  const monitors = [
    ["edge", "Edge API", "api.example.com/health", "UP", 60],
    ["web", "Public Website", "www.example.com", "UP", 60],
    ["auth", "Identity Gateway", "identity.example.com/health", "UP", 120],
    ["payments", "Payments API", "payments.example.com/health", "DOWN", 60],
    ["assets", "Asset CDN", "assets.example.com", "UP", 120],
    ["worker", "Background Workers", "jobs.example.com/health", "PAUSED", 120],
    ["search", "Search API", "search.example.com/health", "PENDING", 300],
  ].map(([id, name, target, state, interval], index) => {
    const observations = [];
    const samples = id === "worker" ? 0 : id === "search" ? 0 : 150;
    for (let i = 0; i < samples; i++) {
      if (i >= 8 && i <= 13) continue;
      const age = i < 36 ? (i + 1) * 2280000 : 1.1 * day + (i - 36) * day * .245;
      const outcome = id === "payments" && i < 3 ? "FAILURE" :
        i === 18 ? "ERROR" : i === 22 ? "TIMEOUT" : i === 40 ? "FAILURE" : "SUCCESS";
      const ms = 90 + index * 21 + Math.round(29 * Math.sin(i * 1.8) + 24 * Math.cos(i * .51) + (i % 9) * 8);
      observations.push({ at: time - age, origin: "Scheduled", outcome, ms: outcome === "SUCCESS" ? ms : null });
    }
    if (id === "payments") {
      const opening = time - 19 * 60000;
      observations.unshift(...[0, 1, 2].map((i) => ({ at: opening - i * 60000, origin: "Scheduled", outcome: "FAILURE", ms: null })));
    }
    return {
      id, name, url: `https://${target}`, state, interval, timeout: 10, method: id === "assets" ? "HEAD" : "GET",
      failure: 3, recovery: 2, version: 1, failures: 0, successes: 0, observations,
      due: state === "PAUSED" ? null : time + interval * 1000, manual: null, accepted: 0,
      pauses: state === "PAUSED" ? [{ start: time - 2 * day, end: null }] : [],
    };
  });
  const incidents = [
    { id: "inc-104", monitor: "payments", name: "Payments API", origin: "https://payments.example.com", opened: time - 19 * 60000, closed: null },
    { id: "inc-103", monitor: "edge", name: "Edge API", origin: "https://api.example.com", opened: time - 3 * day, closed: time - 3 * day + 12 * 60000, reason: "RECOVERED" },
  ];
  return {
    accounts: { [fixtureOwner]: { email: fixtureOwner, name: "Production", created: time - 45 * day, monitors, incidents,
      channel: { configured: true, enabled: true, opened: true, resolved: true },
      deliveries: [
        { incident: "inc-104", event: "Incident opened", status: "UNKNOWN", attempts: 1, at: incidents[0].opened + 2000 },
        { incident: "inc-103", event: "Incident resolved", status: "FAILED", attempts: 3, at: incidents[1].closed + 2000 },
      ] } },
    initialized: true, registration: false, identity: fixtureOwner, session: newSession(), sequence: 200,
  };
}

let data = fixture();
let current = { name: "overview" };
let view = {};
let transport = "connected";
let pendingRefresh = 0;
let lastSuccess = null;
let refreshError = false;
let liveUpdates = true;
let renderedAt = null;
let toastTimer;
let returnRoute = "overview";
let confirmation = null;
let nextOutcome = null;
const workspace = () => {
  if (readingSnapshot) return snapshot;
  return Object.hasOwn(data.accounts, data.identity) ? data.accounts[data.identity] : null;
};
const ownsMonitor = (id) => workspace()?.monitors.find((monitor) => monitor.id === id);
const ownsIncident = (id) => workspace()?.incidents.find((incident) => incident.id === id);
const activeIncident = (account, id) => account.incidents.find((incident) => incident.monitor === id && !incident.closed);
const nextId = (prefix) => `${prefix}-${++data.sequence}`;
const polling = () => pollingScreens.has(current.name);
const initialView = () => ({ period: "24h", chartMonitor: "", search: "", status: "", incident: "", delivery: "", history: "", limit: 8, deliveryLimit: 8 });

function notify(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toastTimer = setTimeout(() => { toast.textContent = ""; }, 4400);
}

function nav(active) {
  const items = [
    ["overview", "Overview", "grid"], ["monitors", "Monitors", "monitor"], ["incidents", "Incidents", "triangle"],
    ["notifications", "Notifications", "bell"], ["workspace", "Workspace", "settings"], ["account", "Account", "user"],
  ];
  return `<nav class="nav" aria-label="Workspace navigation">${items.map(([route, label, icon], index) =>
    `${index === 0 || index === 3 ? `<div class="nav-label">${index === 0 ? "Monitor" : "Settings"}</div>` : ""}
    <a href="${href(route)}"${route === active ? ` aria-current="${route === current.name ? "page" : "location"}"` : ""}>${glyph(icon)}${label}</a>`).join("")}</nav>`;
}

function sideContent(active, mobile = false) {
  return `<div class="side-content">${mobile
    ? `<div class="page-head"><div id="drawer-title">${brand()}</div>${button("close-dialog", "", "x", "icon ghost", 'aria-label="Close navigation" autofocus')}</div>` : brand()}
    <a class="workspace" href="${href("workspace")}"><span class="avatar" aria-hidden="true">${escapeHtml(workspace().name.slice(0, 2).toUpperCase())}</span>
      <span class="workspace-text"><span class="break">${escapeHtml(workspace().name)}</span><span class="small muted">Owner workspace</span></span>${glyph("right")}</a>
    ${nav(active)}<div class="side-footer">${button("demo", "Prototype / Demo Data", "box", "ghost")}</div></div>`;
}

const pageLabels = {
  overview: "Overview", monitors: "Monitors", create: "New monitor", edit: "Edit monitor", monitor: "Monitor details",
  incidents: "Incidents", incident: "Incident details", account: "Account settings", workspace: "Workspace settings",
  notifications: "Notification settings", missing: "Access unavailable",
};

function renderShell(content) {
  const active = ["monitor", "create", "edit"].includes(current.name) ? "monitors" : current.name === "incident" ? "incidents" : current.name;
  shell.innerHTML = `<div class="layout"><aside class="sidebar">${sideContent(active)}</aside><div>
    <header class="topbar"><div class="top-context">${button("drawer", "", "menu", "icon mobile-only ghost", 'aria-label="Open navigation" aria-haspopup="dialog"')}
      <span class="workspace-crumb muted">${escapeHtml(workspace().name)}</span><span class="crumb-divider muted" aria-hidden="true">/</span>
      <span>${pageLabels[current.name]}</span></div>
      <div class="top-actions">${polling() ? button("refresh", "", "refresh", "icon ghost", 'id="refresh" aria-label="Refresh data" title="Refresh data"') : ""}
        <a class="top-account" href="${href("account")}" aria-label="Account settings"><span class="avatar" aria-hidden="true">${escapeHtml(workspace().email.slice(0, 2).toUpperCase())}</span></a>
      </div></header><main id="main" class="content stack" tabindex="-1">${content}</main></div></div>`;
  drawer.innerHTML = sideContent(active, true);
}

const head = (title, description, actions = "") => `<header class="page-head"><div class="break"><h1 id="page-title" tabindex="-1">${escapeHtml(title)}</h1>
  ${description ? `<p class="muted break">${escapeHtml(description)}</p>` : ""}</div>${actions ? `<div class="actions">${actions}</div>` : ""}</header>`;
const panel = (title, subtitle, content, actions = "") => `<section class="panel page-segment"><div class="panel-head"><div><h2>${escapeHtml(title)}</h2>
  ${subtitle ? `<p class="help">${escapeHtml(subtitle)}</p>` : ""}</div>${actions}</div>${content}</section>`;
const blank = (title, detail, action = "", icon = "box") => `<div class="empty">${glyph(icon)}<h3>${escapeHtml(title)}</h3>
  <p class="help">${escapeHtml(detail)}</p>${action}</div>`;
const facts = (items) => `<dl class="data-grid">${items.map(([key, value]) => `<div><dt>${key}</dt><dd>${value}</dd></div>`).join("")}</dl>`;
const metric = (label, value, detail, icon = "pulse") => `<article class="metric"><div class="metric-label">${glyph(icon)}${label}</div>
  <strong class="metric-value${value === "No data" ? " no-data" : ""}">${value}</strong><span class="help">${detail}</span></article>`;
const period = () => `<div class="period" role="group" aria-label="Metric period">${Object.keys(windows).map((key) =>
  button("period", key, null, "compact", `data-window="${key}" aria-pressed="${key === view.period}"`)).join("")}</div>`;
const table = (label, headers, rows, compact = false) => `<div class="table-wrap" tabindex="0" role="region" aria-label="${label}">
  <table aria-label="${label}"${compact ? ' class="compact-table"' : ""}><thead><tr>${headers.map((header) => `<th scope="col">${header}</th>`).join("")}</tr></thead>
  <tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
const pollChrome = () => `<div class="poll-tools"><div id="freshness" class="freshness small muted"></div>
  ${button("live-updates", liveUpdates ? "Pause live updates" : "Resume live updates", liveUpdates ? "pause" : "play", "compact ghost", 'id="live-updates"')}</div>
  <div id="poll-message" role="status" class="banner"></div>`;
const pollBody = () => `<div id="operational" class="stack" aria-busy="true">${blank("Loading data", "Fetching the first workspace snapshot.", "", "refresh")}</div>`;

function metrics(monitor, end = (readingSnapshot ? lastSuccess : null) ?? now()) {
  const start = end - windows[view.period] * day;
  const records = (monitor?.observations ?? []).filter((record) => record.at >= start && record.at <= end);
  const scheduled = records.filter((record) => record.origin === "Scheduled" && !record.stale);
  const good = scheduled.filter((record) => record.outcome === "SUCCESS");
  const failed = scheduled.filter((record) => record.outcome === "FAILURE" || record.outcome === "TIMEOUT");
  const values = good.map((record) => record.ms).sort((a, b) => a - b);
  const rank = (p, minimum) => values.length < minimum ? null : values[Math.ceil(p * values.length) - 1];
  const minutesPaused = Math.round((monitor?.pauses ?? []).reduce((total, pause) =>
    total + Math.max(0, Math.min(end, pause.end ?? end) - Math.max(start, pause.start)), 0) / 60000);
  return {
    start, end, good, failed: failed.length, values,
    manual: records.filter((record) => record.origin === "Manual").length,
    errors: scheduled.filter((record) => record.outcome === "ERROR").length,
    skipped: scheduled.filter((record) => record.outcome === "SKIPPED").length,
    interrupted: scheduled.filter((record) => record.outcome === "INTERRUPTED").length,
    stale: records.filter((record) => record.origin === "Scheduled" && record.stale).length, minutesPaused,
    uptime: good.length + failed.length ? 100 * good.length / (good.length + failed.length) : null,
    average: values.length ? values.reduce((a, b) => a + b, 0) / values.length : null,
    p95: rank(.95, 20), p99: rank(.99, 100),
  };
}

const ms = (value) => value === null ? "No data" : `${Math.round(value)} ms`;
const percent = (value) => value === null ? "No data" : `${value.toFixed(2)}%`;

function chart(sample) {
  const count = 12;
  const bins = Array.from({ length: count }, () => []);
  const size = (sample.end - sample.start) / count;
  for (const record of sample.good) {
    const index = Math.min(count - 1, Math.floor((record.at - sample.start) / size));
    bins[index].push(record.ms);
  }
  const points = bins.map((bin) => bin.length ? bin.reduce((sum, value) => sum + value, 0) / bin.length : null);
  const emptyBuckets = points.filter((value) => value === null).length;
  const chartDescription = `${view.period} UTC · Successful scheduled checks · ${emptyBuckets} ${emptyBuckets === 1 ? "gap" : "gaps"}`;
  if (!sample.good.length) return blank("No data", `No successful scheduled checks · ${view.period} UTC · Response time in ms.`, "", "pulse");

  const top = Math.max(100, Math.ceil(Math.max(...points) / 100) * 100);
  const x = (i) => 56 + (i + .5) * (538 / count);
  const y = (value) => 152 - value * 120 / top;
  let path = "";
  points.forEach((value, i) => {
    if (value !== null) path += `${i && points[i - 1] !== null ? "L" : "M"}${x(i)} ${y(value)} `;
  });
  const axis = (value) => `<text x="47" y="${y(value) + 4}" text-anchor="end">${value}</text>
    <line class="chart-grid" x1="56" x2="594" y1="${y(value)}" y2="${y(value)}"/>`;
  const label = (value) => view.period === "24h" ? iso(value).slice(11, 16) : iso(value).slice(5, 10);
  return `<figure class="page-segment"><figcaption class="help">${chartDescription}</figcaption>
    <svg class="chart" viewBox="0 0 616 211" role="img" aria-label="Average response time in milliseconds by UTC time bucket. Data table follows.">
    <text x="13" y="22">ms</text>${[0, top / 4, top / 2, top * .75, top].map(axis).join("")}
    <path class="chart-line" d="${path}"/>
    ${points.map((value, i) => value === null ? "" : `<circle class="chart-point" cx="${x(i)}" cy="${y(value)}" r="2.6"/>`).join("")}
    ${[0, 3, 6, 9, 12].map((i) => `<text x="${56 + i * 538 / count}" y="179" text-anchor="${i === 12 ? "end" : i === 0 ? "start" : "middle"}">${label(sample.start + i * size)}</text>`).join("")}
    <text x="594" y="207" text-anchor="end">UTC</text></svg>
    <details data-key="chart-data"><summary>View chart data</summary>
      ${table("Response time by UTC bucket", ["From (UTC)", "To (UTC)", "Average (ms)", "Samples"], points.map((value, i) =>
        [stamp(sample.start + i * size), stamp(sample.start + (i + 1) * size), ms(value), bins[i].length]))}</details></figure>`;
}

function monitorActions(monitor, compact = false) {
  const attr = `data-id="${monitor.id}"`;
  const css = compact ? "compact" : "";
  const busy = ["Queued", "Running"].includes(monitor.manual?.status);
  const blocked = monitor.state === "PAUSED" || busy;
  const reason = monitor.state === "PAUSED" ? "Resume before running a manual check." : "A check is in progress.";
  const manual = button("manual", compact ? "Run check" : "Run check now", "play", css,
    `${attr} aria-label="Run check now for ${escapeHtml(monitor.name)}"${blocked ? ` aria-disabled="true" aria-description="${reason}"` : ""}`);
  return `<div class="table-actions">${manual}
    ${button(monitor.state === "PAUSED" ? "resume" : "pause", monitor.state === "PAUSED" ? "Resume" : "Pause",
      monitor.state === "PAUSED" ? "play" : "pause", css, `${attr} id="lifecycle-${monitor.id}"`)}
    ${link(`monitors/${monitor.id}/edit`, "Edit", "edit", `btn ${css}`)}
    ${compact ? "" : button("delete", "Delete", null, "danger", attr)}</div>`;
}

function incidentTable(incidents) {
  if (!incidents.length) return blank("No incidents to show", "Incidents appear here when scheduled checks confirm downtime.", "", "triangle");
  return table("Incidents", ["Monitor", "Status", "Opened", "Closed", "Disposition"], incidents.map((incident) =>
    [link(`incidents/${incident.id}`, incident.name), incident.closed ? pill("Closed", "neutral", "check") : pill("Open", "bad", "triangle"),
      stamp(incident.opened), stamp(incident.closed), closeReasons[incident.reason] ?? "Investigating"]));
}

function overview() {
  const account = workspace();
  const monitors = account.monitors;
  const counts = Object.fromEntries(Object.keys(statuses).map((state) => [state, monitors.filter((monitor) => monitor.state === state).length]));
  const incidents = account.incidents.filter((incident) => !incident.closed);
  const selectedMonitor = ownsMonitor(view.chartMonitor) ?? monitors[0];
  const sample = metrics(selectedMonitor);
  const KPIs = `<div class="cards">${metric("Total monitors", monitors.length, "In this workspace", "monitor")}
    ${metric("Up", counts.UP, "Currently healthy", "check")}
    ${metric("Down", counts.DOWN, "Confirmed unavailable", "triangle")}
    ${metric("Active incidents", incidents.length, "Awaiting resolution", "pulse")}</div>`;
  if (!monitors.length) return `${KPIs}${blank("No monitors yet", "Add a target to start collecting observations.",
    link("monitors/new", "New monitor", "plus", "btn primary"))}${panel("Active incidents", "", incidentTable(incidents))}`;
  const chartControl = `<div class="filters"><div class="field"><label for="chart-monitor">Monitor</label><select id="chart-monitor" data-filter="chartMonitor">
    ${monitors.map((monitor) => `<option value="${monitor.id}"${selected(selectedMonitor.id, monitor.id)}>${escapeHtml(monitor.name)}</option>`).join("")}</select></div>${period()}</div>`;
  const distributions = `<div class="distribution" aria-hidden="true">${Object.entries(counts).filter(([, count]) => count)
    .map(([state, count]) => `<span class="${statuses[state][0]}"></span>`.repeat(count)).join("")}</div>
    <div class="inline">${Object.entries(counts).map(([state, count]) => pill(`${state} ${count}`, ...statuses[state])).join("")}</div>`;
  const open = incidents.length ? incidents.slice(0, 4).map((incident) => `<div class="incident-item">
    ${pill("Open", "bad", "triangle")}${link(`incidents/${incident.id}`, incident.name)}<span class="help">Opened ${stamp(incident.opened)}</span></div>`).join("")
    : blank("All clear", "There are no active incidents.", "", "check");
  return `${KPIs}<div class="split">${panel("Response time", "Per-monitor latency and uptime", `${chartControl}
    ${chart(sample)}<div class="inline"><strong>Uptime ${percent(sample.uptime)}</strong><span class="help">${sample.good.length + sample.failed} eligible checks</span></div>`)}
    <div class="stack">${panel("Monitor status", "", distributions)}
    ${panel("Active incidents", "", open, link("incidents", "View all", "arrow", "btn compact ghost"))}</div></div>
    ${panel("Monitor overview", "", table("Monitor overview", ["Monitor", "Status", "Next check (UTC)"], monitors.slice(0, 8).map((monitor) =>
      [link(`monitors/${monitor.id}`, monitor.name), status(monitor.state), stamp(monitor.due)]), true),
    link("monitors", "All monitors", "arrow", "btn compact ghost"))}`;
}

const field = (name, label, value = "", options = {}) => {
  const { type = "text", help = "", attrs = "" } = options;
  return `<div class="field"><label for="${name}">${label}</label><input id="${name}" name="${name}" type="${type}"
    value="${escapeHtml(value)}" aria-describedby="${name}-error${help ? ` ${name}-help` : ""}" ${attrs}>
    <p class="field-error" id="${name}-error"></p>${help ? `<p class="help" id="${name}-help">${help}</p>` : ""}</div>`;
};
const choices = (name, label, value, options) => `<div class="field"><label for="${name}">${label}</label>
  <select id="${name}" data-filter="${name}">${options.map(([key, text]) => `<option value="${key}"${selected(value, key)}>${text}</option>`).join("")}</select></div>`;
const formEnd = (label, cancel = "") => `<div class="actions"><button class="btn primary" type="submit">${label}</button>
  ${cancel ? link(cancel, "Cancel", null, "btn") : ""}</div>`;
const more = (visible, total, action = "more") => visible < total ? button(action, "Show more", null, "compact") : "";

function monitorRows() {
  const all = workspace().monitors;
  const search = view.search.trim().toLowerCase();
  const matches = all.filter((monitor) => (!view.status || monitor.state === view.status) && monitor.name.toLowerCase().includes(search));
  if (!all.length) return blank("No monitors yet", "Add an HTTP monitor to start collecting observations.", link("monitors/new", "New monitor", "plus", "btn primary"));
  if (!matches.length) return blank("No matching monitors", "Change the search or select a different status.", button("clear-monitors", "Clear filters", null, "compact"));
  return `${table("Workspace monitors", ["Monitor", "Status", "Next check (UTC)", "Last manual check", "Actions"], matches.slice(0, view.limit).map((monitor) =>
    [link(`monitors/${monitor.id}`, monitor.name), status(monitor.state), stamp(monitor.due),
      monitor.manual ? escapeHtml(monitor.manual.status) : "—", monitorActions(monitor, true)]))}${more(view.limit, matches.length)}`;
}

function monitorsList() {
  return panel("Workspace monitors", "", `<div class="filters">
    <div class="field search"><label for="monitor-search">Search by name</label><input type="search" id="monitor-search" placeholder="Search monitors…" data-filter="search" value="${escapeHtml(view.search)}"></div>
    ${choices("status", "Status", view.status, [["", "All statuses"], ...Object.keys(statuses).map((state) => [state, state])])}</div>
    <p id="filter-results" class="sr-only" role="status"></p><div class="page-segment" id="monitor-results">${monitorRows()}</div>`);
}

function monitorForm(monitor) {
  const input = monitor ?? { name: "", url: "", method: "GET", interval: 60, timeout: 10, failure: 3, recovery: 2 };
  const back = monitor ? `monitors/${monitor.id}` : "monitors";
  return `${link(back, monitor ? "Back to monitor" : "Back to monitors", "back", "back-link")}
    ${head(monitor ? "Edit monitor" : "New monitor", monitor?.name ?? "Configure a recurring HTTP or HTTPS check.")}
    <form class="form stack" data-form="monitor" data-version="${input.version ?? 0}" novalidate>
    ${panel("Target", "", `<div class="page-segment">
      ${field("name", "Monitor name", input.name, { attrs: "required" })}
      ${field("url", "Target URL", input.url, { type: "url", help: "Use an HTTP or HTTPS example.com address for this prototype.", attrs: 'required placeholder="https://api.example.com/health"' })}
      <div class="field"><label for="method">HTTP method</label><select id="method" name="method"><option>GET</option><option${selected(input.method, "HEAD")}>HEAD</option></select></div>
      <p class="help">HTTP 2xx indicates success. TLS certificates are verified and redirects are disabled.</p>
    </div>`)}
    ${panel("Check schedule", "", `<div class="form-grid">
      ${field("interval", "Interval (seconds)", input.interval, { type: "number", help: "30–86,400 seconds. Default 60.", attrs: 'min="30" max="86400" required' })}
      ${field("timeout", "Timeout (seconds)", input.timeout, { type: "number", help: "1–30 seconds, capped by interval. Default 10.", attrs: 'min="1" max="30" required' })}
    </div>`)}
    ${panel("Incident thresholds", "", `<div class="form-grid">
      ${field("failure", "Consecutive failures", input.failure, { type: "number", help: "Failures required to open an incident.", attrs: 'min="1" required' })}
      ${field("recovery", "Consecutive successes", input.recovery, { type: "number", help: "Successes required to confirm recovery.", attrs: 'min="1" required' })}
    </div>`)}
    <p id="monitor-form-error" class="banner bad" role="alert"></p>
    ${formEnd(monitor ? "Save changes" : "Create monitor", back)}</form>`;
}

function checkTable(monitor) {
  const records = monitor.observations.filter((record) => record.at >= now() - 30 * day && !["SKIPPED", "INTERRUPTED"].includes(record.outcome)
    && (!view.history || record.origin === view.history));
  if (!records.length) return blank("No check results", "Completed scheduled and manual checks appear here.", "", "clock");
  return `${table("Check history", ["Completed (UTC)", "Origin", "Observed outcome", "Response time"], records.slice(0, view.limit).map((record) =>
    [stamp(record.at), record.origin, `${pill(outcomes[record.outcome], record.outcome === "SUCCESS" ? "ok" :
      ["ERROR", "SKIPPED", "INTERRUPTED"].includes(record.outcome) ? "warn" : "bad",
      record.outcome === "SUCCESS" ? "check" : "triangle")}${record.stale ? " · old configuration" : ""}`, ms(record.ms)]))}
    ${more(view.limit, records.length)}`;
}

function monitorDetail(monitor) {
  const sample = metrics(monitor);
  const incidents = workspace().incidents.filter((incident) => incident.monitor === monitor.id);
  const historyFilter = choices("history", "Origin", view.history, [["", "All checks"], ["Scheduled", "Scheduled"], ["Manual", "Manual"]]);
  return `<div class="inline">${status(monitor.state)}<span class="mono muted break">${monitor.method} · ${escapeHtml(monitor.url)}</span></div>
    <div class="actions">${monitorActions(monitor)}</div>
    ${monitor.manual ? `<p class="banner neutral">Manual check · ${monitor.manual.status}${monitor.manual.at ? ` · ${stamp(monitor.manual.at)}` : ""}. Diagnostic only.</p>` : ""}
    <div class="cards">${metric("Uptime", percent(sample.uptime), `${sample.good.length} success · ${sample.failed} failed / timed out`, "check")}
      ${metric("Average latency", ms(sample.average), `${sample.values.length} successful samples`)}
      ${metric("p95 latency", ms(sample.p95), "At least 20 samples")}
      ${metric("p99 latency", ms(sample.p99), "At least 100 samples")}</div>
    ${panel("Response time", "Latency of successful scheduled checks", `${chart(sample)}
      <p class="help">Excluded · ${sample.manual} manual · ${sample.errors} internal errors · ${sample.skipped} skipped · ${sample.interrupted} interrupted · ${sample.stale} stale results · ${sample.minutesPaused} min paused. Empty buckets indicate gaps.</p>`,
    period())}
    ${panel("Configuration", "", facts([["Interval", `${monitor.interval}s`], ["Timeout", `${monitor.timeout}s`], ["Failure threshold", monitor.failure],
      ["Recovery threshold", monitor.recovery], ["Next check (UTC)", stamp(monitor.due)]]))}
    ${panel("Check history", "Completed results retained for up to 30 days.", `${historyFilter}${checkTable(monitor)}`)}
    ${panel("Incident history", "", incidentTable(incidents))}`;
}

function incidentsList() {
  const incidents = workspace().incidents.filter((incident) => !view.incident || (view.incident === "Closed") === Boolean(incident.closed));
  return panel("Incident history", "Most recently opened first.",
    `${choices("incident", "Status", view.incident, [["", "All incidents"], ["Open", "Open"], ["Closed", "Closed"]])}
    ${incidentTable(incidents.slice(0, view.limit))}${more(view.limit, incidents.length)}`);
}

function deliveries(records) {
  if (!records.length) return blank("No deliveries to show", "Available Telegram delivery dispositions appear here.", "", "bell");
  return `${table("Telegram deliveries", ["Event", "Status", "Attempts", "Created (UTC)"], records.slice(0, view.deliveryLimit).map((delivery) =>
    [current.name === "incident" ? delivery.event : link(`incidents/${delivery.incident}`, delivery.event), pill(delivery.status === "UNKNOWN" ? "Unknown" : delivery.status === "FAILED" ? "Failed" : delivery.status === "SENT" ? "Sent" : "Pending",
      delivery.status === "SENT" ? "ok" : delivery.status === "FAILED" ? "bad" : "warn",
      delivery.status === "SENT" ? "check" : delivery.status === "FAILED" ? "triangle" : "clock"), delivery.attempts, stamp(delivery.at)]))}
    ${more(view.deliveryLimit, records.length, "more-deliveries")}`;
}

function incidentDetail(incident) {
  return `${panel("Incident timeline", "", `<div class="inline">${incident.closed ? pill("Closed", "neutral", "check") : pill("Open", "bad", "triangle")}
    <strong>${closeReasons[incident.reason] ?? "Investigating"}</strong></div>
    ${facts([["Monitor", ownsMonitor(incident.monitor) ? link(`monitors/${incident.monitor}`, incident.name) : `${escapeHtml(incident.name)} · deleted`],
    ["Affected origin", `<span class="mono">${escapeHtml(incident.origin)}</span>`], ["Opened (UTC)", stamp(incident.opened)],
    ["Closed (UTC)", stamp(incident.closed)]])}`)}
    ${panel("Notification deliveries", "Unknown means provider acceptance could not be confirmed.", deliveries(workspace().deliveries.filter((delivery) => delivery.incident === incident.id)))}`;
}

function notificationForm() {
  const channel = workspace().channel;
  return `<form class="form stack" data-form="telegram" novalidate>
    ${panel("Telegram channel", "Use the synthetic destination fields below.", `<div class="inline">
      ${pill(channel.configured ? "Configured" : "Unconfigured", channel.configured ? "ok" : "neutral", channel.configured ? "check" : "circle")}
      ${pill(channel.enabled ? "Enabled" : "Disabled", channel.enabled ? "ok" : "neutral", channel.enabled ? "check" : "pause")}</div>
      <div class="form-grid">${field("bot", "Demo bot token", "", { type: "password", attrs: 'autocomplete="off" placeholder="DEMO-BOT"', help: "Use DEMO-BOT to simulate a new value." })}
      ${field("chat", "Demo chat ID", "", { attrs: 'autocomplete="off" placeholder="DEMO-CHAT"', help: "Use DEMO-CHAT to simulate a new value." })}</div>
      <fieldset><legend>Notify on</legend>
        <label class="checkline"><input type="checkbox" name="opened"${checked(channel.opened)}>Incident opened</label>
        <label class="checkline"><input type="checkbox" name="resolved"${checked(channel.resolved)}>Incident resolved</label></fieldset>
      <label class="checkline"><input type="checkbox" name="enabled"${checked(channel.enabled)}>Enable Telegram notifications</label>
      <p class="help">Leave both destination fields blank to keep the configured destination.</p>${formEnd("Save settings")}`)}
  </form>`;
}

function notificationActivity() {
  const filters = [["", "Failed and unknown"], ["FAILED", "Failed"], ["UNKNOWN", "Unknown"]];
  return panel("Delivery issues", "Unknown deliveries are reviewed without an automatic resend.",
    `${choices("delivery", "Disposition", view.delivery, filters)}${deliveries(workspace().deliveries.filter((delivery) =>
      ["FAILED", "UNKNOWN"].includes(delivery.status) && (!view.delivery || view.delivery === delivery.status)))}`);
}

function authScreen() {
  const signup = current.name === "sign-up";
  const title = signup ? "Create your account" : "Sign in";
  const closed = signup && (!data.registration || !data.initialized);
  const messages = [];
  if (current.note === "expired") messages.push('<p class="banner warn">Your session expired. Sign in to continue.</p>');
  if (!data.initialized) messages.push('<p class="banner warn">Initial setup is required. Ask the installation operator to provision the first Owner before signing in.</p>');
  const body = closed ? blank("Registration is closed", "The installation operator controls public registration.", link("sign-in", "Back to sign in", "back", "btn"), "circle") :
    `<form class="page-segment" data-form="${signup ? "signup" : "signin"}" novalidate>
      ${field("email", "Email", signup ? "" : data.suggestedEmail ?? fixtureOwner, { type: "email", attrs: 'autocomplete="username" required' })}
      ${field("password", "Demo password", "infrapulse-demo", { type: "password", attrs: `autocomplete="${signup ? "new-password" : "current-password"}" required`,
      help: "Use infrapulse-demo for this prototype." })}
      <p id="auth-error" class="banner bad" role="alert"></p>
      <button type="submit" class="btn primary"${data.initialized ? "" : " disabled"}>${signup ? "Create account" : "Sign in"}</button>
    </form>`;
  return `<main id="main" class="auth" tabindex="-1"><div class="auth-inner stack">${brand()}
    <section class="panel stack">${head(title, signup ? "Create an Owner account and workspace." : "Access your monitoring workspace.")}
    ${messages.join("")}${body}
    ${signup ? (closed ? "" : link("sign-in", "Back to sign in", "back", "back-link")) :
      link("sign-up", "Registration availability", "arrow", "back-link")}</section>
    ${button("demo", "Prototype / Demo Data", "box", "ghost")}</div></main>`;
}

function staticPage() {
  const account = workspace();
  switch (current.name) {
    case "overview":
      return head("Overview", "Monitor health and incident activity in your workspace.",
        link("monitors/new", "New monitor", "plus", "btn primary")) + pollChrome() + pollBody();
    case "monitors":
      return head("Monitors", "Manage HTTP checks and inspect current monitor status.",
        link("monitors/new", "New monitor", "plus", "btn primary")) + pollChrome() + pollBody();
    case "monitor":
      return link("monitors", "Back to monitors", "back", "back-link") + head(ownsMonitor(current.id).name, "Monitor details") + pollChrome() + pollBody();
    case "create":
      return monitorForm();
    case "edit":
      return monitorForm(ownsMonitor(current.id));
    case "incidents":
      return head("Incidents", "Review confirmed downtime and incident history.") + pollChrome() + pollBody();
    case "incident":
      return link("incidents", "Back to incidents", "back", "back-link") + head(ownsIncident(current.id).name, "Incident details") + pollChrome() + pollBody();
    case "notifications":
      return head("Notification settings", "Configure workspace alerts and review Telegram delivery issues.") + pollChrome() + notificationForm() + pollBody();
    case "account":
      return head("Account settings", "View your account and manage this session.") +
        panel("Account details", "", facts([["Email", escapeHtml(account.email)], ["Created (UTC)", stamp(account.created)]])) +
        panel("Session", "Signing out ends your current session.", button("logout", "Sign out", "logout", "danger"));
    case "workspace":
      return head("Workspace settings", "Manage settings for your Owner workspace.") + `<form class="form stack" data-form="workspace" novalidate>
        ${panel("Workspace details", "", `${field("workspace-name", "Workspace name", account.name, { attrs: "required" })}${formEnd("Save changes")}`)}
        ${panel("Notifications", "Channel configuration and delivery history are scoped to this workspace.", link("notifications", "Open notification settings", "arrow", "back-link"))}</form>`;
    default:
      return head("Access unavailable", "") + blank("This resource is unavailable", "It may have been removed or you may lack access.", link("overview", "Return to overview", "back", "btn"), "triangle");
  }
}

let snapshot = null;
let readingSnapshot = false;
const accountSnapshot = () => structuredClone(workspace());

function operationalContent() {
  switch (current.name) {
    case "overview": return overview();
    case "monitors": return monitorsList();
    case "monitor": return monitorDetail(ownsMonitor(current.id));
    case "incidents": return incidentsList();
    case "incident": return incidentDetail(ownsIncident(current.id));
    case "notifications": return notificationActivity();
  }
}

function renderOperational(force = false) {
  const container = document.querySelector("#operational");
  if (!container || !snapshot) return;
  const active = document.activeElement;
  const editingSearch = !force && current.name === "monitors" && active?.id === "monitor-search";
  if (editingSearch) {
    readingSnapshot = true;
    try {
      document.querySelector("#monitor-results").innerHTML = monitorRows();
      renderedAt = lastSuccess;
    } finally {
      readingSnapshot = false;
    }
    return;
  }
  if (!force && container.contains(active) && active.matches("select")) return;
  const scroll = [...container.querySelectorAll(".table-wrap")].map((region) => region.scrollLeft);
  const chartOpen = container.querySelector('[data-key="chart-data"]')?.open;
  const selectorParts = ["data-action", "data-id", "data-window", "href", "aria-label"];
  const selector = active?.localName + selectorParts.filter((attr) => active?.hasAttribute(attr))
    .map((attr) => `[${attr}="${CSS.escape(active.getAttribute(attr))}"]`).join("");
  const restoreFocus = container.contains(active);
  let content;
  readingSnapshot = true;
  try {
    content = operationalContent();
  } finally {
    readingSnapshot = false;
  }
  if (container.innerHTML !== content) {
    container.innerHTML = content;
    const details = container.querySelector('[data-key="chart-data"]');
    if (details && chartOpen) details.open = true;
    container.querySelectorAll(".table-wrap").forEach((region, i) => { region.scrollLeft = scroll[i] ?? 0; });
  }
  container.setAttribute("aria-busy", "false");
  if (restoreFocus) {
    const replacement = (active.id && document.getElementById(active.id)) || container.querySelector(selector);
    (replacement ?? document.querySelector("#page-title")).focus({ preventScroll: true });
  }
  renderedAt = lastSuccess;
}

function updateFreshness() {
  if (!polling()) return;
  const indicator = document.querySelector("#freshness");
  const message = document.querySelector("#poll-message");
  if (!indicator || !message) return;
  const stale = lastSuccess !== null && now() - lastSuccess >= 30000;
  const label = lastSuccess === null ? (refreshError ? "Update unavailable" : "Loading") : stale ? "Stale" : "Updated";
  const shownAt = renderedAt ?? lastSuccess;
  const age = shownAt === null ? "" : ` · ${clockText(shownAt)} UTC`;
  const content = `${glyph(stale || refreshError ? "triangle" : "clock")}<strong class="${stale ? "warn" : ""}">${label}</strong><span>${age}${liveUpdates ? "" : " · Live updates paused"}</span>`;
  if (indicator.dataset.content !== content) {
    indicator.innerHTML = content;
    indicator.dataset.content = content;
  }
  const copy = stale ? (liveUpdates ? "Data is stale. Showing the last successful update." : "Live updates paused. Refresh to get current data.") :
    refreshError ? (snapshot ? "Refresh failed. Showing the last successful update." : "Could not load data. Use Refresh data to try again.") : "";
  message.className = `banner ${stale ? "warn" : "bad"}`;
  if (message.textContent !== copy) message.textContent = copy;
}

function refresh({ immediate = false } = {}) {
  if (!polling() || !workspace() || pendingRefresh || (!immediate && !liveUpdates && snapshot)) return;
  const finish = () => {
    pendingRefresh = 0;
    const body = document.querySelector("#operational");
    if (transport === "hold") return;
    if (transport === "offline") {
      refreshError = true;
      if (!snapshot && body) {
        body.innerHTML = blank("Data unavailable", "Try again when the connection is restored.", button("refresh", "Retry", "refresh", "compact"), "triangle");
        body.setAttribute("aria-busy", "false");
      }
    } else {
      const retryWasFocused = body?.contains(document.activeElement) && !snapshot;
      snapshot = accountSnapshot();
      lastSuccess = now();
      refreshError = false;
      renderOperational(immediate || retryWasFocused);
      if (retryWasFocused) document.querySelector("#page-title").focus({ preventScroll: true });
    }
    updateFreshness();
  };
  if (immediate) finish();
  else pendingRefresh = setTimeout(finish, 260);
}

function parseRoute(fragment) {
  const [path, id, tail, extra] = fragment.split("/");
  if (extra) return { name: "missing" };
  if (path === "monitors" && id) {
    if (id === "new" && !tail) return { name: "create" };
    return { name: tail === "edit" ? "edit" : tail ? "missing" : "monitor", id };
  }
  if (path === "incidents" && id && !tail) return { name: "incident", id };
  if (!id && ["overview", "monitors", "incidents", "notifications", "account", "workspace", "sign-in", "sign-up"].includes(path)) return { name: path };
  return { name: "missing" };
}

function route(fragment, note) {
  const target = parseRoute(fragment);
  const auth = ["sign-in", "sign-up"].includes(target.name);
  if (!workspace() && !auth) {
    returnRoute = fragment;
    return navigate("sign-in", { replace: true, note });
  }
  if (auth && workspace()) return navigate("overview", { replace: true });
  if ((["monitor", "edit"].includes(target.name) && !ownsMonitor(target.id)) ||
      (target.name === "incident" && !ownsIncident(target.id))) target.name = "missing";
  clearTimeout(pendingRefresh);
  pendingRefresh = 0;
  snapshot = null;
  lastSuccess = null;
  renderedAt = null;
  refreshError = false;
  current = { ...target, note };
  view = initialView();
  if (auth) shell.innerHTML = authScreen();
  else renderShell(staticPage());
  document.title = `InfraPulse · ${pageLabels[current.name] ?? (current.name === "sign-up" ? "Sign up" : "Sign in")}`;
  window.scrollTo(0, 0);
  document.querySelector("#page-title").focus({ preventScroll: true });
  if (polling()) {
    updateFreshness();
    refresh();
  }
}

function navigate(fragment, { replace = false, note } = {}) {
  const method = replace ? "replaceState" : "pushState";
  if (location.hash !== href(fragment)) history[method](null, "", href(fragment));
  route(fragment, note);
}

function readLocation() {
  route(location.hash.startsWith("#/") ? location.hash.slice(2) : workspace() ? "overview" : "sign-in");
}

function simulateDelivery(account, incident, event) {
  const channel = account.channel;
  if (!channel.enabled || !channel[event]) return;
  account.deliveries.unshift({ incident: incident.id, event: event === "opened" ? "Incident opened" : "Incident resolved",
    status: "PENDING", attempts: 0, at: now(), channelVersion: channel.version ?? 0 });
}

function closeIncident(account, monitor, reason, time) {
  const incident = activeIncident(account, monitor.id);
  if (!incident) return;
  incident.closed = time;
  incident.reason = reason;
  if (reason === "RECOVERED") simulateDelivery(account, incident, "resolved");
}

function scheduledResult(account, monitor, record) {
  if (record.outcome === "ERROR") return;
  const incident = activeIncident(account, monitor.id);
  if (record.outcome === "SUCCESS") {
    monitor.failures = 0;
    monitor.successes += 1;
    if (!incident || monitor.successes >= monitor.recovery) {
      monitor.state = "UP";
      closeIncident(account, monitor, "RECOVERED", record.at);
    }
  } else {
    monitor.successes = 0;
    monitor.failures += 1;
    if (monitor.failures >= monitor.failure) {
      monitor.state = "DOWN";
      if (!incident) {
        const entry = { id: nextId("incident"), monitor: monitor.id, name: monitor.name,
          origin: new URL(monitor.url).origin, opened: record.at, closed: null };
        account.incidents.unshift(entry);
        simulateDelivery(account, entry, "opened");
      }
    }
  }
}

function addObservation(monitor, outcome, origin, time, stale = false) {
  const record = { at: time, outcome, origin, ms: outcome === "SUCCESS" ? 85 + monitor.version * 9 + (Math.floor(time / 1000) % 58) : null, stale };
  monitor.observations.unshift(record);
  return record;
}

function cancelManual(monitor) {
  if (monitor.manual?.status === "Queued") monitor.manual = { status: "Skipped", at: now() };
}

function runManual(monitor) {
  const time = now();
  if (monitor.state === "PAUSED") return notify("Resume this monitor before requesting a manual check.");
  if (monitor.task || ["Queued", "Running"].includes(monitor.manual?.status)) return notify("A check is already in progress. Try again after it finishes.");
  const wait = Math.ceil((monitor.accepted + 30000 - time) / 1000);
  if (wait > 0) return notify(`Manual check rate limit. Try again in ${wait}s.`);
  monitor.accepted = time;
  monitor.manual = { status: "Queued", start: time + 900, version: monitor.version, generation: monitor.generation };
  notify("Manual check queued.");
  refresh({ immediate: true });
}

function tickWorkspace(account, time) {
  for (const monitor of account.monitors) {
    const manual = monitor.manual;
    if (manual?.status === "Queued" && time >= manual.start) {
      manual.status = "Running";
      manual.finish = time + 1500;
    } else if (manual?.status === "Running" && time >= manual.finish) {
      const outcome = monitor.id === "payments" && manual.version === 1 ? "FAILURE" : "SUCCESS";
      addObservation(monitor, outcome, "Manual", time, manual.version !== monitor.version || manual.generation !== monitor.generation || monitor.state === "PAUSED");
      monitor.manual = { status: `Completed · ${outcomes[outcome]}`, at: time };
    }
    if (monitor.task && time >= monitor.task.finish) {
      const task = monitor.task;
      const stale = monitor.state === "PAUSED" || monitor.version !== task.version || monitor.generation !== task.generation;
      const result = addObservation(monitor, task.outcome, "Scheduled", time, stale);
      if (!stale) scheduledResult(account, monitor, result);
      monitor.task = null;
    }
    if (monitor.state === "PAUSED" || !monitor.due || monitor.due > time) continue;
    const due = monitor.due;
    const interval = monitor.interval * 1000;
    monitor.due += interval * (Math.floor((time - due) / interval) + 1);
    if (monitor.task || ["Queued", "Running"].includes(monitor.manual?.status) ||
      (manual?.finish && monitor.accepted <= due && manual.finish >= due)) {
      addObservation(monitor, "SKIPPED", "Scheduled", time);
      continue;
    }
    const injected = nextOutcome?.id === monitor.id ? nextOutcome.outcome : null;
    if (injected) nextOutcome = null;
    const outcome = injected ?? (monitor.id === "payments" && monitor.url === "https://payments.example.com/health" ? "FAILURE" : "SUCCESS");
    monitor.task = { outcome, version: monitor.version, generation: monitor.generation, finish: time + 1600 };
  }
  for (const delivery of account.deliveries) {
    if (delivery.status === "PENDING" && time - delivery.at >= 8000) {
      const eligible = (account.channel.version ?? 0) === delivery.channelVersion && account.channel.enabled;
      delivery.status = eligible ? "SENT" : "FAILED";
      delivery.attempts = eligible ? 1 : 0;
    }
  }
}

function confirmAction(title, copy, label, callback, danger = false) {
  confirmation = callback;
  modal.innerHTML = `<div class="stack"><h2 id="modal-title">${title}</h2><p class="muted" id="modal-copy">${escapeHtml(copy)}</p>
    <div class="actions">${button("close-dialog", "Cancel", null, "", "autofocus")}
    ${button("confirm", label, null, danger ? "danger" : "primary")}</div></div>`;
  modal.showModal();
}

function changeLifecycle(action, monitor) {
  const account = workspace();
  const time = now();
  if (action === "delete") {
    closeIncident(account, monitor, "MONITOR_DELETED", time);
    account.monitors = account.monitors.filter((item) => item.id !== monitor.id);
    navigate("monitors");
    return notify("Monitor deleted. Incident history retained.");
  }
  const pausing = action === "pause";
  monitor.state = pausing ? "PAUSED" : "PENDING";
  monitor.due = pausing ? null : time + monitor.interval * 1000;
  monitor.successes = monitor.failures = 0;
  monitor.generation = (monitor.generation ?? 0) + 1;
  if (pausing) {
    monitor.pauses.push({ start: time, end: null });
    cancelManual(monitor);
  } else {
    monitor.pauses.at(-1).end = time;
  }
  refresh({ immediate: true });
  notify(pausing ? "Monitor paused." : "Monitoring resumed. Waiting for a qualifying result.");
}

function showErrors(form, errors) {
  for (const control of form.querySelectorAll("[aria-describedby]")) {
    const error = errors[control.name];
    if (error) control.setAttribute("aria-invalid", "true");
    else control.removeAttribute("aria-invalid");
    form.querySelector(`#${control.id}-error`).textContent = error ?? "";
  }
  const first = form.elements.namedItem(Object.keys(errors)[0] ?? "");
  first?.focus();
  return Boolean(first);
}

function monitorInput(form) {
  const values = new FormData(form);
  const errors = {};
  const input = { name: values.get("name").trim(), method: values.get("method") };
  if (!input.name) errors.name = "Enter a monitor name.";
  try {
    const raw = values.get("url").trim();
    const url = new URL(raw);
    if (!/^https?:\/\//i.test(raw) || url.username || url.password || raw.includes("#")) throw new Error("Invalid URL");
    if (!(url.hostname === "example.com" || url.hostname.endsWith(".example.com"))) {
      errors.url = "Use example.com or one of its subdomains in this prototype.";
    }
    input.url = url.href;
  } catch {
    errors.url = "Enter a valid HTTP or HTTPS URL without credentials or a fragment.";
  }
  for (const [key, min, max, message] of [
    ["interval", 30, 86400, "Enter a whole number from 30 to 86,400."],
    ["timeout", 1, 30, "Enter a whole number from 1 to 30."],
    ["failure", 1, Infinity, "Enter a positive whole number."],
    ["recovery", 1, Infinity, "Enter a positive whole number."],
  ]) {
    input[key] = Number(values.get(key));
    if (!Number.isSafeInteger(input[key]) || input[key] < min || input[key] > max) errors[key] = message;
  }
  if (!errors.timeout && !errors.interval && input.timeout > input.interval) errors.timeout = "Timeout must fit within the interval.";
  return showErrors(form, errors) ? null : input;
}

function saveMonitor(form) {
  const input = monitorInput(form);
  if (!input) return;
  const account = workspace();
  const monitor = ownsMonitor(current.id);
  const addressChanged = monitor && monitor.url !== input.url;
  const save = () => {
    if (monitor && monitor.version !== Number(form.dataset.version)) {
      document.querySelector("#monitor-form-error").textContent = "This monitor changed while you were editing. Review the saved configuration before trying again.";
      return;
    }
    if (!monitor) {
      const id = nextId("monitor");
      account.monitors.push({ ...input, id, state: "PENDING", version: 1, successes: 0, failures: 0, manual: null,
        accepted: 0, observations: [], pauses: [], due: now() + input.interval * 1000 });
      navigate(`monitors/${id}`);
      return notify("Monitor created.");
    }
    if (Object.keys(input).some((key) => input[key] !== monitor[key])) {
      const intervalChanged = input.interval !== monitor.interval;
      Object.assign(monitor, input);
      monitor.version += 1;
      monitor.successes = monitor.failures = 0;
      cancelManual(monitor);
      if (addressChanged) {
        closeIncident(account, monitor, "CONFIGURATION_CHANGED", now());
        if (monitor.state !== "PAUSED") monitor.state = "PENDING";
      }
      if (monitor.state !== "PAUSED" && (addressChanged || intervalChanged)) monitor.due = now() + monitor.interval * 1000;
    }
    navigate(`monitors/${monitor.id}`);
    notify("Monitor settings saved.");
  };
  if (addressChanged) {
    const state = monitor.state === "PAUSED" ? "This monitor stays paused until you resume it. No check will start from this edit." :
      "The monitor enters PENDING and waits for a qualifying scheduled result.";
    confirmAction("Change target URL?", `${state} Any open incident closes as Configuration changed.`, "Change target URL", save);
  } else save();
}

function saveTelegram(form) {
  const values = new FormData(form);
  const account = workspace();
  const saved = account.channel;
  const bot = values.get("bot");
  const chat = values.get("chat");
  const enabled = values.has("enabled");
  const errors = {};
  if (bot && bot !== "DEMO-BOT") errors.bot = "Enter DEMO-BOT or leave this field blank.";
  if (chat && chat !== "DEMO-CHAT") errors.chat = "Enter DEMO-CHAT or leave this field blank.";
  if (!saved.configured && (bot || chat || enabled)) {
    if (!bot) errors.bot = "Enter DEMO-BOT to configure the destination.";
    if (!chat) errors.chat = "Enter DEMO-CHAT to configure the destination.";
  }
  if (showErrors(form, errors)) return;
  const save = () => {
    const input = { configured: saved.configured || Boolean(bot && chat), enabled, opened: values.has("opened"), resolved: values.has("resolved") };
    if (bot || chat || Object.keys(input).some((key) => input[key] !== saved[key])) {
      Object.assign(saved, input, { version: (saved.version ?? 0) + 1 });
    }
    const wrapper = document.createElement("div");
    wrapper.innerHTML = notificationForm();
    form.replaceWith(wrapper.firstElementChild);
    document.querySelector('[data-form="telegram"] button[type="submit"]').focus({ preventScroll: true });
    notify("Telegram settings saved.");
  };
  if (saved.enabled && !enabled) confirmAction("Disable Telegram?", "New incident events will stop creating Telegram deliveries for this workspace.", "Disable Telegram", save, true);
  else save();
}

function newAccount(email) {
  data.accounts[email] = { email, name: "My workspace", created: now(), monitors: [], incidents: [], deliveries: [],
    channel: { configured: false, enabled: false, opened: true, resolved: true } };
}

function authSubmit(form, signup) {
  const values = new FormData(form);
  const email = values.get("email").trim().toLowerCase();
  const errors = {};
  if (!email.endsWith("@example.com") || form.elements.email.validity.typeMismatch) errors.email = "Use a valid example.com email address.";
  if (values.get("password") !== "infrapulse-demo") errors.password = "Use the demo password shown below the field.";
  if (showErrors(form, errors)) return;
  const error = form.querySelector("#auth-error");
  if (signup) {
    if (!data.initialized || !data.registration) {
      route("sign-up");
      return;
    }
    if (Object.hasOwn(data.accounts, email)) {
      error.textContent = "This account could not be created. Try a different email or sign in.";
      return;
    }
    newAccount(email);
    data.suggestedEmail = email;
    returnRoute = "overview";
    navigate("sign-in");
    return notify("Account created. Sign in to open your workspace.");
  }
  if (!Object.hasOwn(data.accounts, email)) {
    error.textContent = "Sign-in failed. Check your email and password.";
    return;
  }
  data.identity = email;
  data.session = newSession();
  data.suggestedEmail = email;
  navigate(returnRoute, { replace: true });
  returnRoute = "overview";
}

function signOut(expired = false) {
  if (expired) returnRoute = location.hash.slice(2) || "overview";
  else returnRoute = "overview";
  data.suggestedEmail = data.identity;
  data.identity = null;
  data.session = null;
  navigate("sign-in", { replace: true, note: expired ? "expired" : "" });
  if (!expired) notify("Signed out.");
}

function renewSession(announce = false) {
  if (!data.session || data.session.renewalUntil <= now()) return signOut(true);
  data.session = newSession(data.session.generation);
  if (announce) notify("Demo session renewed. Your current workspace remains open.");
}

function showDemo() {
  const account = workspace();
  const choicesForFixture = account?.monitors.filter((monitor) => monitor.state !== "PAUSED") ?? [];
  demo.innerHTML = `<div class="stack"><div class="page-head"><div><h2 id="demo-title">Prototype / Demo Data</h2>
    <p class="help">Simulated data, checks, credentials and deliveries. Changes last until reload.</p></div>
    ${button("close-dialog", "", "x", "icon ghost", 'aria-label="Close demo controls" autofocus')}</div>
    <fieldset class="page-segment"><legend>Data updates</legend>
      <div class="actions">${button("transport", "Connected", null, "compact", `data-mode="connected" aria-pressed="${transport === "connected"}"`)}
      ${button("transport", "Loading", null, "compact", `data-mode="hold" aria-pressed="${transport === "hold"}"`)}
      ${button("transport", "Error", null, "compact", 'data-mode="offline"')}
      ${button("transport", "Refresh error", null, "compact", 'data-mode="refresh-error"')}
      ${button("transport", "Stale", null, "compact", 'data-mode="stale"')}</div>
      <p class="help">Apply Loading or Error on a polling screen. Connected resumes automatic updates.</p></fieldset>
    ${choicesForFixture.length ? `<form data-form="observation" class="page-segment">
      <div class="form-grid"><div class="field"><label for="fixture-monitor">Fixture monitor</label><select id="fixture-monitor" name="fixture-monitor">
        ${choicesForFixture.map((monitor) => `<option value="${monitor.id}">${escapeHtml(monitor.name)}</option>`).join("")}</select></div>
        <div class="field"><label for="fixture-outcome">Scheduled outcome</label><select id="fixture-outcome" name="fixture-outcome">
          ${["SUCCESS", "FAILURE", "TIMEOUT", "ERROR"].map((outcome) => `<option value="${outcome}">${outcomes[outcome]}</option>`).join("")}</select></div></div>
      <button type="submit" class="btn compact">Queue fixture observation</button></form>` : ""}
    <fieldset class="page-segment"><legend>Installation and session fixtures</legend>
      <div class="actions">${button("registration", data.registration ? "Close registration" : "Open registration", null, "compact", data.initialized ? "" : "disabled")}
      ${button(data.initialized ? "setup" : "bootstrap", data.initialized ? "Simulate setup required" : "Simulate operator bootstrap", null, "compact")}
      ${account ? button("expire", "Expire session", null, "compact") + button("recovery", "Renew session", null, "compact") +
        link("monitors/unavailable", "Access unavailable", null, "btn compact") : ""}</div></fieldset>
    ${button("reset", "Reset demo data", null, "danger")}</div>`;
  demo.showModal();
}

function demoTransport(mode) {
  demo.close();
  transport = ["stale", "refresh-error"].includes(mode) ? "offline" : mode;
  if (mode === "hold") {
    route(location.hash.slice(2) || "overview");
  } else if (mode === "stale" && polling()) {
    if (!snapshot) snapshot = accountSnapshot();
    lastSuccess = now() - 31000;
    renderOperational(true);
    refresh({ immediate: true });
  } else if (mode === "refresh-error" && polling()) {
    clearTimeout(pendingRefresh);
    pendingRefresh = 0;
    refresh({ immediate: true });
  } else if (mode === "offline" && polling()) {
    route(location.hash.slice(2) || "overview");
    clearTimeout(pendingRefresh);
    pendingRefresh = 0;
    refresh({ immediate: true });
  }
  if (mode === "connected") {
    liveUpdates = true;
    updateLiveToggle();
    refresh();
    notify("Connection restored.");
  }
}

function updateLiveToggle() {
  const control = document.querySelector("#live-updates");
  if (!control) return;
  control.innerHTML = `${glyph(liveUpdates ? "pause" : "play")}${liveUpdates ? "Pause live updates" : "Resume live updates"}`;
  updateFreshness();
}

function applyFilter(control) {
  const key = control.dataset.filter;
  view[key] = control.value;
  view.limit = view.deliveryLimit = 8;
  if (["search", "status"].includes(key)) {
    const region = document.querySelector("#monitor-results");
    readingSnapshot = true;
    try {
      region.innerHTML = monitorRows();
      const count = region.querySelectorAll("tbody tr").length;
      document.querySelector("#filter-results").textContent = count ? `${count} results shown.` : "No results.";
    } finally {
      readingSnapshot = false;
    }
  } else renderOperational(true);
}

document.addEventListener("submit", (event) => {
  const form = event.target;
  const kind = form.dataset.form;
  if (!kind) return;
  event.preventDefault();
  if (kind === "signin" || kind === "signup") return authSubmit(form, kind === "signup");
  if (!workspace()) return navigate("sign-in");
  if (kind === "monitor") return saveMonitor(form);
  if (kind === "telegram") return saveTelegram(form);
  const values = new FormData(form);
  if (kind === "workspace") {
    const name = values.get("workspace-name").trim();
    if (showErrors(form, name ? {} : { "workspace-name": "Enter a workspace name." })) return;
    workspace().name = name;
    renderShell(staticPage());
    document.querySelector('[data-form="workspace"] button[type="submit"]').focus({ preventScroll: true });
    return notify("Workspace name updated.");
  }
  if (kind === "observation") {
    const monitor = ownsMonitor(values.get("fixture-monitor"));
    if (!monitor || monitor.state === "PAUSED") return;
    nextOutcome = { id: monitor.id, outcome: values.get("fixture-outcome") };
    monitor.due = now();
    demo.close();
    notify("Fixture outcome queued for a scheduled check.");
  }
});

document.addEventListener("change", (event) => {
  if (event.target.matches("select[data-filter]")) applyFilter(event.target);
});
document.addEventListener("input", (event) => {
  if (event.target.matches("input[data-filter]")) applyFilter(event.target);
  if (event.target.matches('input[aria-invalid="true"]')) {
    event.target.removeAttribute("aria-invalid");
    document.querySelector(`#${event.target.id}-error`).textContent = "";
  }
});
document.addEventListener("click", (event) => {
  const anchor = event.target.closest("a[href]");
  if (anchor?.classList.contains("skip")) {
    event.preventDefault();
    document.querySelector("#main").focus();
    return;
  }
  if (anchor?.hash.startsWith("#/") && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
    event.preventDefault();
    if (drawer.open) drawer.close();
    if (demo.open) demo.close();
    navigate(anchor.hash.slice(2));
    return;
  }
  const control = event.target.closest("[data-action]");
  if (!control) return;
  const { action, id, window: range, mode } = control.dataset;
  const monitor = ownsMonitor(id);
  switch (action) {
    case "drawer": return drawer.showModal();
    case "close-dialog": return control.closest("dialog").close();
    case "demo":
      if (drawer.open) drawer.close();
      return showDemo();
    case "confirm": {
      const callback = confirmation;
      modal.close();
      return callback?.();
    }
    case "refresh": return refresh({ immediate: true });
    case "live-updates":
      liveUpdates = !liveUpdates;
      if (!liveUpdates && snapshot) {
        clearTimeout(pendingRefresh);
        pendingRefresh = 0;
      }
      updateLiveToggle();
      if (liveUpdates) refresh();
      return;
    case "period":
      view.period = range;
      return renderOperational(true);
    case "more":
    case "more-deliveries": {
      const key = action === "more" ? "limit" : "deliveryLimit";
      const region = control.previousElementSibling?.querySelector("table");
      const label = region?.getAttribute("aria-label");
      view[key] += 8;
      renderOperational(true);
      document.querySelector(`.table-wrap[aria-label="${CSS.escape(label ?? "")}"]`)?.focus();
      return;
    }
    case "clear-monitors":
      view.search = view.status = "";
      view.limit = 8;
      renderOperational(true);
      return document.querySelector("#monitor-search")?.focus();
    case "manual":
      if (monitor) runManual(monitor);
      return;
    case "pause":
      if (monitor?.state !== "PAUSED" && monitor) confirmAction("Pause monitor?", "Scheduled and manual checks are suspended. Any open incident stays open.", "Pause monitor", () => changeLifecycle(action, monitor));
      return;
    case "resume":
      if (monitor?.state === "PAUSED") changeLifecycle(action, monitor);
      return;
    case "delete":
      if (monitor) confirmAction("Delete monitor?", "Future checks stop and check history is removed. Incident history is retained. Any open incident closes as Monitor deleted.", "Delete monitor", () => changeLifecycle(action, monitor), true);
      return;
    case "logout": return signOut();
    case "expire":
      demo.close();
      return signOut(true);
    case "recovery":
      demo.close();
      return renewSession(true);
    case "transport": return demoTransport(mode);
    case "registration":
      data.registration = !data.registration;
      demo.close();
      if (current.name === "sign-up") route("sign-up");
      return notify(data.registration ? "Demo registration opened." : "Demo registration closed.");
    case "setup":
      return confirmAction("Simulate initial setup?", "This replaces the current demo accounts and monitoring data with an uninitialized installation.",
        "Simulate setup", () => {
          demo.close();
          data = { accounts: {}, initialized: false, registration: false, identity: null, sequence: 200 };
          returnRoute = "overview";
          nextOutcome = null;
          navigate("sign-in", { replace: true });
        }, true);
    case "bootstrap":
      if (!data.initialized) {
        newAccount(fixtureOwner);
        data.initialized = true;
        demo.close();
        route("sign-in");
        notify("First Owner provisioned by the simulated operator.");
      }
      return;
    case "reset":
      return confirmAction("Reset demo data?", "This discards local prototype changes and restores the original workspace.", "Reset demo data", () => {
        demo.close();
        data = fixture();
        transport = "connected";
        liveUpdates = true;
        nextOutcome = null;
        returnRoute = "overview";
        navigate("overview", { replace: true });
        notify("Demo data reset.");
      }, true);
  }
});
modal.addEventListener("close", () => { if (!modal.open) confirmation = null; });
demo.addEventListener("close", () => {
  if (document.activeElement === document.body && matchMedia("(max-width: 999px)").matches) {
    document.querySelector('[data-action="drawer"]')?.focus();
  }
});
window.addEventListener("popstate", readLocation);
window.addEventListener("focus", () => refresh());
window.addEventListener("online", () => refresh());
document.addEventListener("visibilitychange", () => { if (!document.hidden) refresh(); });
matchMedia("(max-width: 999px)").addEventListener("change", (event) => { if (!event.matches && drawer.open) drawer.close(); });

setInterval(() => {
  const time = now();
  if (data.session && data.session.accessUntil <= time) renewSession();
  for (const account of Object.values(data.accounts)) tickWorkspace(account, time);
  if (polling()) {
    updateFreshness();
    if (snapshot && renderedAt !== lastSuccess) renderOperational();
  }
}, 500);
setInterval(() => { if (!document.hidden) refresh(); }, 10000);

readLocation();
