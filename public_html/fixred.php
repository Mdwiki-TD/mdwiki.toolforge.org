<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix redirects</h3>
    </div>
    <div class="card-body">
<?php
//---
$title = $_REQUEST['title'] ?? '';
//---
if ($title == '') {
    //---
    echo <<<HTML
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
								<input class='form-control' type='text' id='title' name='title' value='$title' required/>
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
	HTML;
    //---
} else {
    //---
    $python3 = "jsub -N fixred python3 ./core/pwb.py mdpy/fixred -page2:" . rawurlencode($title) . ' save' ;
    //---
    if (isset($_REQUEST['test'])) print $python3;
    //---
    $result = shell_exec($python3);
    //---
    print $result;
    //---
    };
//---
echo '</div>';
//---
require('foter.php');
?>