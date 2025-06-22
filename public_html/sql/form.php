<?php
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}
// ---
// include_once __DIR__ . '/td_api.php';
// include_once __DIR__ . '/sql_result.php';

$queries = [
    "RTT_cats" => "SELECT title, cat, category
        FROM pages, articles_cats
        WHERE cat = 'RTT' and article_id = title
        and category != 'RTT' and category != '' and category is not null

        # update pages JOIN articles_cats set cat = category where cat = 'RTT' and article_id = title and category != '' and category is not null and category != 'RTT'
        ",
    "articles_cats" => "SELECT title, cat, category
        FROM pages, articles_cats
        WHERE (cat = '' OR cat IS NULL) and article_id = title
        and category != '' and category is not null

        # update pages JOIN articles_cats set cat = category where (cat = '' OR cat IS NULL) and article_id = title and category != '' and category is not null
        ",
    "video" => "SELECT *
        FROM pages WHERE title LIKE '%Video:%' AND cat != 'Videowiki scripts'
        # update pages set cat = 'Videowiki scripts' where title LIKE '%Video:%'
    ",
    "users" => "#INSERT INTO users (username)
        SELECT
        distinct user from pages where user not in (select username from users)
    ",
    "update_words" => "UPDATE
        pages p
        JOIN words w ON w.w_title = p.title
        SET p.word = CASE
                        WHEN p.translate_type = 'all' THEN w.w_all_words
                        ELSE w.w_lead_words
                    END
        WHERE p.word = 0 OR p.word IS NULL
        ",
    "qu1" => "SELECT
        A.id as id1, A.target as t1,
        B.id as id2, B.target as t2
        FROM views A, views B
        WHERE A.target = B.target
        and A.lang = B.lang
        and A.id != B.id
        ",
    "qu2" => "SELECT * from pages p1
        where (p1.target = '' OR p1.target IS NULL) and EXISTS  (SELECT 1 FROM pages p2 WHERE p1.title = p2.title and p2.target != ''
        and p1.lang = p2.lang
        )",
    "qu3" => "SELECT A.lang as lang,A.title as title,
        A.id AS id1, A.user AS u1, A.target as T1, A.date as d1,
        B.id AS id2, B.user AS u2, B.target as T2, B.date as d2
        FROM pages A, pages B
        WHERE A.id <> B.id
        AND A.title = B.title
        AND A.lang = B.lang
        and A.target != ''
        ORDER BY A.title",
    "qu4" => "SELECT
        A.id as id1, A.title as t1, A.qid as q1,
        B.id as id2, B.title as t2, B.qid as q2
        FROM qids A, qids B
        WHERE A.title = B.title
        and A.id != B.id
        ",
    "qu5" => "SELECT
        A.id as id1, A.title as t1, A.qid as q1,
        B.id as id2, B.title as t2, B.qid as q2
        FROM qids A, qids B
        WHERE A.qid = B.qid
        and A.title != B.title
        and A.id != B.id
        and B.qid != ''
        ",
    "qu6" => "SELECT * from pages where (target = '' OR target IS NULL) and date < ADDDATE(CURDATE(), INTERVAL -7 DAY)",
    "qu7" => "SELECT
        A.id as id1, A.title as t1, A.qid as q1,
        B.id as id2, B.title as t2, B.qid as q2
        FROM qids A, qids_others B
        WHERE A.title = B.title
        and A.qid = B.qid
        ",
    "in_process" => "SELECT id from pages p1 where (p1.target = '' OR p1.target IS NULL) and EXISTS (SELECT 1 FROM in_process p2 WHERE p1.lang = p2.lang and p1.lang = p2.lang and p1.title = p2.title and p1.user = p2.user )
# DELETE from pages
",
];

function make_form($pass, $code)
{
    global $queries;
    // ---
    $qua = (!empty($code)) ? $code : "SELECT A.id from pages A, pages B where (A.target = '' OR A.target IS NULL) and A.lang = B.lang and A.title = B.title and B.target != ''";
    // ---
    $form = "<div class='container-fluid'>";
    // ---
    $form .= <<<HTML
        <div class='row'>
            <div class='col-md'>
                <ul>
                    <li><a href='#' onclick="to_code('show tables')">show tables</a></li>
                    <li>
                        Describe:
                        <ul>
                            <li><a href='#' onclick="to_code('describe words')">words</a></li>
                            <li><a href='#' onclick="to_code('describe pages')">pages</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div class='col-md'>
                select * from :
                <ul>
                    <li><a href='#' onclick="to_code('select * from words')">words</a></li>
                    <li><a href='#' onclick="to_code('select * from pages')">pages</a></li>
                    <li><a href='#' onclick="to_code('select * from qids')">qids</a></li>
                </ul>
            </div>
            <div class='col-md'>
                Duplicate:
                <ul>
                    <li><a href='#' onclick="copy_qua('qu7')">Qids Qids_others</a></li>
                    <li><a href='#' onclick="copy_qua('qu4')">qids</a></li>
                    <li><a href='#' onclick="copy_qua('qu5')">qids2</a></li>
                </ul>
            </div>
            <div class='col-md'>
                Duplicate:
                <ul>
                    <li><a href='#' onclick="copy_qua('qu2')"> pages to remove</a></li>
                    <li><a href='#' onclick="copy_qua('qu3')">pages2</a></li>
                    <li><a href='#' onclick="copy_qua('qu1')">views</a></li>
                </ul>
            </div>
            <div class='col-md'>
                INSERT:
                <ul>
                    <li><a href='#' onclick="copy_qua('users')">Users</a></li>
                </ul>
            </div>
            <div class='col-md'>
                UPDATE:
                <ul>
                    <li><a href='#' onclick="copy_qua('update_words')">pages words</a></li>
                    <li><a href='#' onclick="copy_qua('video')">videos</a></li>
                    <li><a href='#' onclick="copy_qua('articles_cats')">articles_cats</a></li>
                    <li><a href='#' onclick="copy_qua('RTT_cats')">RTT_cats</a></li>
                </ul>
            </div>
            <div class='col-md'>
                DELETE:
                <ul>
                    <li><a href='#' onclick="copy_qua('qu6')">In process > 7</a></li>
                    <li><a href='#' onclick="copy_qua('in_process')">In process pages</a></li>
                </ul>
            </div>
        </div>
        <form action='index.php' method='POST'>
            <div class='row'>
                <div class='col-9'>
                    <div class="row justify-content-center">
                        <div class="col-11">
                        <label for="editor" class="form-label fw-semibold">🛠 SQL Query</label>
                        <div id="editor" style="height: 300px; width: 100%;">$qua</div>
                        <textarea id="code" name="code" style="display: none;"></textarea>
                        </div>
                    </div>
                </div>
                <div class='col-3'>
                    <div class='input-group mb-2'>
                        <span class='input-group-text'>
                            <label class='mr-sm-2' for='pass'>code:</label>
                        </span>
                        <input class='form-control' type='text' name='pass' value='$pass' />
                    </div>
                    <div class='input-group mb-3'>
                        <div class='custom-control custom-checkbox custom-control-inline'>
                            <input type='checkbox' class='custom-control-input' name='test' value='1'>
                            <label class='custom-control-label' for='test'>test</label>
                        </div>
                    </div>
                    <div class='input-group'>
                        <div class='aligncenter'>
                            <input class='btn btn-outline-primary' type='submit' name='start' value='Start' />
                        </div>
                    </div>
                </div>
            </div>
        </form>
    HTML;
    // ---
    $form .= "<script> var queries = " . json_encode($queries) . "</script>";
    // ---
    return $form;
}

/*
$sql = <<<____SQL CREATE TABLE IF NOT EXISTS `ticket_hist` ( `tid` int(11) NOT NULL, `trqform` varchar(40) NOT NULL, `trsform` varchar(40) NOT NULL, `tgen` datetime NOT NULL, `tterm` datetime, `tstatus` tinyint(1) NOT NULL ) ENGINE=ARCHIVE COMMENT='ticket archive' ; ____SQL; $result=$this->db->getConnection()->exec($sql);

*/
