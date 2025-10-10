<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG Language Extractor</title>
    <!-- Bootstrap 5.3 CSS -->
    <!-- load jquery -->
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js'></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light py-4">

    <div class="container">
        <h4 class="mb-4 text-center">SVG Languages</h4>

        <div class="row g-4">
            <!-- Card 1 -->
            <div class="col-md-6 col-lg-4">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: Parkinsons-disease-prevalence-ihme,World,1990.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:Parkinsons-disease-prevalence-ihme,World,1990.svg"></div>
                    </div>
                </div>
            </div>

            <!-- Card 2 -->
            <div class="col-md-6 col-lg-4">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: test.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:test.svg"></div>
                    </div>
                </div>
            </div>

            <!-- Card 3 -->
            <div class="col-md-6 col-lg-4">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: maternal-mortality,World,1751.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:maternal-mortality,World,1751.svg"><span></span></div>
                    </div>
                </div>
            </div>

            <!-- Card 4 -->
            <div class="col-md-6 col-lg-4">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: zzzzzzzzzzzzzzzzzzzzz.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:zzzzzzzzzzzzzzzzzzzzz.svg"><span></span></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        class RealMwApi {
            async get(params) {
                // const end_point = 'https://commons.wikimedia.org/w/api.php';
                const end_point = 'https://ar.wikipedia.org/w/api.php';
                const url = new URL(end_point);
                for (const [key, value] of Object.entries(params)) {
                    url.searchParams.append(key, value);
                }
                url.searchParams.append('origin', '*'); // required for CORS in browser

                const res = await fetch(url);
                if (!res.ok) {
                    throw new Error(`HTTP error ${res.status}`);
                }
                return res.json();
            }
        }

        // Replace mw.Api with the real fetch-based implementation
        const mw = {
            Api: RealMwApi,
            loader: {
                using(modules) {
                    console.log('Loaded modules:', modules);
                    return Promise.resolve();
                }
            }
        };
    </script>
    <script src="../FileLanguages.js"></script>

    <script>
        let divs = $('.get_languages');

        var $button = $('<button>', {
            type: 'button',
            class: 'cdx-button cdx-button--action-progressive cdx-button--weight-primary cdx-button--size-medium',
            text: 'Load'
        });

        divs.append($button);

        $('.get_languages button').on('click', function() {
            const one = $(this);
            const fileName = one.parent().attr('data-file');
            const itemSpan = one.parent().find("span");
            itemSpan.text(fileName);
        });
    </script>
</body>

</html>
