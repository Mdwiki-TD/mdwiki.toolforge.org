<?php

use OAuth\Settings\Settings;
use OAuth\User\CurrentUser;

if (substr(__DIR__, 0, 2) == 'I:') {
    include_once 'I:/MD_TOOLS/mdwiki.toolforge.org/PHP_REPOS/auth_repo/src/include_all.php';
} else {
    ini_set('session.use_strict_mode', '1');
    include_once __DIR__ . '/auth/include_all.php';
}

/*@phpstan-ignore-next-line */
$currentUser = CurrentUser::getInstance();
$settings = Settings::getInstance();

$msg = $currentUser->getAlertMessage();

if ($msg) {
    echo <<<HTML
	<div class='container'>
		<div class="alert alert-danger" role="alert">
			<i class="bi bi-exclamation-triangle"></i> $msg
		</div>
	</div>
	HTML;
}

if ($currentUser->isLoggedIn()) {
    $global_username = $currentUser->getUsername();
} else {
    $global_username = "";
}

define('global_username', $global_username);
