<?php
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
}

include_once __DIR__ . '/../header.php';
include_once __DIR__ . '/bots/tfj.php';

use function BOTS\TFJ\do_tfj_sh;

echo <<<HTML
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix redirects</h3>
    </div>
    <div class="card-body">
HTML;
//---
$title = $_GET['title'] ?? '';
$test  = $_GET['test'] ?? '';
//---
echo <<<HTML
	<div class='container'>
HTML;
//---
$testinput = (!empty($test)) ? '<input type="hidden" name="test" value="1" />' : '';
//---
// global $username;
// ---
$start_icon = "<input class='btn btn-outline-primary' type='submit' value='send'>";
// ---
if (empty($username)) $start_icon = '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
// ---
echo <<<HTML
	<form action='fixred.php' method='GET'>
		$testinput
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
						$start_icon
					</h4>
				</div>
			</div>
		</div>
	</form>
HTML;

function get_results($title)
{
	//---
	global $test;
	//---
	$title2 = str_replace('+', '_', $title);
	$title2 = str_replace(' ', '_', $title2);
	$title2 = str_replace('"', '\\"', $title2);
	$title2 = str_replace("'", "\\'", $title2);
	$title2 = rawurlencode($title2);
	//---
	$ccc = " mdpy/fixred -page2:$title2 save";
	//---
	$params = array(
		'dir' => "c8",
		'localdir' => "c8",
		'pyfile' => 'pwb.py',
		'other' => $ccc,
		'test' => $test
	);
	//---
	$result = do_tfj_sh($params, 'fixred');
	//---
	return $result;
}
//---
if (!empty($title) && !empty($username)) {
	echo "starting:<br>";
	//---
	$resultb = get_results($title);
	//---
	echo "finished. result:($resultb)<br>";
	//---
	echo $resultb;
};
//---
echo <<<HTML
	</div>
HTML;
//---
include_once __DIR__ . '/../footer.php';
