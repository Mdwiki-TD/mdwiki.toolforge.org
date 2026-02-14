# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the mdwiki.toolforge.org codebase - a collection of web tools for WikiProjectMed hosted on Wikimedia Toolforge. The main tool is the Translation Dashboard, which identifies Wikidata items that have a page on mdwiki.org but not in other Wikipedia languages.

## Deployment

The project is deployed to Wikimedia Toolforge. Pushing to the `main` branch triggers automatic deployment via GitHub Actions (.github/workflows/d.yaml):
- The workflow runs `shs/update_html.sh` on the Toolforge server
- This script clones the repo, removes sensitive directories (Translation_Dashboard, publish, api), and copies files to `public_html/`

For deploying individual repositories/components, use:
```bash
shs/deploy_repo.sh <repo_name> <target_dir> [branch]
# Example: shs/deploy_repo.sh cats_maker bots/cats_maker
```

## Architecture

### PHP Web Application
- `public_html/` - Main web root served by lighttpd
- `public_html/header.php` - Shared header with Bootstrap 5, jQuery, DataTables, and navigation
- `public_html/footer.php` - Shared footer
- `public_html/userinfos_wrap.php` - OAuth authentication wrapper (loads from `auth_repo/oauth/user_infos.php` on local Windows, or `public_html/auth/oauth/` on server)

### Translation Dashboard
The main application lives in `public_html/with_vendor/Translation_Dashboard/` (a separate repository):
- Uses namespaces (e.g., `TD`, `Actions`, `Infos`)
- Key directories: `actions/`, `auth/`, ` Tables/`, `sql/`, `results/`, `publish/`
- OAuth authentication via MediaWiki OAuth client
- Database tables defined in `sql.sql`

### Other Tools
- `public_html/views/` - PageViews dashboard (standalone HTML/PHP)
- `public_html/prior/` - Prior List tool
- `public_html/tools/` - Various utility tools (redirect, import-history, fixref, etc.)
- `public_html/login/` - Simple authentication system

### PHP Dependencies
Managed via Composer in `composer.json`:
- `phpmailer/phpmailer` - Email functionality
- `google/apiclient` - Google API integration
- `mediawiki/oauthclient` - MediaWiki OAuth
- `wiki-connect/parsewiki` - Wiki text parsing

### Python Bot Jobs
Scheduled jobs run on Toolforge via `toolforge-jobs`. Configuration in `mdwiki-jobs.yaml`:
- Uses pywikibot scripts from `core8/pwb.py`
- Jobs include: translation syncing, database backups, reference fixing, pageview stats, Wikidata QID management
- Shell scripts in `jobs/` directory

## Database

MariaDB database with tables for:
- `categories` - Translation categories and campaigns
- `translations` - Translation tracking
- `users` and `coordinator` - User management
- `enwiki_pageviews` - English Wikipedia pageview data
- `in_process` - Articles currently being translated

## Local Development

The codebase detects local Windows development (`substr(__DIR__, 0, 2) == 'I:'`) and adjusts paths accordingly.

Enable debug mode by adding `?test` parameter or setting a `test` cookie.

## Scheduled Jobs

Toolforge jobs are defined in `mdwiki-jobs.yaml`. To manage jobs:
```bash
# List jobs
toolforge-jobs list

# Run a job manually
toolforge-jobs run <job_name> --image <image> --command "<command>"

# Example images: tf-python39, python3.9, bullseye, mariadb
```

## File Conventions

- Configuration files stored in `confs/` (gitignored - contains sensitive data like OAuth keys, database credentials)
- The `.gitignore` excludes vendor directories, log files, and sensitive configuration
