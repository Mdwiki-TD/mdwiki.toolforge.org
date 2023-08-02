<?php
namespace TopIndex;

use function Functions\makeColSm4;
use function LeaderTables\createNumbersTable;
use function LeaderTables\makeLangTable;

if (isset($_REQUEST['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function generateLeaderboardTable(): void {
    $numbersTable = createNumbersTable();
    $numbersCol   = makeColSm4('Numbers', $numbersTable, $numb=3);

    // TODO: Uncomment these lines to include a users table.
    // $usersTable = makeUsersTable();
    // $usersCol   = makeColSm4('Top Translators', $usersTable, $numb=5);
    $usersCol      = '';

    $languagesTable = makeLangTable();
    $languagesCol = makeColSm4('Top Languages', $languagesTable, $numb=6);

    echo <<<HTML
        <div class="container-fluid">
            <span align="center">
                <h3>Leaderboard</h3>
            </span>
            <div class="row">
                $numbersCol
                <!-- $usersCol -->
                $languagesCol
            </div>
        </div>
    HTML;
}
?>
