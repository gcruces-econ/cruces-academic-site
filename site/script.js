const DATA_PATH = "./data/site-data.json";
const DOCUMENT_BASE_PATH = "./assets/documents";

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function itemHref(item) {
  if (item.url) {
    return item.url;
  }

  return encodeURI(`${DOCUMENT_BASE_PATH}/${item.file}`);
}

function itemLinkAttributes(item) {
  if (item.url && item.url.startsWith("mailto:")) {
    return "";
  }

  return ' target="_blank" rel="noreferrer"';
}

function makeLink(label, item) {
  return `<a class="text-link" href="${itemHref(item)}"${itemLinkAttributes(item)}>${escapeHtml(label)}</a>`;
}

function citationKey(item) {
  return item.url || item.file || item.title || "";
}

function makeCitationButtons(item) {
  const key = citationKey(item);
  if (!key) {
    return "";
  }

  const buttons = [];
  if (item.citationApa) {
    buttons.push(`
      <button
        class="button button-inline citation-button"
        type="button"
        data-citation-copy="apa"
        data-citation-key="${escapeHtml(key)}"
        data-default-label="APA Citation"
      >
        APA Citation
      </button>
    `);
  }

  if (item.citationBibtex) {
    buttons.push(`
      <button
        class="button button-inline citation-button"
        type="button"
        data-citation-copy="bibtex"
        data-citation-key="${escapeHtml(key)}"
        data-default-label="BibTeX Citation"
      >
        BibTeX Citation
      </button>
    `);
  }

  return buttons.join("");
}

function makeCardActions(item, primaryLabel) {
  if (!(item.url || item.file)) {
    return "";
  }

  return `<div class="card-links">${makeLink(primaryLabel, item)}</div>`;
}

function formatAbstract(abstract) {
  return abstract
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean)
    .map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`)
    .join("");
}

function makeAbstractToggle(panelId, item) {
  const actions = [];

  if (item.abstract) {
    actions.push(`
      <button
        class="button button-inline abstract-toggle"
        type="button"
        data-abstract-toggle
        aria-expanded="false"
        aria-controls="${panelId}"
      >
        Show abstract
      </button>
    `);
  }

  const citationButtons = makeCitationButtons(item);
  if (citationButtons) {
    actions.push(citationButtons);
  }

  if (!actions.length) {
    return "";
  }

  return `
    <div class="abstract-block">
      <div class="abstract-actions">
        ${actions.join("")}
      </div>
      ${item.abstract ? `
        <div class="abstract-panel" id="${panelId}" hidden>
          ${formatAbstract(item.abstract)}
        </div>
      ` : ""}
    </div>
  `;
}

function matchesQuery(values, query) {
  if (!query) {
    return true;
  }

  return values
    .filter(Boolean)
    .join(" ")
    .toLowerCase()
    .includes(query);
}

function renderHeroLinks(heroLinks, profileLinks) {
  if (!heroLinks) {
    return;
  }

  heroLinks.innerHTML = profileLinks
    .map(
      (item) => `
        <a class="mini-link" href="${itemHref(item)}"${itemLinkAttributes(item)}>
          <span class="mini-link-copy">
            <strong>${escapeHtml(item.title)}</strong>
            <span>${escapeHtml(item.description)}</span>
          </span>
        </a>
      `
    )
    .join("");
}

function renderPapers(paperGrid, selectedPapers, query) {
  if (!paperGrid) {
    return 0;
  }

  const filtered = selectedPapers.filter((paper) =>
    matchesQuery(
      [paper.title, paper.authors, paper.venue, paper.description, paper.year, paper.abstract || ""],
      query
    )
  );

  if (!filtered.length) {
    paperGrid.innerHTML = `
      <article class="paper-card empty-state">
        <p class="card-kicker">No matches</p>
        <h3>No published articles match this search</h3>
        <p class="paper-description">Try a broader term such as tax, labor, poverty, or Argentina.</p>
      </article>
    `;

    return 0;
  }

  paperGrid.innerHTML = filtered
    .map((paper, index) => {
      const abstractId = `paper-abstract-${index}`;

      return `
        <article class="paper-card">
          <div class="paper-card-header">
            <div>
              <p class="card-kicker">Published article</p>
              <h3>${escapeHtml(paper.title)}</h3>
              <p class="paper-meta">${escapeHtml(paper.authors)}</p>
            </div>
            <span class="paper-year">${escapeHtml(paper.year)}</span>
          </div>
          <p class="paper-venue">${escapeHtml(paper.venue)}</p>
          ${makeAbstractToggle(abstractId, paper)}
          ${makeCardActions(paper, paper.linkLabel || "Open paper")}
        </article>
      `;
    })
    .join("");

  return filtered.length;
}

function renderStack(listElement, items, options = {}) {
  if (!listElement) {
    return;
  }

  const {
    itemType = null,
    idPrefix = "stack-item",
    emptyTitle = "No items to display",
    emptyDescription = "There are no items available in this section."
  } = options;

  if (!items.length) {
    listElement.innerHTML = `
      <article class="stack-item empty-state">
        ${itemType ? `<p class="card-kicker">${escapeHtml(itemType)}</p>` : ""}
        <h3>${escapeHtml(emptyTitle)}</h3>
        <p>${escapeHtml(emptyDescription)}</p>
      </article>
    `;
    return;
  }

  listElement.innerHTML = items
    .map((item, index) => {
      const abstractId = `${idPrefix}-abstract-${index}`;

      return `
        <article class="stack-item">
          <div class="stack-item-header">
            <div>
              ${itemType ? `<p class="card-kicker">${escapeHtml(itemType)}</p>` : ""}
              <h3>${escapeHtml(item.title)}</h3>
            </div>
            ${item.status ? `<span class="status-pill">${escapeHtml(item.status)}</span>` : ""}
          </div>
          <p>${escapeHtml(item.description)}</p>
          ${makeAbstractToggle(abstractId, item)}
          ${makeCardActions(item, item.linkLabel || "Open link")}
        </article>
      `;
    })
    .join("");
}

function renderWorkingPapers(workingList, workingPapers, query) {
  const filtered = workingPapers.filter((item) =>
    matchesQuery([item.title, item.description, item.status, item.abstract || ""], query)
  );

  renderStack(workingList, filtered, {
    itemType: "Working paper",
    idPrefix: "working-paper",
    emptyTitle: "No working papers match this search",
    emptyDescription: "Try another term to search the full working paper archive."
  });

  return filtered.length;
}

function renderPolicies(policyGrid, policyPublications) {
  if (!policyGrid) {
    return;
  }

  policyGrid.innerHTML = policyPublications
    .map(
      (item) => `
        <article class="policy-card">
          <div class="paper-card-header">
            <div>
              <p class="card-kicker">Policy or book</p>
              <h3>${escapeHtml(item.title)}</h3>
            </div>
            <span class="paper-year">${escapeHtml(item.year)}</span>
          </div>
          <p>${escapeHtml(item.description)}</p>
          <div class="card-links">
            ${makeLink(item.linkLabel || "Open publication", item)}
          </div>
        </article>
      `
    )
    .join("");
}

function renderSearchSummary(paperCount, searchInput, selectedPapers, workingPapers, query, articleCount, workingCount) {
  if (!paperCount || !searchInput) {
    return;
  }

  if (!query) {
    paperCount.textContent = `${selectedPapers.length} published articles and ${workingPapers.length} working papers currently listed here. Each record can expand to show its abstract.`;
  } else {
    paperCount.textContent = `${articleCount} article${articleCount === 1 ? "" : "s"} and ${workingCount} working paper${workingCount === 1 ? "" : "s"} match "${searchInput.value.trim()}".`;
  }
}

function buildCitationStore(data) {
  const store = new Map();

  for (const collection of [data.selectedPapers || [], data.workingPapers || []]) {
    for (const item of collection) {
      const key = citationKey(item);
      if (!key || (!item.citationApa && !item.citationBibtex)) {
        continue;
      }

      store.set(key, {
        apa: item.citationApa || "",
        bibtex: item.citationBibtex || ""
      });
    }
  }

  return store;
}

async function copyTextToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return;
    } catch (error) {
      console.warn("Clipboard API failed, falling back to execCommand.", error);
    }
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.top = "0";
  textarea.style.left = "-9999px";
  textarea.style.opacity = "0";
  document.body.append(textarea);
  textarea.focus();
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);
  const copied = document.execCommand("copy");
  textarea.remove();

  if (!copied) {
    throw new Error("Copy command failed");
  }
}

function updateButtonLabel(button, label) {
  const defaultLabel = button.dataset.defaultLabel || button.textContent;
  clearTimeout(button._labelResetTimer);
  button.textContent = label;
  button._labelResetTimer = setTimeout(() => {
    button.textContent = defaultLabel;
  }, 1800);
}

function bindCardInteractions(citationStore) {
  document.addEventListener("click", async (event) => {
    const citationButton = event.target.closest("[data-citation-copy]");
    if (citationButton) {
      const kind = citationButton.getAttribute("data-citation-copy");
      const key = citationButton.getAttribute("data-citation-key");
      const citation = citationStore.get(key)?.[kind];

      if (!citation) {
        updateButtonLabel(citationButton, "Unavailable");
        return;
      }

      try {
        await copyTextToClipboard(citation);
        updateButtonLabel(citationButton, kind === "apa" ? "APA copied" : "BibTeX copied");
      } catch (error) {
        console.error(error);
        updateButtonLabel(citationButton, "Copy failed");
      }

      return;
    }

    const abstractButton = event.target.closest("[data-abstract-toggle]");
    if (!abstractButton) {
      return;
    }

    const panel = document.getElementById(abstractButton.getAttribute("aria-controls"));
    if (!panel) {
      return;
    }

    const isExpanded = abstractButton.getAttribute("aria-expanded") === "true";
    abstractButton.setAttribute("aria-expanded", String(!isExpanded));
    abstractButton.textContent = isExpanded ? "Show abstract" : "Hide abstract";
    panel.hidden = isExpanded;
  });
}

async function loadSiteData() {
  const response = await fetch(DATA_PATH);

  if (!response.ok) {
    throw new Error(`Unable to load site data (${response.status})`);
  }

  return response.json();
}

function renderSite(data) {
  const {
    profileLinks = [],
    selectedPapers = [],
    workingPapers = [],
    ongoingProjects = [],
    policyPublications = []
  } = data;

  const paperGrid = document.querySelector("#paper-grid");
  const searchInput = document.querySelector("#paper-search");
  const paperCount = document.querySelector("#paper-count");
  const heroLinks = document.querySelector("#hero-links");
  const workingList = document.querySelector("#working-list");
  const ongoingList = document.querySelector("#ongoing-list");
  const policyGrid = document.querySelector("#policy-grid");

  renderHeroLinks(heroLinks, profileLinks);

  const renderSearchResults = () => {
    const query = searchInput ? searchInput.value.trim().toLowerCase() : "";
    const articleCount = renderPapers(paperGrid, selectedPapers, query);
    const workingCount = renderWorkingPapers(workingList, workingPapers, query);

    renderSearchSummary(
      paperCount,
      searchInput,
      selectedPapers,
      workingPapers,
      query,
      articleCount,
      workingCount
    );
  };

  renderSearchResults();
  renderStack(ongoingList, ongoingProjects, { itemType: "Current project" });
  renderPolicies(policyGrid, policyPublications);

  if (searchInput) {
    searchInput.addEventListener("input", renderSearchResults);
  }
}

function renderDataError(error) {
  console.error(error);

  const paperGrid = document.querySelector("#paper-grid");
  const workingList = document.querySelector("#working-list");
  const policyGrid = document.querySelector("#policy-grid");

  const message = `
    <article class="paper-card empty-state">
      <p class="card-kicker">Content unavailable</p>
      <h3>Site data could not be loaded</h3>
      <p class="paper-description">Run the Quarto pre-render step or <code>python3 scripts/build_site_content.py</code> to regenerate <code>data/site-data.json</code>.</p>
    </article>
  `;

  if (paperGrid) {
    paperGrid.innerHTML = message;
  }

  if (workingList) {
    workingList.innerHTML = message;
  }

  if (policyGrid) {
    policyGrid.innerHTML = message;
  }
}

async function initSite() {
  try {
    const data = await loadSiteData();
    bindCardInteractions(buildCitationStore(data));
    renderSite(data);
  } catch (error) {
    renderDataError(error);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSite, { once: true });
} else {
  initSite();
}
