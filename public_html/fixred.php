<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix redirects</h3>
    </div>
    <div class="card-body">
<?php
//---
$title = $_GET['title'];
//---
if ($title == '') {
    //---
    echo "
    <form action='fixred.php' method='GET'>
        <div class='container'>
            <div class='container'>
                <div class='row'>
                    <div class='col-lg-12'>
                        <h6>To run the bot on all pages type: all.</h6>
                    </div>
                    <div class='col-lg-12'>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' name='title' value='$title' required/>
                        </div>
                    </div>
                    <div class='col-lg-12'>
                        <h4 class='aligncenter'>
                        <input class='btn btn-primary' type='submit' value='send' />
                        </h4>
                    </div>
                </div>
            </div>
        </div>
    </form>
    ";
    //---
} else {
    //---
    $dir = '/data/project/mdwiki/core'; 
    $python3 = "jsub -N fixred python3 $dir/pwb.py mdpy/fixred -page2:" . rawurlencode($title) . ' save' ;
    //---
    if (isset($_REQUEST['test'])) print $python3;
    //---
    $result = shell_exec($python3);
    //---
    print $result;
    //---
    };
//---
?>
</div>
<?php require('foter.php'); ?>