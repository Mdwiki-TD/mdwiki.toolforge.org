<?php

namespace FixWikiRefs\Fix;

use function WpRefs\FixPage\fix_page_with_setting;
use function FixWikiRefs\WikiText\get_wikipedia_text;

/*
usage:

use function FixWikiRefs\Fix\get_results_new;

*/

function get_results_new($sourcetitle, $title, $lang, $mdwiki_revid, $text = "")
{
    //---
    $err = "";
    //---
    if (empty($text)) {
        [$err, $text] = get_wikipedia_text($title, $lang);
    }
    //---
    if (!empty($err)) {
        return [$err, $text];
    }
    //---
    $newtext = fix_page_with_setting(
        $sourcetitle,
        $title,
        $text,
        $lang,
        $mdwiki_revid,
        null,
        null,
        null,
    );
    //---
    $newtext = trim($newtext);
    //---
    if ($newtext == $text) {
        return ["no changes", ""];
    }
    //---
    return ["", $newtext];
}
