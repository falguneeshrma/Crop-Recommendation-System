
const predictForm = document.getElementById("predictForm");
const predictBtn = document.getElementById("predictBtn");
const fillSampleBtn = document.getElementById("fillSampleBtn");

const resultEmpty = document.getElementById("resultEmpty");
const resultBody = document.getElementById("resultBody");
const resultError = document.getElementById("resultError");
const cropNameEl = document.getElementById("cropName");
const confidenceFill = document.getElementById("confidenceFill");
const confidenceLabel = document.getElementById("confidenceLabel");
const explanationText = document.getElementById("explanationText");

const askForm = document.getElementById("askForm");
const askBtn = document.getElementById("askBtn");
const cropScope = document.getElementById("cropScope");
const questionInput = document.getElementById("questionInput");
const chatLog = document.getElementById("chatLog");

const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

// sample readings roughly typical for rice, just so people can click through the demo fast
const SAMPLE = { N: 90, P: 42, K: 43, temperature: 24.5, humidity: 82, ph: 6.5, rainfall: 220 };

fillSampleBtn.addEventListener("click", () => {
  for (const [key, value] of Object.entries(SAMPLE)) {
    predictForm.elements[key].value = value;
  }
});

// tiny markdown-ish renderer — handles the bullet points and **bold** the LLM tends to use,
// nothing fancier is needed here
function renderExplanation(text) {
  const lines = text.split("\n");
  let html = "";
  let inList = false;

  for (let line of lines) {
    line = line.trim();
    if (!line) continue;

    if (line.startsWith("- ") || line.startsWith("* ")) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${boldify(line.slice(2))}</li>`;
    } else {
      if (inList) { html += "</ul>"; inList = false; }
      html += `<p>${boldify(line)}</p>`;
    }
  }
  if (inList) html += "</ul>";
  return html;
}

function boldify(str) {
  return str.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
}

predictForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = Object.fromEntries(new FormData(predictForm));
  for (const key in data) data[key] = parseFloat(data[key]);

  predictBtn.disabled = true;
  document.getElementById("predictBtnLabel").textContent = "thinking…";
  resultError.classList.add("hidden");

  try {
    const res = await fetch("/predict-and-explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `request failed (${res.status})`);
    }

    const result = await res.json();

    resultEmpty.classList.add("hidden");
    resultBody.classList.remove("hidden");

    cropNameEl.textContent = result.crop;
    const pct = Math.round(result.confidence * 100);
    confidenceFill.style.width = pct + "%";
    confidenceLabel.textContent = pct + "%";
    explanationText.innerHTML = renderExplanation(result.explanation);

    // prefill the ask box with the crop we just got, so follow-ups stay scoped to it
    cropScope.value = result.crop;

  } catch (err) {
    resultBody.classList.add("hidden");
    resultEmpty.classList.add("hidden");
    resultError.textContent = "Couldn't get a recommendation — " + err.message;
    resultError.classList.remove("hidden");
  } finally {
    predictBtn.disabled = false;
    document.getElementById("predictBtnLabel").textContent = "Get Recommendation";
  }
});

askForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = questionInput.value.trim();
  if (!question) return;

  addBubble("user", question);
  questionInput.value = "";
  askBtn.disabled = true;

  const thinkingBubble = addBubble("bot", "…");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        crop: cropScope.value.trim() || null,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `request failed (${res.status})`);
    }

    const result = await res.json();
    thinkingBubble.querySelector(".text").innerHTML = renderExplanation(result.answer);

    if (result.sources && result.sources.length) {
      const tagsEl = document.createElement("div");
      tagsEl.className = "sources";
      tagsEl.innerHTML = result.sources.map(s => `<span class="src-tag">${s}</span>`).join("");
      thinkingBubble.appendChild(tagsEl);
    }

  } catch (err) {
    thinkingBubble.querySelector(".text").textContent = "Something went wrong — " + err.message;
  } finally {
    askBtn.disabled = false;
    chatLog.scrollTop = chatLog.scrollHeight;
  }
});

function addBubble(role, text) {
  const hint = chatLog.querySelector(".chat-hint-msg");
  if (hint) hint.remove();

  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  const textEl = document.createElement("div");
  textEl.className = "text";
  textEl.textContent = text;
  bubble.appendChild(textEl);

  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
  return bubble;
}

// ping /health on load so the status pill actually means something
async function checkBackend() {
  try {
    const res = await fetch("/health");
    if (!res.ok) throw new Error();
    statusDot.classList.add("ok");
    statusText.textContent = "backend online";
  } catch {
    statusDot.classList.add("bad");
    statusText.textContent = "backend unreachable";
  }
}
checkBackend();
