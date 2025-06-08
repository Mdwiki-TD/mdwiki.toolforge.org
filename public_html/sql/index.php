<?php
if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
// ---
include_once __DIR__ . '/td_api.php';
// ---
$user_coordinators = get_td_api(['get' => 'coordinator', 'select' => 'user']);
// ---
include_once __DIR__ . '/../header.php';
//---
if (strpos(__FILE__, "I:\\") !== false) {
    include_once __DIR__ . '/../../../auth/auth/user_infos.php';
    include_once __DIR__ . '/../../../auth/auth/user_infos.php';
} else {
    include_once __DIR__ . '/../auth/auth/user_infos.php';
    include_once __DIR__ . '/../auth/auth/user_infos.php';
}
//---
include_once __DIR__ . '/sql_result.php';
include_once __DIR__ . '/form.php';
//---
$u_name = isset($GLOBALS['global_username']) ? $GLOBALS['global_username'] : '';
// ---
if ($u_name == '' || !in_array($u_name, $user_coordinators)) {
    echo "user:" . $u_name . " not allowed";
    echo json_encode($user_coordinators);
    echo "<meta http-equiv='refresh' content='0; url=/Translation_Dashboard/index.php'>";
    exit;
};
// ---
echo <<<HTML
    <style>
    #code {
        font-family: Monaco, Consolas, "Ubuntu Mono", monospace;
        width: 100%;
        height: auto;
        min-height: 144px;
    }
    </style>
HTML;
// ---
echo "<div class='container-fluid'>";
// ---
$pass = $_POST['pass'] ?? '';
$code = $_POST['code'] ?? '';
// ---
echo make_form($pass, $code);
// ---
if (!empty($code)) {
    get_sql_result($code, $pass);
};
// ---
echo "</div>";
// ---
$old = <<<HTML
    <script>
        function to_code(text) {
            $("#code").val(text);
        }
        function copy_qua(id) {
            const queryString = queries[id];
            $("#code").val(queryString);
        }
    </script>
HTML;
// ---
echo <<<HTML
<script>
    var editor = ace.edit("editor");
    editor.session.setMode("ace/mode/sql");
    editor.setTheme("ace/theme/sqlserver");
    editor.setOptions({
        fontSize: "16px",
        showPrintMargin: false,
        wrap: true
        });

    // لتمرير القيمة إلى textarea عند الإرسال
    document.querySelector("form")?.addEventListener("submit", function () {
        document.getElementById("code").value = editor.getValue();
    });

    function to_code(text) {
        editor.setValue(text, -1); // -1 = بدون تحريك الكيرسر
    }

    function copy_qua(id) {
        const queryString = queries[id]; // تأكد أن المتغير queries موجود مسبقًا
        editor.setValue(queryString, -1);
    }
</script>
HTML;
// ---
include_once __DIR__ . '/../footer.php';
