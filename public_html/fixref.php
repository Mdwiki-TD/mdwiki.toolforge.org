<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Normalize references (mdwiki).</h3>
    </div>
    <div class="card-body">
<?php
//---
$titlelist  = $_REQUEST['titlelist'] ?? '';
$number     = $_REQUEST['number'] ?? '';
//---
function writee($file,$text) {
    $myfile = fopen( 'find/' . $file, "w");
    fwrite($myfile , $text);
    fclose($myfile);
    }
//---
function make_form() {
    //---
    global $titlelist, $number;
    //---
    $number2 = $number;
    //---
    echo "
    <form action='fixref.php' method='POST'>    
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
      ";
};
//---
if ($number == '' && $titlelist == '') {
    make_form();
} elseif ($number != '' or $titlelist != '') {
    //$nn = '';
    //---
    $dir = '/data/project/mdwiki/core8'; 
    $jsub = '';
    //---
    $nn = rand();
    if ( $titlelist != '' ) {
        $filename = $nn . '_fix_ref_list.txt';
        writee( $filename , $titlelist );
        $jsub = "python3 $dir/pwb.py mdpy/fixref -file:" . $filename;
        //---
    } elseif ( $number != '' ) {
        $jsub = "python3 $dir/pwb.py mdpy/fixref allpages -number:" . $number;
    };
    //---
    $jsub = 'jsub -N fixref' . "$nn $jsub" ;
    //---
    echo "<h4 style='color:green'>The bot will start in seconds.</h4>";
    //---
    if (isset($_REQUEST['test'])) print $jsub;
    //---
    $result = shell_exec($jsub);
    print $result;
    };
//---
?>
</div>
<?php require('foter.php'); ?>