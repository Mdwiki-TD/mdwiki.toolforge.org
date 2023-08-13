<?php

namespace TopIndex;

use function Functions\ColSm;
use function LeaderTables\NumbsTableNew;
use function LeaderTables\LangsTableNew;
use function LeaderTables\UsersTableNew;

if (isset($_REQUEST['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function generateLeaderboardTable(): void
{
    $numbersTable = NumbsTableNew();
    $numbersCol   = ColSm('Numbers', $numbersTable, $numb = 3);
    // TODO: Uncomment these lines to include a users table.
    // $usersTable = UsersTableNew();
    // $usersCol   = ColSm('Top Translators', $usersTable, $numb=5);
    $usersCol      = '';

    $languagesTable = LangsTableNew();
    $languagesCol = ColSm('Top Languages', $languagesTable, $numb = 8);

    echo <<<HTML
        <div class="container-fluid">
            <span align="center">
                <h3>Leaderboard</h3>
            </span>
            <div class="row">
                <div class="col-md-3">
                    $numbersCol
                </div>
                <div class="col-md-8">
                    $languagesCol
                </div>
            </div>
        </div>
    HTML;
}
