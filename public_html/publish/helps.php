<?php

namespace Publish\Helps;
/*
Usage:
include_once __DIR__ . '/../publish/helps.php';
use function Publish\Helps\get_access_from_db;
use function Publish\Helps\add_access_to_db;
use function Publish\Helps\pub_test_print;
*/

include_once __DIR__ . '/include.php';

use Defuse\Crypto\Crypto;
use function Publish\MdwikiSql\execute_query;
use function Publish\MdwikiSql\fetch_query;


function decode_value($value)
{
    global $cookie_key;
    try {
        $value = Crypto::decrypt($value, $cookie_key);
    } catch (\Exception $e) {
        $value = $value;
    }
    return $value;
}

function encode_value($value)
{
    global $cookie_key;
    try {
        $value = Crypto::encrypt($value, $cookie_key);
    } catch (\Exception $e) {
        $value = $value;
    };
    return $value;
}

function pub_test_print($s)
{
    //---
    if (!isset($_REQUEST['test'])) return;
    //---
    if (gettype($s) == 'string') {
        echo "\n<br>\n$s";
    } else {
        echo "\n<br>\n";
        print_r($s);
    }
}

function get_url_curl(string $url): string
{
    // global $usr_agent;

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // curl_setopt($ch, CURLOPT_COOKIEJAR, "cookie.txt");
    // curl_setopt($ch, CURLOPT_COOKIEFILE, "cookie.txt");

    // curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);

    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $output = curl_exec($ch);
    if ($output === FALSE) {
        pub_test_print("<br>cURL Error: " . curl_error($ch) . "<br>$url");
    }

    curl_close($ch);

    return $output;
}

function add_access_to_db($user, $access_key, $access_secret)
{
    $t = [
        trim($user),
        encode_value($access_key),
        encode_value($access_secret)
    ];
    //---
    $query = <<<SQL
        INSERT INTO access_keys (user_name, access_key, access_secret)
        VALUES (?, ?, ?)
        ON DUPLICATE KEY UPDATE
            access_key = VALUES(access_key),
            access_secret = VALUES(access_secret);
    SQL;
    //---
    execute_query($query, $t);
};

function get_access_from_db($user)
{
    // تأكد من تنسيق اسم المستخدم
    $user = trim($user);

    // SQL للاستعلام عن access_key و access_secret بناءً على اسم المستخدم
    $query = <<<SQL
        SELECT access_key, access_secret
        FROM access_keys
        WHERE user_name = ?;
    SQL;

    // تنفيذ الاستعلام وتمرير اسم المستخدم كمعامل
    $result = fetch_query($query, [$user]);

    // التحقق مما إذا كان قد تم العثور على نتائج
    if ($result) {
        $result = $result[0];
        return [
            'access_key' => decode_value($result['access_key']),
            'access_secret' => decode_value($result['access_secret'])
        ];
    } else {
        // إذا لم يتم العثور على نتيجة، إرجاع null أو يمكنك تخصيص رد معين
        return null;
    }
}
