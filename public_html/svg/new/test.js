
// == Test Function 3: Using Wikimedia Commons file name (reuse getFileURL + fetchAndExtractSVG) ==
async function testWithFileName(fileName) {
    const { error, langs } = await getFileTranslations(fileName);
    return ["", langs];
}

// == Show results helper ==
function showResults(jsonData, resultBox) {

    const result = jsonData.length === 0
        ? 'No data found'
        : 'Languages: ' + jsonData.join(', ');

    resultBox.textContent = result;
}

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
