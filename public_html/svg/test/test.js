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
    const { error, url } = await getFileURL(fileName);

    if (!url || url === "") {
        console.error('testWithFileName no result');
        return [error, []];
    }

    const result = await testWithURL(url);
    return ["", result];
}

// == Show results helper ==
function showResults(jsonData, resultBox) {

    const result = jsonData.length === 0
        ? 'No data found'
        : 'Languages: ' + jsonData.join(', ');

    resultBox.textContent = result;
}

// == Event Listeners ==
document.getElementById('fileTestBtn').addEventListener('click', async () => {
    // ---
    const file = document.getElementById('svgFileInput').files[0];
    // ---
    if (!file) { alert('Please select a file first.'); return; }
    // ---
    const resultBox = document.getElementById('fileResult');
    // ---
    resultBox.textContent = "Loading..."
    // ---
    const result = await testWithFile(file);
    // ---
    showResults(result, resultBox);
});

document.getElementById('urlTestBtn').addEventListener('click', async () => {
    // ---
    const url = document.getElementById('svgUrlInput').value.trim();
    // ---
    if (!url) { alert('Please enter a URL first.'); return; }
    // ---
    const resultBox = document.getElementById('urlResult');
    // ---
    resultBox.textContent = "Loading..."
    // ---
    const result = await testWithURL(url);
    // ---
    showResults(result, resultBox);
});

document.getElementById('fileNameBtn').addEventListener('click', async () => {
    // ---
    const fileName = document.getElementById('svgFileNameInput').value.trim();
    // ---
    if (!fileName) { alert('Please enter a file name.'); return; }
    // ---
    const resultBox = document.getElementById('fileNameResult');
    // ---
    resultBox.textContent = "Loading..."
    // ---
    const [err, result] = await testWithFileName(fileName);
    // ---
    if (err) {
        resultBox.textContent = err.toString();
        return;
    }
    // ---
    showResults(result, resultBox);
});
