<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix duplicte redirects.</h3>
    </div>
    <div class="card-body">
<?php
//---
$start = $_REQUEST['start'];
$test = $_REQUEST['test'];
//---
if ($start == '') {
    echo "
    <form action='dup.php' method='POST'>
        <div class='col-lg-12'>
            <h4 class='aligncenter'>
                <input class='btn btn-primary' type='submit' name='start' value='Start' />
            </h4>
        </div>
    </form>";
} else {
    //---
    $dir = './core'; 
    //---
    $faf = "jsub -N fixduplict python3 $dir/pwb.py mdpy/dup save";
    //---
    if ($test != '') print $faf;
    //---
    $result = shell_exec($faf);
    print $result;
    //---
};
//---
?>
</div>
<?php require('foter.php'); ?>