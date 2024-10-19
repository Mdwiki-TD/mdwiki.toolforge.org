<?php
require __DIR__ . '/../header.php';
//---
?>
<style>
    .filterDiv {
        display: none;
    }

    .show2 {
        display: list-item;
    }

    .container {
        overflow: hidden;
    }

    .btne {
        border: none;
        outline: none;
        padding: 12px 16px;
        background-color: #f1f1f1;
        cursor: pointer;
    }

    .btne:hover {
        background-color: #ddd;
    }

    .btne.active {
        background-color: #5d8aa8;
    }
</style>
<?php
//---
$test = $_REQUEST['test'] ?? "";
$id = $_REQUEST['id'] ?? "";
//---
$restart_text = "<a href='job.php?id=$id&to=restart' class='btn btn-primary' target='_blank'>Restart</a>";
// ---
$done_file = $id_dir = __DIR__ . "/find/$id/done.txt";
// ---
if (!is_file($done_file)) {
    $restart_text = "<a href='job.php?id=$id&to=stop' class='btn btn-danger' target='_blank'>Stop</a>";
}
// ---
$strs = "Log file for id:$id $restart_text";
//---
if ($id == '') $strs = 'log files';
//---
echo "
    <div class='card-header aligncenter' style='font-weight:bold;'>
        <h3>$strs</h3>
    </div>
    <div class='card-body'>
        <div class='container'>

";
//---
function str_end_with($haystack, $needle)
{
    return $needle === "" || substr($haystack, -strlen($needle)) === $needle;
};

function make_rows($dirs)
{

    $fs = "
        <div class='col-md'>
            <ul>";
    //---
    $nd = "
            </ul>
        </div>
        ";
    //---
    $row = "
        <div class='row'>
        $fs
        ";
    //---
    // len of $dirs
    $ln = count($dirs);
    //---
    // divid $ln by 3
    $ln2 = $ln / 3;
    $ln2 = $ln2 + 1;
    //---
    $n = 0;
    //---
    foreach ($dirs as $dir) {
        //---
        $file_name = basename($dir);
        //---
        $lastModified = date('m/d/Y H:i:s', filemtime($dir));
        //---
        $n++;
        //---
        if (
            $n >= $ln2
        ) {
            $row .= "
          $nd
          $fs
          ";
            $n = 0;
        };
        //---
        $row .= "
        <li>
          <div class='group'>
              <a href='replace-log.php?id=$file_name'><b><span>$file_name</span></b></a>
              $lastModified
          </div>
        </li>
        ";
    }
    //---
    $row .= "
    $nd
    </div>
    ";
    //---
    return $row;
}
function open_dir()
{
    //---
    $logs_dir = __DIR__ . "/find";
    //---
    // make list of $logs_dir subdirs
    $dirs = glob($logs_dir . '/*');
    // ---
    // sort $dirs by last modified time
    usort($dirs, function ($a, $b) {
        return filemtime($b) - filemtime($a);
    });
    // ---
    $dirs_notdone = array_filter($dirs, function ($dir) {
        return !is_file($dir . '/done.txt');
    });
    // ---
    $dirs_done = array_filter($dirs, function ($dir) {
        return is_file($dir . '/done.txt');
    });
    // ---
    echo "
        <div class='card-title' style='font-weight:bold;'>
            <h3>Jobs not done:</h3>
        </div>
    ";
    // ---
    echo make_rows($dirs_notdone);
    //---
    echo "
        <div class='card-title' style='font-weight:bold;'>
            <h3>Jobs done:</h3>
        </div>";
    // ---
    echo make_rows($dirs_done);
    //---
};
//---
if ($id == '') {
    //---
    open_dir();
    //---
} else {
    //---
    $id_dir = __DIR__ . "/find/$id";
    //---
    $textx_file = $id_dir . "/text.txt";
    if (is_file($textx_file)) {
        $textlog = file_get_contents($textx_file);
        echo '<pre>' . $textlog . '</pre>';
    };
    //---
    $find_file = $id_dir . "/find.txt";
    $replace_file = $id_dir . "/replace.txt";
    $log_file = $id_dir . "/log.txt";
    //---
    if (is_file($find_file) && is_file($replace_file)) {
        //---
        $find    = file_get_contents($find_file);
        $replace = file_get_contents($replace_file);
        //---
        $find_row = "
        <div class='form-group'>
            <label for='find'>Find:</label>
            <textarea class='form-control' id='find' name='find' readonly='true'>$find</textarea>
        </div>";
        //---
        $replace_row = "
        <div class='form-group'>
            <label for='replace'>Replace with:</label>
            <textarea class='form-control' id='replace' name='replace' readonly='true'>$replace</textarea>
        </div>";
        //---
        echo "
        <div class='container-fluid'>
            <div class='row'>
                <div class='col-sm'>$find_row</div>
                <div class='col-sm'>$replace_row</div>
            </div>
        </div>";
    };
    //---
    $rows = '';
    //---
    $log = file_get_contents($log_file);
    //---
    $log = '{' . $log .  '"0":0}';
    $table = json_decode($log);
    //---
    $all = 0;
    $no_change = 0;
    $done = 0;
    $nodone = 0;
    //---
    foreach ($table as $title => $diffid) {
        //---
        if ($title != '0') {
            //---
            $all += 1;
            //---
            $url = "https://mdwiki.org/w/index.php?title=" . $title;
            //---
            $type = '';
            $color = '';
            $text = '';
            //---
            $sta = "
            <li class='filterDiv";
            $end = '</li>
            ';
            //---
            if ($diffid == "no changes") {
                //---
                $no_change += 1;
                $type = 'nochange';
                $color = '';
                $text = 'no changes';
                //---
            } elseif ($diffid > 0) {
                $done += 1;
                $type = 'done';
                $color = 'green';
                $text = 'done';
                $url = "https://mdwiki.org/w/index.php?diff=prev&oldid=" . $diffid;
            } else {
                //---
                $nodone += 1;
                $type = 'nodone';
                $color = 'red';
                $text = 'not done';
            };
            //---
            $rows .= "$sta $type'>page: <a href='$url'><b><span style='color:$color'>$title</span></b></a> $text. $end";
            //---
        };
    };
    //---
    // if ($nodone == 0) $rows .= "<li class='filterDiv nodone'>a</li>";
    //---
    if ($test != '') {
        $rows .= "
        <li>$log</li>";
    };
    //---
    echo "
    <div id='myBtnContainer'>
      <button class='btne active' id='all' onclick=filterSelection('all')>All ($all)</button>
      <button class='btne' id='done' onclick=filterSelection('done')>Done ($done)</button>
      <button class='btne' id='nodone' onclick=filterSelection('nodone')>Not Done ($nodone)</button>
      <button class='btne' id='nochange' onclick=filterSelection('nochange')>No Changes ($no_change)</button>
    </div>
    <br>
    <ul class='container-fluid' style='list-style-type: decimal;'>
    $rows
    </ul>
    <br>";
};
//---
// echo'</div>';
//---
?>


<script>
    filterSelection("all")

    function filterSelection(c) {
        $('.btne').removeClass('active');
        $('#' + c).addClass('active');

        var x, i;
        x = document.getElementsByClassName("filterDiv");
        if (c == "all") c = "";
        for (i = 0; i < x.length; i++) {
            w3RemoveClass(x[i], "show2");
            if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show2");
        }
    }

    function w3AddClass(element, name) {
        var i, arr1, arr2;
        arr1 = element.className.split(" ");
        arr2 = name.split(" ");
        for (i = 0; i < arr2.length; i++) {
            if (arr1.indexOf(arr2[i]) == -1) {
                element.className += " " + arr2[i];
            }
        }
    }

    function w3RemoveClass(element, name) {
        var i, arr1, arr2;
        arr1 = element.className.split(" ");
        arr2 = name.split(" ");
        for (i = 0; i < arr2.length; i++) {
            while (arr1.indexOf(arr2[i]) > -1) {
                arr1.splice(arr1.indexOf(arr2[i]), 1);
            }
        }
        element.className = arr1.join(" ");
    }
</script>
<?php
echo '<!-- start foter -->
';
require __DIR__ . '/../footer.php';
//---
?>
