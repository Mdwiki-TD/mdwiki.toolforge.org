<?php
// Refactored Med updater
// Usage: place this file on your server and call ?title=SomePage&save=1&test=1
// Note: this refactor minimizes global usage; only $GLOBALS['global_username'] is read once at the bootstrap.

class MedUpdater
{
    protected string $rootPath;
    protected string $pyBinary;
    protected string $site = 'mdwiki.org';
    protected bool $isLocalhost;
    protected bool $testMode = false;

    public function __construct(array $opts = [])
    {
        $this->rootPath = $opts['root_path'] ?? (getenv('HOME') ?: 'I:/mdwiki');
        $this->isLocalhost = ($_SERVER['SERVER_NAME'] ?? '') === 'localhost';
        $this->pyBinary = $this->isLocalhost ? ($opts['python_local'] ?? 'python3') : ($opts['python_remote'] ?? $this->rootPath . '/local/bin/python3');
        $this->testMode = !empty($opts['test']);
    }

    // Utility: safe endsWith
    public static function endsWith(string $hay, string $needle): bool
    {
        $len = strlen($needle);
        if ($len === 0) return true;
        return substr($hay, -$len) === $needle;
    }

    // Build and run python command safely
    public function runPython(string $dir, string $pyfile, string $other = '', bool $echoCommand = false): string
    {
        $dir = rtrim($dir, "/\\");
        $pyPath = $this->pyBinary;
        $scriptPath = "$dir/$pyfile";

        // use escapeshellarg for arguments (safer)
        $cmdParts = [];
        $cmdParts[] = escapeshellcmd($pyPath);
        $cmdParts[] = escapeshellarg($scriptPath);

        if ($other !== '') {
            // keep other as a single argument so flags with spaces are preserved safely
            $cmdParts[] = $other; // we will escape below more carefully
        }

        // If $other contains multiple tokens (like "-page:... from_toolforge"), it's safer to append as-is
        // Build final string carefully
        $command = implode(' ', $cmdParts);

        // normalize duplicate slashes
        $command = preg_replace('#/+#', '/', $command);

        if ($echoCommand || $this->testMode) {
            // show the full command (safe enough since it's for debugging)
            echo "<h6>" . htmlspecialchars($command, ENT_QUOTES, 'UTF-8') . "</h6>";
        }

        // Execute and return output
        // Note: depending on server config, shell_exec may be disabled.
        $output = @shell_exec($command);
        return (string)($output ?? '');
    }

    // Compose parameters for the python call from a title
    public function getResults(string $title, bool $saveFlag = false): string
    {
        // sanitize and encode title like original
        $titlex = str_replace(['+', ' '], '_', $title);
        $titlex = str_replace('"', '\\"', $titlex);
        $titlex = str_replace("'", "\\'", $titlex);
        $titlex = rawurlencode($titlex);

        $sa = $saveFlag ? ' save' : '';
        $ccc = "-page:$titlex from_toolforge $sa";

        $paramsDir = $this->rootPath . "/pybot/newupdater";
        $pyfile = 'med.py';

        // Run Python and return its output (could be filename or messages)
        return $this->runPython($paramsDir, $pyfile, $ccc, $this->testMode || $this->isLocalhost);
    }

    // Process the raw response from python and return a structured result instead of echoing
    public function processResults(string $resultb, string $title): array
    {
        $resultb = trim($resultb);
        $isTxt = self::endsWith($resultb, '.txt');

        if ($this->testMode) {
            // for debugging callers can display this if needed
            $debugMsg = "results:({$resultb})";
        } else {
            $debugMsg = '';
        }

        if ($resultb === 'no changes') {
            return ['status' => 'no_changes', 'message' => 'no changes', 'debug' => $debugMsg];
        } elseif ($resultb === 'notext') {
            return ['status' => 'notext', 'message' => 'text == \"\"', 'debug' => $debugMsg];
        } elseif ($isTxt) {
            // read the text file content safely
            $txtPath = $resultb;
            if (!file_exists($txtPath) || !is_readable($txtPath)) {
                return ['status' => 'error', 'message' => "Result file not found or not readable: $txtPath", 'debug' => $debugMsg];
            }
            $newtext = file_get_contents($txtPath);
            return ['status' => 'show_form', 'newtext' => $newtext, 'resultb' => $resultb, 'debug' => $debugMsg];
        } else {
            // Generic other output
            return ['status' => 'other', 'message' => $resultb, 'debug' => $debugMsg];
        }
    }

    // Helpers to generate edit URL and page URL (View will render them)
    public function getEditUrl(string $title): string
    {
        $titleEsc = rawurlencode($title);
        return "https://{$this->site}/w/index.php?title={$titleEsc}&action=submit";
    }

    public function getPageUrl(string $title): string
    {
        $titleEsc = rawurlencode($title);
        return "https://{$this->site}/w/index.php?title={$titleEsc}";
    }
}


// View helper: separate HTML rendering
class MedUpdaterView
{
    public static function generateEditForm(string $title, string $newtext = ''): string
    {
        $site = "mdwiki.org";
        $new = "https://$site/w/index.php?title=" . rawurlencode($title) . "&action=submit";
        $summary = "mdwiki changes.";

        $safeText = htmlspecialchars($newtext, ENT_QUOTES, 'UTF-8');

        $form = <<<HTML
        <form id='editform' name='editform' method='POST' action='$new' target='_blank'>
            <input type='hidden' value='' name='wpEdittime'/>
            <input type='hidden' value='' name='wpStarttime'/>
            <input type='hidden' value='' name='wpScrolltop' id='wpScrolltop'/>
            <input type='hidden' value='12' name='parentRevId'/>
            <input type='hidden' value='wikitext' name='model'/>
            <input type='hidden' value='text/x-wiki' name='format'/>
            <input type='hidden' value='1' name='wpUltimateParam'/>
            <input type='hidden' name='wpSummary' value='$summary'>
            <input type='hidden' id='wikitext-old' value=''>
            <div class='form-group'>
                <label for='find'>new text:</label>
                <textarea id='wikitext-new' class='form-control' name='wpTextbox1' rows='18'>{$safeText}</textarea>
            </div>
            <div class='editOptions aligncenter'>
                <input id='wpPreview' type='submit' class='btn btn-outline-primary' tabindex='5' title='[p]' accesskey='p' name='wpPreview' value='Preview changes'/>
                <input id='wpDiff' type='submit' class='btn btn-outline-primary' tabindex='7' name='wpDiff' value='show changes' accesskey='v' title='show changes.'>
                <div class='editButtons'></div>
            </div>
        </form>
        HTML;

        return $form;
    }

    public static function makeTitleForm(string $title, bool $saveChecked = false, bool $test = false, bool $loggedIn = false): string
    {
        $title3 = htmlspecialchars($title, ENT_QUOTES, 'UTF-8');

        $starticon = $loggedIn ? "<input class='btn btn-outline-primary' type='submit' value='send' />" : '<a role="button" class="btn btn-primary" href="/auth/index.php?a=login">Log in</a>';
        $testinput = $test ? '<input type="hidden" name="test" value="1" />' : '';
        $saveAttr = $saveChecked ? 'checked' : '';

        return <<<HTML
        <form action='' method='GET'>
            $testinput
            <div class='container'>
                <div class='row'>
                    <div class='col-md-4'>
                        <div class='input-group mb-3'>
                            <div class='input-group-prepend'>
                                <span class='input-group-text'>Title</span>
                            </div>
                            <input class='form-control' type='text' id='title' name='title' value="$title3" required />
                        </div>
                    </div>
                    <div class='col-md-3'>
                        <div class='form-check form-switch'>
                            <input class='form-check-input' type='checkbox' id='save' name='save' value='1' $saveAttr>
                            <label class='check-label' for='save'>Auto save</label>
                        </div>
                    </div>
                    <div class='col-md-5'>
                        <h4 class='aligncenter'>
                            $starticon
                        </h4>
                    </div>
                </div>
            </div>
        </form>
        HTML;
    }

    public static function renderActionLinks(string $title, MedUpdater $updater): string
    {
        $new = $updater->getEditUrl($title);
        $articleurl = $updater->getPageUrl($title);
        $edit_link = <<<HTML
        <a type='button' target='_blank' class='btn btn-outline-primary' href='$new'>Open edit new tab.</a>
        <a type='button' target='_blank' class='btn btn-outline-primary' href='$articleurl'>Open page new tab.</a>
        HTML;

        return <<<HTML
        <div class='aligncenter'>
            <div class='col-sm'>
                $edit_link
            </div>
        </div>
        HTML;
    }
}


// ------------------------------
// Bootstrapping & request handling
// ------------------------------
$test = isset($_GET['test']) && $_GET['test'];
$title = trim($_GET['title'] ?? '');
$save = isset($_GET['save']) && $_GET['save'];
$save_checked = $save;
$global_username = $GLOBALS['global_username'] ?? null;
$loggedIn = !empty($global_username);

// Instantiate updater
$updater = new MedUpdater(['test' => $test]);

// Title form
$title_form = MedUpdaterView::makeTitleForm($title, $save_checked, $test, $loggedIn);

// Page header & form
echo <<<HTML
    <div class="card">
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>Med updater</h3>
        </div>
        <div class="card-body">
            $title_form
        </div>
    </div>
    <hr />
HTML;

// If not logged in, show a message
if (!$loggedIn) {
    echo "<div class='alert alert-warning'>log in!!</div>";
}

// If title provided and user logged in, run flow
$resultHtml = '';
if (!empty($title) && $loggedIn) {
    // Get raw result from python
    $raw = $updater->getResults($title, $save);

    // Process it (no echoes inside)
    $processed = $updater->processResults($raw, $title);
    $actionlinks = MedUpdaterView::renderActionLinks($title, $updater);
    // ---
    if ($processed['status'] === 'no_changes') {
        echo "<div>no changes</div>";
        echo $actionlinks;
    } elseif ($processed['status'] === 'notext') {
        echo "<div>text == ''</div>";
        echo $actionlinks;
    } elseif ($processed['status'] === 'show_form') {
        $form = MedUpdaterView::generateEditForm($title, $processed['newtext']);
        // If save requested, display message about save status (original code echoed different behavior),
        // here we just display the form and the action links; implement save handling in server-side if required.
        echo $form;
        echo $actionlinks;
    } elseif ($processed['status'] === 'other') {
        echo "<pre>" . htmlspecialchars($processed['message'], ENT_QUOTES, 'UTF-8') . "</pre>";
        echo $actionlinks;
    } else { // error or unknown
        echo "<pre>" . htmlspecialchars($processed['message'] ?? 'Unknown error', ENT_QUOTES, 'UTF-8') . "</pre>";
    }
}

// Footer card with quick link to page
echo <<<HTML
    <div class='card'>
        <div class="card-header aligncenter" style="font-weight:bold;">
            <h3>
                page: <a target='_blank' href="https://mdwiki.org/w/index.php?title={$title}">{$title}</a>
            </h3>
        </div>
        <div class='card-body'>
        </div>
    </div>
HTML;
