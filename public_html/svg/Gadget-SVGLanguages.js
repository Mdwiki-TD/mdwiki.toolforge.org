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
function extractLanguagesFromSVG(text) {
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(text, "image/svg+xml");

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
        console.log(`switches data: `, data.length)
        return data;
    }

    let anyText = svgDoc.querySelectorAll('text');
    console.log(`anyText data: `, anyText.length);
    if (anyText.length) {
        return ["en"];
    }

    console.log(`extractLanguagesFromSVG no result.`);

    return [];
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
        return extractLanguagesFromSVG(text);
    } catch (error) {
        console.error(error);
        return [];
    }
}

// Helper: get file URL from Wikimedia Commons using mw.Api
async function getFileURL(fileName) {
    // return object { error, url }
    if (!fileName) return { error: 'Empty fileName', url: null };

    const normalizedName = fileName.replace(/^File:/i, '').trim();
    const api = new mw.Api();
    let data;
    try {
        data = await api.get({
            action: 'query',
            titles: `File:${normalizedName}`,
            prop: 'imageinfo',
            iiprop: 'url',
            formatversion: "latest",
            format: 'json'
        });

    } catch (err) {
        console.error('mw.Api error:', err);
        return { error: 'API error', url: null };
    }

    const pages = data.query && data.query.pages;
    if (!pages) return { error: 'Unexpected API response', url: null };

    // pages is an object keyed by pageid; pick the first value
    const page = Array.isArray(pages) ? pages[0] : Object.values(pages)[0];

    if (!page) return { error: 'Page not found in API response', url: null };

    // If the file does not exist locally or on Commons
    if (page.missing && !page.known) {
        return { error: `File ${page.title} does not exist.`, url: null };
    }

    // If the file exists on Commons (shared repository)
    console.log(`ℹ️ File ${page.title} exists on Wikimedia Commons (shared repository).`);

    const fileUrl = page.imageinfo && page.imageinfo[0] && page.imageinfo[0].url;
    if (fileUrl && fileUrl !== "") {
        console.log(`fileUrl: ${fileUrl}`)
        return { error: "", url: fileUrl };
    }

    return { error: `File URL not found for ${page.title}`, url: null };
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

    itemSpan.text('Loading languages');

    const { error, url } = await getFileURL(fileName);
    if (!url) {
        console.error(error);
        itemSpan.text(error || 'Error: Could not find file URL');
        return;
    }

    const languages = await fetchAndExtractSVG(url);
    const result = (!languages || languages.length === 0)
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
    });

    // divs.append(button);
    // divs.append($('<span>'));
    */
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
