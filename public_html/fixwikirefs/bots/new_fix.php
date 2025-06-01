<?php

use function WpRefs\FixPage\DoChangesToText1;
// $text = DoChangesToText1($sourcetitle, $title, $text, $lang, $mdwiki_revid)

function get_results_new($sourcetitle, $title, $lang, $text = "")
{
    //---
    if (empty($text)) {
        $text = get_wikipedia_text($title, $lang);
    }
    //---
    $newtext = DoChangesToText1($sourcetitle, $title, $text, $lang, 0);
    //---
    return $newtext;
}
