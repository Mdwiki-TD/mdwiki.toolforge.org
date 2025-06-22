<?PHP

namespace LeaderTables;

include_once __DIR__ . '/tables.php';

$mainlang = $_GET['lang'] ?? '';

function make_modal_fade($label, $text, $id, $button = '')
{
    $exampleModalLabel = rand(1000, 9999);
    return <<<HTML

        <!-- Logout Modal-->
        <div class="modal fade" id="$id" tabindex="-1" role="dialog" aria-labelledby="$exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h6 class="modal-title" id="$exampleModalLabel">$label</h6>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">$text</div>
                    <div class="modal-footer">
                        $button
                        <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    HTML;
}
function NumbsTableNew(): string
{
    global $numbers, $mainlang;

    // Initialize the HTML string with the table header
    $Numbers_table = <<<HTML
    <table class="sortable table table-striped table-sm">
    <thead>
        <tr>
            <th class="spannowrap">Type</th>
            <th>Number</th>
        </tr>
    </thead>
    <tbody>
    HTML;

    // Define the keys that should be skipped
    $skip_keys = ['Articles', 'Languages'];

    // Loop through each key-value pair in the numbers array
    foreach ($numbers as $key => $value) {

        // If the key is one of the skipped keys and $mainlang is not an empty string, continue to the next iteration
        // This effectively skips the current key-value pair and goes to the next one.
        if (in_array($key, $skip_keys) && $mainlang !== '') {
            continue;
        }

        // if (in_array($key, $skip_keys) && $mainlang !== '') {

        // if type is array then count
        // if (is_array($value)) $value = count($value);

        // Format the value as a number
        // This adds commas as thousands separators for readability
        $value = number_format($value);

        // Add a new row to the table for the current key-value pair
        $Numbers_table .= <<<HTML
        <tr>
            <td><b>$key</b></td>
            <td>$value</td>
        </tr>
    HTML;
    }

    // Close the table body and the table itself
    $Numbers_table .= <<<HTML
    </tbody>
    </table>
    HTML;

    // Return the resulting HTML string
    return $Numbers_table;
};

function UsersTableNew(): string
{
    global $top_translators, $translators_views, $translators_words, $mainlang;

    // Start the table with a header row
    $text = <<<HTML
    <table class="table table-striped table-sm soro2">
        <thead>
            <tr>
                <th class="spannowrap">#</th>
                <th class="spannowrap">User</th>
                <th>Number</th>
                <th>Words</th>
                <th>Views</th>
            </tr>
        </thead>
        <tbody>
    HTML;

    // Sort translators by descending order of user count.
    arsort($top_translators);

    $numb = 0;

    // Loop through each translator.
    foreach ($top_translators as $user => $usercount) {

        // Increment number count.
        $numb++;

        // Get the translator's views and words count, or default to 0 if not available.
        $views = isset($translators_views[$user]) ? number_format($translators_views[$user]) : 0;
        $words = isset($translators_words[$user]) ? number_format($translators_words[$user]) : 0;

        // URL encode the username, replacing '+' with '_'.
        $use = rawurlencode($user);
        $use = str_replace('+', '_', $use);

        // Generate the URL for user's talk page.
        $talk_url = "//$mainlang.wikipedia.org/w/index.php?title=User_talk:$user&action=edit&section=new";

        // Append the HTML for a new row in the table for the translator.
        $text .= <<<HTML
        <tr>
            <td>$numb</td>
            <td><a target="_blank" href="$talk_url">$user</a></td>
            <td>$usercount</td>
            <td>$words</td>
            <td>$views</td>
        </tr>
        HTML;
    };

    // End of HTML table.
    $text .= <<<HTML
        </tbody>
        <tfoot></tfoot>
    </table>
    HTML;

    // Return the generated HTML.
    return $text;
}

function module_copy(): string
{
    global $top_translators, $mainlang;

    $text = "<textarea cols='55' rows='10' id='users_targets' name='users_targets'>";

    arsort($top_translators);

    foreach ($top_translators as $user => $usercount) {

        $mass = "#{{#target:User:$user|$mainlang.wikipedia.org}}";
        $text .= $mass . "\n";
    };
    //---
    $text .= '</textarea>';
    //---
    $modal = make_modal_fade('', $text, 'targets', '<a class="btn btn-outline-primary" onclick="copy_target_text(\'users_targets\')">Copy</a>');
    //---
    return $modal;
}

function LangsTableNew(): string
{

    global $translates_by_lang;

    // Sort the array in reverse order by value
    arsort($translates_by_lang);

    // Initialize the HTML text for the table with headers
    $text = <<<HTML
    <table class='sortable table table-striped table-sm'>
    <thead>
        <tr>
            <th>#</th>
            <th class='spannowrap'>Language</th>
            <th>Count</th>
            <th>Words</th>
            <th>Views</th>
        </tr>
    </thead>
    <tbody>
    HTML;

    // Initialize row number
    $numb = 0;

    // Loop through each language in the array
    foreach ($translates_by_lang as $langcode => $table) {

        // Get the Articles numbers, words and views
        $comp  = count($table['titles']);
        $words = number_format($table['words']);
        $views = number_format($table['views']);

        // Only add a table row if there are articles for this language
        if ($comp > 0) {

            $numb++;

            // Add a table row with the language details
            $text .= <<<HTML
                <tr>
                    <td>$numb</td>
                    <td><a href='index.php?lang=$langcode'>$langcode</a></td>
                    <td>$comp</td>
                    <td>$words</td>
                    <td>$views</td>
                </tr>
            HTML;
        };
    };

    // Close the table body and table tags in the HTML
    $text .= <<<HTML
        </tbody>
        </table>
    HTML;

    // Return the HTML text
    return $text;
}
