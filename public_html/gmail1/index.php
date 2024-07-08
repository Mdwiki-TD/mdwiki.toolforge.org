<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// echo __DIR__;

// [START gmail_quickstart]
include_once __DIR__ . '/vendor/autoload.php';

// if (php_sapi_name() != 'cli') throw new Exception('This application must be run on the command line.');

use Google\Client;
use Google\Service\Gmail;
use Google\Service\Gmail\Message;
use Google\Service\Gmail\Draft;

/**
 * Returns an authorized API client.
 * @return Client the authorized client object
 */
function getClient() {
    $client = new Client();
    $client->setApplicationName('Gmail API PHP Quickstart');
    $client->setScopes('https://mail.google.com/');
    $client->setAuthConfig('credentials.json');
    $client->setAccessType('offline');
    $client->setPrompt('select_account consent');

    // Load previously authorized token from a file, if it exists.
    // The file token.json stores the user's access and refresh tokens, and is
    // created automatically when the authorization flow completes for the first
    // time.
    $tokenPath = 'tokenphp.json';
    if (file_exists($tokenPath)) {
        $accessToken = json_decode(file_get_contents($tokenPath), true);
        $client->setAccessToken($accessToken);
    }

    // If there is no previous token or it's expired.
    if ($client->isAccessTokenExpired()) {
        // Refresh the token if possible, else fetch a new one.
        if ($client->getRefreshToken()) {
            $client->fetchAccessTokenWithRefreshToken($client->getRefreshToken());
        } else {
            // Request authorization from the user.
            $authUrl = $client->createAuthUrl();
            printf("Open the following link in your browser:\n%s\n", $authUrl);
            print 'Enter verification code: ';
            $authCode = trim(fgets(STDIN));

            // Exchange authorization code for an access token.
            $accessToken = $client->fetchAccessTokenWithAuthCode($authCode);
            $client->setAccessToken($accessToken);

            // Check to see if there was an error.
            // if (array_key_exists('error', $accessToken)) {
            $error = $accessToken['error'] ?? null;
            if ($error) {
                throw new Exception(join(', ', $accessToken));
            }
        }
        // Save the token to a file.
        if (!file_exists(dirname($tokenPath))) {
            mkdir(dirname($tokenPath), 0700, true);
        }
        file_put_contents($tokenPath, json_encode($client->getAccessToken()));
    }
    return $client;
}


// Get the API client and construct the service object.
$client = getClient();
$service = new Gmail($client);

$user = 'me';

// Print the labels in the user's account.
/*
$results = $service->users_labels->listUsersLabels($user);

if (count($results->getLabels()) == 0) {
    print "No labels found.\n";
} else {
    print "Labels:\n";
    foreach ($results->getLabels() as $label) {
        printf("- %s\n", $label->getName());
    }
}
*/
// [END gmail_quickstart]

// Helper function to create an email

//---
$msg        = $_REQUEST['msg'] ?? '';
if (empty($msg)) {
    echo "Please enter a message.";
    exit;
};
//---
$email_to   = $_REQUEST['email_to'] ?? '';
$email_from = $_REQUEST['email_from'] ?? 'mdwiki.org@gmail.com';
$msg_title  = $_REQUEST['msg_title'] ?? 'Wiki Project Med Translation Dashboard';
//---
$ccme       = isset($_REQUEST['ccme']) ? 1 : 0;
$cc_to      = $_REQUEST['cc_to'] ?? '';
//---
$msg1 = <<<HTML
    <!DOCTYPE html>
    <html lang='en' dir='ltr' style='
            font-family: sans-serif;
            line-height: 1.15;
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: transparent;'>
        <head>
            <title>Translation Dashboard</title>
        </head>

        <body dir='ltr' style='
            margin: 0;
            font-size: 1rem;
            font-weight: 400;
            line-height: 1.5;
            color: #212529;
            text-align: left;
            background-color: #fff;
            padding-bottom: 10px;
            padding-top: 10px;
            padding-right: 30px;
            padding-left: 30px'>
        $msg
        </body>
    </html>
HTML;
//---
function createEmail() {
    global $email_from, $email_to, $msg_title, $msg1, $ccme, $cc_to;
    $email = "From: WikiProjectMed<$email_from>\r\n";
    $email .= "To: $email_to\r\n";
    //---
    if ($ccme == 1 && $cc_to != '') {
        $email .= "Cc: $cc_to\r\n";
    }
    //---
    $email .= "Subject: $msg_title\r\n";
    $email .= "MIME-Version: 1.0\r\n";
    $email .= "Content-Type: text/html; charset=utf-8\r\n";
    $email .= "\r\n";
    echo($email);
    $email .= $msg1;
    return $email;
}

$data = createEmail();
$rawmsg = rtrim(strtr(base64_encode($data), '+/', '-_'), '=');

// Create the email
$msg1 = new Google_Service_Gmail_Message();
$msg1->setRaw($rawmsg);

// Send the email
$snd = $service->users_messages->send('me', $msg1);
// check for errors
// if (array_key_exists('error', $snd)) {
$errors = $snd['error'] ?? null;
if ($errors) {
    print "Error: " . $snd['error']['message'] . "\n";
    exit;
} else {
    echo "<p style='color: green;'>Your message send to $email_to successfully...</p>";
    print "Message ID: " . $snd['id'] . "\n";
}
//---
// print_r(json_encode($snd));
