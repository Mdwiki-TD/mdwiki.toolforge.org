<?php

namespace FixWikiRefs\Fix;

use function WpRefs\FixPage\DoChangesToText1;
use function FixWikiRefs\WikiText\get_wikipedia_text;

/*
usage:

use function FixWikiRefs\Fix\get_results_new;

*/

function get_results_new($sourcetitle, $title, $lang, $text = "")
{
    //---
    if (empty($text)) {
        $text = get_wikipedia_text($title, $lang);
    }
    //---
    if (empty($text)) {
        return "notext";
    }
    //---
    if ($text == "redirect") {
        return "redirect";
    }
    //---
    $newtext = DoChangesToText1($sourcetitle, $title, $text, $lang, 0);
    //---
    $newtext = trim($newtext);
    //---
    if ($newtext == $text) {
        return "no changes";
    }
    //---
    return $newtext;
}
