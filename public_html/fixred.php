<?php 
require ('header.php');
print_h3_title("Fix redirects");
//---
$title = $_REQUEST['title'] ?? '';
//---
require 'bots/tfj.php';
// $result = do_tfj(array( 'name' => '', 'command' => ''));
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
	$t3 = rawurlencode($title);
    //---
    $python3 = "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/fixred -page2:$t3 save";
    //---
    $result = do_tfj(array( 'name' => 'fixred', 'command' => $python3));
    //---
    echo $result;
    //---
    };
//---
require 'footer.php';
?>