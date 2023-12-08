<?php 
require 'header.php';

echo <<<HTML
	<div class="card-header aligncenter" style="font-weight:bold;">
		<h3>Normalize references (mdwiki).</h3>
	</div>
	<div class="card-body">
HTML;
//---
$titlelist  = $_REQUEST['titlelist'] ?? '';
$number     = $_REQUEST['number'] ?? '';
$test       = $_REQUEST['test'] ?? '';
//---
function make_form($titlelist, $number, $test) {
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
							<input class='btn btn-primary' type='submit' value='send'>
						</h4>
					</div>
				</div>
			</div>
		</div>
	</form>
HTML;
}
//---
if ($number == '' && $titlelist == '') {
	make_form($titlelist, $number, $test);
} else {
	//---
	$nn = rand();
	//---
	$command = "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/fixref/start";
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
			fwrite($myfile , $titlelist);
			fclose($myfile);
			//---
			$command .= " -file:$filename";
			//---
		}
	} elseif ($number != '') {
		$command .= " allpages -number:$number";
	}
	//---
	$jobs_run = "toolforge jobs run fixref$nn --command '$command' --image python3.9";
	//---
	echo "<h4 style='color:green'>The bot will start in seconds.</h4>";
	//---
	if ($test != '') print $jobs_run;
	//---
	$result = shell_exec($jobs_run);
	print $result;
}
//---
echo "</div>";
require 'foter.php';