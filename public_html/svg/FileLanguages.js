/*
  # Gadget for Wikipedia using mw.Api() to extract SVG languages

  ## To use it:
    - In your local wiki add next line to [[Special:MyPage/common.js|common.js]]:
      mw.loader.load('//meta.wikimedia.org/w/index.php?title=User:Mr._Ibrahem/Gadget-SVGLanguages.js&action=raw&ctype=text/javascript');

    - For global use add next line to [[:metawiki:Special:MyPage/global.js|global.js]]:
      importScript("User:Mr._Ibrahem/Gadget-SVGLanguages.js");

  ## Examples
    - [[:metawiki:User:Mr. Ibrahem/Gadget-SVGLanguages]]

  ## Usage example:
    - input			{{SVGLanguages|Parkinsons-disease-prevalence-ihme,World,1990.svg}}
    - output		[[:File:Parkinsons-disease-prevalence-ihme,World,1990.svg|File]] languages: pt, es, ca, eu, cs, si, ar
*/


// Helper: extract languages from SVG DOM
function extractLanguagesFromSVG(svgDoc) {
    const switches = svgDoc.querySelectorAll('switch');
    const savedLanguages = new Set();

    switches.forEach(sw => {
        const texts = sw.querySelectorAll('text');
        texts.forEach(text => {
            const lang = text.getAttribute('systemLanguage');
            if (lang) {
                savedLanguages.add(lang);
            }
        });
    });
    let data = Array.from(savedLanguages);
    if (data.length) {
        return data;
    }
    let texts = svgDoc.querySelectorAll('text');
    if (texts.length) {
        return ["en"];
    }
    return null;
}

// Helper: fetch SVG content from URL
async function fetchAndExtractSVG(url) {
    let text = "";
    try {
        const response = await fetch(url);
        if (!response.ok) {
            console.error(`Failed to fetch SVG: ${response.statusText}`);
            return [];
        }

        text = await response.text();
    } catch (error) {
        console.error(error);
        return [];
    }
    try {
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

    const data = await api.get({
        action: 'query',
        titles: `File:${normalizedName}`,
        prop: 'imageinfo',
        iiprop: 'url',
        formatversion: "latest",
        format: 'json'
    });

    const pages = data.query.pages;
    const pageArray = Array.isArray(pages) ? pages : Object.values(pages);

    const page = pageArray[0];

    // If the file does not exist locally or on Commons
    if (page.missing && !page.known) {
        return [`❌ File ${page.title} does not exist.`, ""];
    }

    // If the file exists on Commons (shared repository)
    console.log(`ℹ️ File ${page.title} exists on Wikimedia Commons (shared repository).`);

    const fileUrl = page.imageinfo?.[0]?.url;
    if (fileUrl) {
        return ["", fileUrl];
    }

    return ["⚠️ File URL not found.", ""];
};

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

    itemSpan.text('Loading languages');

    const [err, fileUrl] = await getFileURL(fileName);
    if (!fileUrl) {
        console.error(err);
        itemSpan.text(err ? err : 'Error: Could not find file URL');
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

    /*var button = $('<button>', {
        type: 'button',
        class: 'cdx-button cdx-button--action-progressive cdx-button--weight-primary cdx-button--size-medium',
        text: 'Load'
    });*/

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
