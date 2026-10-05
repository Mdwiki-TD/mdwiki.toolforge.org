<?php

namespace FixWikiRefs\Fix;

use function FixWikiRefs\WikiText\get_wikipedia_text;

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
    if (function_exists('\WpRefs\FixPage\fix_page_with_setting')) {
        $newtext = \WpRefs\FixPage\fix_page_with_setting(
            $sourcetitle,
            $title,
            $text,
            $lang,
            $mdwiki_revid,
            null,
            null,
            null,
        );
    }
    //---
    $newtext = trim($newtext);
    //---
    if ($newtext == $text) {
        return ["no changes", ""];
    }
    //---
    return ["", $newtext];
}
