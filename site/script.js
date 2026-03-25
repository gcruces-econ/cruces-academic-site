const {
  profileLinks,
  selectedPapers,
  workingPapers,
  ongoingProjects,
  policyPublications,
  resources
} = window.siteData;

const paperGrid = document.querySelector("#paper-grid");
const searchInput = document.querySelector("#paper-search");
const paperCount = document.querySelector("#paper-count");
const heroLinks = document.querySelector("#hero-links");
const workingList = document.querySelector("#working-list");
const ongoingList = document.querySelector("#ongoing-list");
const policyGrid = document.querySelector("#policy-grid");
const resourceGrid = document.querySelector("#resource-grid");
const documentBasePath = "./assets/documents";

function escapeHtml(value = "") {
  return value
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

  return encodeURI(`${documentBasePath}/${item.file}`);
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

function formatAbstract(abstract) {
  return abstract
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean)
    .map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`)
    .join("");
}

function makeAbstractToggle(panelId, item) {
  if (!item.abstract) {
    return "";
  }

  return `
    <div class="abstract-block">
      <button
        class="button button-inline abstract-toggle"
        type="button"
        data-abstract-toggle
        aria-expanded="false"
        aria-controls="${panelId}"
      >
        Show abstract
      </button>
      <div class="abstract-panel" id="${panelId}" hidden>
        ${formatAbstract(item.abstract)}
      </div>
    </div>
  `;
}

function matchesQuery(values, query) {
  if (!query) {
    return true;
  }

  return values.join(" ").toLowerCase().includes(query);
}

function getSearchQuery() {
  return searchInput.value.trim().toLowerCase();
}

function renderHeroLinks() {
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

function renderPapers(query) {
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
          <p class="paper-description">${escapeHtml(paper.description)}</p>
          ${makeAbstractToggle(abstractId, paper)}
          <div class="card-links">
            ${makeLink(paper.linkLabel || "Open paper", paper)}
          </div>
        </article>
      `;
    })
    .join("");

  return filtered.length;
}

function renderWorkingPapers(query) {
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

function renderStack(listElement, items, options = {}) {
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
          ${item.url || item.file ? `<div class="card-links">${makeLink(item.linkLabel || "Open link", item)}</div>` : ""}
        </article>
      `;
    })
    .join("");
}

function renderPolicies() {
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

function renderResources() {
  resourceGrid.innerHTML = resources
    .map(
      (item) => `
        <article class="resource-card">
          <p class="card-kicker">Archive file</p>
          <h3>${escapeHtml(item.title)}</h3>
          <p>${escapeHtml(item.description)}</p>
          <div class="card-links">
            ${makeLink(item.linkLabel || "Open file", item)}
          </div>
        </article>
      `
    )
    .join("");
}

function renderSearchSummary(query, articleCount, workingCount) {
  if (!query) {
    paperCount.textContent = `${selectedPapers.length} published articles and ${workingPapers.length} working papers currently listed here. Each record can expand to show its abstract.`;
    return;
  }

  paperCount.textContent = `${articleCount} article${articleCount === 1 ? "" : "s"} and ${workingCount} working paper${workingCount === 1 ? "" : "s"} match "${searchInput.value.trim()}".`;
}

function renderSearchResults() {
  const query = getSearchQuery();
  const articleCount = renderPapers(query);
  const workingCount = renderWorkingPapers(query);
  renderSearchSummary(query, articleCount, workingCount);
}

searchInput.addEventListener("input", renderSearchResults);
document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-abstract-toggle]");
  if (!button) {
    return;
  }

  const panel = document.getElementById(button.getAttribute("aria-controls"));
  if (!panel) {
    return;
  }

  const isExpanded = button.getAttribute("aria-expanded") === "true";
  button.setAttribute("aria-expanded", String(!isExpanded));
  button.textContent = isExpanded ? "Show abstract" : "Hide abstract";
  panel.hidden = isExpanded;
});

renderHeroLinks();
renderSearchResults();
renderStack(ongoingList, ongoingProjects, { itemType: "Current project" });
renderPolicies();
renderResources();
