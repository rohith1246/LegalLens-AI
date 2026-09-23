/**
 * LegalLens AI - Frontend Application Core
 * AI Legal Copilot & Contract Intelligence
 * PromptWars 2026 (Google for Developers Track)
 */

// Application State
const state = {
  activeContract: {
    id: "msa_freelance",
    title: "Freelance Master Services Agreement (MSA)",
    category: "Services & Independent Contractor",
    parties: "Acme Innovations Inc. (Client) & Alex Rivera (Contractor)",
    text: ""
  },
  samples: {},
  analysisData: null,
  comparisonData: null,
  interrogateHistory: [],
  explainerMode: "eli5", // "eli5" | "exec"
  userApiKey: localStorage.getItem("legallens_groq_key") || "",
  workflowStep: 1 // 1 | 2 | 3
};

// ============================================================
// INITIALIZATION
// ============================================================
document.addEventListener("DOMContentLoaded", async () => {
  initLucide();
  setupEventListeners();
  await checkEngineStatus();
  await fetchSampleContracts();
  
  // Load default freelance MSA
  if (state.samples["msa_freelance"]) {
    setContract(state.samples["msa_freelance"]);
  }
  
  // Set default redline texts
  if (state.samples["msa_freelance"] && state.samples["msa_comparison_v2"]) {
    document.getElementById("diffTextA").value = state.samples["msa_freelance"].text;
    document.getElementById("diffTextB").value = state.samples["msa_comparison_v2"].text;
  }

  // Initial workflow step
  goToWorkflowStep(1);

  // Initial background audit prime
  await runFullAudit(true);
});

function initLucide() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// ============================================================
// EVENT LISTENERS SETUP
// ============================================================
function setupEventListeners() {
  // Tab Switching
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      switchTab(tabId);
    });
  });

  // Sample Dropdown
  const sampleDropdownBtn = document.getElementById("sampleDropdownBtn");
  const sampleDropdownMenu = document.getElementById("sampleDropdownMenu");
  if (sampleDropdownBtn && sampleDropdownMenu) {
    sampleDropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      sampleDropdownMenu.classList.toggle("hidden");
    });
    document.addEventListener("click", () => {
      sampleDropdownMenu.classList.add("hidden");
    });
  }

  // API Key Modal
  document.getElementById("apiKeyModalBtn").addEventListener("click", openApiKeyModal);

  // Export Report Modal
  document.getElementById("exportReportBtn").addEventListener("click", openExportModal);

  // Inspector Toggle
  document.getElementById("toggleInspectorBtn").addEventListener("click", toggleInspector);

  // File Upload
  document.getElementById("fileUploadInput").addEventListener("change", handleFileUpload);

  // Run Analysis Button
  document.getElementById("runAnalysisBtn").addEventListener("click", () => {
    runFullAudit();
    goToWorkflowStep(3);
  });

  // Textarea input sync
  const contractInput = document.getElementById("contractTextInput");
  contractInput.addEventListener("input", (e) => {
    state.activeContract.text = e.target.value;
    updateCharCount();
  });

  // Explainer View Toggles
  document.getElementById("viewEli5Btn").addEventListener("click", () => setExplainerMode("eli5"));
  document.getElementById("viewExecBtn").addEventListener("click", () => setExplainerMode("exec"));

  // Redliner Compare
  document.getElementById("runComparisonBtn").addEventListener("click", runComparison);

  // Interrogator Form
  document.getElementById("interrogateForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("interrogateInput");
    const q = input.value.trim();
    if (q) {
      askInterrogator(q);
      input.value = "";
    }
  });

  // Scenario Simulator Form
  document.getElementById("scenarioForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("scenarioInput");
    const scenario = input.value.trim();
    if (scenario) {
      runScenarioSimulation(scenario);
    }
  });

  // Redraft Drafter Form
  document.getElementById("redraftForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const clause = document.getElementById("redraftClauseInput").value.trim();
    const goal = document.getElementById("redraftGoalSelect").value;
    if (clause) {
      runClauseRedraft(clause, goal);
    }
  });

  // Multilingual Form
  document.getElementById("translateForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const lang = document.getElementById("targetLanguageSelect").value;
    runTranslation(lang);
  });
}

// ============================================================
// SYSTEM & SAMPLES API CALLS
// ============================================================
async function checkEngineStatus() {
  try {
    const res = await fetch("/api/status", {
      headers: getAuthHeaders()
    });
    const data = await res.json();
    const label = document.getElementById("engineStatusLabel");
    if (data.has_custom_key || state.userApiKey) {
      label.innerText = "Engine: Groq LLaMA 3.3 70B (Ultra-Fast)";
    } else {
      label.innerText = "Engine: LegalLens High-Fidelity Engine";
    }
  } catch (err) {
    console.error("Status check failed:", err);
  }
}

async function fetchSampleContracts() {
  try {
    const res = await fetch("/api/samples");
    const data = await res.json();
    if (data.samples) {
      data.samples.forEach(s => {
        state.samples[s.id] = s;
      });
    }
  } catch (err) {
    console.error("Failed to load sample contracts:", err);
  }
}

function getAuthHeaders() {
  const headers = { "Content-Type": "application/json" };
  if (state.userApiKey) {
    headers["X-Groq-Key"] = state.userApiKey;
  }
  return headers;
}

// ============================================================
// WORKFLOW STEPPER PIPELINE MANAGEMENT
// ============================================================
function goToWorkflowStep(step) {
  state.workflowStep = step;

  const step1El = document.getElementById("stepper-step-1");
  const step2El = document.getElementById("stepper-step-2");
  const step3El = document.getElementById("stepper-step-3");
  const sec1 = document.getElementById("workflow-step-1");
  const sec2 = document.getElementById("workflow-step-2");
  const sec3 = document.getElementById("workflow-step-3");
  const backBtn = document.getElementById("workflowBackBtn");
  const nextBtn = document.getElementById("workflowNextBtn");
  const nextText = document.getElementById("workflowNextText");

  // Reset circle classes helper
  const setCircleStyle = (el, type) => {
    const circle = el.querySelector(".step-circle");
    if (type === "active") {
      circle.className = "step-circle w-9 h-9 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm shadow-md transition-all";
    } else if (type === "completed") {
      circle.className = "step-circle w-9 h-9 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-sm shadow-md transition-all";
    } else {
      circle.className = "step-circle w-9 h-9 rounded-full bg-slate-100 text-slate-600 border border-slate-300 flex items-center justify-center font-bold text-sm transition-all";
    }
  };

  // Step 1 State
  if (step === 1) {
    setCircleStyle(step1El, "active");
    setCircleStyle(step2El, "inactive");
    setCircleStyle(step3El, "inactive");

    sec1.classList.remove("hidden");
    sec2.classList.add("hidden");
    sec3.classList.add("hidden");

    backBtn.classList.add("hidden");
    nextText.innerText = "Select AI Objective";
  } 
  // Step 2 State
  else if (step === 2) {
    setCircleStyle(step1El, "completed");
    setCircleStyle(step2El, "active");
    setCircleStyle(step3El, "inactive");

    sec1.classList.remove("hidden"); // keep document preview context
    sec2.classList.remove("hidden");
    sec3.classList.add("hidden");

    backBtn.classList.remove("hidden");
    nextText.innerText = "View Intelligence";
  } 
  // Step 3 State
  else if (step === 3) {
    setCircleStyle(step1El, "completed");
    setCircleStyle(step2El, "completed");
    setCircleStyle(step3El, "active");

    sec1.classList.add("hidden");
    sec2.classList.add("hidden");
    sec3.classList.remove("hidden");

    backBtn.classList.remove("hidden");
    nextText.innerText = "Restart Pipeline ↺";
  }

  initLucide();
}

function nextWorkflowStep() {
  if (state.workflowStep === 1) {
    goToWorkflowStep(2);
  } else if (state.workflowStep === 2) {
    executeObjective("tab-simplifier");
  } else {
    goToWorkflowStep(1);
  }
}

function prevWorkflowStep() {
  if (state.workflowStep === 3) {
    goToWorkflowStep(2);
  } else if (state.workflowStep === 2) {
    goToWorkflowStep(1);
  }
}

async function executeObjective(tabId) {
  // Show animated pipeline processing dialog
  const modal = document.getElementById("workflowProcessingModal");
  modal.classList.remove("hidden");
  modal.setAttribute("aria-hidden", "false");

  const stage1 = document.getElementById("pipe-stage-1");
  const stage2 = document.getElementById("pipe-stage-2");
  const stage3 = document.getElementById("pipe-stage-3");

  // Stage 1 animation
  stage1.className = "flex items-center space-x-2 text-indigo-700 font-bold";
  initLucide();

  // Run or prime audit if not yet loaded
  if (!state.analysisData) {
    await runFullAudit(true);
  }

  await new Promise(r => setTimeout(r, 300));
  stage1.className = "flex items-center space-x-2 text-emerald-700 font-medium";
  stage1.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i><span>1. Ingestion & token bounding complete</span>`;

  stage2.className = "flex items-center space-x-2 text-indigo-700 font-bold";
  initLucide();

  await new Promise(r => setTimeout(r, 350));
  stage2.className = "flex items-center space-x-2 text-emerald-700 font-medium";
  stage2.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i><span>2. Liability & commercial exposure analyzed</span>`;

  stage3.className = "flex items-center space-x-2 text-indigo-700 font-bold";
  stage3.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i><span>3. Executive intelligence & actions synthesized</span>`;
  initLucide();

  await new Promise(r => setTimeout(r, 200));

  // Hide modal and switch
  modal.classList.add("hidden");
  modal.setAttribute("aria-hidden", "true");

  switchTab(tabId);
  goToWorkflowStep(3);

  // If Redline Diff tab was chosen, run comparison
  if (tabId === "tab-redline" && !state.comparisonData) {
    loadRedlineComparisonSamples();
  }
}

// ============================================================
// TAB NAVIGATION (WCAG 2.1 Accessible)
// ============================================================
function switchTab(tabId) {
  // Tab buttons styling and ARIA states
  document.querySelectorAll(".tab-btn").forEach(btn => {
    const isCurrent = btn.getAttribute("data-tab") === tabId;
    btn.setAttribute("aria-selected", isCurrent ? "true" : "false");
    btn.tabIndex = isCurrent ? 0 : -1;
    if (isCurrent) {
      btn.classList.add("active", "border-indigo-600", "text-indigo-900", "bg-slate-50");
      btn.classList.remove("border-transparent", "text-slate-500");
    } else {
      btn.classList.remove("active", "border-indigo-600", "text-indigo-900", "bg-slate-50");
      btn.classList.add("border-transparent", "text-slate-500");
    }
  });

  // Tab contents visibility
  document.querySelectorAll(".tab-content").forEach(content => {
    if (content.id === tabId) {
      content.classList.remove("hidden");
    } else {
      content.classList.add("hidden");
    }
  });

  initLucide();
}

// ============================================================
// CONTRACT MANAGEMENT & LOADING
// ============================================================
function setContract(sample) {
  state.activeContract = {
    id: sample.id,
    title: sample.title,
    category: sample.category || "General Agreement",
    parties: sample.parties || "Contracting Parties",
    text: sample.text
  };

  document.getElementById("activeContractTitle").innerText = state.activeContract.title;
  document.getElementById("activeContractCategory").innerText = state.activeContract.category;
  document.getElementById("activeContractParties").innerText = `Parties: ${state.activeContract.parties}`;
  document.getElementById("contractTextInput").value = state.activeContract.text;
  
  updateCharCount();
}

function loadSampleContract(id) {
  if (state.samples[id]) {
    setContract(state.samples[id]);
    runFullAudit();
  }
}

function loadSampleContractV1() {
  if (state.samples["msa_freelance"]) {
    document.getElementById("diffTextA").value = state.samples["msa_freelance"].text;
  }
}

function loadSampleContractV2() {
  if (state.samples["msa_comparison_v2"]) {
    document.getElementById("diffTextB").value = state.samples["msa_comparison_v2"].text;
  }
}

function loadRedlineComparisonSamples() {
  loadSampleContractV1();
  loadSampleContractV2();
  switchTab("tab-redline");
  runComparison();
}

function updateCharCount() {
  const len = state.activeContract.text.length;
  const words = state.activeContract.text.trim().split(/\s+/).filter(Boolean).length;
  document.getElementById("charCountLabel").innerText = `${len.toLocaleString()} chars • ${words.toLocaleString()} words`;
}

function toggleInspector() {
  const inspector = document.getElementById("contractInspector");
  const btn = document.getElementById("toggleInspectorBtn");
  const btnText = document.getElementById("inspectorBtnText");
  const isHidden = inspector.classList.contains("hidden");
  
  if (isHidden) {
    inspector.classList.remove("hidden");
    inspector.setAttribute("aria-hidden", "false");
    btn.setAttribute("aria-expanded", "true");
    btnText.innerText = "Hide Contract Text";
  } else {
    inspector.classList.add("hidden");
    inspector.setAttribute("aria-hidden", "true");
    btn.setAttribute("aria-expanded", "false");
    btnText.innerText = "View Contract Text";
  }
}

async function handleFileUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const btn = document.getElementById("runAnalysisBtn");
  const originalText = btn.innerHTML;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Extracting...</span>`;
  initLucide();

  try {
    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    if (data.error) {
      alert(`Upload Error: ${data.error}`);
      return;
    }

    state.activeContract = {
      id: "uploaded_doc",
      title: data.filename,
      category: "Uploaded Document",
      parties: "Detected from content",
      text: data.text
    };

    setContract(state.activeContract);
    await runFullAudit();
    goToWorkflowStep(2);
  } catch (err) {
    alert(`File upload failed: ${err.message}`);
  } finally {
    btn.innerHTML = originalText;
    initLucide();
  }
}

// ============================================================
// 1. CONTRACT SIMPLIFIER & RISK RADAR
// ============================================================
async function runFullAudit(isSilent = false) {
  const btn = document.getElementById("runAnalysisBtn");
  const origHTML = btn.innerHTML;
  if (!isSilent) {
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Auditing...</span>`;
    initLucide();
  }

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        text: state.activeContract.text,
        api_key: state.userApiKey
      })
    });

    const data = await res.json();
    if (data.error) {
      if (!isSilent) alert(`Analysis error: ${data.error}`);
      return;
    }

    state.analysisData = data;
    renderAnalysisData(data);
  } catch (err) {
    console.error("Audit failed:", err);
  } finally {
    if (!isSilent) {
      btn.innerHTML = origHTML;
      initLucide();
    }
  }
}

function renderAnalysisData(data) {
  // 1. Health Score & Meter
  const score = Math.max(0, Math.min(100, data.overall_health_score || 50));
  const scoreDisplay = document.getElementById("scoreDisplay");
  scoreDisplay.innerText = score;

  // Circle gauge math (circumference = 2 * PI * 42 ~= 264)
  const circle = document.getElementById("scoreMeterCircle");
  const circumference = 264;
  const offset = circumference - (score / 100) * circumference;
  circle.style.strokeDashoffset = offset;

  // Colors based on score
  const badge = document.getElementById("riskTierBadge");
  if (score >= 75) {
    circle.style.stroke = "#10b981"; // green
    badge.className = "mt-2 px-3 py-1 text-xs font-bold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200";
    badge.innerText = data.risk_tier || "Low Risk / Safe Terms";
  } else if (score >= 50) {
    circle.style.stroke = "#f59e0b"; // amber
    badge.className = "mt-2 px-3 py-1 text-xs font-bold rounded-full bg-amber-50 text-amber-700 border border-amber-200";
    badge.innerText = data.risk_tier || "Moderate Risk";
  } else {
    circle.style.stroke = "#f43f5e"; // rose
    badge.className = "mt-2 px-3 py-1 text-xs font-bold rounded-full bg-rose-50 text-rose-700 border border-rose-200";
    badge.innerText = data.risk_tier || "High Risk Exposure";
  }

  // 2. Key Metrics
  if (data.key_metrics) {
    document.getElementById("metricFinancial").innerText = data.key_metrics.total_financial_exposure || "N/A";
    document.getElementById("metricPayment").innerText = data.key_metrics.payment_terms || "N/A";
    document.getElementById("metricTermination").innerText = data.key_metrics.termination_notice || "N/A";
    document.getElementById("metricJurisdiction").innerText = data.key_metrics.governing_jurisdiction || "N/A";
  }

  // 3. Explainer Summary
  updateExplainerContent();

  // 4. Rights & Obligations Matrix
  if (data.rights_and_obligations) {
    const yourRights = data.rights_and_obligations.your_rights || [];
    const yourObligations = data.rights_and_obligations.your_obligations || [];
    const counterObligations = data.rights_and_obligations.counterparty_obligations || [];

    document.getElementById("yourRightsList").innerHTML = yourRights.map(r => `<li>• ${escapeHtml(r)}</li>`).join("") || "<li>None specified</li>";
    document.getElementById("yourObligationsList").innerHTML = yourObligations.map(o => `<li>• ${escapeHtml(o)}</li>`).join("") || "<li>None specified</li>";
    document.getElementById("counterpartyObligationsList").innerHTML = counterObligations.map(c => `<li>• ${escapeHtml(c)}</li>`).join("") || "<li>None specified</li>";
  }

  // 5. Red Flags Radar
  const redFlagsContainer = document.getElementById("redFlagsContainer");
  if (data.red_flags && data.red_flags.length > 0) {
    redFlagsContainer.innerHTML = data.red_flags.map((rf) => {
      let severityBadge = "bg-rose-50 text-rose-700 border-rose-200";
      if (rf.severity === "Medium") severityBadge = "bg-amber-50 text-amber-700 border-amber-200";
      if (rf.severity === "Low") severityBadge = "bg-slate-100 text-slate-700 border-slate-200";

      return `
        <div class="redflag-card bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-2">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div class="flex items-center space-x-2">
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md border ${severityBadge}">${escapeHtml(rf.severity || 'High')}</span>
              <span class="text-xs font-bold text-slate-900">${escapeHtml(rf.clause_reference || 'Clause')}</span>
              <span class="text-[11px] text-slate-500">(${escapeHtml(rf.category || 'Legal Risk')})</span>
            </div>
            <button onclick="prepareClauseRedraft('${escapeHtml(rf.clause_reference)}', '${escapeHtml(rf.problem)}')" class="self-start sm:self-auto flex items-center space-x-1 text-xs font-semibold text-fuchsia-700 hover:text-fuchsia-800 bg-fuchsia-50 hover:bg-fuchsia-100 px-2.5 py-1 rounded-md border border-fuchsia-200 transition">
              <i data-lucide="pencil-ruler" class="w-3.5 h-3.5"></i>
              <span>Draft Counter-Clause</span>
            </button>
          </div>
          <div class="text-xs text-slate-700 font-medium">
            <strong class="text-slate-900">The Problem:</strong> ${escapeHtml(rf.problem)}
          </div>
          <div class="text-xs text-rose-800 bg-rose-50 p-2.5 rounded-lg border border-rose-200 font-medium">
            <strong>Real-World Consequence:</strong> ${escapeHtml(rf.real_world_consequence)}
          </div>
          <div class="text-xs text-emerald-800 bg-emerald-50 p-2.5 rounded-lg border border-emerald-200 font-medium">
            <strong>Recommended Remedy:</strong> ${escapeHtml(rf.recommended_remedy)}
          </div>
        </div>
      `;
    }).join("");
  } else {
    redFlagsContainer.innerHTML = `<div class="p-4 text-xs text-slate-500 bg-white rounded-xl border border-slate-200">No critical red flags detected.</div>`;
  }

  // 6. Action Checklist
  if (data.action_checklist) {
    const checklist = document.getElementById("actionChecklist");
    checklist.innerHTML = data.action_checklist.map(item => `
      <li class="flex items-start space-x-2">
        <i data-lucide="arrow-right-circle" class="w-4 h-4 text-indigo-600 shrink-0 mt-0.5"></i>
        <span>${escapeHtml(item)}</span>
      </li>
    `).join("");
  }

  initLucide();
}

function setExplainerMode(mode) {
  state.explainerMode = mode;
  const eli5Btn = document.getElementById("viewEli5Btn");
  const execBtn = document.getElementById("viewExecBtn");

  if (mode === "eli5") {
    eli5Btn.className = "px-3 py-1 text-xs rounded-md bg-indigo-600 text-white font-semibold shadow-sm transition focus:outline-none focus:ring-1 focus:ring-indigo-400";
    eli5Btn.setAttribute("aria-checked", "true");
    execBtn.className = "px-3 py-1 text-xs rounded-md text-slate-600 hover:text-slate-900 font-semibold transition focus:outline-none focus:ring-1 focus:ring-indigo-400";
    execBtn.setAttribute("aria-checked", "false");
    document.getElementById("summaryHeading").innerText = "Layman's Plain-English Breakdown";
  } else {
    execBtn.className = "px-3 py-1 text-xs rounded-md bg-indigo-600 text-white font-semibold shadow-sm transition focus:outline-none focus:ring-1 focus:ring-indigo-400";
    execBtn.setAttribute("aria-checked", "true");
    eli5Btn.className = "px-3 py-1 text-xs rounded-md text-slate-600 hover:text-slate-900 font-semibold transition focus:outline-none focus:ring-1 focus:ring-indigo-400";
    eli5Btn.setAttribute("aria-checked", "false");
    document.getElementById("summaryHeading").innerText = "Executive Commercial Summary";
  }

  updateExplainerContent();
}

function updateExplainerContent() {
  if (!state.analysisData) return;
  const summaryBox = document.getElementById("summaryContent");
  if (state.explainerMode === "eli5") {
    summaryBox.innerText = state.analysisData.layman_eli5 || state.analysisData.executive_summary || "No summary available.";
  } else {
    summaryBox.innerText = state.analysisData.executive_summary || state.analysisData.layman_eli5 || "No summary available.";
  }
}

// ============================================================
// 2. CONTRACT REDLINER & SEMANTIC DIFF ENGINE
// ============================================================
async function runComparison() {
  const textA = document.getElementById("diffTextA").value.trim();
  const textB = document.getElementById("diffTextB").value.trim();

  if (!textA || !textB) {
    alert("Please enter or load contract text for both Version 1 and Version 2.");
    return;
  }

  const btn = document.getElementById("runComparisonBtn");
  const origHTML = btn.innerHTML;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Comparing...</span>`;
  initLucide();

  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        text_a: textA,
        text_b: textB,
        api_key: state.userApiKey
      })
    });

    const data = await res.json();
    if (data.error) {
      alert(`Comparison error: ${data.error}`);
      return;
    }

    state.comparisonData = data;
    renderComparisonData(data);
  } catch (err) {
    console.error("Comparison failed:", err);
  } finally {
    btn.innerHTML = origHTML;
    initLucide();
  }
}

function renderComparisonData(data) {
  // Delta Badge
  const deltaBadge = document.getElementById("redlineRiskDeltaBadge");
  const delta = data.net_risk_delta || "Neutral";
  deltaBadge.innerText = delta;

  if (delta.toLowerCase().includes("favorable")) {
    deltaBadge.className = "px-2.5 py-0.5 text-xs font-bold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200";
  } else if (delta.toLowerCase().includes("risk")) {
    deltaBadge.className = "px-2.5 py-0.5 text-xs font-bold rounded-full bg-rose-50 text-rose-700 border border-rose-200";
  } else {
    deltaBadge.className = "px-2.5 py-0.5 text-xs font-bold rounded-full bg-slate-100 text-slate-700 border border-slate-200";
  }

  document.getElementById("redlineScoreDelta").innerText = data.score_delta || "";
  document.getElementById("redlineSummary").innerText = data.comparison_summary || "";
  document.getElementById("redlineVerdict").innerText = data.negotiation_verdict || "Review changes";

  // Clause shifts list
  const shiftsContainer = document.getElementById("clauseShiftsContainer");
  if (data.clause_changes && data.clause_changes.length > 0) {
    shiftsContainer.innerHTML = data.clause_changes.map(change => {
      let impactBadge = "bg-emerald-50 text-emerald-700 border-emerald-200";
      if (change.impact === "High Risk") impactBadge = "bg-rose-50 text-rose-700 border-rose-200";
      if (change.impact === "Neutral") impactBadge = "bg-slate-100 text-slate-700 border-slate-200";

      return `
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-slate-900">${escapeHtml(change.section_title)}</span>
            <div class="flex items-center space-x-2">
              <span class="px-2 py-0.5 text-[10px] uppercase font-bold rounded bg-slate-200 text-slate-700">${escapeHtml(change.change_type || 'Modified')}</span>
              <span class="px-2 py-0.5 text-[10px] font-bold rounded border ${impactBadge}">${escapeHtml(change.impact)}</span>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div class="bg-white p-2.5 rounded-lg border border-slate-200">
              <span class="text-[10px] uppercase font-bold text-slate-500 block mb-1">Version 1 (Original)</span>
              <p class="text-slate-700">${escapeHtml(change.original_intent)}</p>
            </div>
            <div class="bg-indigo-50/50 p-2.5 rounded-lg border border-indigo-200">
              <span class="text-[10px] uppercase font-bold text-indigo-700 block mb-1">Version 2 (Redline)</span>
              <p class="text-slate-800">${escapeHtml(change.revised_intent)}</p>
            </div>
          </div>
          <div class="text-xs text-indigo-900 bg-indigo-50/80 p-2.5 rounded-lg border border-indigo-200">
            <strong>Legal Impact & Analysis:</strong> ${escapeHtml(change.analysis)}
          </div>
        </div>
      `;
    }).join("");
  } else {
    shiftsContainer.innerHTML = `<div class="p-3 text-xs text-slate-500">No major substantive clause shifts detected.</div>`;
  }

  initLucide();
}

// ============================================================
// 3. CLAUSE INTERROGATOR (GROUNDED COPILOT)
// ============================================================
async function askInterrogator(question) {
  const container = document.getElementById("interrogateMessages");

  // User Message
  const userMsgEl = document.createElement("div");
  userMsgEl.className = "flex items-start space-x-3 justify-end";
  userMsgEl.innerHTML = `
    <div class="bg-indigo-600 text-white p-3.5 rounded-2xl max-w-xl text-xs shadow-sm font-medium">
      ${escapeHtml(question)}
    </div>
    <div class="w-7 h-7 rounded-lg bg-indigo-700 flex items-center justify-center shrink-0 text-white">
      <i data-lucide="user" class="w-4 h-4"></i>
    </div>
  `;
  container.appendChild(userMsgEl);
  container.scrollTop = container.scrollHeight;
  initLucide();

  // Assistant Loading Placeholder
  const loadingEl = document.createElement("div");
  loadingEl.className = "flex items-start space-x-3";
  loadingEl.innerHTML = `
    <div class="w-7 h-7 rounded-lg bg-sky-600 flex items-center justify-center shrink-0 text-white">
      <i data-lucide="bot" class="w-4 h-4"></i>
    </div>
    <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-2xl max-w-xl text-xs text-slate-500 flex items-center space-x-2">
      <i data-lucide="loader-2" class="w-4 h-4 animate-spin text-sky-600"></i>
      <span>Researching contract clauses...</span>
    </div>
  `;
  container.appendChild(loadingEl);
  container.scrollTop = container.scrollHeight;
  initLucide();

  try {
    const res = await fetch("/api/interrogate", {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        text: state.activeContract.text,
        question: question,
        history: state.interrogateHistory,
        api_key: state.userApiKey
      })
    });

    const data = await res.json();
    loadingEl.remove();

    if (data.error) {
      const errEl = document.createElement("div");
      errEl.className = "text-xs text-rose-600 p-2 font-bold";
      errEl.innerText = `Error: ${data.error}`;
      container.appendChild(errEl);
      return;
    }

    // Render Assistant Response
    const assistantMsgEl = document.createElement("div");
    assistantMsgEl.className = "flex items-start space-x-3";

    let citationsHtml = "";
    if (data.clause_citations && data.clause_citations.length > 0) {
      citationsHtml = `
        <div class="space-y-1.5 pt-2 border-t border-slate-200">
          <span class="text-[10px] uppercase font-bold text-sky-700 block">Verified Clause Citations:</span>
          ${data.clause_citations.map(c => `
            <div class="bg-white p-2.5 rounded-lg border border-sky-200 text-xs">
              <div class="flex items-center justify-between mb-1">
                <strong class="text-sky-900">${escapeHtml(c.clause_name)}</strong>
                <button onclick="highlightInInspector('${escapeHtml(c.clause_name)}')" class="text-[10px] text-sky-600 font-semibold hover:underline">View in Contract</button>
              </div>
              <blockquote class="italic text-slate-700 border-l-2 border-sky-500 pl-2 text-[11px] mb-1">"${escapeHtml(c.quote)}"</blockquote>
              <p class="text-slate-600 text-[11px]">${escapeHtml(c.explanation)}</p>
            </div>
          `).join("")}
        </div>
      `;
    }

    let tacticalHtml = "";
    if (data.tactical_advice) {
      tacticalHtml = `
        <div class="bg-amber-50 border border-amber-200 p-2.5 rounded-lg text-[11px] text-amber-800 font-medium">
          <strong>Tactical Precaution:</strong> ${escapeHtml(data.tactical_advice)}
        </div>
      `;
    }

    let followupsHtml = "";
    if (data.suggested_followups && data.suggested_followups.length > 0) {
      followupsHtml = `
        <div class="pt-1 flex flex-wrap gap-1.5">
          <span class="text-[10px] text-slate-400 self-center">Follow-up:</span>
          ${data.suggested_followups.map(f => `
            <button onclick="askInterrogator('${escapeHtml(f)}')" class="text-[10px] bg-white hover:bg-slate-100 text-sky-700 px-2 py-0.5 rounded-md border border-slate-200 shadow-sm transition">
              ${escapeHtml(f)}
            </button>
          `).join("")}
        </div>
      `;
    }

    assistantMsgEl.innerHTML = `
      <div class="w-7 h-7 rounded-lg bg-sky-600 flex items-center justify-center shrink-0 text-white">
        <i data-lucide="bot" class="w-4 h-4"></i>
      </div>
      <div class="bg-slate-50 border border-slate-200 p-4 rounded-2xl max-w-2xl text-slate-800 space-y-3 shadow-sm">
        <p class="leading-relaxed text-xs font-medium">${escapeHtml(data.answer)}</p>
        ${citationsHtml}
        ${tacticalHtml}
        ${followupsHtml}
      </div>
    `;

    container.appendChild(assistantMsgEl);
    container.scrollTop = container.scrollHeight;
    initLucide();

    // Store in history
    state.interrogateHistory.push({ role: "user", content: question });
    state.interrogateHistory.push({ role: "assistant", content: data.answer });

  } catch (err) {
    loadingEl.remove();
    console.error("Interrogation failed:", err);
  }
}

function highlightInInspector(clauseName) {
  toggleInspector();
  const inspector = document.getElementById("contractInspector");
  inspector.classList.remove("hidden");
  document.getElementById("inspectorBtnText").innerText = "Hide Contract Text";

  const textarea = document.getElementById("contractTextInput");
  const fullText = textarea.value;
  
  // Clean clause search term (e.g. "Section 6")
  const match = clauseName.match(/(?:Section|Clause)\s*(\d+)/i);
  let searchTarget = clauseName;
  if (match) {
    searchTarget = match[0];
  }

  const idx = fullText.toLowerCase().indexOf(searchTarget.toLowerCase());
  if (idx !== -1) {
    textarea.focus();
    textarea.setSelectionRange(idx, idx + searchTarget.length + 80);
    textarea.scrollTop = (idx / fullText.length) * textarea.scrollHeight;
  }
}

// ============================================================
// 4. "WHAT-IF" SCENARIO SIMULATOR
// ============================================================
function setScenario(text) {
  document.getElementById("scenarioInput").value = text;
  runScenarioSimulation(text);
}

async function runScenarioSimulation(scenario) {
  const submitBtn = document.querySelector("#scenarioForm button[type='submit']");
  const origHTML = submitBtn.innerHTML;
  submitBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Simulating...</span>`;
  initLucide();

  try {
    const res = await fetch("/api/simulate", {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        text: state.activeContract.text,
        scenario: scenario,
        api_key: state.userApiKey
      })
    });

    const data = await res.json();
    if (data.error) {
      alert(`Simulation error: ${data.error}`);
      return;
    }

    renderScenarioData(data, scenario);
  } catch (err) {
    console.error("Simulation failed:", err);
  } finally {
    submitBtn.innerHTML = origHTML;
    initLucide();
  }
}

function renderScenarioData(data, scenario) {
  document.getElementById("scenarioTitle").innerText = data.scenario_title || scenario;
  document.getElementById("scenarioOutcome").innerText = data.projected_outcome || "";

  // Leverage Badge
  const badge = document.getElementById("scenarioLeverageBadge");
  const lev = data.user_leverage || "Moderate";
  badge.innerText = lev;
  if (lev.toLowerCase().includes("strong")) {
    badge.className = "px-2.5 py-0.5 text-xs font-bold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200";
  } else if (lev.toLowerCase().includes("moderate")) {
    badge.className = "px-2.5 py-0.5 text-xs font-bold rounded-full bg-amber-50 text-amber-700 border border-amber-200";
  } else {
    badge.className = "px-2.5 py-0.5 text-xs font-bold rounded-full bg-rose-50 text-rose-700 border border-rose-200";
  }

  // Action plan list
  const actionList = document.getElementById("scenarioActionPlan");
  if (data.step_by_step_action_plan) {
    actionList.innerHTML = data.step_by_step_action_plan.map(s => `<li>• ${escapeHtml(s)}</li>`).join("");
  }

  // Traps list
  const trapsList = document.getElementById("scenarioTraps");
  if (data.traps_to_avoid) {
    trapsList.innerHTML = data.traps_to_avoid.map(t => `<li>• ${escapeHtml(t)}</li>`).join("");
  }

  initLucide();
}

// ============================================================
// 5. SMART COUNTER-CLAUSE DRAFTER
// ============================================================
function prepareClauseRedraft(clauseRef, problem) {
  switchTab("tab-redraft");
  goToWorkflowStep(3);
  const textarea = document.getElementById("redraftClauseInput");
  
  // Search the active contract text for this clause if possible
  const fullText = state.activeContract.text;
  let snippet = "";
  const match = clauseRef.match(/(?:Section|Clause)\s*(\d+)/i);
  if (match) {
    const term = match[0];
    const idx = fullText.indexOf(term);
    if (idx !== -1) {
      snippet = fullText.substring(idx, idx + 600).trim();
    }
  }

  textarea.value = snippet || `${clauseRef}: ${problem}`;
  runClauseRedraft(textarea.value, "balanced");
}

async function runClauseRedraft(clause, goal) {
  const submitBtn = document.querySelector("#redraftForm button[type='submit']");
  const origHTML = submitBtn.innerHTML;
  submitBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Drafter Active...</span>`;
  initLucide();

  try {
    const res = await fetch("/api/redraft", {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        clause: clause,
        goal: goal,
        context: state.activeContract.text,
        api_key: state.userApiKey
      })
    });

    const data = await res.json();
    if (data.error) {
      alert(`Redraft error: ${data.error}`);
      return;
    }

    renderRedraftData(data);
  } catch (err) {
    console.error("Redraft failed:", err);
  } finally {
    submitBtn.innerHTML = origHTML;
    initLucide();
  }
}

function renderRedraftData(data) {
  document.getElementById("redraftCritique").innerText = data.original_clause_critique || "";
  document.getElementById("redraftWording").innerText = data.recommended_redraft || "";
  document.getElementById("redraftEmailPitch").innerText = data.negotiation_email_pitch || "";
  initLucide();
}

// ============================================================
// 6. MULTILINGUAL ACCESS ENGINE
// ============================================================
async function runTranslation(targetLanguage) {
  const submitBtn = document.querySelector("#translateForm button[type='submit']");
  const origHTML = submitBtn.innerHTML;
  submitBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Translating...</span>`;
  initLucide();

  // Translate executive summary or first 1500 chars of contract
  const textToTranslate = state.analysisData?.executive_summary || state.activeContract.text.substring(0, 1500);

  try {
    const res = await fetch("/api/translate", {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        text: textToTranslate,
        target_language: targetLanguage,
        api_key: state.userApiKey
      })
    });

    const data = await res.json();
    if (data.error) {
      alert(`Translation error: ${data.error}`);
      return;
    }

    renderTranslationData(data);
  } catch (err) {
    console.error("Translation failed:", err);
  } finally {
    submitBtn.innerHTML = origHTML;
    initLucide();
  }
}

function renderTranslationData(data) {
  document.getElementById("transTargetLangBadge").innerText = data.target_language || "Translated";
  document.getElementById("transTitle").innerText = data.translated_title || "Summary";
  document.getElementById("transPlainExplanation").innerText = data.plain_explanation_target_lang || "";
  document.getElementById("transContent").innerText = data.translated_content || "";

  // Glossary
  const glossaryContainer = document.getElementById("transGlossary");
  if (data.key_terms_glossary && data.key_terms_glossary.length > 0) {
    glossaryContainer.innerHTML = data.key_terms_glossary.map(item => `
      <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
        <div class="flex items-center justify-between text-xs mb-1">
          <strong class="text-slate-900">${escapeHtml(item.english_term)}</strong>
          <span class="text-teal-700 font-bold">${escapeHtml(item.translated_term)}</span>
        </div>
        <p class="text-[11px] text-slate-600 leading-snug">${escapeHtml(item.meaning)}</p>
      </div>
    `).join("");
  } else {
    glossaryContainer.innerHTML = `<div class="text-xs text-slate-500">No glossary terms.</div>`;
  }

  initLucide();
}

// ============================================================
// MODAL & UTILITY FUNCTIONS
// ============================================================
function openApiKeyModal() {
  const modal = document.getElementById("apiKeyModal");
  modal.classList.remove("hidden");
  document.getElementById("groqApiKeyInput").value = state.userApiKey;
  initLucide();
}

function closeApiKeyModal() {
  document.getElementById("apiKeyModal").classList.add("hidden");
}

function saveApiKey() {
  const key = document.getElementById("groqApiKeyInput").value.trim();
  state.userApiKey = key;
  if (key) {
    localStorage.setItem("legallens_groq_key", key);
  } else {
    localStorage.removeItem("legallens_groq_key");
  }

  // Send to backend session
  fetch("/api/set-api-key", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: key })
  }).then(() => {
    checkEngineStatus();
    closeApiKeyModal();
    alert(key ? "Groq API Key activated for live LLaMA 3.3 70B inference!" : "Reverted to Built-in High-Fidelity Engine.");
  });
}

function clearApiKey() {
  document.getElementById("groqApiKeyInput").value = "";
  saveApiKey();
}

function openExportModal() {
  const modal = document.getElementById("exportModal");
  modal.classList.remove("hidden");

  // Generate complete Markdown Audit Report
  const d = state.analysisData || {};
  const markdown = `
# LEGALLENS AI — CONTRACT AUDIT REPORT
Generated by LegalLens AI for PromptWars 2026

DOCUMENT TITLE: ${state.activeContract.title}
PARTIES: ${state.activeContract.parties}
OVERALL SAFETY SCORE: ${d.overall_health_score || 'N/A'} / 100
RISK LEVEL: ${d.risk_tier || 'N/A'}

=======================================================
1. EXECUTIVE BRIEFING
=======================================================
${d.executive_summary || 'N/A'}

=======================================================
2. PLAIN-ENGLISH (LAYMAN / ELI5) EXPLANATION
=======================================================
${d.layman_eli5 || 'N/A'}

=======================================================
3. CORE COMMERCIAL TERMS & FINANCIAL EXPOSURE
=======================================================
- Financial Exposure: ${d.key_metrics?.total_financial_exposure || 'N/A'}
- Payment Terms: ${d.key_metrics?.payment_terms || 'N/A'}
- Termination Notice: ${d.key_metrics?.termination_notice || 'N/A'}
- Governing Law & Forum: ${d.key_metrics?.governing_jurisdiction || 'N/A'}

=======================================================
4. RED FLAGS & CONTRACTUAL ASYMMETRIES
=======================================================
${(d.red_flags || []).map((rf, i) => `
[${rf.id || `RF-${i+1}`}] ${rf.clause_reference} (Severity: ${rf.severity})
Category: ${rf.category}
Problem: ${rf.problem}
Real-World Consequence: ${rf.real_world_consequence}
Recommended Remedy: ${rf.recommended_remedy}
`).join("\n")}

=======================================================
5. PRE-SIGNING ACTION CHECKLIST
=======================================================
${(d.action_checklist || []).map(item => `[ ] ${item}`).join("\n")}

=======================================================
DISCLAIMER: This report was generated by an AI assistant for informational purposes and does not constitute formal legal representation. Always consult licensed legal counsel for binding commercial decisions.
`.trim();

  document.getElementById("auditReportMarkdown").innerText = markdown;
  initLucide();
}

function closeExportModal() {
  document.getElementById("exportModal").classList.add("hidden");
}

function copyContractText() {
  const text = document.getElementById("contractTextInput").value;
  navigator.clipboard.writeText(text).then(() => alert("Contract text copied to clipboard!"));
}

function copyElementText(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => alert("Copied to clipboard!"));
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
