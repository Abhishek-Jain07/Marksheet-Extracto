const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const extractBtn = document.getElementById('extract-btn');
const previewContainer = document.getElementById('preview-container');
const imagePreview = document.getElementById('image-preview');
const fileName = document.getElementById('file-name');
const jsonOutput = document.getElementById('json-output');
const loader = document.getElementById('loader');
const viewContents = document.querySelectorAll('.view-content');
const tabBtns = document.querySelectorAll('.tab-btn');
const formattedContent = document.getElementById('formatted-content');

let selectedFile = null;

// Drag & Drop
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFile(e.target.files[0]);
});

function handleFile(file) {
    selectedFile = file;
    fileName.textContent = file.name;
    previewContainer.classList.remove('hidden');
    extractBtn.disabled = false;

    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => imagePreview.src = e.target.result;
        reader.readAsDataURL(file);
    } else {
        imagePreview.src = "https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg"; // PDF placeholder
    }
}

// Extract
extractBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // UI Reset
    loader.classList.remove('hidden');
    jsonOutput.textContent = '';
    formattedContent.innerHTML = '';
    extractBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/extract', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Extraction failed');
        }

        const data = await response.json();
        const jsonStr = JSON.stringify(data, null, 2);
        jsonOutput.textContent = jsonStr;
        renderFormatted(data);
    } catch (error) {
        jsonOutput.textContent = `Error: ${error.message}`;
    } finally {
        loader.classList.add('hidden');
        extractBtn.disabled = false;
    }
});

// Tabs
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        viewContents.forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(`${btn.dataset.tab}-view`).classList.add('active');
    });
});

function renderFormatted(data) {
    let html = '';

    // Candidate
    html += `<div class="data-group"><h4>Candidate Details (${formatConf(data.candidate.confidence)})</h4>`;
    for (const [key, val] of Object.entries(data.candidate)) {
        if (key !== 'confidence' && val) {
            html += `<div class="field-row"><span class="label">${key.replace(/_/g, ' ')}:</span> <span>${val}</span></div>`;
        }
    }
    html += `</div>`;

    // Subjects
    html += `<div class="data-group"><h4>Subjects</h4>`;
    data.subjects.forEach(sub => {
        html += `<div class="field-row" style="border-bottom:1px dashed #eee; padding:5px 0;">
            <span class="label">${sub.name}</span>
            <span>${sub.marks.obtained}/${sub.marks.max_marks} (${sub.marks.grade || '-'})</span>
        </div>`;
    });
    html += `</div>`;

    // Result
    html += `<div class="data-group"><h4>Overall Result</h4>
        <div class="field-row"><span class="label">Result:</span> <span>${data.overall_result || 'N/A'}</span></div>
        <div class="field-row"><span class="label">Average Confidence:</span> ${formatConf(data.average_confidence)}</div>
    </div>`;

    formattedContent.innerHTML = html;
}

function formatConf(score) {
    const pct = Math.round(score * 100);
    let cls = 'confidence-high';
    if (score < 0.8) cls = 'confidence-med';
    if (score < 0.5) cls = 'confidence-low';
    return `<span class="${cls}">${pct}%</span>`;
}
