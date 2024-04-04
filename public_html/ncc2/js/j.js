
function fetch_api(params, callback) {
    // ---
    const endpoint = window.location.origin + '/ncc/api/files.php';
    url = endpoint;
    // ---
    if (jQuery.isEmptyObject(params) === false) {
        url += "?" + jQuery.param(params);
    }
    // ---
    console.log("j.js:" + url)
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
    const params = {
        action: 'get_cat_members',
        lang: lang,
        cat: cat
    };
    // ---
    fetch_api(params, callback);
}

function start_all_langs(cat) {
    // ---
    const params = {
        action: 'get_langs',
        cat: cat,
        addlenth: 1
    };
    // ---
    fetch_api(params,
        function (langs) {
            // ---
            var i = 0;
            // ---
            // langs = {"af":0,"ar":30,"es":8,"fa":0,"ha":38,"it":0,"ja":45,"or":734,"pl":2,"sq":5}
            // work for each lang
            for (const [lang, count] of Object.entries(langs)) {
                // ---
                i++;
                // ---
                console.log(lang, count);
                // ---
                var urlv = "index.php?lang=" + lang + "&cat=" + cat;
                // ---
                add_to_value("all_langs", 1);
                add_to_value("all_files", count);
                //---
                var tr = $("<tr></tr>");
                // ---
                tr.append($("<td></td>").text(i + 1));
                tr.append($("<td></td>").html("<a href='" + urlv + "'>" + lang + "</a>"));
                tr.append($("<td></td>").html("<a href='https://" + lang + ".wikipedia.org/wiki/Category:" + cat + "'>Category</a>"));
                tr.append($("<td></td>").html("<span id='" + lang + "_files'>" + count + "</span>"));
                tr.append($("<td></td>").html("<span id='" + lang + "_views'>0</span>"));
                // ---
                // $("#" + lang + "_files").text(count);
                // ---
                // add row to table id="langs" tbody
                $("#langs tbody").append(tr);
                // ---            
            }
        }
    );
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