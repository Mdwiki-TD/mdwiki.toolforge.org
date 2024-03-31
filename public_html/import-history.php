<?PHP
//---
require 'header.php';
//---
print_h3_title("Import history from enwiki");
//---
require 'bots/tfj.php';
// $result = do_tfj(array( 'name' => "", 'command' => $command));
//---
$test       = $_REQUEST['test'] ?? '';
$from       = $_REQUEST['from'] ?? '';
$title      = $_REQUEST['title'] ?? '';
$titlelist  = $_REQUEST['titlelist'] ?? '';
$code       = $_REQUEST['code'] ?? '';
//---
$err = '';
//---
if ( $code != 'James#99' && $code != 'james#99' && $code != '') {
    $err = "<span style='font-size:13pt;'>! (" . $code . ")</span><span style='font-size:13pt;color:red'> is wrong code.</span>";
};
//---
if ( ($titlelist == '' && $title == '') or $code == '' or ( $code != 'James#99' && $code != 'james#99' ) ) {
    //---
    echo <<<HTML
        <form action='import-history.php' method='POST'>
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
                                <input class='btn btn-outline-primary' type='submit' value='send'>
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    HTML;
    //---
} else {
    //---
    $command = "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/imp";
    //---
    $text = "";
    //---
    if ($title != '') {
        $command .= " -page:" . rawurlencode($title) . ' -from:' . rawurlencode($from) . ' save';
        //---
        $text .= 'The Bot will import ' . rawurldecode($title) . ' history';
        //---
        if ($from != '') $text .= ' from (' . rawurldecode($from) . ') in seconds.';
        //---
        $text .= ' in seconds.';
        //---
    } else {
        //---
        $filee = '/data/project/mdwiki/public_html/texts/importlist.txt';
        //---
        $myfile = fopen($filee, "w");
        fwrite($myfile , $titlelist);
        fclose($myfile);
        //---
        $command .= " -file:" . $filee . ' save' ;
        //---
        $text .= 'The Bot will import history for titles in the list in seconds.';
        //---
    };
    $text = "<span style='font-size:15pt;color:green'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$text</span>";
    //---
    echo "<br>";
    //---
    // $runj = "/usr/bin/toolforge jobs run historyy --image python3.9 --command \"$command\"";
	// if ($test != '') echo $runj;
    // $result = shell_exec($runj);
    //---
    $result = do_tfj(array( 'name' => "historyy", 'command' => $command));
    //---
    echo $result;
    //---
    }
//---
require 'footer.php';
//---
?>