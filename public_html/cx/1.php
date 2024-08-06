<?php

// https://cxserver.wikimedia.org/v2/page/en/ar/Hippocrates_(disambiguation)
header("Content-type: application/json");

if (isset($_GET['test'])) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}

$title = $_GET['title'] ?? '';

$HTML_text = <<<HTML
    <p id="mwRA">Typically recommended initial treatments include <a rel="mw:WikiLink" href="./Non_invasive_positive_pressure_ventilation" title="Non invasive positive pressure ventilation" class="mw-redirect" id="mwRQ">non invasive positive pressure ventilation</a> (NIPPV) and <a rel="mw:WikiLink" href="./Intravenous_nitroglycerin" title="Intravenous nitroglycerin" class="mw-redirect" id="mwRg">intravenous nitroglycerin</a>.<sup about="#mwt80" class="mw-ref reference" id="cite_ref-Ag2016_3-4" rel="dc:references" typeof="mw:Extension/ref" data-mw='{"name":"ref","attrs":{"name":"Ag2016"},"body":{"id":"mw-reference-text-cite_note-Ag2016-3"}}'><a href="./Sympathetic_crashing_acute_pulmonary_edema#cite_note-Ag2016-3" style="counter-reset: mw-Ref 3;" id="mwRw"><span class="mw-reflink-text" id="mwSA">[3]</span></a></sup> NIPPV should use high pressures of 15 to 18 cm H2O and large amounts of nitroglycerin are typically required.<sup about="#mwt81" class="mw-ref reference" id="cite_ref-EMCrit2024_1-14" rel="dc:references" typeof="mw:Extension/ref" data-mw='{"name":"ref","attrs":{"name":"EMCrit2024"}}'><a href="./Sympathetic_crashing_acute_pulmonary_edema#cite_note-EMCrit2024-1" style="counter-reset: mw-Ref 1;" id="mwSQ"><span class="mw-reflink-text" id="mwSg">[1]</span></a></sup> If this is insufficient <a rel="mw:WikiLink" href="./Clevidipine" title="Clevidipine" id="mwSw">clevidipine</a>, <a rel="mw:WikiLink" href="./Nicardipine" title="Nicardipine" id="mwTA">nicardipine</a>, or <a rel="mw:WikiLink" href="./Enalaprilat" title="Enalaprilat" id="mwTQ">enalaprilat</a> may be used.<sup about="#mwt82" class="mw-ref reference" id="cite_ref-EMCrit2024_1-15" rel="dc:references" typeof="mw:Extension/ref" data-mw='{"name":"ref","attrs":{"name":"EMCrit2024"}}'><a href="./Sympathetic_crashing_acute_pulmonary_edema#cite_note-EMCrit2024-1" style="counter-reset: mw-Ref 1;" id="mwTg"><span class="mw-reflink-text" id="mwTw">[1]</span></a></sup> Routine use of <a rel="mw:WikiLink" href="./Diuretics" title="Diuretics" id="mwUA">diuretics</a>, such as <a rel="mw:WikiLink" href="./Furosemide" title="Furosemide" id="mwUQ">furosemide</a>, is not recommended.<sup about="#mwt83" class="mw-ref reference" id="cite_ref-Ag2016_3-5" rel="dc:references" typeof="mw:Extension/ref" data-mw='{"name":"ref","attrs":{"name":"Ag2016"}}'><a href="./Sympathetic_crashing_acute_pulmonary_edema#cite_note-Ag2016-3" style="counter-reset: mw-Ref 3;" id="mwUg"><span class="mw-reflink-text" id="mwUw">[3]</span></a></sup> It generally resolves rapidly, though may recur.<sup about="#mwt84" class="mw-ref reference" id="cite_ref-EMCrit2024_1-16" rel="dc:references" typeof="mw:Extension/ref" data-mw='{"name":"ref","attrs":{"name":"EMCrit2024"}}'><a href="./Sympathetic_crashing_acute_pulmonary_edema#cite_note-EMCrit2024-1" style="counter-reset: mw-Ref 1;" id="mwVA"><span class="mw-reflink-text" id="mwVQ">[1]</span></a></sup> It is a relatively common reason to present to the <a rel="mw:WikiLink" href="./Emergency_room" title="Emergency room" id="mwVg">emergency room</a>.<sup about="#mwt85" class="mw-ref reference" id="cite_ref-Ag2016_3-6" rel="dc:references" typeof="mw:Extension/ref" data-mw='{"name":"ref","attrs":{"name":"Ag2016"}}'><a href="./Sympathetic_crashing_acute_pulmonary_edema#cite_note-Ag2016-3" style="counter-reset: mw-Ref 3;" id="mwVw"><span class="mw-reflink-text" id="mwWA">[3]</span></a></sup></p>

    </section><section data-mw-section-id="1" id="mwWQ"><h2 id="Treatment">Treatment</h2>
    HTML;


    // Decode HTML_text using htmlentities
// $HTML_text = htmlentities($HTML_text, ENT_QUOTES, 'UTF-8');
$HTML_text = utf8_encode($HTML_text);

// Prepare JSON data
$jsonData = [
    "sourceLanguage" => "mdwiki",
    "title" => $title,
    "revision" => $revid,
    "segmentedContent" => $HTML_text
];

// Encode data as JSON with appropriate options
$jsonOutput = json_encode($jsonData);

// Output the JSON
echo $jsonOutput;
