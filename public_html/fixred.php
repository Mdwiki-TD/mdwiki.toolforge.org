<?php
require ('header.php');
print_h3_title("Fix redirects");
//---
$title = $_REQUEST['title'] ?? '';
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
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
							<input class='btn btn-outline-primary' type='submit' value='send' />
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
	$t3 = rawurlencode($title);
    //---
    $python3 = "$ROOT_PATH/local/bin/python3 $ROOT_PATH/core8/pwb.py mdpy/fixred -page2:$t3 save";
    //---
    $result = shell_exec($python3);
    // ---
    echo $result;
    //---
    };
//---
require 'footer.php';
