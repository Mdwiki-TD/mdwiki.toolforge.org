<?php
require 'header.php';
print_h3_title("Normalize references (mdwiki).");
//---
$titlelist  = $_REQUEST['titlelist'] ?? '';
$number     = $_REQUEST['number'] ?? '';
$test       = $_REQUEST['test'] ?? '';
//---
// the root path is the first part of the split file path
$pathParts = explode('public_html', __FILE__);
$ROOT_PATH = $pathParts[0];
//---
require  'bots/tfj.php';
//---
function make_form($titlelist, $number, $test)
{
	global $username;
	// ---
	$start_icon = "<input class='btn btn-outline-primary' type='submit' value='send'>";
	// ---
	if ($username == '') $start_icon = '<a role="button" class="btn btn-primary" href="/Translation_Dashboard/auth.php?a=login">Log in</a>';
	// ---
	$testinput = ($test != '') ? '<input type="hidden" name="test" value="1" />' : '';
	//---
	echo <<<HTML
	<form action='fixref.php' method='POST'>
		$testinput
		<div class='container'>
			<div class='container'>
				<div class='row'>
					<div class='col-lg-12'>
						<div class='form-group'>
							<label for='find'><h4>All pages:</h4></label>
							<div class='input-group mb-3'>
								<div class='input-group-prepend'>
									<span class='input-group-text'>Number of pages</span>
								</div>
								<input class='form-control' type='number' name='number' value='$number' placeholder='5000'/>
							</div>
						</div>
					</div>
					<div class='col-lg-12'>
						<h3 class='aligncenter'>or</h3>
					</div>
					<div class='col-lg-12'>
						<div class='form-group'>
							<label for='titlelist'><h4>List of titles:</h4></label>
							<textarea class='form-control' cols='60' rows='7' id='titlelist' name='titlelist'>$titlelist</textarea>
						</div>
					</div>
					<div class='col-lg-12'>
						<h4 class='aligncenter'>
							$start_icon
						</h4>
					</div>
				</div>
			</div>
		</div>
	</form>
HTML;
}

// require 'bots/python.php';
function get_results($aargs)
{
    //---
    global $test;
    //---
    $ccc = " mdpy/fixref/start $aargs save";
    //---
    $params = array(
        'dir' => "core8",
        'localdir' => "core8",
        'pyfile' => 'pwb.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
	$result = do_tfj_sh($params, "fixref");
    //---
    return $result;
}
if ($number == '' && $titlelist == '') {
	make_form($titlelist, $number, $test);
} else {
	//---
	$nn = rand();
	//---
	$command = "";
	//---
	$titlelist = trim($titlelist);
	//---
	if ($titlelist != '') {
		// split py lines
		$lines = explode("\n", $titlelist);
		// if lenth of lines == 1 then
		//---
		if (count($lines) == 1) {
			$title = $lines[0];
			$command .= " -title:$title";
		} else {
			$filename = $nn . '_fix_ref_list.txt';
			//---
			$myfile = fopen('find/' . $filename, "w");
			fwrite($myfile, $titlelist);
			fclose($myfile);
			//---
			$command .= " -file:$filename";
			//---
		}
	} elseif ($number != '') {
		$command .= " allpages -number:$number";
	}
	//---
	echo "<h4 style='color:green'>The bot will start in seconds.</h4>";
	//---
	if ($test != '') echo $command;
	//---
	$result = get_results($command);
	//---
	echo $result;
}
//---
require 'footer.php';
