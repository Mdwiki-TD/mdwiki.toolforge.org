
function fetch_url(endpoint, params, callback) {
    // ---
    url = endpoint;
    // ---
    if (jQuery.isEmptyObject(params) === false) {
        url += "?" + jQuery.param(params);
    }
    // ---
    console.log("j.js:" + url)
    // ---
    var result = [];
    // ---
    jQuery.ajax({
        url: url,
        type: 'GET',
        error: function (data) {
            console.log("xx: error:");
        },
        success: function (data) {
            console.log("xx: success:");
            console.log(data);
            callback(data, params.lang);
        }
    });
    // ---
    return result;
}
function makeViewByNumber(target, numb, lang) {
    // Remove spaces and tab characters
    target = target.trim();
    var numb2 = (numb !== '') ? numb : "?";
    var start = '2019-01-01';
    var end = new Date(new Date() - 864e5).toISOString().split('T')[0]; // Yesterday's date

    var queryParams = {
        project: lang + ".wikipedia.org",
        platform: 'all-access',
        agent: 'all-agents',
        range: 'all-time',
        redirects: '0',
        pages: target
    };

    var url = 'https://pageviews.wmcloud.org/?' + new URLSearchParams(queryParams).toString();
    var start2 = '20240101';

    var hrefjson = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' + lang + '.wikipedia/all-access/all-agents/' + encodeURIComponent(target) + '/daily/' + start2 + '/2025010100';

    var link = "<a target='_blank' href='" + url + "'>" + numb2 + "</a>";

    if (numb2 === '?' || numb2 === 0 || numb2 === '0') {
        link = "<a target='_blank' name='toget' hrefjson='" + hrefjson + "' href='" + url + "'>" + numb2 + "</a>";
    }

    return link;
}

function add_to_value(id, value) {
    var p = $('#' + id).text();
    // add the value to id value
    var nu = parseFloat(p) + value;
    $('#' + id).text(nu);
}

function lang_work(lang, cat, callback) {
    // ---
    const endpoint = window.location.origin + '/ncc/api/files.php';
    const params = {
        lang: lang,
        cat: cat
    };
    // ---
    fetch_url(endpoint, params, callback);
}

function get_langs(cat) {
    var cats = {
        "Files_imported_from_NC_Commons": ["af", "ar"],
        "Translated_from_MDWiki": ["af", "ar", "es", "fa", "ha", "it", "ja", "or", "pl", "sq"]
    }
    return cats[cat];
}

function start_all_langs(cat) {
    // ---    
    var langs = get_langs(cat);
    // ---
    // work for each lang
    for (var i = 0; i < langs.length; i++) {
        // ---
        var lang = langs[i];
        // ---
        var urlv = "index.php?lang=" + lang + "&cat=" + cat;
        // ---
        add_to_value("all_langs", 1);
        //---
        var tr = $("<tr></tr>");
        // ---
        tr.append($("<td></td>").text(i + 1));
        tr.append($("<td></td>").html("<a href='" + urlv + "'>" + lang + "</a>"));
        tr.append($("<td></td>").html("<a href='https://" + lang + ".wikipedia.org/wiki/Category:" + cat + "'>Category</a>"));
        tr.append($("<td></td>").html("<span id='" + lang + "_files'>0</span>"));
        tr.append($("<td></td>").html("<span id='" + lang + "_views'>0</span>"));
        // ---
        // add row to table id="langs" tbody
        $("#langs tbody").append(tr);
        // ---
    }
    // ---
    // work for each lang
    for (var i = 0; i < langs.length; i++) {
        // ---
        var lang = langs[i];
        // ---
        lang_work(lang, cat, function (data, lang) {
            // ---
            all_files = data.length;
            // ---
            add_to_value("all_files", all_files);
            // ---
            $("#" + lang + "_files").text(all_files);
        });
    }
}
function start_one_lang(mainlang, cat) {
    lang_work(mainlang, cat, function (data, mainlang) {
        // ---
        add_to_value("all_files", data.length);
        add_to_value("all_langs", 1);
        //---
        for (var i = 0; i < data.length; i++) {
            // ---
            var file_name = data[i];
            // ---
            var views_link = makeViewByNumber(file_name, "", mainlang);
            // ---
            var file_name_url = "https://" + mainlang + ".wikipedia.org/wiki/" + file_name;
            // ---
            var tr = $("<tr></tr>");
            tr.append($("<td></td>").text(i + 1));
            tr.append($("<td></td>").html("<a target='_blank' href='" + file_name_url + "'>" + file_name + "</a>"));
            tr.append($("<td></td>").html(views_link));

            // add row to table id="files_table" tbody
            $("#files_table tbody").append(tr);
        }
    });
    }

function start(mainlang, cat) {
    // if mainlang then start_one_lang(mainlang) else start_all_langs();
    if (!cat) {
        cat = "Files_imported_from_NC_Commons";
    };
    // ---
    if (mainlang) {
        start_one_lang(mainlang, cat);
    } else {
        start_all_langs(cat);
    }
}