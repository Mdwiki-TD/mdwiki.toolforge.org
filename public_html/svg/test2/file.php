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
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</head>

<body class="bg-light py-4">

    <div class="container">
        <h4 class="mb-4 text-center">SVG Languages</h4>

        <div class="row cols row-cols-2 g-2">
            <!-- Card 1 -->
            <div class="col">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: Parkinsons-disease-prevalence-ihme,Asia,2002.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:Parkinsons-disease-prevalence-ihme,Asia,2002.svg"></div>
                    </div>
                </div>
            </div>

            <!-- Card 2 -->
            <div class="col">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: test.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:test.svg"></div>
                    </div>
                </div>
            </div>

            <!-- Card 3 -->
            <div class="col">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title text-primary">File: maternal-mortality,World,1751.svg</h6>
                        <p class="mb-1 fw-semibold">Languages:</p>
                        <div class="get_languages" data-file="File:maternal-mortality,World,1751.svg"><span></span></div>
                    </div>
                </div>
            </div>

            <!-- Card 4 -->
            <div class="col">
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

    <script src="../mw.js"></script>
    <script src="../Gadget-SVGLanguages.js"></script>

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
