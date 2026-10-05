<?php

namespace FixWikiRefs\SavePage;

use RefsOAuth\MdwikiSql\Database;
use function RefsOAuth\SendEdit\auth_make_edit;

use Defuse\Crypto\Crypto;
use Defuse\Crypto\Key;

function decode_value($value)
{
    if (empty(trim($value))) return "";
    $decryptKeyString = getenv('DECRYPT_KEY') ?: $_ENV['DECRYPT_KEY'] ?? '';
    $use_key = $decryptKeyString ? Key::loadFromAsciiSafeString($decryptKeyString) : null;

    if ($use_key === null) return "";

    try {
        return Crypto::decrypt($value, $use_key);
    } catch (\Exception $e) {
        return "";
    }
}

function get_access_from_db($user)
{
    $user = trim($user);

    $query = <<<SQL
        SELECT access_key, access_secret
        FROM access_keys
        WHERE user_name = ?;
    SQL;

    // Create a new database object
    $db = new Database();

    // Execute a SQL query
    $result = $db->fetchquery($query, [$user]);


    if (!$result) {
        return null;
    }

    $result = $result[0];

    return [
        'access_key' => decode_value($result['access_key']),
        'access_secret' => decode_value($result['access_secret'])
    ];
}

function saveit($title, $lang, $text, $user_name)
{
    if ($user_name == '') {
        return false;
    }
    // ---
    $summary = "Fix references, Expand infobox #mdwiki .toolforge.org.";
    // ---
    $access = get_access_from_db($user_name);
    // ---
    if ($access == null) {
        return false;
    };
    // ---
    $access_key = $access['access_key'];
    $access_secret = $access['access_secret'];
    // ---
    $result = auth_make_edit($title, $text, $summary, $lang, $access_key, $access_secret);
    // ---
    return $result;
}
