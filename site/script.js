const { paperTags, selectedPapers, workingPapers, ongoingProjects, policyPublications, resources } =
  window.siteData;

const paperGrid = document.querySelector("#paper-grid");
const tagFilters = document.querySelector("#tag-filters");
const searchInput = document.querySelector("#paper-search");
const paperCount = document.querySelector("#paper-count");
const workingList = document.querySelector("#working-list");
const ongoingList = document.querySelector("#ongoing-list");
const policyGrid = document.querySelector("#policy-grid");
const resourceGrid = document.querySelector("#resource-grid");
const toggleAbstractsButton = document.querySelector("#toggle-abstracts");
const documentBasePath = "./assets/documents";

let activeTag = "All";
let allAbstractsOpen = false;

function fileHref(file) {
  return encodeURI(`${documentBasePath}/${file}`);
}

function makeLink(label, file) {
  return `<a class="text-link" href="${fileHref(file)}" target="_blank" rel="noreferrer">${label}</a>`;
}

function renderTagFilters() {
  tagFilters.innerHTML = paperTags
    .map(
      (tag) => `
        <button
          type="button"
          class="filter-chip ${tag === activeTag ? "active" : ""}"
          data-tag="${tag}"
        >
          ${tag}
        </button>
      `
    )
    .join("");

  tagFilters.querySelectorAll(".filter-chip").forEach((button) => {
    button.addEventListener("click", () => {
      activeTag = button.dataset.tag;
      renderTagFilters();
      renderPapers();
    });
  });
}

function paperMatchesSearch(paper, query) {
  if (!query) {
    return true;
  }

  const haystack = [paper.title, paper.authors, paper.venue, paper.description, paper.abstract, ...paper.tags]
    .join(" ")
    .toLowerCase();

  return haystack.includes(query);
}

function renderPapers() {
  const query = searchInput.value.trim().toLowerCase();
  const filtered = selectedPapers.filter((paper) => {
    const tagMatch = activeTag === "All" || paper.tags.includes(activeTag);
    return tagMatch && paperMatchesSearch(paper, query);
  });

  paperCount.textContent = `${filtered.length} paper${filtered.length === 1 ? "" : "s"} shown`;

  if (!filtered.length) {
    paperGrid.innerHTML = `
      <article class="paper-card">
        <h3>No papers match the current filter</h3>
        <p class="paper-description">Try another tag or broaden the search terms.</p>
      </article>
    `;
    return;
  }

  paperGrid.innerHTML = filtered
    .map(
      (paper, index) => `
        <article class="paper-card" style="animation-delay:${index * 35}ms">
          <div class="paper-card-header">
            <div>
              <h3>${paper.title}</h3>
              <p class="paper-meta">${paper.authors}<br />${paper.venue}</p>
            </div>
            <span class="paper-year">${paper.year}</span>
          </div>
          <ul class="paper-tags">
            ${paper.tags.map((tag) => `<li>${tag}</li>`).join("")}
          </ul>
          <p class="paper-description">${paper.description}</p>
          <details ${allAbstractsOpen ? "open" : ""}>
            <summary>Abstract</summary>
            <p>${paper.abstract}</p>
          </details>
          <div class="card-links">
            ${makeLink("Open paper", paper.file)}
          </div>
        </article>
      `
    )
    .join("");
}

function renderStack(listElement, items) {
  listElement.innerHTML = items
    .map(
      (item) => `
        <article class="stack-item">
          <div class="stack-item-header">
            <h3>${item.title}</h3>
            <span class="status-pill">${item.status}</span>
          </div>
          <p>${item.description}</p>
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
            <h3>${item.title}</h3>
            <span class="paper-year">${item.year}</span>
          </div>
          <p>${item.description}</p>
          <div class="card-links">
            ${makeLink("Open publication", item.file)}
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
          <h3>${item.title}</h3>
          <p>${item.description}</p>
          <div class="card-links">
            ${makeLink("Download", item.file)}
          </div>
        </article>
      `
    )
    .join("");
}

searchInput.addEventListener("input", renderPapers);

toggleAbstractsButton.addEventListener("click", () => {
  allAbstractsOpen = !allAbstractsOpen;
  toggleAbstractsButton.textContent = allAbstractsOpen ? "Close all abstracts" : "Open all abstracts";
  renderPapers();
});

renderTagFilters();
renderPapers();
renderStack(workingList, workingPapers);
renderStack(ongoingList, ongoingProjects);
renderPolicies();
renderResources();
