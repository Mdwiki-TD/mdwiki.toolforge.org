<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Create redirects.</h3>
    </div>
    <div class="card-body">
<?php
//---
$title      = $_REQUEST['title'] ?? '';
$titlelist  = $_REQUEST['titlelist'] ?? '';
//---
function Get_Value() {
    //---
    global $title, $titlelist;
    //---
    echo "
    <form action='redirect.php' method='POST'>
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
                        <h4 class='aligncenter'>
                            <input class='btn btn-primary' type='submit' value='send'>
                        </h4>
                    </div>
                </div>
            </div>
        </div>
    </form>
      ";
    //---
    }
//---
function worknew() {
    //---
    global $title, $titlelist;
    //---
    //echo $_SERVER['SERVER_NAME'];
    echo "<span style='font-size:15pt;color:green'>";
    echo '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    //---
	$filee = '/data/project/mdwiki/public_html/texts/redirectlist.txt';
    //---
    if ($title != '') {
        $python3 = "-page2:" . rawurlencode($title);
        //---
        echo '<span class="">The Bot will create redirects for ' . rawurldecode($title) . ' in seconds.</span>';
        //---
    } else {
        //---
        $myfile = fopen( 'redirectlist.txt' , "w");
        fwrite($myfile , $titlelist);
        fclose($myfile);
        //---
        $python3 = "python3 -file:$filee";
        echo '<span class="">The Bot will create redirects for titles in the list in seconds.</span>';
        //---
    };
    //---
	$command = "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/red $python3 save";
	$nana = "toolforge jobs run redirectx --command '$command' --image python3.9";
    //---
    echo '</span>';
    print "<br>";
    //---
    if (isset($_REQUEST['test'])) print $nana;
    //---
    $result = shell_exec($nana);
    //---
    print $result;
    //---
    }
//---
if ($title == '' and $titlelist == '') {
    echo Get_Value() ;
} else {
    echo worknew() ;
};
?>
</div>
<?php require 'foter.php'; ?>