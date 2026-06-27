[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Mdwiki-TD/mdwiki.toolforge.org)

# mdwiki.toolforge.org

<a href="https://mdwiki.toolforge.org/">https://mdwiki.toolforge.org/<a/>

# End points

| Endpoint        | Method | Description             |
| --------------- | ------ | ----------------------- |
| `/`             | GET    | Main entry / Dashboard  |
| `/fixwikirefs/` | GET    | Fix References tool     |
| `/views/`       | GET    | Pageviews Dashboard     |
| `/prior/`       | GET    | Prior List Dashboard    |
| `/WHO/`         | GET    | WHO Essential Medicines |
| `/gmail1/`      | POST   | Gmail Sender            |
| `/404.php`      | GET    | Custom 404 handler      |

# Tools end points

| Endpoint              | Method | Description                       |
| --------------------- | ------ | --------------------------------- |
| `/mdwiki4.php`        | GET    | Redirect → mdw updater            |
| `/mdwiki5.php`        | GET    | Redirect → mdw updater            |
| `/redirect.php`       | GET    | Redirect → create redirects job   |
| `/fixred.php`         | GET    | Redirect → fix redlinks           |
| `/fixref.php`         | GET    | Redirect → fix references job     |
| `/dup.php`            | GET    | Redirect → duplicate redirect job |
| `/import-history.php` | GET    | Redirect → import history job     |
| `/replace.php`        | GET    | Redirect → find & replace job     |

# Sub end points

| Endpoint                  | Method   | Description                       |
| ------------------------- | -------- | --------------------------------- |
| `/api/` or `/api.php`     | GET/POST | API Gateway (delegates to TD_API) |
| `/Translation_Dashboard/` | GET      | Translation Dashboard main        |
| `/auth/`                  | GET/POST | OAuth Login / logout / callback   |
