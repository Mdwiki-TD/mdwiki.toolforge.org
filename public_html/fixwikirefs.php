<?php
require ('header.php');
//---
print_h3_title("Fix references in Wikipedia's:");
//---
$test       = $_GET['test'] ?? '';
$lang       = $_GET['lang'] ?? '';
$title      = $_GET['title'] ?? '';
$save       = isset($_GET['save']) ? 'save' : '';
// $title      = str_replace("'", "", $title);
$movedots   = isset($_GET['movedots']) ? 'checked' : '';
$infobox    = isset($_GET['infobox']) ? 'checked' : '';
//---
?>
    <div class="card-body">
        <form action='fixwikirefs.php' method='GET'>
            <div class='container'>
                <div class='container'>
                    <div class='row'>
                        <div class='col-md-4'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Title</span>
                                </div>
                                <input class='form-control' type='text' id='title' name='title' value=<?php echo add_quotes($title); ?> required/>
                            </div>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Langcode</span>
                                </div>
                                <input class='form-control' type='text' name='lang' value='<?php echo $lang ?>' required/>
                            </div>
                        </div>
                        <div class='col-md-3'>

                            <div class='form-check form-switch'>
                                <input class='form-check-input' type='checkbox' id='save' name='save' value='1' <?php echo isset($_GET['save']) ? 'checked' : '' ?>>
                                <label class='check-label' for='save'>Auto save</label>
			    </div>
				
				<div class='form-check form-switch'>
                                <input class='form-check-input' type='checkbox' id='movedots' name='movedots' value='1' <?php echo $movedots ?>>
                                <label class='form-check-label' for='movedots'>Move dots after references</label>
                            </div>

                            <div class='form-check form-switch'>
                                <input class='form-check-input' type='checkbox' id='infobox' name='infobox' value='1' <?php echo $infobox ?>>
                                <label class='form-check-label' for='infobox'>Expand Infobox</label>
                            </div>
                        </div>
                        <div class='col-md-5'>
                            <h4 class='aligncenter'>
                            <input class='btn btn-primary' type='submit' value='send' />
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
        </form>
<?php
//---
require 'bots/python.php';
//---
function get_results() { 
    //---
    global $test, $lang, $title, $movedots, $infobox, $save;
    //---
    $title2 = str_replace( '+' , '_' , $title );
    $title2 = str_replace( ' ' , '_' , $title2 );
    $title2 = str_replace( '"' , '\\"' , $title2 );
    $title2 = str_replace( "'" , "\\'" , $title2 );
    //---
    $mv = '';
    if ($movedots != '') $mv .= 'movedots';
    if ($infobox != '')  $mv .= ' infobox';
    //---
    $ccc = "returnfile -page:$title2 -lang:$lang $mv $save";
    //---
    $params = array(
        'dir' => '/data/project/mdwiki/pybot/md_core/wprefs',
        'localdir' => '../wprefs',
        'pyfile' => 'bot1.py',
        'other' => $ccc,
        'test' => $test
    );
    //---
    $result = do_py($params);
    //---
    return $result;
}
//---
function strstartswith($text, $end) {
    return strpos($text, $end) === 0;
}
//---
function endsWith($string, $endString) {
    $len = strlen($endString);
    return substr($string, -$len) === $endString;
};
//---
function worknew() {
    //---
    global $lang, $title, $test;
    //---
    $new = "https://$lang.wikipedia.org/w/index.php?title=$title&action=submit";
    //---
    echo "<br>";
    $form = "
	<span style='font-size: 18px;'>New text :</span><br>
	<form id='editform' name='editform' method='POST' action='" . $new . "'>
	<input type='hidden' value='' name='wpEdittime'/>
	<input type='hidden' value='' name='wpStarttime'/>
	<input type='hidden' value='' name='wpScrolltop' id='wpScrolltop'/>
	<input type='hidden' value='12' name='parentRevId'/>
	<input type='hidden' value='wikitext' name='model'/>
	<input type='hidden' value='text/x-wiki' name='format'/>
	<input type='hidden' value='1' name='wpUltimateParam'/>
	<input type='hidden' name='wpSummary' value='Fix references, Expend infobox mdwiki.toolforge.org.'>
	<input type='hidden' id='wikitext-old' value=''>
    ";
    //---
    $resultb = get_results();
    $resultb = trim($resultb);
    //---
    $t1 = strstartswith( $resultb , '/mdwiki/public_html/wprefcash/' );
    $t2 = strstartswith( $resultb , '/data/project/mdwiki/public_html/wprefcash/' );
    //---
    $t3 = endsWith( $resultb , '.txt' );
    // $t3 = strstartswith( $resultb , '/mdwiki/public_html/wprefcash/' );
    //---
    $edit_line = "<br>
    <div class='aligncenter'>
        <a class='btn btn-primary' href='$new'>Go to edit page.</a>
    </div>
    ";
    //---
    if ($test == 'x') {
	echo "<br>($resultb)<br>";
    };
    if ($resultb == 'no changes') {
        echo "no changes";
    } elseif ($resultb == "notext") {
        echo("text == ''");
	    
    } elseif ($resultb == "ok") {
        echo("save done.");
	    
    } elseif ($t1 || $t2 || $t3 || isset($_REQUEST['test'])) {
        $newtext = file_get_contents( $resultb );
        $form = $form . "<textarea id='wikitext-new' class='form-control' name='wpTextbox1'>" . $newtext . "</textarea>
        <br>
    <div class='editOptions aligncenter'>
        <input id='wpPreview' type='submit' class='btn btn-primary' tabindex='5' title='[p]' accesskey='p' name='wpPreview' value='Preview changes'/>
        <input id='wpDiff' type='submit' class='btn btn-primary' tabindex='7' name='wpDiff' value='Make edits' accesskey='v' title='show changes.'>
    <div class='editButtons'>
    </div>
    </div>
    </form>";
        echo $form;
        $edit_line = '';
    };
    //---
    echo "$edit_line";
    //---
};
//--
if ($title != '' && $lang != '') worknew();
//---
require 'footer.php';
?>
