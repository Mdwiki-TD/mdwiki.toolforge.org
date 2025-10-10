// == Use original extractLanguagesFromSVG from the main script ==

// == Test Function 1: Using a local File input ==
async function testWithFile(file) {
    const text = await file.text();

    const languages = extractLanguagesFromSVG(text);
    console.log("Languages found in file:", languages);
    return languages;
}

// == Test Function 2: Using a URL to fetch SVG (reuse fetchAndExtractSVG) ==
async function testWithURL(url) {
    const languages = await fetchAndExtractSVG(url);
    console.log("Languages found in URL:", languages);
    return languages;
}

// == Test Function 3: Using Wikimedia Commons file name (reuse getFileURL + fetchAndExtractSVG) ==
async function testWithFileName(fileName) {
    const [err, fileUrl] = await getFileURL(fileName);
    if (!fileUrl) throw new Error(err || "File URL not found");

    const languages = await fetchAndExtractSVG(fileUrl);
    console.log("Languages found in file name:", languages);
    return languages;
}

// == Show results helper ==
function showResults(jsonData, id) {
    const resultBox = document.getElementById(id);
    resultBox.textContent = "Languages found: " + (jsonData.length ? jsonData.join(', ') : "None");
}

// == Event Listeners ==
document.getElementById('fileTestBtn').addEventListener('click', async () => {
    const file = document.getElementById('svgFileInput').files[0];
    if (!file) { alert('Please select a file first.'); return; }
    const result = await testWithFile(file);
    showResults(result, 'fileResult');
});

document.getElementById('urlTestBtn').addEventListener('click', async () => {
    const url = document.getElementById('svgUrlInput').value.trim();
    if (!url) { alert('Please enter a URL first.'); return; }
    const result = await testWithURL(url);
    showResults(result, 'urlResult');
});

document.getElementById('fileNameBtn').addEventListener('click', async () => {
    const fileName = document.getElementById('svgFileNameInput').value.trim();
    if (!fileName) { alert('Please enter a file name.'); return; }
    const result = await testWithFileName(fileName);
    showResults(result, 'fileNameResult');
});
