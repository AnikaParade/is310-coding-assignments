const exampleRecords = [
  {
    title: "Cinderella",
    original_tale: "Cinderella",
    creator: "Charles Perrault",
    year: "1697",
    medium: "Literary fairy tale"
  },
  {
    title: "The Bloody Chamber",
    original_tale: "Bluebeard",
    creator: "Angela Carter",
    year: "1979",
    medium: "Short story"
  }
];

const fieldLabels = {
  title: "Title",
  original_tale: "Original fairy tale",
  creator: "Author/creator",
  year: "Publication/release year",
  medium: "Medium",
  protagonist_agency: "Protagonist agency",
  gender_representation: "Gender representation",
  setting_change: "Setting change",
  moral_message: "Moral/message",
  adaptation_notes: "Interpretation notes"
};

const form = document.querySelector("#record-form");
const reviewPanel = document.querySelector("#review-panel");
const reviewDetails = document.querySelector("#review-details");
const status = document.querySelector("#status");
let pendingRecord = null;
const records = [];

function addTableRow(tbody, values) {
  const row = document.createElement("tr");
  values.forEach(value => {
    const cell = document.createElement("td");
    cell.textContent = value || "";
    row.appendChild(cell);
  });
  tbody.appendChild(row);
}

exampleRecords.forEach(record => {
  addTableRow(document.querySelector("#example-records"), [
    record.title, record.original_tale, record.creator, record.year, record.medium
  ]);
});

function getFormRecord() {
  const formData = new FormData(form);
  return Object.fromEntries(formData.entries());
}

function showReview(record) {
  reviewDetails.replaceChildren();
  Object.entries(fieldLabels).forEach(([key, label]) => {
    const dt = document.createElement("dt");
    dt.textContent = label;
    const dd = document.createElement("dd");
    dd.textContent = record[key] || "";
    reviewDetails.append(dt, dd);
  });
  reviewPanel.classList.remove("hidden");
}

form.addEventListener("submit", event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  pendingRecord = getFormRecord();
  showReview(pendingRecord);
  status.textContent = "Review the details before confirming.";
});

document.querySelector("#confirm-record").addEventListener("click", () => {
  if (!pendingRecord) return;
  records.push(pendingRecord);
  renderRecords();
  form.reset();
  pendingRecord = null;
  reviewPanel.classList.add("hidden");
  status.textContent = "Record confirmed and added to the collection. Download JSON to save a copy.";
});

document.querySelector("#edit-record").addEventListener("click", () => {
  reviewPanel.classList.add("hidden");
  status.textContent = "Your entry is still in the form so you can edit it.";
});

document.querySelector("#clear-form").addEventListener("click", () => {
  form.reset();
  pendingRecord = null;
  reviewPanel.classList.add("hidden");
  status.textContent = "Form cleared.";
});

function renderRecords() {
  const tbody = document.querySelector("#collected-records");
  tbody.replaceChildren();
  records.forEach(record => {
    addTableRow(tbody, [
      record.title, record.original_tale, record.creator, record.year,
      record.medium, record.adaptation_notes
    ]);
  });
  document.querySelector("#record-count").textContent =
    `${records.length} record${records.length === 1 ? "" : "s"} added.`;
}

document.querySelector("#download-json").addEventListener("click", () => {
  if (records.length === 0) {
    status.textContent = "Add at least one record before downloading.";
    return;
  }
  const blob = new Blob([JSON.stringify(records, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "fairy_tale_data.json";
  link.click();
  URL.revokeObjectURL(url);
  status.textContent = "JSON download started.";
});
