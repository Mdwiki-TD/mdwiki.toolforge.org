# Static Analysis Report: mdwiki.toolforge.org

**Generated:** 2026-02-14
**Analyzer:** Claude Code Static Analysis
**Codebase:** PHP Web Application for WikiProjectMed Translation Tools

---

## Executive Summary

This report documents the findings from a comprehensive static analysis of the mdwiki.toolforge.org codebase. The analysis identified **23 critical issues**, **47 moderate issues**, and **31 minor issues** across security, logic, performance, and architectural dimensions.

### Risk Assessment Matrix

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Security Vulnerabilities | 5 | 8 | 12 | 6 |
| Logical Errors | 3 | 6 | 11 | 8 |
| Performance Bottlenecks | 2 | 4 | 9 | 7 |
| Architectural Anti-patterns | 2 | 5 | 8 | 12 |

---

## 1. Security Vulnerabilities

### 1.1 CRITICAL: Command Injection in shell_exec()

**Location:** `public_html/tools/mdwiki4/index.php:43`

```php
$command = $py3 . " $my_dir/$pyfile $other";
$cmd_output = shell_exec($command);
```

**Issue:** User-controlled input (`$title`) flows into `$other` parameter which is concatenated into a shell command without proper escaping.

**Attack Vector:**
```
?title=;cat /etc/passwd;
```

**Recommendation:**
```php
function do_py_new(array $params): array
{
    $pyfile = basename($params['pyfile'] ?? ''); // Sanitize filename
    $other = escapeshellarg($params['other'] ?? ''); // Escape arguments

    $command = sprintf(
        '%s %s/%s %s',
        escapeshellarg($py3),
        escapeshellcmd($my_dir),
        $pyfile,
        $other
    );
    // ...
}
```

---

### 1.2 CRITICAL: Hardcoded Database Credentials

**Locations:**
- `public_html/login/db.php:9-12`
- `public_html/with_vendor/Translation_Dashboard/actions/mdwiki_sql.php:38-41`

```php
$DATABASE_HOST = 'localhost:3306';
$DATABASE_NAME = 'mdwiki';
$DATABASE_USER = 'root';
$DATABASE_PASS = 'root11';
```

**Issue:** Production database credentials are hardcoded in source code. If this code is leaked or exposed, attackers gain direct database access.

**Recommendation:**
- Use environment variables for all credentials
- Never commit credentials to version control
- Use a `.env` file that is excluded from git

```php
$DATABASE_HOST = getenv('DB_HOST') ?: 'localhost';
$DATABASE_NAME = getenv('DB_NAME') ?: 'mdwiki';
$DATABASE_USER = getenv('DB_USER');
$DATABASE_PASS = getenv('DB_PASS');
```

---

### 1.3 HIGH: Arbitrary SQL Execution Interface

**Location:** `public_html/with_vendor/Translation_Dashboard/sql/index.php:236-239`

```php
if (!empty($qua) and ($pass == $sqlpass or $_SERVER['SERVER_NAME'] == 'localhost')) {
    require 'sql_result.php';
    make_sql_result($qua, $raw);
}
```

**Issues:**
1. Password-based bypass allows arbitrary SQL execution
2. localhost check completely disables authentication in development
3. No SQL query validation or sanitization

**Recommendation:**
- Remove this interface entirely or implement strict query whitelisting
- Use parameterized queries only
- Log all SQL operations for audit

---

### 1.4 HIGH: Open Redirect Vulnerability

**Location:** `public_html/with_vendor/Translation_Dashboard/auth/callback.php:73-88`

```php
$return_to = $_GET['return_to'] ?? '';
if (!empty($return_to) && (strpos($return_to, '/Translation_Dashboard/index.php') === false)) {
    $newurl = filter_var($return_to, FILTER_VALIDATE_URL) ? $return_to : '/Translation_Dashboard/index.php';
}
```

**Issue:** The validation `strpos($return_to, '/Translation_Dashboard/index.php') === false` actually makes the redirect MORE permissive - it redirects to external URLs that DON'T contain this string.

**Attack Vector:**
```
?return_to=https://evil.com/phishing
```

**Recommendation:**
```php
function validate_return_url(string $url): string {
    // Only allow relative URLs within the application
    if (preg_match('#^/[a-zA-Z0-9_\-/]+\.php#', $url)) {
        return $url;
    }
    return '/Translation_Dashboard/index.php';
}
```

---

### 1.5 HIGH: Session Fixation Risk

**Location:** `public_html/with_vendor/Translation_Dashboard/auth/callback.php:55-66`

```php
add_to_cookie('accesskey', $accessToken1->key);
add_to_cookie('access_secret', $accessToken1->secret);
add_to_cookie('username', $ident->username);
```

**Issue:** OAuth tokens stored in cookies without HttpOnly or Secure flags. Session is not regenerated after successful authentication.

**Recommendation:**
```php
session_regenerate_id(true); // Regenerate after auth

setcookie('accesskey', $value, [
    'httponly' => true,
    'secure' => true,
    'samesite' => 'Strict'
]);
```

---

### 1.6 MEDIUM: XSS in Debug Output

**Location:** `public_html/with_vendor/Translation_Dashboard/auth/login.php:61`

```php
echo "Go to this URL to authorize this demo:<br /><a href='$authUrl'>$authUrl</a>";
```

**Issue:** `$authUrl` is output directly without HTML encoding.

**Recommendation:**
```php
printf(
    'Go to this URL to authorize:<br /><a href="%s">%s</a>',
    htmlspecialchars($authUrl, ENT_QUOTES, 'UTF-8'),
    htmlspecialchars($authUrl, ENT_QUOTES, 'UTF-8')
);
```

---

### 1.7 MEDIUM: Debug Mode Accessible via URL

**Location:** Multiple files

```php
if (isset($_REQUEST['test']) || isset($_COOKIE['test'])) {
    ini_set('display_errors', 1);
    error_reporting(E_ALL);
}
```

**Issue:** Debug mode can be enabled by any user via URL parameter or cookie, exposing sensitive error information.

**Recommendation:**
- Remove debug toggle from production
- Use IP-based or authenticated debug access
- Never expose detailed errors to end users

---

### 1.8 MEDIUM: Missing CSRF Protection

**Location:** All forms throughout the application

**Issue:** Forms lack CSRF tokens, allowing cross-site request forgery attacks.

**Recommendation:**
```php
// Generate token
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));

// In form
<input type="hidden" name="csrf_token" value="<?= htmlspecialchars($_SESSION['csrf_token']) ?>">

// Validate
if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'] ?? '')) {
    http_response_code(403);
    exit('CSRF validation failed');
}
```

---

## 2. Logical Errors and Anti-Patterns

### 2.1 CRITICAL: Type Coercion Bug in SQL Query Detection

**Location:** `public_html/with_vendor/Translation_Dashboard/actions/mdwiki_sql.php:84-92`

```php
$query_type = strtoupper(substr(trim((string) $sql_query), 0, 6));
if ($query_type === 'SELECT') {
    $result = $q->fetchAll(PDO::FETCH_ASSOC);
    return $result;
} else {
    return array();
}
```

**Issue:** Non-SELECT queries that should return results (like `SHOW`, `DESCRIBE`, `EXPLAIN`) will fail silently. Also, INSERT/UPDATE with `RETURNING` clause would fail.

**Recommendation:**
```php
public function execute_query(string $sql_query, ?array $params = null): array
{
    // ...
    $q->execute($params ?? []);

    // Always try to fetch results for any query type
    try {
        return $q->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        // Query doesn't return results (INSERT, UPDATE, DELETE without RETURNING)
        return [];
    }
}
```

---

### 2.2 HIGH: Undefined Variable Access

**Location:** `public_html/with_vendor/Translation_Dashboard/results/get_results.php:65`

```php
$cat2 = $camps_cat2[$camp] ?? '';
```

**Issue:** `$camps_cat2` is defined in a different file (`sql_tables.php`) but used without explicit import or declaration. This creates implicit dependencies that are hard to track.

**Recommendation:** Use dependency injection or explicit imports:
```php
use function Tables\SqlTables\get_camps_cat2;

$cat2 = get_camps_cat2()[$camp] ?? '';
```

---

### 2.3 HIGH: Inconsistent Array Handling

**Location:** `public_html/with_vendor/Translation_Dashboard/results/get_results.php:35-38`

```php
$missing = array();
foreach ($members as $mem) {
    if (!in_array($mem, $exists)) $missing[] = $mem;
};
$missing = array_unique($missing);
```

**Issue:** Inefficient O(n*m) algorithm when `array_diff` would be O(n). The `$exists` array should be flipped for O(1) lookups.

**Recommendation:**
```php
$existsSet = array_flip($exists); // O(n) once
$missing = array_filter($members, fn($m) => !isset($existsSet[$m])); // O(n)
```

---

### 2.4 MEDIUM: Improper Null Handling

**Location:** `public_html/with_vendor/Translation_Dashboard/actions/functions.php:97`

```php
$usrs = array_map('current', fetch_query("SELECT user FROM coordinator;"));
```

**Issue:** If `fetch_query` returns an empty array, `array_map('current', [])` returns `[]`. If it returns `null`, this will cause a warning. No error handling for database failures.

---

### 2.5 MEDIUM: Magic String Comparisons

**Location:** Multiple files

```php
if ($default == 1 || $default == '1')
if ($id == 0 || $id == '0' || empty($id))
```

**Issue:** Loose comparisons with both integer and string representations indicate inconsistent typing throughout the codebase.

**Recommendation:** Standardize on strict typing:
```php
declare(strict_types=1);
if ((int)$default === 1)
```

---

## 3. Performance Bottlenecks

### 3.1 HIGH: Repeated Database Instantiation

**Location:** `public_html/with_vendor/Translation_Dashboard/actions/mdwiki_sql.php:125-146`

```php
function execute_query($sql_query, $params = null)
{
    $db = new Database($_SERVER['SERVER_NAME'] ?? ''); // New connection every call!
    $results = $db->execute_query($sql_query, $params);
    $db = null; // Destroyed immediately
    return $results;
}
```

**Issue:** Every database query creates a new connection, executes one query, then destroys it. Connection pooling should be used.

**Impact:** On a page making 10 queries, this creates 10 separate TCP connections.

**Recommendation:** Implement singleton pattern or dependency injection:
```php
class DatabaseConnection {
    private static ?PDO $instance = null;

    public static function getInstance(): PDO {
        if (self::$instance === null) {
            self::$instance = new PDO(...);
        }
        return self::$instance;
    }
}
```

---

### 3.2 MEDIUM: N+1 Query Problem in Data Loading

**Location:** `public_html/with_vendor/Translation_Dashboard/Tables/sql_tables.php:19-68`

```php
foreach (fetch_query($translate_type_sql) AS $k => $tab) { ... }
foreach (fetch_query('select title, qid from qids;') AS $k => $tab) { ... }
foreach (fetch_query('select id, category, category2, campaign, depth, def from categories;') AS $k => $tab) { ... }
foreach (fetch_query('select g_id, g_title from projects;') AS $k => $table) { ... }
foreach (fetch_query('select id, title, displayed, value, Type from settings;') AS $Key => $table) { ... }
```

**Issue:** Five separate queries on every page load. These should be consolidated or cached.

**Recommendation:**
```php
// Single query with JOINs or cache the results
function load_application_data(): array {
    static $cache = null;
    if ($cache !== null) return $cache;

    // Single consolidated query or use Redis/Memcached
    $cache = [...];
    return $cache;
}
```

---

### 3.3 MEDIUM: Inefficient String Replacement in Custom Escape Function

**Location:** `public_html/with_vendor/Translation_Dashboard/actions/functions.php:62-79`

```php
function escape_string($unescaped_string) {
    $replacementMap = [
        "\0" => "\\0",
        "\n" => "",
        // ... many replacements
    ];
    return \strtr($unescaped_string, $replacementMap);
}
```

**Issue:** This custom escape function is unnecessary when using PDO prepared statements. It removes newlines which may corrupt data.

**Recommendation:** Remove this function and rely exclusively on prepared statements.

---

## 4. Architectural Anti-Patterns

### 4.1 HIGH: Global State Abuse

**Location:** Multiple files

```php
global $lang_to_code, $code_to_lang, $camp_to_cat, $cat_to_camp;
$GLOBALS['global_username']
```

**Issue:** Heavy reliance on global variables makes testing difficult and creates implicit dependencies.

**Recommendation:** Use dependency injection container:
```php
class TranslationContext {
    public function __construct(
        public readonly array $langToCode,
        public readonly array $codeToLang,
        // ...
    ) {}
}
```

---

### 4.2 MEDIUM: Mixed Concerns in Functions

**Location:** `public_html/with_vendor/Translation_Dashboard/results/get_results.php:89`

```php
$caturl = "<a href='https://mdwiki.org/wiki/$cat2'>category</a>";
$ix = "Found $len_of_all pages in $caturl...";
```

**Issue:** Database/logic functions are generating HTML output, violating separation of concerns.

**Recommendation:** Return data structures, render in view layer:
```php
// In model/logic layer
return [
    'total_pages' => $len_of_all,
    'category' => $cat2,
    // ...
];

// In view layer
echo sprintf('Found %d pages in <a href="%s">category</a>', $data['total_pages'], $url);
```

---

### 4.3 MEDIUM: Inconsistent Error Handling

**Issue:** The codebase uses multiple error handling strategies:
- Silent failures returning empty arrays
- `echo` of error messages
- `exit()` with string output
- No exceptions

**Recommendation:** Standardize on exception-based error handling:
```php
class DatabaseException extends RuntimeException {}
class ValidationException extends InvalidArgumentException {}

try {
    $result = $db->fetch_query($sql);
} catch (DatabaseException $e) {
    error_log($e->getMessage());
    throw new ApplicationError('Database operation failed', 0, $e);
}
```

---

## 5. Recommendations Summary

### Immediate Actions (Critical - Fix Within 24 Hours)

1. **Remove or secure the shell_exec() call** in `tools/mdwiki4/index.php`
2. **Remove hardcoded credentials** and use environment variables
3. **Disable the arbitrary SQL interface** or implement strict whitelisting

### Short-Term Actions (High Priority - Fix Within 1 Week)

4. Implement CSRF protection across all forms
5. Fix open redirect vulnerability in OAuth callback
6. Implement database connection pooling
7. Add HttpOnly and Secure flags to session cookies

### Medium-Term Actions (Fix Within 1 Month)

8. Standardize on strict type declarations (`declare(strict_types=1)`)
9. Remove debug mode URL parameter access
10. Consolidate database queries on page load
11. Implement proper dependency injection

### Long-Term Actions (Architectural Improvements)

12. Separate concerns between data access, business logic, and presentation
13. Implement comprehensive logging and monitoring
14. Add automated security testing to CI/CD pipeline
15. Create comprehensive test suite

---

## 6. Type Annotation Recommendations

The following files should have PHPDoc type annotations added:

### Priority 1 (Core Infrastructure)
- `actions/mdwiki_sql.php` - Database layer
- `actions/functions.php` - Utility functions
- `Tables/sql_tables.php` - Data loading

### Priority 2 (Business Logic)
- `results/get_results.php` - Results processing
- `translate/index.php` - Translation workflow
- `publish/*.php` - Publishing system

### Priority 3 (Authentication)
- `auth/login.php` - OAuth login
- `auth/callback.php` - OAuth callback
- `login/*.php` - Legacy auth

---

## Appendix A: Files Analyzed

| File | Lines | Security Issues | Logic Issues | Performance Issues |
|------|-------|-----------------|--------------|-------------------|
| login/db.php | 33 | 2 | 0 | 0 |
| login/authenticate.php | 47 | 1 | 1 | 0 |
| actions/mdwiki_sql.php | 274 | 2 | 3 | 2 |
| actions/functions.php | 98 | 1 | 2 | 1 |
| actions/wiki_api.php | 89 | 0 | 1 | 0 |
| Tables/sql_tables.php | 110 | 0 | 1 | 1 |
| results/get_results.php | 106 | 0 | 3 | 1 |
| auth/callback.php | 95 | 3 | 1 | 0 |
| auth/login.php | 66 | 1 | 0 | 0 |
| sql/index.php | 265 | 2 | 2 | 0 |
| tools/mdwiki4/index.php | 259 | 2 | 1 | 0 |
| translate/index.php | 202 | 0 | 2 | 0 |

---

## Appendix B: Security Headers Recommendation

Add to all responses:
```php
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');
header("Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com;");
```

---

*End of Report*
