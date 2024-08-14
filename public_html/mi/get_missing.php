<?php

namespace MI\GetMissing;

use function Actions\Functions\test_print;
use function Actions\MdwikiApi\get_mdwiki_url_with_params;
use function Actions\WikiApi\get_url_result_curl;
use function Translate\EnAPI\do_edit;

class Missing
{
    private $code;
    private $cat;
    public function __construct($code, $cat)
    {
        $this->code = $code;
        $this->cat = $cat;
    }

    private function getTextFromMdWiki()
    {
        $first = '';
        $params2 = array(
            "action" => "parse",
            "format" => "json",
            "page" => $this->title,
            "prop" => "wikitext"
        );
        $json2 = get_mdwiki_url_with_params($params2);

        $allText = $json2["parse"]["wikitext"]["*"] ?? '';

        if ($this->wholeArticle) {
            $first = $allText;
        } else {
            $params = array(
                "action" => "parse",
                "format" => "json",
                "page" => $this->title,
                "section" => "0",
                "prop" => "wikitext"
            );
            $json1 = get_mdwiki_url_with_params($params);
            $first = $json1["parse"]["wikitext"]["*"] ?? '';
            // ---
            if ($first != '') {
                $first .= "\n==References==\n<references />";
            }
        }

        $text = $first;

        return array("text" => $text, "allText" => $allText);
    }

    public function parseText()
    {
        $txt = $this->getTextFromMdWiki();
        $text = $txt["text"] ?? "";
        $allText = $txt["allText"] ?? "";

        if ($text === '') {
            echo ('no text');
            return "notext";
        }

        return $newText;
    }

    private function PostToEnwiki($newText)
    {
        if ($newText === '') {
            echo ('no text');
            return "notext";
        }
        $suus = 'from https://mdwiki.org/wiki/' . str_replace(' ', '_', $this->title);
        $title2 = 'User:Mr. Ibrahem/' . $this->title;

        if ($this->wholeArticle) {
            $title2 = 'User:Mr. Ibrahem/' . $this->title . '/full';
        }

        $result = do_edit($title2, $newText, $suus);
        $success = $result['edit']['result'] ?? '';

        if ($success == 'Success') {
            return true;
        }

        return $success;
    }
    public function result()
    {
        /*
        1. get text from mdwiki.org
        2. fix ref
        3. fix text
        4. put to enwiki
        5. return result
        */

        $tab = array(
            "missing" => [],
            "exists" => [],
        );

        return $tab;
    }
}

function get_miss($code, $cat)
{

    $bot = new Missing($code, $cat);

    $result = $bot->result();

    return $result;
}
