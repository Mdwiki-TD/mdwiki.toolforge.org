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
    //$dir = '/data/project/mdwiki/mdpy/'; 
    //---
    //echo $_SERVER['SERVER_NAME'];
    echo "<span style='font-size:15pt;color:green'>";
    echo '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    //---
    //$dir = '';  
    $dir = '/data/project/mdwiki/core8'; 
    $filee = 'texts/redirectlist.txt';
    $jsub = '';
    //---
    if ( $_SERVER['SERVER_NAME'] == 'mdwiki.toolforge.org' ) { 
        $jsub = 'jsub -N redirect ';
        $filee = '/data/project/mdwiki/public_html/texts/redirectlist.txt';
    };
    //---
    // python3 /data/project/mdwiki/mdpy/red.py -page2:Aneurysmal_bone_cyst save
    if ($title != '') {
        $python3 = "python3 $dir/pwb.py mdpy/red -page2:" . rawurlencode($title) . ' save' ;
        //---
        echo '<span class="">The Bot will create redirects for ' . rawurldecode($title) . ' in seconds.</span>';
        //---
    } else {
        //---
        $myfile = fopen( 'redirectlist.txt' , "w");
        fwrite($myfile , $titlelist);
        fclose($myfile);
        //---
        //$python3 = ' ' . $dir . 'red.py -file:' . $filee . ' save' ;
        $python3 = "python3 $dir/pwb.py mdpy/red  -file:$filee save";
        echo '<span class="">The Bot will create redirects for titles in the list in seconds.</span>';
        //---
    };
    //---
	$nana = $jsub . $python3;
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