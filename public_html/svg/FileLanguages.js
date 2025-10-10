/*
    Gadget for Wikipedia using mw.Api() to extract SVG languages
    Add importScript("User:Mr._Ibrahem/Gadget-SVGLanguages.js"); to [[Special:MyPage/common.js]]
    Examples: [[User:Mr. Ibrahem/Gadget-SVGLanguages]]
    Usage example:
    - usage			{{SVGLanguages|Parkinsons-disease-prevalence-ihme,World,1990.svg}}
    - result		File languages: pt, es, ca, eu, cs, si, ar, fallback
*/

// Helper: extract languages from SVG DOM
function extractLanguagesFromSVG(svgDoc) {
    const switches = svgDoc.querySelectorAll('switch');
    const savedLanguages = new Set();

    switches.forEach(sw => {
        const texts = sw.querySelectorAll('text');
        texts.forEach(text => {
            const lang = text.getAttribute('systemLanguage') || 'fallback';
            savedLanguages.add(lang);
        });
    });

    return Array.from(savedLanguages);
}

// Helper: fetch SVG content from URL
async function fetchAndExtractSVG(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to fetch SVG: ${response.statusText}`);

        const text = await response.text();
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(text, "image/svg+xml");

        return extractLanguagesFromSVG(svgDoc);
    } catch (error) {
        console.error(error);
        return [];
    }
}

// Helper: get file URL from Wikimedia Commons using mw.Api
async function getFileURL(fileName) {
    const normalizedName = fileName.replace(/^File:/i, '');
    const api = new mw.Api();

    try {
        const data = await api.get({
            action: 'query',
            titles: `File:${normalizedName}`,
            prop: 'imageinfo',
            iiprop: 'url',
            format: 'json'
        });

        const pages = data.query.pages;
        const pageKey = Object.keys(pages)[0];
        const fileUrl = pages[pageKey].imageinfo?.[0]?.url;
        if (!fileUrl) throw new Error('File URL not found');

        return fileUrl;
    } catch (error) {
        console.error(error);
        return null;
    }
}

// Main function: process all <div class="get_languages" file="...">
async function oneFile(item) {
    // const itemSpan = item.find("span") || item;
    const itemSpan = item;
    itemSpan.text("");
    const fileName = item.attr('data-file');
    if (!fileName || fileName === "" || fileName === "{{{1}}}") {
        itemSpan.text('Error: Could not find file name');
        return;
    }

    itemSpan.text('Loading languages fileName: ', fileName);

    const fileUrl = await getFileURL(fileName);
    if (!fileUrl) {
        itemSpan.text('Error: Could not find file URL');
        return;
    }

    const languages = await fetchAndExtractSVG(fileUrl);
    const result = languages.length === 0
        ? 'No languages found'
        : ' ' + languages.join(', ');

    itemSpan.text(result);
}

async function initGetLanguages() {
    let divs = $('.get_languages');

    var button = $('<button>', {
        type: 'button',
        class: 'cdx-button cdx-button--action-progressive cdx-button--weight-primary cdx-button--size-medium',
        text: 'Load'
    });

    // divs.append($('<span>'));
    // divs.append(button);

    console.log("start initGetLanguages, get_languages divs: ", divs.length);

    if (!divs.length) {
        return;
    }

    // $('.get_languages .cdx-button').on('click', async function () {
    //     console.log("cdx-button");
    //     let $div = $(this);
    //     await oneFile($div);
    // });

    divs.each(async function () {
        let $div = $(this);
        await oneFile($div);
    });
}


$(document).ready(async function () {
    mw.loader.using(['mediawiki.api', 'oojs-ui', 'mediawiki.util']).then(async function () {
        await initGetLanguages();
    });
});
