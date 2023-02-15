<?php require ('header.php'); ?>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>qdels</h3>
    </div>
    <div class="card-body">
<?php
//---
$job = $_GET['job'];
$jsub = "qdel $job";
//---
$qstat = $_GET['qstat'];
$jsub1 = "$qstat";
//---
if ($job != '') { 
    $result = shell_exec($jsub);
    echo $result;
	
} elseif ($jsub1 != '') { 
    $result = shell_exec($jsub1);
    print_r($result);
} else {
    echo "<meta http-equiv='refresh' content='0; url=index.php'>";
}
//---
?>
	</div>
<?php require ('foter.php'); ?>