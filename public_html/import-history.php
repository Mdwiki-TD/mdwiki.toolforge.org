<?PHP
//---
require 'header.php';
//---
echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Import history from enwiki</h3>
    </div>
    <div class="card-body">
HTML;
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
                                <input class='btn btn-primary' type='submit' value='send'>
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
    $jsub = 'jsub -N historyy /data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/imp ';
    //---
    $text = "";
    //---
    if ($title != '') {
        $jsub .= " -page:" . rawurlencode($title) . ' -from:' . rawurlencode($from) . ' save' ;
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
        $jsub .= " -file:" . $filee . ' save' ;
        //---
        $text .= 'The Bot will import history for titles in the list in seconds.';
        //---
    };
    $text = "<span style='font-size:15pt;color:green'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$text</span>";
    //---
	if ($test != '') echo $jsub;
    //---
    echo "<br>";
    //---
    $result = shell_exec($jsub);
    print $result;
    //---
    }
//---
echo "</div>";
//---
require 'foter.php';
//---
?>