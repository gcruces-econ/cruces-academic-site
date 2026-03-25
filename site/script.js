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
const profileGrid = document.querySelector("#profile-grid");
const workingList = document.querySelector("#working-list");
const ongoingList = document.querySelector("#ongoing-list");
const policyGrid = document.querySelector("#policy-grid");
const resourceGrid = document.querySelector("#resource-grid");
const researchTotal = document.querySelector("#research-total");
const articleTotal = document.querySelector("#article-total");
const workingTotal = document.querySelector("#working-total");
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

function makeLink(label, item) {
  return `<a class="text-link" href="${itemHref(item)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`;
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

function renderProfiles() {
  profileGrid.innerHTML = profileLinks
    .map(
      (item) => `
        <article class="resource-card">
          <p class="card-kicker">Profile</p>
          <h3>${escapeHtml(item.title)}</h3>
          <p>${escapeHtml(item.description)}</p>
          <div class="card-links">
            ${makeLink(item.linkLabel || "Open link", item)}
          </div>
        </article>
      `
    )
    .join("");
}

function renderHighlights() {
  researchTotal.textContent = String(selectedPapers.length + workingPapers.length);
  articleTotal.textContent = String(selectedPapers.length);
  workingTotal.textContent = String(workingPapers.length);
}

function renderPapers(query) {
  const filtered = selectedPapers.filter((paper) =>
    matchesQuery([paper.title, paper.authors, paper.venue, paper.description, paper.year], query)
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
    .map(
      (paper) => `
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
          <div class="card-links">
            ${makeLink(paper.linkLabel || "View on IDEAS", paper)}
          </div>
        </article>
      `
    )
    .join("");

  return filtered.length;
}

function renderWorkingPapers(query) {
  const filtered = workingPapers.filter((item) =>
    matchesQuery([item.title, item.description, item.status], query)
  );

  renderStack(workingList, filtered, {
    itemType: "Working paper",
    emptyTitle: "No working papers match this search",
    emptyDescription: "Try another term to search the full IDEAS/RePEc working paper list."
  });

  return filtered.length;
}

function renderStack(listElement, items, options = {}) {
  const {
    itemType = null,
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
    .map(
      (item) => `
        <article class="stack-item">
          <div class="stack-item-header">
            <div>
              ${itemType ? `<p class="card-kicker">${escapeHtml(itemType)}</p>` : ""}
              <h3>${escapeHtml(item.title)}</h3>
            </div>
            ${item.status ? `<span class="status-pill">${escapeHtml(item.status)}</span>` : ""}
          </div>
          <p>${escapeHtml(item.description)}</p>
          ${item.url || item.file ? `<div class="card-links">${makeLink(item.linkLabel || "Open link", item)}</div>` : ""}
        </article>
      `
    )
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
    paperCount.textContent = `${selectedPapers.length} published articles and ${workingPapers.length} working papers pulled from IDEAS/RePEc. Search updates both sections below.`;
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

renderProfiles();
renderHighlights();
renderSearchResults();
renderStack(ongoingList, ongoingProjects, { itemType: "Current project" });
renderPolicies();
renderResources();
