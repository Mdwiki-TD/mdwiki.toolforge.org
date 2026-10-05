<?php

namespace App\Controllers;

use function FixWikiRefs\SavePage\saveit;
use function FixWikiRefs\Fix\get_results_new;

class FixRefsController
{
    private string $user_name;

    public function __construct()
    {
        $this->user_name = (isset($GLOBALS['global_username']) && $GLOBALS['global_username'] != '')
            ? $GLOBALS['global_username']
            : '';
    }
    public function handleRequest(array $getRequest): void
    {
        $title        = $getRequest['title'] ?? '';
        $save         = isset($getRequest['save']) ? 'save' : '';
        $movedots     = isset($getRequest['movedots']) ? 'checked' : '';
        $infobox      = isset($getRequest['infobox']) ? 'checked' : '';
        $lang         = isset($getRequest['lang']) ? trim($getRequest['lang']) : '';
        $sourcetitle  = isset($getRequest['sourcetitle']) ? trim($getRequest['sourcetitle']) : (isset($getRequest['source_title']) ? trim($getRequest['source_title']) : '');
        $mdwiki_revid = $getRequest['revid'] ?? $getRequest['mdwiki_revid'] ?? '';
        $text         = $getRequest['text'] ?? $_POST['text'] ?? '';

        echo <<<HTML
            <div class="card">
                <div class="card-header aligncenter" style="font-weight:bold;">
                    <h3>Fix references in Wikipedia's: <a href='https://hashtags.wmcloud.org/?query=mdwiki' target='_blank'>#mdwiki</a></h3>
                </div>
                <!-- padding bottom 0 -->
                <div class="card-body pb-0">
        HTML;

        $shouldShowResult = (!empty($title) && !empty($lang) && !empty($this->user_name));

        echo $this->printForm(
            $title,
            $lang,
            $save,
            $movedots,
            $infobox,
            $sourcetitle,
            $mdwiki_revid,
            $text,
            $shouldShowResult
        );

        echo "<!-- x --></div></div><!-- x -->";

        if ($shouldShowResult && $lang !== 'en') {
            $new_tt = $this->workNew($title, $lang, $save, $sourcetitle, $mdwiki_revid, $movedots, $infobox);
            echo <<<HTML
                    <!-- <hr /> -->
                    <div class='card mt-3'>
                        <div class="card-header aligncenter" style="font-weight:bold;">
                            <h3>
                                <i class="bi bi-file-earmark-text"></i>
                                <a target='_blank' href="https://{$lang}.wikipedia.org/w/index.php?title={$title}">{$title}</a>
                            </h3>
                        </div>
                        <div class='card-body'>
                            {$new_tt}
                        </div>
                    </div>
            HTML;
        }

        echo "</div></div>";
    }

    private function printForm(
        string $title,
        string $lang,
        string $save,
        string $movedots,
        string $infobox,
        string $sourcetitle = '',
        string $mdwiki_revid = '',
        string $text = '',
        bool $shouldShowResult = false
    ): string {
        // Escape all inputs
        $title        = htmlspecialchars($title, ENT_QUOTES, 'UTF-8');
        $lang         = htmlspecialchars($lang, ENT_QUOTES, 'UTF-8');
        $sourcetitle  = htmlspecialchars($sourcetitle, ENT_QUOTES, 'UTF-8');
        $mdwiki_revid = htmlspecialchars($mdwiki_revid, ENT_QUOTES, 'UTF-8');
        $text         = htmlspecialchars($text, ENT_QUOTES, 'UTF-8');

        $save_checked = ($save !== '') ? 'checked' : '';

        $start_icon = "<input class='btn btn-outline-primary' type='submit' value='start'>";
        if ($this->user_name === '') {
            $start_icon = '<a role="button" class="btn btn-primary" href="/auth/login.php">Log in</a>';
        }

        $text_part = <<<HTML
            <div class="mb-3">
                <label for="text" class="form-label">Text Content</label>
                <textarea class="form-control" id="text" name="text" rows="5">$text</textarea>
            </div>
            HTML;

        if (!$text && $shouldShowResult) $text_part = '';

        return <<<HTML
            <form action='/fixwikirefs.php' method='GET'>
                <div class='container'>
                    <div class='row'>
                        <div class='col-md-4'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Langcode</span>
                                </div>
                                <input class='form-control' type='text' id='lang' name='lang' value='{$lang}' placeholder="e.g., en, ar" required />
                            </div>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>Wikipedia title</span>
                                </div>
                                <input class='form-control' type='text' id='title' name='title' value='{$title}' required />
                            </div>
                        </div>
                        <div class='col-md-4'>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>MDWiki Source Title</span>
                                </div>
                                <input class='form-control' type='text' id='sourcetitle' name='sourcetitle' value='{$sourcetitle}' />
                            </div>
                            <div class='input-group mb-3'>
                                <div class='input-group-prepend'>
                                    <span class='input-group-text'>MDWiki Revision ID</span>
                                </div>
                                <input class='form-control' type='text' id='revid' name='revid' value='{$mdwiki_revid}' />
                            </div>
                        </div>
                        <div class='col-md-3'>
                            <div class='form-check form-switch'>
                                <input class='form-check-input' type='checkbox' id='save' name='save' value='1' {$save_checked}>
                                <label class='check-label' for='save'>Auto save</label>
                            </div>

                            <div class='form-check form-switch'>
                                <input class='form-check-input' type='checkbox' id='movedots' name='movedots' value='1' {$movedots}>
                                <label class='form-check-label' for='movedots'>Move dots after references</label>
                            </div>

                            <div class='form-check form-switch'>
                                <input class='form-check-input' type='checkbox' id='infobox' name='infobox' value='1' {$infobox}>
                                <label class='form-check-label' for='infobox'>Expand Infobox</label>
                            </div>
                        </div>
                        <div class='col-md-1'>
                            <h4 class='aligncenter'>
                                {$start_icon}
                            </h4>
                        </div>
                    </div>
                    {$text_part}
                </div>
            </form>
        HTML;
    }

    private function makeResultForm(string $new, string $newtext): string
    {
        $summary = "Fix references, Expand infobox #mdwiki .toolforge.org.";

        return <<<HTML
            <form id='editform' name='editform' method='POST' action='{$new}' target='_blank'>
                <input type='hidden' value='' name='wpEdittime'/>
                <input type='hidden' value='' name='wpStarttime'/>
                <input type='hidden' value='' name='wpScrolltop' id='wpScrolltop'/>
                <input type='hidden' value='12' name='parentRevId'/>
                <input type='hidden' value='wikitext' name='model'/>
                <input type='hidden' value='text/x-wiki' name='format'/>
                <input type='hidden' value='1' name='wpUltimateParam'/>
                <input type='hidden' name='wpSummary' value='{$summary}'>
                <input type='hidden' id='wikitext-old' value=''>
                <div class="mb-3">
                    <label for="wikitext-new" class="form-label fw-semibold">
                        New Wikitext
                    </label>
                    <textarea id="wikitext-new" class="form-control" name="wpTextbox1" rows="5">{$newtext}</textarea>
                </div>
                <div class='editOptions aligncenter'>
                    <input id='wpPreview' type='submit' class='btn btn-outline-primary' tabindex='5' title='[p]' accesskey='p' name='wpPreview' value='Preview changes'/>
                    <input id='wpDiff' type='submit' class='btn btn-outline-primary' tabindex='7' name='wpDiff' value='show changes' accesskey='v' title='show changes.'>
                    <div class='editButtons'>
                    </div>
                </div>
            </form>
        HTML;
    }

    private function workNew(
        string $title,
        string $lang,
        string $save,
        string $sourcetitle,
        string $mdwiki_revid,
        string $movedots,
        string $infobox
    ): string {
        $site = "{$lang}.wikipedia.org";

        $new = "https://{$site}/w/index.php?title={$title}&action=submit";
        $articleurl = "https://{$site}/w/index.php?title={$title}";

        $text_re = "";

        [$err, $resultb] = get_results_new($sourcetitle, $title, $lang, $mdwiki_revid);

        $edt_link_row = <<<HTML
            <div class='aligncenter'>
                <div class='col-sm'>
                    <a type='button' target='_blank' class='btn btn-outline-primary' href='{$new}'>Open edit new tab.</a>
                    <a type='button' target='_blank' class='btn btn-outline-primary' href='{$articleurl}'>Open page new tab.</a>
                </div>
            </div>
        HTML;

        if (!empty($err)) {
            $text_re .= $this->published_alert($err, "warning");
            $text_re .= $edt_link_row;
            return $text_re;
        }

        if ($resultb === "redirect") {
            $text_re .= $this->published_alert("Page is redirect", "warning");
            $text_re .= $edt_link_row;
            return $text_re;
        }

        if ($resultb === 'no changes') {
            $text_re .= $this->published_alert("No changes", "warning");
            $text_re .= $edt_link_row;
            return $text_re;
        }

        if ($resultb === "notext") {
            $text_re .= $this->published_alert("No text", "warning");
            $text_re .= $edt_link_row;
            return $text_re;
        }

        $newtext = $resultb;

        if (!empty($save)) {
            return $this->make_save_result($title, $lang, $newtext, $new);
        }

        $text_re .= $this->makeResultForm($new, $newtext);

        return $text_re;
    }

    private function make_save_result($title, $lang, $newtext, $new)
    {
        // ---
        $result = "";
        // ---
        $save2 = saveit($title, $lang, $newtext, $this->user_name);
        // ---
        $error_code = ($save2['error']['code'] ?? '') ?? '';
        $error_info = ($save2['error']['info'] ?? '') ?? '';
        // ---
        // if (isset($_GET['test'])) { var_export(json_encode($save2, JSON_PRETTY_PRINT)); }
        // ---
        $Success = isset($save2['edit']['result']) && $save2['edit']['result'] == 'Success';
        // ---
        if ($Success) {
            // '{ "edit": { "result": "Success", "pageid": 7613329, "title": "Anemia na gravidez", "contentmodel": "wikitext", "oldrevid": 70215097, "newrevid": 70257752, "newtimestamp": "2025-06-08T00:30:18Z" } }'
            // ---
            $newrevid = $save2['edit']['newrevid'] ?? '0';
            // ---
            $result .= $this->published_success_alert($lang, $newrevid, $title);
        } else {
            // ---
            $aleart = $this->published_alert("Changes are not published, try to do it manually. Error: $error_code ($error_info)", "danger");
            // ---
            $result .= $aleart;
            $result .= $this->makeResultForm($new, $newtext);
        }
        // ---
        return $result;
    }
    private function published_success_alert($lang, $newrevid, $title)
    {
        return <<<HTML
            <div class="container-fluid">
                <div class="row justify-content-center">
                    <div class="col-md-9 col-12">
                        <div class="alert alert-success d-flex align-items-center" role="alert">
                            <i class="bi bi-check-circle-fill me-2"></i> Changes have been published.
                            <div class="ms-auto d-flex gap-2">
                                <a href="https://$lang.wikipedia.org/w/index.php?title=Special:Diff/$newrevid" target="_blank" class="btn btn-outline-primary btn-sm">
                                    <i class="bi bi-file-earmark-text me-1"></i> Diff
                                </a>
                                <a href="https://$lang.wikipedia.org/w/index.php?title=$title&action=history" target="_blank" class="btn btn-outline-primary btn-sm">
                                    <i class="bi bi-clock-history me-1"></i> History
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        HTML;
    }

    private function published_alert($text, $type)
    {
        return <<<HTML
            <div class="container-fluid">
                <div class="row justify-content-center">
                    <div class="col-md-9 col-12">
                        <div class="alert alert-$type d-flex align-items-center" role="alert">
                            $text
                        </div>
                    </div>
                </div>
            </div>
        HTML;
    }
}
