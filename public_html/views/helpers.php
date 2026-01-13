<?php

if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

function build_card_with_table(string $title, string $table_html, string $extra_classes = ''): string
{
    return <<<HTML
        <div class="card $extra_classes">
            <div class="card-header">
                <span class="card-title h2">$title</span>
                <div class="card-tools">
                    <button type="button" class="btn-tool" data-card-widget="collapse">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>
            <div class="card-body">
                $table_html
            </div>
        </div>
    HTML;
}
