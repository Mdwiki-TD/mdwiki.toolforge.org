<?php
if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

require 'leader_tables.php';

/**
 * Generate a string containing HTML for the category table.
 * 
 * @return string The HTML string for the category table.
 */
function generateLeaderboardTable(): string {
    $numbersTable = createNumbersTable();
    $numbersCol   = makeColSm4('Numbers', $numbersTable, $numb=3);

    // TODO: Uncomment these lines to include a users table.
    // $usersTable = makeUsersTable();
    // $usersCol   = makeColSm4('Top Translators', $usersTable, $numb=5);
    $usersCol      = '';

    $languagesTable = makeLangTable();
    $languagesCol = makeColSm4('Top Languages', $languagesTable, $numb=6);

    return <<<HTML
        <span align="center">
            <h3>Leaderboard</h3>
        </span>
        <div class="row">
            $numbersCol
            <!-- $usersCol -->
            $languagesCol
        </div>
    HTML;
}

$leaderboardHtml = generateLeaderboardTable();

echo <<<HTML
<div class="container-fluid">
    $leaderboardHtml
</div>
HTML;
?>
