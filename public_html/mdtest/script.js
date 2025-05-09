

function load_data() {
    let table;
    // ---
    // localhost or mdwiki.toolforge.org
    let end_point = (window.location.hostname === 'localhost') ? 'http://localhost:9001' : 'https://mdwiki.toolforge.org';
    end_point += '/api.php?';
    // ---
    end_point = "result.json?"
    // ---
    let params = new URLSearchParams(window.location.search);
    // ---
    let lang = params.get('lang') || 'not_empty';
    let table_name = params.get('table') || 'pages';
    // ---
    $('#limitForm').on('submit', function (e) {
        e.preventDefault();
        // ---
        let limit = $('#limitInput').val();
        // ---
        var n_params = {
            lang: lang,
            get: table_name,
            limit: limit
        };
        // ---
        table.ajax.url(end_point + new URLSearchParams(n_params)).load();
    });

    var new_params = {
        lang: lang,
        get: table_name,
        limit: $('#limitInput').val()
    };
    // ---
    table = $('#catsTable').DataTable({
        ajax: {
            url: end_point + new URLSearchParams(new_params),
            type: 'GET',
            dataType: 'json',
            dataSrc: ''
        },
        columns: [
            { data: null, render: function (data, type, row, meta) { return meta.row + 1; } },
            // { data: 'id', visible: false },
            {
                data: 'user',
                render: function (data) {
                    const url = '/Translation_Dashboard/leaderboard.php?user=' + encodeURIComponent(data.replace(/ /g, '_'));
                    return `<a href="${url}" target="_blank">${data}</a>`;
                }
            },
            {
                data: 'title',
                render: function (data) {
                    const url = 'https://mdwiki.org/wiki/' + encodeURIComponent(data.replace(/ /g, '_'));
                    return `<a href="${url}" target="_blank">${data}</a>`;
                }
            },
            {
                data: 'target'
            },
            {
                data: 'pupdate'
            }
        ],
        dom: '<"top"lfBp>rt<"bottom"ip>',
        // buttons: ['copy', 'excel', 'pdf', 'print'],
        // stateSave: true,
        searching: true,
        rowCallback: function (row, data) {
            // تمييز الصفوف غير المعدلة
            if (data.done === 'no') {
                $(row).addClass('table-warning');
            }
        },
        /*initComplete: function () {
            this.api().columns().every(function (i) {
                if (i === 0) return;
                var that = this;
                $('input', this.footer()).on('keyup change clear', function () {
                    if (that.search() !== this.value) {
                        that.search(this.value).draw();
                    }
                });
            });
        }*/
    });

    $('#clearFilter').on('click', function () {
        table.column(3).search('').draw();
    });
}
