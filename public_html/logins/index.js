const baseBackgroundColors = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(255, 205, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(153, 102, 255, 0.2)'
];

const baseBorderColors = [
    'rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)'
];

function time_diff(data) {
    const first = new Date(data.first);
    const last = new Date(data.last);
    const seconds = Math.floor((last - first) / 1000);
    const d = Math.floor(seconds / 86400);
    const h = Math.floor((seconds % 86400) / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    let out = [];
    if (d) out.push(d + "d");
    if (h) out.push(h + "h");
    if (m) out.push(m + "m");
    if (s || out.length === 0) out.push(s + "s");
    return out.join(" ");
}

function getsortedSites(data) {
    const siteCounts = {};

    // حساب عدد الاستعلامات لكل موقع
    data.forEach(entry => {
        const site = entry.site || 'Unknown';
        if (!siteCounts[site]) {
            siteCounts[site] = 0;
        }
        // convert entry.count to int
        siteCounts[site] += parseInt(entry.count);
    });

    // تحويل siteCounts إلى مصفوفة لتسهيل الفرز
    const sortedSites = Object.entries(siteCounts)
        .sort((a, b) => b[1] - a[1]) // ترتيب تنازلي حسب عدد الاستعلامات
        .slice(0, 10); // اختيار أول 10 مواقع فقط

    return sortedSites;
}
function getSiteLabel(site) {
    const labels = {
        'www.mdwiki.org': 'mdwiki',
        'www.wikidata.org': 'wikidata',
    };

    let label = labels[site] || site;

    if (label.includes('.wikipedia.org')) {
        label = label.replace('.wikipedia.org', ' wiki');
    }

    return label;
}
function createSiteNavigation(sortedSites) {
    sortedSites.forEach(([site, count]) => {
        // add to navs
        // <li class="nav-item"><a class="nav-link">2025</a></li>
        let id = Math.random().toString(36).slice(2);
        let label = getSiteLabel(site);
        // ---
        $('#navs').append(`
            <li class="nav-item">
                <button class="nav-link" id="${id}-tab" data-bs-toggle="tab" data-bs-target="#All-tab-pane"
                site="${site}"
                type="button" role="tab" aria-controls="All-tab-pane" aria-selected="false">${label} (${count.toLocaleString()})</button>
            </li>
        `);
    })
}

function getsortedActions(data, site) {
    const Counts = {};

    // filter data by site
    if (site != "" && site != "All") {
        data = data.filter(entry => entry.site === site);
    }
    // حساب عدد الاستعلامات لكل موقع
    data.forEach(entry => {
        const action = entry.action || 'Unknown';
        if (!Counts[action]) {
            Counts[action] = 0;
        }
        // convert entry.count to int
        Counts[action] += parseInt(entry.count);
    });

    // تحويل siteCounts إلى مصفوفة لتسهيل الفرز
    const sortedSites = Object.entries(Counts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

    return sortedSites;
}

function ActionsCharts(data, site) {
    const sortedSites = getsortedActions(data, site);
    // ---
    $(document).on('click', '[data-bs-target]', function () {
        // ---
        let site = $(this).attr('site');
        // ---
        const sorted_Sites = getsortedActions(data, site);
        // ---
        $("#ActionsChartContainer").html('<canvas id="ActionsChart" height="100"></canvas>');
        // ---
        renderActionsChart(sorted_Sites, site);
        // ---
    });
    // ---
    renderActionsChart(sortedSites, site);
}

function renderActionsChart(sortedSites, site) {
    const labels = sortedSites.map(item => item[0]);
    const counts = sortedSites.map(item => item[1]);

    const ctx = document.getElementById('ActionsChart').getContext('2d');

    const backgroundColors = labels.map((_, i) =>
        baseBackgroundColors.slice().reverse()[i % baseBackgroundColors.length]
    );

    const borderColors = labels.map((_, i) =>
        baseBorderColors.slice().reverse()[i % baseBorderColors.length]
    );


    // إذا كان الرسم موجود مسبقًا فقم بتحديثه بدلاً من إنشائه من جديد
    let ActionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Actions by type: (${site})`,
                data: counts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: `Actions by type: (${site})`
                },
                datalabels: {
                    anchor: 'end',
                    align: 'right',
                    color: 'black',
                    font: {
                        weight: 'bold'
                    },
                    formatter: function (value) {
                        return value;
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: false,
                        text: 'API requests'
                    }
                },
                x: {
                    title: {
                        display: false,
                        text: 'Site'
                    }
                }
            }
        }
    });
}

function drawChart(data) {

    const sortedSites = getsortedSites(data);
    createSiteNavigation(sortedSites);
    const labels = sortedSites.map(item => item[0]);
    const counts = sortedSites.map(item => item[1]);

    const ctx = document.getElementById('loginsChart').getContext('2d');

    const backgroundColors = labels.map((_, i) =>
        baseBackgroundColors[i % baseBackgroundColors.length]
    );

    const borderColors = labels.map((_, i) =>
        baseBorderColors[i % baseBorderColors.length]
    );

    let loginsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total queries by site',
                data: counts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Total queries by site (top 10)"
                },
                datalabels: {
                    anchor: 'end',
                    align: 'right',
                    color: 'black',
                    font: {
                        weight: 'bold'
                    },
                    formatter: function (value) {
                        return value;
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: false,
                        text: 'API requests'
                    }
                },
                x: {
                    title: {
                        display: false,
                        text: 'Site'
                    }
                }
            }
        }
    });
}

async function load_table(apiUrl, id, site = "") {
    let table_data = {
        ajax: {
            url: apiUrl,
            type: 'GET',
            dataType: 'json',
            dataSrc: function (json) {
                drawChart(json); // رسم الرسم البياني هنا
                ActionsCharts(json, "All");
                return json;
            }
        },
        paging: false,
        info: false,
        columns: [
            {
                data: null,
                render: (_, __, ___, meta) => meta.row + 1
            },
            {
                data: 'count',
                render: function (data) {
                    return Number(data).toLocaleString();
                }
            },
            {
                data: 'action'
            },
            {
                data: 'site'
            },
            {
                data: 'result'
            },
            {
                data: 'username'
            },
            {
                data: 'first'
            },
            {
                data: 'last'
            },
            {
                data: null,
                render: time_diff
            }
        ]
    }
    // ---
    let table = $(id).DataTable(table_data);
    // ---
    $(document).on('click', '[data-bs-target]', function () {
        // ---
        let site = $(this).attr('site');
        // ---
        if (site == "All") {
            site = "";
        }
        // ---
        table.column(3).search(site).draw();
    });
}

async function start(apiUrl) {
    await load_table(apiUrl, "#catsTableAll", "");

}
