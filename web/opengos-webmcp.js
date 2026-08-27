(function () {
  "use strict";
  var W = window.ANAMIZEDWebMCP;
  var logEl = document.getElementById("webmcp-log");
  var statusEl = document.getElementById("webmcp-status");
  var PROGRAMS = [
    { id: "oss-public-goods", name: "Open-source / public-goods grants", bias: "open-source" },
    { id: "infra", name: "Agent infrastructure pilots", bias: "infrastructure" },
    { id: "research", name: "Safety + evaluation research", bias: "research" }
  ];
  var tools = [
    { name: "status", description: "OpenGOS page health.", inputSchema: { type: "object", properties: {} }, annotations: { readOnlyHint: true }, execute: async function () { return { name: "opengos", surface: "webmcp", status: "ok", programs: PROGRAMS.length }; } },
    { name: "list_programs", description: "List demo grant program buckets.", inputSchema: { type: "object", properties: {} }, annotations: { readOnlyHint: true }, execute: async function () { return { programs: PROGRAMS }; } },
    { name: "match_need", description: "Rank demo programs against a need. Local heuristic.", inputSchema: { type: "object", properties: { need: { type: "string" } }, required: ["need"] }, annotations: { readOnlyHint: true },
      execute: async function (params) {
        var need = String(params.need || "").toLowerCase();
        var ranked = PROGRAMS.map(function (p) { return { program: p, score: need.indexOf(p.bias) >= 0 ? 2 : 1 }; }).sort(function (a, b) { return b.score - a.score; });
        return { need: params.need, ranked: ranked };
      } },
    { name: "draft_outline", description: "Outline stub only. Does not submit. Requires confirmation.", inputSchema: { type: "object", properties: { program_id: { type: "string" }, project: { type: "string" } }, required: ["program_id", "project"] }, annotations: { readOnlyHint: false },
      execute: async function (params) {
        if (!W.confirmWrite("Draft an outline stub for " + params.project + "?")) return { cancelled: true };
        W.log(logEl, "draft_outline " + params.program_id);
        return { submitted: false, program_id: params.program_id, project: params.project, outline: ["Problem and beneficiaries", "Work plan", "Verify contract", "Budget and evaluation ownership"], note: "Stub only. Paid draft is a Desk / x402 SKU." };
      } }
  ];
  async function boot() {
    statusEl.textContent = W.supported() ? "WebMCP available — grants tools registered" : "WebMCP API not in this browser.";
    W.log(logEl, JSON.stringify(await W.registerAll(tools)));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
