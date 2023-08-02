<?PHP
include_once('tables.php');
include_once('functions.php');
$mainlang = $_REQUEST['lang'] ?? '';

function createNumbersTable() {
    global $numbers, $mainlang;
    $Numbers_table = <<<HTML
    <table class="sortable table table-striped table-sm">
    <thead>
        <tr>
            <th class="spannowrap">Type</th>
            <th>Number</th>
        </tr>
    </thead>
    <tbody>
    HTML;
    foreach ( $numbers as $key => $value ) {
        //---
        // skip keys 
        $skip_keys = ['Articles', 'Languages'];
        if (in_array($key, $skip_keys) && $mainlang !== '') {
            continue;
        }

        // if (in_array($key, $skip_keys) && $mainlang !== '') {
        //---
        // if type is array then count
        if (is_array($value)) {
            $value = count($value);
        }
        $value = number_format($value);
        $Numbers_table .= <<<HTML
        <tr>
            <td><b>$key</b></td>
            <td>$value</td>
        </tr>
    HTML;
    };

    $Numbers_table .= <<<HTML
    </tbody>
    </table>
    HTML;
    
    return $Numbers_table;
};
function makeUsersTable() {
    
    global $sql_users_tab, $Users_word_table, $Views_by_users;
    //---
    global $top_translators, $translators_views, $translators_words, $mainlang;
    
    $text = <<<HTML
    <table class="sortable table table-striped soro2 table-sm">
        <thead>
            <tr>
                <th class="spannowrap">#</th>
                <th class="spannowrap">User</th>
                <th>Number</th>
                <th>Words</th>
                <th>Views</th>
            </tr>
        </thead>
        <tbody>
    HTML;
    
    arsort($top_translators);
    
    $numb = 0;
    
    foreach ( $top_translators as $user => $usercount ) {
            
        $numb += 1;
            
        $views = isset($translators_views[$user]) ? number_format($translators_views[$user]) : 0;
        $words = isset($translators_words[$user]) ? number_format($translators_words[$user]) : 0;
        
        $use = rawurlEncode($user);
        $use = str_replace ( '+' , '_' , $use );
        $talk_url = "//$mainlang.wikipedia.org/w/index.php?title=User_talk:$user&action=edit&section=new";

        $text .= <<<HTML
        <tr>
            <td>$numb</td>
            <td><a target='_blank' href='$talk_url'>$user</a></td>
            <td>$usercount</td>
            <td>$words</td>
            <td>$views</td>
        </tr>
        HTML;
    };
    
    $text .= <<<HTML
        </tbody>
        <tfoot></tfoot>
    </table>
    HTML;
    
    return $text;
}
function makeLangTable() {
    
    global $lang_code_to_en, $code_to_lang, $sql_Languages_tab, $all_views_by_lang;
    //---
    global $translates_by_lang;
    
    arsort($translates_by_lang);
    $text = <<<HTML
    <table class='sortable table table-striped table-sm'>
    <thead>
        <tr>
            <th>#</th>
            <th class='spannowrap'>Language</th>
            <th>Count</th>
            <th>Words</th>
            <th>Views</th>
        </tr>
    </thead>
    <tbody>
    HTML;
    
    $numb=0;
    
    foreach ( $translates_by_lang as $langcode => $table ) {
        
        # Get the Articles numbers
        $comp  = count($table['titles']);
        $words = number_format($table['words']);
        $views = number_format($table['views']);
        //---
        if ( $comp > 0 ) {
            
            $numb ++;
            
            $text .= <<<HTML
                <tr>
                    <td>$numb</td>
                    <td><a href='index.php?lang=$langcode'>$langcode</a></td>
                    <td>$comp</td>
                    <td>$words</td>
                    <td>$views</td>
                </tr>
            HTML;
            
        };
    };
    
    $text .= <<<HTML
        </tbody>
        </table>
    HTML;
    
    return $text;
}