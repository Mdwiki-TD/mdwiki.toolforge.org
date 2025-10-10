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

const SVG_LANG_CACHE = new Map(); // simple in-memory cache

// Helper: extract languages from SVG DOM string
function extractLanguagesFromSVG(text) {
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(text, "image/svg+xml");

    // detect XML parse errors
    if (svgDoc.getElementsByTagName('parsererror').length) {
        console.error('SVG parse error');
        return [];
    }

    const savedLanguages = new Set();

    // 1) search <switch> -> <text> elements with systemLanguage
    const switches = svgDoc.querySelectorAll('switch');
    switches.forEach(sw => {
        const texts = sw.querySelectorAll('text');
        texts.forEach(t => {
            const lang = t.getAttribute('systemLanguage');
            if (lang) {
                savedLanguages.add(lang);
            }
        });
    });

    // 2) if we have languages return them
    let data = Array.from(savedLanguages);
    if (data.length) {
        console.log(`switches data: `, data.length);
        return data;
    }
    // 3) If there are text nodes but no language metadata assume English
    const anyText = svgDoc.querySelectorAll('text');
    console.log(`anyText data: `, anyText.length);
    if (anyText.length) {
        return ['en'];
    }

    console.log(`extractLanguagesFromSVG no result.`);

    // none found
    return [];
}

// Helper: fetch SVG content with timeout and return parsed languages
async function fetchAndExtractSVG(url, timeoutMs = 8000) {
    if (!url) return [];

    // use cache
    if (SVG_LANG_CACHE.has(url)) {
        return SVG_LANG_CACHE.get(url);
    }

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeoutMs);

    let text;
    try {
        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(id);
        if (!response.ok) {
            console.error('Failed to fetch SVG:', response.status, response.statusText);
            return [];
        }
        text = await response.text();
    } catch (err) {
        clearTimeout(id);
        console.error('Fetch error:', err && err.name ? err.name : err);
        return [];
    }

    try {
        const langs = extractLanguagesFromSVG(text);
        SVG_LANG_CACHE.set(url, langs);
        return langs;
    } catch (err) {
        console.error('SVG parse error:', err);
        return [];
    }
}

// Helper: get file URL from MediaWiki using mw.Api
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
        console.log(`fileUrl: ${fileUrl}`);
        return { error: "", url: fileUrl };
    }

    return { error: `File URL not found for ${page.title}`, url: null };
}

// Main per-item worker. Accepts jQuery-wrapped element
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
    if (!url || url === "") {
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

// Initialize: process all .get_languages elements concurrently but wait for all
async function initGetLanguages() {
    const divs = $('.get_languages');
    console.log('start initGetLanguages, get_languages divs: ', divs.length);

    if (!divs.length) return;

    // convert to array of promises and run them concurrently
    const promises = divs.toArray().map(el => oneFile($(el)));
    await Promise.allSettled(promises);
}

// Document ready and load MediaWiki modules, then init
$(document).ready(function () {
    mw.loader.using(['mediawiki.api', 'oojs-ui', 'mediawiki.util'])
        .then(initGetLanguages)
        .catch(err => {
            console.error('Failed to load MW modules:', err);
        });
});
