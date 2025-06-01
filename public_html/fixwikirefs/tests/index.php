<?php
if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};
include_once __DIR__ . '/../../header.php';
?>
<div>
    <div class="card-header aligncenter" style="font-weight:bold;">
        <h3>Fix references in Wikipedia's:</h3>
    </div>
    <div class="card-body">
        <form id="myForm">
            <div class='row'>
                <div class='col-md-4'>
                    <div class='input-group mb-3'>
                        <div class='input-group-prepend'>
                            <span class='input-group-text'>Langcode</span>
                        </div>
                        <input type="text" id="lang" name="lang" value="de">
                        <input type="text" id="do_test" name="do_test" value="1" style="display:none;">
                    </div>
                </div>
                <div class='col-md-4'>
                    <h4 class='aligncenter'>
                        <input class='btn btn-outline-primary' type="submit" value="Submit">
                        <span id="load" class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="display:none;"></span>
                    </h4>
                </div>
                <div class='col-md-12'>
                    <div class='input-group mb-3'>
                        <textarea class='form-control' id="text" name="text">La '''plazomicina''' , que es vendida bajo varias marcas incluyendo  Zemdri, es un [[Aminoglucósido|antibiótico aminoglucósido]] utilizado para tratar [[Infección urinaria|infecciones complicadas del tracto urinario]] .  <ref name="AHFS2019" /> A partir de 2019 se recomienda solo para aquellas personas en quienes las alternativas no son una opción. <ref name="AHFS2019" /> Este medicamento se administra mediante [[Terapia intravenosa|inyección en una vena]] . <ref name="AHFS2019" />
                    </textarea>
                    </div>
                </div>
            </div>
    </div>
    <div id='command'></div>
</div>
<div class="card">
    <div class="card-header aligncenter" style="font-weight:bold;">
        Result: <div id='result'></div>
    </div>
    <div class='card-body'>
        <div class='form-group'>
            <textarea id='newtext' class='form-control' name='newtext'></textarea>
        </div>
    </div>
</div>

<script>
    document.getElementById('myForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission
        $("#load").show();

        // Create a FormData object from the form
        let formData = new FormData(this);

        // Send a POST request to the PHP page
        await fetch('do_text.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('command').innerHTML = data.command;
                document.getElementById('result').innerHTML = data.result;
                document.getElementById('newtext').value = data.newtext;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        $("#load").hide();
    });
</script>

<?php
//---
require __DIR__ . '/../../footer.php';
