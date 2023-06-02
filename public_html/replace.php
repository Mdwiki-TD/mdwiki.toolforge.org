<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Find and replace.</h3>
    </div>
    <div class="card-body">
<?php
//---
$listtype   = $_REQUEST['listtype'] ?? '';
$test       = $_REQUEST['test'] ?? '';
$find       = $_REQUEST['find'] ?? '';
$replace    = $_REQUEST['replace'] ?? '';
$number     = $_REQUEST['number'] ?? '';
$code       = $_REQUEST['code'] ?? '';
//---
function Get_Value() {
    //---
    global $code, $find, $replace, $test, $number;
    //---
    $code_note = "";
    if ( $code != '' and $code != 'james#99' ) $code_note = "<span style='font-size:12pt;color:red'>! (" . $code . ") is wrong code.</span>";
    //---
    $find_row = "
    <div class='form-group'>
        <label for='find'>Find:</label>
        <textarea class='form-control' cols='40' rows='6' id='find' name='find' required>$find</textarea>
    </div>";
    //---
    $replace_row = "
    <div class='form-group'>
        <label for='replace'>Replace with:</label>
        <textarea class='form-control' cols='40' rows='6' id='replace' name='replace' placeholder='(write empty to replace it with empty value.)' required>$replace</textarea>
    </div>";
    //---
    $input_1 = "
    <div class='input-group mb-3'>
        <div class='input-group-prepend'>
            <span class='input-group-text'>Number of replacements</span>
        </div>
        <input  class='form-control' type='number' name='number' value='$number' placeholder='max'/>
    </div>
    <div class='input-group mb-3'>
        <div class='input-group-prepend'>
            <span class='input-group-text'>Code</span>
        </div>
        <input class='form-control' type='text' name='code' value='$code' required/>$code_note
    </div>";
    //---
    $test_1 = "";
    if ($test != '') $test_1 = "
    <div class='custom-control custom-radio custom-control-inline'>
        <input type='radio' class='custom-control-input' id='c1' name='test' value='1'>
        <label class='custom-control-label' for='c1'>Test</label>
    </div>
    ";
    //---
    $input_2 = "
    <div class='custom-control custom-radio custom-control-inline'>
        <input type='radio' class='custom-control-input' id='customRadio' name='listtype' value='newlist' checked>
        <label class='custom-control-label' for='customRadio'>Use API search</label>
    </div>
    <div class='custom-control custom-radio custom-control-inline'>
        <input type='radio' class='custom-control-input' id='customRadio2' name='listtype' value='oldlist'>
        <label class='custom-control-label' for='customRadio2'>Work in all pages</label>
    </div>
    $test_1
    ";
    //---
    echo "
    <form action='replace.php' method='POST'>
        <div class='container-fluid'>
            <div class='row'>
                <div class='col-sm'>$find_row</div>
                <div class='col-sm'>$replace_row</div>
            </div> 
            <div class='row'>
                <div class='col-sm'>$input_1</div>
                <div class='col-sm'>$input_2</div>
            </div>
            <div class='col-lg-12'>
                <h4 class='aligncenter'>
                    <input class='btn btn-primary' type='submit' value='send'>
                </h4>
            </div>
        </div>
    </form>";
    //---
    }
//---
function writee($file,$text) {
    $myfile = fopen( 'find/' . $file, "w");
    fwrite($myfile , $text);
    fclose($myfile);
    }
//---
function worknew($find, $replace, $number) {
    //---
    global $listtype;
    //---
    $nn = rand();
    //$nn = "";
    //---
    if ( $find != '' and $replace != '' ) {
        writee( $nn . '_find.txt' , $find );
        writee( $nn . '_replace.txt' , $replace );
    }
    //---
    // python3 /data/project/mdwiki/mdpy/replace1.py -rand:84230289 ask newlist
    $jsub = 'python3 /data/project/mdwiki/core8/pwb.py mdpy/replace1 -rand:' . $nn . ' -number:' . $number ;
    //---
    if ($listtype == 'newlist') {
        $jsub .= ' newlist';
    };
    //---
    $jsub = '/usr/bin/jsub -N replace' . $nn . ' ' . $jsub ;
    //---
    $test = $_REQUEST['test'];
    //---
    if ($test != '') { echo $jsub;};
    //---
    echo "<span style='font-size:15pt;color:green'>";
    echo "<br>";
    echo 'The bot will start the replacements in seconds.';
    echo '<br>';
    echo 'Log will be <a href="replace-log.php?id=' . $nn . '"><b>Here.</b></a>';
    echo '</span>';
    //---
    echo "<br>";
    $result = shell_exec($jsub);
    print $result;
    //---
    //} else {
        //echo "<span style='font-size:15pt;color:red'>Wrong code.</span>";
        //print( "<br>" );
        //print( "<br>" );
        //Get_Value();
    //};
    //---
    }
//---
if ( $find == '' or $replace == '' or $code == '' or ( $code != '' and $code != 'james#99' ) ) {
    echo Get_Value() ;
} else {
    echo worknew($find, $replace, $number) ;
};
//---

//---
?>
</div>
<?php require('foter.php'); ?>
