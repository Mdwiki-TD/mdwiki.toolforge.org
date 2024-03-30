<?php
require 'header.php';
require 'filter.php';
use function FilterCat\filter_cat_form;

$cat   = $_GET['cat'] ?? '';
$lang  = $_GET['lang'] ?? '';

$all_langs_table = <<<HTML
    <div class="row">
        <div class="col-md-3">
            <div class="card">
                <div class="card-header aligncenter" style="font-weight:bold;">
                    Numbers
                </div>
                <div class="card-body">
                    <table id="numbers" class="datatable table table-striped table-sm">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Number</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td><b>Files</b></td><td><span id="all_files">0</span></td></tr>
                            <tr><td><b>Languages</b></td><td><span id="all_langs" id="all_langs">0</span></td></tr>
                            <tr><td><b>Views</b></td><td><span id="all_views">0</span></td></tr>
                        </tbody>
                    </table>
                </div>
                <!-- <div class="card-footer"></div> -->
            </div>
            <br>
        </div>
        <div class="col-md-9">
            <div class="card">
                <div class="card-header aligncenter" style="font-weight:bold;">
                    Languages
                </div>
                <div class="card-body">
                    <table id="langs" class='datatable table table-striped table-sm'>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Language</th>
                                <th>Cat</th>
                                <th>Files</th>
                                <th>Views</th>
                            </tr>
                        </thead>
                        <tbody>
                        </tbody>
                    </table>
                </div>
            </div>
            <br>
        </div>
    </div>
HTML;

$filter_cat = filter_cat_form("index.php", $cat);

$table = <<<HTML
    $all_langs_table
HTML;

$one_lang_table = <<<HTML
    <div class='container'>
            <div class='row content'>
                <div class='col-md-3'>
                    <table class="table table-striped table-sm">
                        <tr><td><b>Views: </b></td><td><span id='hrefjsontoadd'>0</span></td></tr>
                        <tr><td><b>Files: </b></td><td><span id='all_files'>0</span></td></tr>
                    </table>
                </div>
                <div class='col-md-5'><h2 class='text-center'>Language: $lang</h2></div>
                <div class='col-md-4'></div>
            </div>
            <div class='card'>
                <div class='card-body' style='padding:5px 0px 5px 5px;'>
                    <table id="files_table" class='table table-striped compact soro'>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Title</th>
                                <th>Views</th>
                            </tr>
                        </thead>
                        <tbody>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
HTML;

if ($lang != '') {
    $table = <<<HTML
        $one_lang_table
    HTML;
}

$start = "start('$lang', '$cat');";
echo <<<HTML
    <script src="j.js"></script>
    <main id="body">
        <div id="maindiv" class="container">
            <div class="container">
                $filter_cat
                $table
            </div>
        </div>
    </main>
    <script>
        
        $(document).ready(function() {
            $start
            // wait 3 seconds before starting

            setTimeout(function() {
                    
                $('.datatablez').DataTable({
                    paging: false,
                    info: false,
                    searching: false
                });
		        to_get();
		    }, 3000);

        });
    </script>
</div>
</main>

</body>

</html>
HTML;

