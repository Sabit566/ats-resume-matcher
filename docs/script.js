const API_BASE = "https://ats-resume-matcher-bvyb.onrender.com"; // same-origin; change to e.g. "http://localhost:8000" if serving frontend separately

const els = {
  apiStatus: document.getElementById("apiStatus"),
  dropzone: document.getElementById("dropzone"),
  fileInput: document.getElementById("fileInput"),
  dzFileName: document.getElementById("dzFileName"),
  resumeTextArea: document.getElementById("resumeTextArea"),
  jdTextArea: document.getElementById("jdTextArea"),
  scanBtn: document.getElementById("scanBtn"),
  errorMsg: document.getElementById("errorMsg"),
  inputDeck: document.getElementById("inputDeck"),
  resultsDeck: document.getElementById("resultsDeck"),
  rescanBtn: document.getElementById("rescanBtn"),
  gaugeScore: document.getElementById("gaugeScore"),
  gaugeLevel: document.getElementById("gaugeLevel"),
  candidateName: document.getElementById("candidateName"),
  candidateMeta: document.getElementById("candidateMeta"),
  methodNote: document.getElementById("methodNote"),
  strengthsList: document.getElementById("strengthsList"),
  missingByCategory: document.getElementById("missingByCategory"),
  suggestionsList: document.getElementById("suggestionsList"),
};

const ERROR_MESSAGES = {
  chart: "Unable to render charts. Resume analysis completed successfully. Charts could not be displayed.",
};

let selectedFile = null;

class ApiError extends Error {
  constructor(message, response) {
    super(message);
    this.name = "ApiError";
    this.response = response;
  }
}

class RenderError extends Error {
  constructor(message, cause) {
    super(message);
    this.name = "RenderError";
    this.cause = cause;
  }
}

function setError(message) {
  els.errorMsg.textContent = message;
}

function clearError() {
  els.errorMsg.textContent = "";
}

function setScanButtonState(inProgress, label) {
  els.scanBtn.disabled = inProgress;
  els.scanBtn.querySelector(".scan-btn-label").textContent = label;
}

function getElement(id) {
  return document.getElementById(id);
}

function createChartSafe(canvasId, config) {
  try {
    return window.ChartManager.createChart(canvasId, config);
  } catch (cause) {
    throw new RenderError(`Could not initialize chart for ${canvasId}`, cause);
  }
}

async function fetchMatch(form) {
  const res = await fetch(`${API_BASE}/api/match`, { method: "POST", body: form });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new ApiError(`Server returned ${res.status}${body ? ` - ${body}` : ""}`, res);
  }
  return res.json();
}

// ---- health check ----
fetch(`${API_BASE}/api/health`)
  .then(r => r.ok ? r.json() : Promise.reject())
  .then(() => {
    els.apiStatus.classList.add("ok");
    els.apiStatus.innerHTML = `<span class="dot"></span> engine ready`;
  })
  .catch(() => {
    els.apiStatus.classList.add("err");
    els.apiStatus.innerHTML = `<span class="dot"></span> engine unreachable`;
  });

// ---- dropzone wiring ----
els.dropzone.addEventListener("click", () => els.fileInput.click());
els.dropzone.addEventListener("keydown", e => {
  if (e.key === "Enter" || e.key === " ") els.fileInput.click();
});
els.fileInput.addEventListener("change", e => setFile(e.target.files[0]));

["dragenter", "dragover"].forEach(evt =>
  els.dropzone.addEventListener(evt, e => {
    e.preventDefault();
    els.dropzone.classList.add("drag");
  })
);
["dragleave", "drop"].forEach(evt =>
  els.dropzone.addEventListener(evt, e => {
    e.preventDefault();
    els.dropzone.classList.remove("drag");
  })
);
els.dropzone.addEventListener("drop", e => {
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
});

function setFile(file) {
  selectedFile = file;
  els.dzFileName.textContent = file ? `Selected: ${file.name}` : "";
}

// ---- scan ----
els.scanBtn.addEventListener("click", runScan);
els.rescanBtn.addEventListener("click", () => {
  els.resultsDeck.hidden = true;
  els.inputDeck.hidden = false;
  clearError();
});

async function runScan() {
  clearError();
  const jdText = els.jdTextArea.value.trim();
  const resumeText = els.resumeTextArea.value.trim();

  if (!jdText) {
    setError("Paste a job description first.");
    return;
  }
  if (!selectedFile && !resumeText) {
    setError("Upload a resume file or paste resume text.");
    return;
  }

  setScanButtonState(true, "Scanning…");

  try {
    const form = new FormData();
    form.append("jd_text", jdText);
    if (selectedFile) {
      form.append("resume_file", selectedFile);
    } else {
      form.append("resume_text", resumeText);
    }

    const data = await fetchMatch(form);
    els.inputDeck.hidden = true;
    els.resultsDeck.hidden = false;

    try {
      renderResults(data);
    } catch (err) {
      if (err instanceof RenderError) {
        console.error("Render error", err, err.cause);
        setError(ERROR_MESSAGES.chart);
      } else {
        throw err;
      }
    }
  } catch (err) {
    console.error("Scan failed", err);
    if (err instanceof ApiError) {
      setError(`Scan failed: ${err.message}`);
    } else if (err instanceof RenderError) {
      setError(ERROR_MESSAGES.chart);
    } else {
      setError(`Scan failed: ${err.message || "Unknown error"}`);
    }
  } finally {
    setScanButtonState(false, "Run Scan");
  }
}

// ---- rendering ----
function levelColor(level) {
  return { Excellent: "#6ee7a0", Good: "#5ee7a4", Moderate: "#f5b955", Low: "#fb7768" }[level] || "#5ee7a4";
}

function renderResults(data) {
  const color = levelColor(data.match_level);

  els.gaugeScore.textContent = `${Math.round(data.overall_score || 0)}%`;
  els.gaugeScore.style.color = color;
  els.gaugeLevel.textContent = data.match_level || "—";

  els.candidateName.textContent = data.candidate?.name || "Candidate";
  const metaParts = [data.candidate?.email, data.candidate?.phone].filter(Boolean);
  els.candidateMeta.textContent = metaParts.join("  ·  ");
  els.methodNote.textContent = `Semantic engine: ${data.semantic_method || "unknown"}`;

  renderBars(data.breakdown || {});
  renderGauge(data.overall_score || 0, color);
  renderPie(data.breakdown || {});
  renderRadar(data.breakdown || {});
  renderStrengths(Array.isArray(data.strengths) ? data.strengths : []);
  renderMissing(data.skills?.missing_by_category || {});
  renderSuggestions(Array.isArray(data.suggestions) ? data.suggestions : []);
}

function renderGauge(score, color) {
  createChartSafe("gaugeChart", {
    type: "doughnut",
    data: {
      datasets: [{
        data: [score, Math.max(0, 100 - score)],
        backgroundColor: [color, "#1c2029"],
        borderWidth: 0,
      }],
    },
    options: {
      cutout: "78%",
      rotation: -90,
      circumference: 360,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      animation: { animateRotate: true, duration: 900 },
    },
  });
}

function renderBars(breakdown) {
  const map = {
    semantic: breakdown.semantic_similarity || 0,
    skills: breakdown.skills_match || 0,
    experience: breakdown.experience_match || 0,
    education: breakdown.education_match || 0,
    keyword: breakdown.keyword_coverage || 0,
  };

  Object.entries(map).forEach(([key, val]) => {
    const fill = getElement(`bar-${key}`);
    const label = getElement(`val-${key}`);
    if (!fill || !label) {
      console.warn(`Missing bar or label element for ${key}`);
      return;
    }
    requestAnimationFrame(() => { fill.style.width = `${val}%`; });
    label.textContent = `${val}%`;
  });
}

function renderPie(breakdown) {
  createChartSafe("pieChart", {
    type: "pie",
    data: {
      labels: ["Semantic", "Skills", "Experience", "Education", "Keywords"],
      datasets: [{
        data: [
          (breakdown.semantic_similarity || 0) * 0.40,
          (breakdown.skills_match || 0) * 0.25,
          (breakdown.experience_match || 0) * 0.15,
          (breakdown.education_match || 0) * 0.10,
          (breakdown.keyword_coverage || 0) * 0.10,
        ],
        backgroundColor: ["#5eead4", "#6ee7a0", "#f5b955", "#fb7768", "#8ea2ff"],
        borderColor: "#191d25",
        borderWidth: 2,
      }],
    },
    options: {
      plugins: {
        legend: { position: "bottom", labels: { color: "#8b92a4", font: { family: "IBM Plex Mono", size: 11 } } },
      },
    },
  });
}

function renderRadar(breakdown) {
  createChartSafe("radarChart", {
    type: "radar",
    data: {
      labels: ["Semantic", "Skills", "Experience", "Education", "Keywords"],
      datasets: [{
        label: "Match %",
        data: [
          breakdown.semantic_similarity || 0,
          breakdown.skills_match || 0,
          breakdown.experience_match || 0,
          breakdown.education_match || 0,
          breakdown.keyword_coverage || 0,
        ],
        backgroundColor: "rgba(94,234,212,0.15)",
        borderColor: "#5ee7a4",
        pointBackgroundColor: "#5ee7a4",
      }],
    },
    options: {
      scales: {
        r: {
          angleLines: { color: "#262b36" },
          grid: { color: "#262b36" },
          pointLabels: { color: "#8b92a4", font: { family: "IBM Plex Mono", size: 10 } },
          ticks: { display: false, backdropColor: "transparent" },
          suggestedMin: 0, suggestedMax: 100,
        },
      },
      plugins: { legend: { display: false } },
    },
  });
}

function renderStrengths(strengths) {
  els.strengthsList.innerHTML = "";
  if (!Array.isArray(strengths) || strengths.length === 0) {
    els.strengthsList.innerHTML = `<li class="empty-note">No strong overlaps detected yet.</li>`;
    return;
  }
  strengths.forEach(s => {
    const li = document.createElement("li");
    li.textContent = s;
    els.strengthsList.appendChild(li);
  });
}

function renderMissing(byCategory) {
  els.missingByCategory.innerHTML = "";
  const entries = Object.entries(byCategory || {});
  if (!entries.length) {
    els.missingByCategory.innerHTML = `<p class="chip-list empty-note">Nothing missing — great coverage.</p>`;
    return;
  }
  entries.forEach(([cat, skills]) => {
    const block = document.createElement("div");
    block.className = "missing-category";
    const h4 = document.createElement("h4");
    h4.textContent = cat;
    const ul = document.createElement("ul");
    ul.className = "chip-list";
    (Array.isArray(skills) ? skills : []).forEach(sk => {
      const li = document.createElement("li");
      li.textContent = sk;
      ul.appendChild(li);
    });
    block.appendChild(h4);
    block.appendChild(ul);
    els.missingByCategory.appendChild(block);
  });
}

function renderSuggestions(suggestions) {
  els.suggestionsList.innerHTML = "";
  (Array.isArray(suggestions) ? suggestions : []).forEach(s => {
    const li = document.createElement("li");
    li.textContent = s;
    els.suggestionsList.appendChild(li);
  });
}
