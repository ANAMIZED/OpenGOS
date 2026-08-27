(function (root) {
  "use strict";
  function getModelContext() {
    if (typeof document !== "undefined" && document.modelContext) return document.modelContext;
    if (typeof navigator !== "undefined" && navigator.modelContext) return navigator.modelContext;
    return null;
  }
  async function registerAll(tools) {
    var ctx = getModelContext();
    var results = [];
    for (var i = 0; i < tools.length; i++) {
      var tool = tools[i];
      try {
        if (!ctx || typeof ctx.registerTool !== "function") { results.push({ ok: false, name: tool.name, reason: "webmcp-unavailable" }); continue; }
        await ctx.registerTool({ name: tool.name, description: tool.description, inputSchema: tool.inputSchema || { type: "object", properties: {} }, execute: tool.execute, annotations: tool.annotations || {} });
        results.push({ ok: true, name: tool.name });
      } catch (err) { results.push({ ok: false, name: tool.name, reason: String(err) }); }
    }
    return results;
  }
  function confirmWrite(message) { return typeof window !== "undefined" && window.confirm ? window.confirm(message) : false; }
  function log(el, line) { if (!el) return; el.textContent = "[" + new Date().toISOString().slice(11, 19) + "] " + line + "\n" + el.textContent; }
  root.ANAMIZEDWebMCP = { supported: function () { return Boolean(getModelContext()); }, registerAll: registerAll, confirmWrite: confirmWrite, log: log };
})(typeof window !== "undefined" ? window : globalThis);
