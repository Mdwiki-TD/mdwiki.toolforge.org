<?PHP
namespace FilterCat;

function makeDropdown($tab, $cat, $id, $add) {
    //---
    $options = "";
    //---
    foreach ( $tab AS $dd ) {
        //---
        $se = '';
        //---
        if ( $cat == $dd ) $se = 'selected';
        //---
        $options .= <<<HTML
            <option value='$dd' $se>$dd</option>
        HTML;
        //---
    };
    //---
	$sel_line = "";
	//---
    if ($add != '' ) {
	    $sel = "";
	    if ( $cat == $add ) $sel = "celected";
        $sel_line = "<option value='$add' $sel>$add</option>";
    }
	//---
    return <<<HTML
        <select dir="ltr" id="$id" name="$id" class="form-select" data-bs-theme="auto">
            $sel_line
            $options
        </select>
    HTML;
};
//---
function filter_stat($cat) {
	$cats_titles = [
        "Files_imported_from_NC_Commons",
        "Translated_from_MDWiki",
    ];
	//---
	$d33 = <<<HTML
		<div class="input-group">
			<span class="input-group-text">%s</span>
			%s
		</div>
	HTML;
	//---
	$y1 = makeDropdown($cats_titles, $cat, 'cat', '');
	$uuu = sprintf($d33, 'Category:', $y1);
	//---
    return $uuu;
}
function filter_cat_form($index, $cat) {
    $uuu = filter_stat($cat);
    //---
    $lang = $_GET['lang'] ?? '';
    $lang_input = "<input type='hidden' name='lang' value='$lang' />";
    //---
    $filter_cat = <<<HTML
        <div class='card-body'>
            <form method='get' action='$index'>
                $lang_input
                <div class='row'>
                    <div class='col-md-5'>
                        $uuu
                    </div>
                    <div class='aligncenter col-md-2'>
                        <input class='btn btn-primary' type='submit' name='start' value='Filter' />
                    </div>
                </div>
            </form>
        </div>
    HTML;
    //---
    $res = <<<HTML
        <div class="container">
            $filter_cat
        </div>
    HTML;
    //---
    return $res;
}