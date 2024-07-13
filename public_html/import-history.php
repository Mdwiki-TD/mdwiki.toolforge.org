<?PHP
//---
require 'header.php';
//---
print_h3_title("Import history from enwiki");
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
//---
$test       = $_REQUEST['test'] ?? '';
$from       = $_REQUEST['from'] ?? '';
$title      = $_REQUEST['title'] ?? '';
$titlelist  = $_REQUEST['titlelist'] ?? '';
$code       = $_REQUEST['code'] ?? '';
//---
$err = '';
//---
if ($code != 'James#99' && $code != 'james#99' && $code != '') {
    $err = "<span style='font-size:13pt;'>! (" . $code . ")</span><span style='font-size:13pt;color:red'> is wrong code.</span>";
};
//---
require 'bots/tfj.php';

function get_results($aargs)
{
    //---
    global $test;
    //---
    $ccc = " mdpy/imp $aargs save";
    //---
    $params = array(
        'dir' => "core8",
        'localdir' => "core8",
        'pyfile' => 'pwb.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_tfj_sh($params, "import");
    //---
    return $result;
}

//---
function make_form($test, $title, $titlelist, $code, $err)
{
    global $username;
    // ---
    $start_icon = "<input class='btn btn-outline-primary' type='submit' value='send'>";
    // ---
    if ($username == '') $start_icon = '<a role="button" class="btn btn-primary" href="/Translation_Dashboard/auth.php?a=login">Log in</a>';
    // ---
    $testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
    // ---
    return <<<HTML
        <form action='import-history.php' method='POST'>
            $testinput
            <div class='container'>
                <div class='container'>
                    <div class='row'>
                        <div class='col-lg-12'>
                            <div class='form-group'>
                                <div class='input-group mb-3'>
                                    <div class='input-group-prepend'>
                                        <span class='input-group-text'>Title:</span>
                                    </div>
                                    <input class='form-control' type='text' id='title' name='title' value='$title'/>
                                </div>
                            </div>
                        </div>
                        <div class='col-lg-12'>
                            <h3 class='aligncenter'>or</h3>
                        </div>
                        <div class='col-lg-12'>
                            <div class='form-group'>
                                <div class='input-group mb-3'>
                                    <div class='input-group-prepend'>
                                        <span class='input-group-text'>List of titles:</span>
                                    </div>
                                    <textarea class='form-control' cols='20' rows='7' id='titlelist' name='titlelist'>$titlelist</textarea>
                                </div>
                            </div>
                        </div>
                        <div class='col-lg-12'>
                            <div class='form-group'>
                                <div class='input-group mb-3'>
                                    <div class='input-group-prepend'>
                                        <span class='input-group-text'>Code:</span>
                                    </div>
                                    <input class='form-control' type='text' name='code' value='$code' required/>
                                    $err
                                </div>
                            </div>
                        </div>
                        <div class='col-lg-12'>
                            <h4 class='aligncenter'>
                                $start_icon
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    HTML;
    //---
}
if (($titlelist == '' && $title == '') or $code == '' or ($code != 'James#99' && $code != 'james#99')) {
    //---
    echo make_form($test, $title, $titlelist, $code, $err);
    //---
} else {
    //---
    $command = "";
    //---
    $text = "";
    //---
    if ($title != '') {
        $command .= " -page:" . rawurlencode($title) . ' -from:' . rawurlencode($from);
        //---
        $text .= 'The Bot will import ' . rawurldecode($title) . ' history';
        //---
        if ($from != '') $text .= ' from (' . rawurldecode($from) . ') in seconds.';
        //---
        $text .= ' in seconds.';
        //---
    } else {
        //---
        $filee = "$ROOT_PATH/public_html/texts/importlist.txt";
        //---
        $myfile = fopen($filee, "w");
        fwrite($myfile, $titlelist);
        fclose($myfile);
        //---
        $command .= " -file:" . $filee;
        //---
        $text .= 'The Bot will import history for titles in the list in seconds.';
        //---
    };
    $text = "<span style='font-size:15pt;color:green'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$text</span>";
    //---
    echo "<br>";
    //---
    $result = get_results($command);
    //---
    echo $result;
    //---
}
//---
require 'footer.php';
//---
