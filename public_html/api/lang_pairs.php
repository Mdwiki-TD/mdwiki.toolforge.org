<?php

namespace API\Langs;
/*
Usage:
use function API\Langs\get_lang_names_all;
use function API\Langs\get_lang_names;
*/

$print_t = false;

if (isset($_REQUEST['test'])) {
    $print_t = true;
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
}

define('print_te', $print_t);

$lang_tables = [
    "ami" => [
        "code" => "ami",
        "autonym" => "Pangcah",
        "name" => ""
    ],
    "anp" => [
        "code" => "anp",
        "autonym" => "अंगिका",
        "name" => ""
    ],
    "arc" => [
        "code" => "arc",
        "autonym" => "ܐܪܡܝܐ",
        "name" => ""
    ],
    "blk" => [
        "code" => "blk",
        "autonym" => "ပအိုဝ်ႏဘာႏသာႏ",
        "name" => ""
    ],
    "dag" => [
        "code" => "dag",
        "autonym" => "dagbanli",
        "name" => ""
    ],
    "guc" => [
        "code" => "guc",
        "autonym" => "wayuunaiki",
        "name" => ""
    ],
    "gur" => [
        "code" => "gur",
        "autonym" => "farefare",
        "name" => ""
    ],
    "guw" => [
        "code" => "guw",
        "autonym" => "gungbe",
        "name" => ""
    ],
    "ii" => [
        "code" => "ii",
        "autonym" => "",
        "name" => "Sichuan Yi"
    ],
    "kcg" => [
        "code" => "kcg",
        "autonym" => "Tyap",
        "name" => ""
    ],
    "pcm" => [
        "code" => "pcm",
        "autonym" => "Naijá",
        "name" => ""
    ],
    "pwn" => [
        "code" => "pwn",
        "autonym" => "pinayuanan",
        "name" => ""
    ],
    "shi" => [
        "code" => "shi",
        "autonym" => "Taclḥit",
        "name" => ""
    ],
    "aa" => [
        "code" => "aa",
        "autonym" => "Afar",
        "name" => "Afar"
    ],
    "ab" => [
        "code" => "ab",
        "autonym" => "Аԥсуа",
        "name" => "Abkhazian"
    ],
    "ace" => [
        "code" => "ace",
        "autonym" => "Basa Acèh",
        "name" => "Achinese"
    ],
    "ady" => [
        "code" => "ady",
        "autonym" => "Адыгэбзэ",
        "name" => "Adyghe"
    ],
    "af" => [
        "code" => "af",
        "autonym" => "Afrikaans",
        "name" => "Afrikaans"
    ],
    "ak" => [
        "code" => "ak",
        "autonym" => "Akana",
        "name" => "Akan"
    ],
    "als" => [
        "code" => "als",
        "autonym" => "Alemannisch",
        "name" => "Alemannisch"
    ],
    "alt" => [
        "code" => "alt",
        "autonym" => "Алтай",
        "name" => "Southern Altai"
    ],
    "am" => [
        "code" => "am",
        "autonym" => "አማርኛ",
        "name" => "Amharic"
    ],
    "an" => [
        "code" => "an",
        "autonym" => "Aragonés",
        "name" => "Aragonese"
    ],
    "ang" => [
        "code" => "ang",
        "autonym" => "Englisc",
        "name" => "Old English"
    ],
    "ar" => [
        "code" => "ar",
        "autonym" => "العربية",
        "name" => "Arabic"
    ],
    "as" => [
        "code" => "as",
        "autonym" => "অসমীয়া",
        "name" => "Assamese"
    ],
    "ast" => [
        "code" => "ast",
        "autonym" => "Asturianu",
        "name" => "Asturian"
    ],
    "atj" => [
        "code" => "atj",
        "autonym" => "Atikamekw",
        "name" => "Atikamekw"
    ],
    "av" => [
        "code" => "av",
        "autonym" => "Авар",
        "name" => "Avaric"
    ],
    "avk" => [
        "code" => "avk",
        "autonym" => "Kotava",
        "name" => "Kotava"
    ],
    "awa" => [
        "code" => "awa",
        "autonym" => "अवधी",
        "name" => "Awadhi"
    ],
    "ay" => [
        "code" => "ay",
        "autonym" => "Aymar",
        "name" => "Aymara"
    ],
    "az" => [
        "code" => "az",
        "autonym" => "Azərbaycanca",
        "name" => "Azerbaijani"
    ],
    "azb" => [
        "code" => "azb",
        "autonym" => "تۆرکجه",
        "name" => "South Azerbaijani"
    ],
    "ba" => [
        "code" => "ba",
        "autonym" => "Башҡорт",
        "name" => "Bashkir"
    ],
    "ban" => [
        "code" => "ban",
        "autonym" => "Bali",
        "name" => "Balinese"
    ],
    "bar" => [
        "code" => "bar",
        "autonym" => "Boarisch",
        "name" => "Bavarian"
    ],
    "bat-smg" => [
        "code" => "bat-smg",
        "autonym" => "Žemaitėška",
        "name" => "Samogitian"
    ],
    "bcl" => [
        "code" => "bcl",
        "autonym" => "Bikol",
        "name" => "Central Bikol"
    ],
    "be" => [
        "code" => "be",
        "autonym" => "Беларуская",
        "name" => "Belarusian"
    ],
    "be-tarask" => [
        "code" => "be-tarask",
        "autonym" => "Беларуская",
        "name" => "Belarusian (Taraškievica orthography)"
    ],
    "bg" => [
        "code" => "bg",
        "autonym" => "Български",
        "name" => "Bulgarian"
    ],
    "bh" => [
        "code" => "bh",
        "autonym" => "भोजपुरी",
        "name" => "Bhojpuri"
    ],
    "bi" => [
        "code" => "bi",
        "autonym" => "Bislama",
        "name" => "Bislama"
    ],
    "bjn" => [
        "code" => "bjn",
        "autonym" => "Bahasa Banjar",
        "name" => "Banjar"
    ],
    "bm" => [
        "code" => "bm",
        "autonym" => "Bamanankan",
        "name" => "Bambara"
    ],
    "bn" => [
        "code" => "bn",
        "autonym" => "বাংলা",
        "name" => "Bangla"
    ],
    "bo" => [
        "code" => "bo",
        "autonym" => "བོད་སྐད",
        "name" => "Tibetan"
    ],
    "bpy" => [
        "code" => "bpy",
        "autonym" => "ইমার ঠার/বিষ্ণুপ্রিয়া মণিপুরী",
        "name" => "Bishnupriya"
    ],
    "br" => [
        "code" => "br",
        "autonym" => "Brezhoneg",
        "name" => "Breton"
    ],
    "bs" => [
        "code" => "bs",
        "autonym" => "Bosanski",
        "name" => "Bosnian"
    ],
    "bug" => [
        "code" => "bug",
        "autonym" => "Basa Ugi",
        "name" => "Buginese"
    ],
    "bxr" => [
        "code" => "bxr",
        "autonym" => "Буряад",
        "name" => "Russia Buriat"
    ],
    "ca" => [
        "code" => "ca",
        "autonym" => "Català",
        "name" => "Catalan"
    ],
    "cbk-zam" => [
        "code" => "cbk-zam",
        "autonym" => "Chavacano de Zamboanga",
        "name" => "Chavacano"
    ],
    "cdo" => [
        "code" => "cdo",
        "autonym" => "Mìng-dĕ̤ng-ngṳ̄",
        "name" => "Min Dong Chinese"
    ],
    "ce" => [
        "code" => "ce",
        "autonym" => "Нохчийн",
        "name" => "Chechen"
    ],
    "ceb" => [
        "code" => "ceb",
        "autonym" => "Sinugboanong Binisaya",
        "name" => "Cebuano"
    ],
    "ch" => [
        "code" => "ch",
        "autonym" => "Chamoru",
        "name" => "Chamorro"
    ],
    "cho" => [
        "code" => "cho",
        "autonym" => "Choctaw",
        "name" => "Choctaw"
    ],
    "chr" => [
        "code" => "chr",
        "autonym" => "ᏣᎳᎩ",
        "name" => "Cherokee"
    ],
    "chy" => [
        "code" => "chy",
        "autonym" => "Tsetsêhestâhese",
        "name" => "Cheyenne"
    ],
    "ckb" => [
        "code" => "ckb",
        "autonym" => "Soranî / کوردی",
        "name" => "Central Kurdish"
    ],
    "co" => [
        "code" => "co",
        "autonym" => "Corsu",
        "name" => "Corsican"
    ],
    "cr" => [
        "code" => "cr",
        "autonym" => "Nehiyaw",
        "name" => "Cree"
    ],
    "crh" => [
        "code" => "crh",
        "autonym" => "Qırımtatarca",
        "name" => "Crimean Tatar"
    ],
    "cs" => [
        "code" => "cs",
        "autonym" => "Čeština",
        "name" => "Czech"
    ],
    "csb" => [
        "code" => "csb",
        "autonym" => "Kaszëbsczi",
        "name" => "Kashubian"
    ],
    "cu" => [
        "code" => "cu",
        "autonym" => "Словѣньскъ",
        "name" => "Church Slavic"
    ],
    "cv" => [
        "code" => "cv",
        "autonym" => "Чăваш",
        "name" => "Chuvash"
    ],
    "cy" => [
        "code" => "cy",
        "autonym" => "Cymraeg",
        "name" => "Welsh"
    ],
    "da" => [
        "code" => "da",
        "autonym" => "Dansk",
        "name" => "Danish"
    ],
    "de" => [
        "code" => "de",
        "autonym" => "Deutsch",
        "name" => "German"
    ],
    "din" => [
        "code" => "din",
        "autonym" => "Thuɔŋjäŋ",
        "name" => "Dinka"
    ],
    "diq" => [
        "code" => "diq",
        "autonym" => "Zazaki",
        "name" => "Zazaki"
    ],
    "dsb" => [
        "code" => "dsb",
        "autonym" => "Dolnoserbski",
        "name" => "Lower Sorbian"
    ],
    "dty" => [
        "code" => "dty",
        "autonym" => "डोटेली",
        "name" => "Doteli"
    ],
    "dv" => [
        "code" => "dv",
        "autonym" => "ދިވެހިބަސް",
        "name" => "Divehi"
    ],
    "dz" => [
        "code" => "dz",
        "autonym" => "ཇོང་ཁ",
        "name" => "Dzongkha"
    ],
    "ee" => [
        "code" => "ee",
        "autonym" => "Eʋegbe",
        "name" => "Ewe"
    ],
    "el" => [
        "code" => "el",
        "autonym" => "Ελληνικά",
        "name" => "Greek"
    ],
    "eml" => [
        "code" => "eml",
        "autonym" => "Emiliàn e rumagnòl",
        "name" => "Emiliano-Romagnolo"
    ],
    "en" => [
        "code" => "en",
        "autonym" => "English",
        "name" => "English"
    ],
    "eo" => [
        "code" => "eo",
        "autonym" => "Esperanto",
        "name" => "Esperanto"
    ],
    "es" => [
        "code" => "es",
        "autonym" => "Español",
        "name" => "Spanish"
    ],
    "et" => [
        "code" => "et",
        "autonym" => "Eesti",
        "name" => "Estonian"
    ],
    "eu" => [
        "code" => "eu",
        "autonym" => "Euskara",
        "name" => "Basque"
    ],
    "ext" => [
        "code" => "ext",
        "autonym" => "Estremeñu",
        "name" => "Extremaduran"
    ],
    "fa" => [
        "code" => "fa",
        "autonym" => "فارسی",
        "name" => "Persian"
    ],
    "ff" => [
        "code" => "ff",
        "autonym" => "Fulfulde",
        "name" => "Fulah"
    ],
    "fi" => [
        "code" => "fi",
        "autonym" => "Suomi",
        "name" => "Finnish"
    ],
    "fiu-vro" => [
        "code" => "fiu-vro",
        "autonym" => "Võro",
        "name" => "võro"
    ],
    "fj" => [
        "code" => "fj",
        "autonym" => "Na Vosa Vakaviti",
        "name" => "Fijian"
    ],
    "fo" => [
        "code" => "fo",
        "autonym" => "Føroyskt",
        "name" => "Faroese"
    ],
    "fr" => [
        "code" => "fr",
        "autonym" => "Français",
        "name" => "French"
    ],
    "frp" => [
        "code" => "frp",
        "autonym" => "Arpetan",
        "name" => "Arpitan"
    ],
    "frr" => [
        "code" => "frr",
        "autonym" => "Nordfriisk",
        "name" => "Northern Frisian"
    ],
    "fur" => [
        "code" => "fur",
        "autonym" => "Furlan",
        "name" => "Friulian"
    ],
    "fy" => [
        "code" => "fy",
        "autonym" => "Frysk",
        "name" => "Western Frisian"
    ],
    "ga" => [
        "code" => "ga",
        "autonym" => "Gaeilge",
        "name" => "Irish"
    ],
    "gag" => [
        "code" => "gag",
        "autonym" => "Gagauz",
        "name" => "Gagauz"
    ],
    "gan" => [
        "code" => "gan",
        "autonym" => "贛語",
        "name" => "Gan Chinese"
    ],
    "gcr" => [
        "code" => "gcr",
        "autonym" => "Kriyòl Gwiyannen",
        "name" => "Guianan Creole"
    ],
    "gd" => [
        "code" => "gd",
        "autonym" => "Gàidhlig",
        "name" => "Scottish Gaelic"
    ],
    "gl" => [
        "code" => "gl",
        "autonym" => "Galego",
        "name" => "Galician"
    ],
    "glk" => [
        "code" => "glk",
        "autonym" => "گیلکی",
        "name" => "Gilaki"
    ],
    "gn" => [
        "code" => "gn",
        "autonym" => "Avañe'ẽ",
        "name" => "Guarani"
    ],
    "gom" => [
        "code" => "gom",
        "autonym" => "गोंयची कोंकणी / Gõychi Konknni",
        "name" => "Goan Konkani"
    ],
    "gor" => [
        "code" => "gor",
        "autonym" => "Hulontalo",
        "name" => "Gorontalo"
    ],
    "got" => [
        "code" => "got",
        "autonym" => "𐌲𐌿𐍄𐌹𐍃𐌺",
        "name" => "Gothic"
    ],
    "gu" => [
        "code" => "gu",
        "autonym" => "ગુજરાતી",
        "name" => "Gujarati"
    ],
    "gv" => [
        "code" => "gv",
        "autonym" => "Gaelg",
        "name" => "Manx"
    ],
    "ha" => [
        "code" => "ha",
        "autonym" => "Hausa / هَوُسَ",
        "name" => "Hausa"
    ],
    "hak" => [
        "code" => "hak",
        "autonym" => "Hak-kâ-fa / 客家話",
        "name" => "Hakka Chinese"
    ],
    "haw" => [
        "code" => "haw",
        "autonym" => "Hawaiʻi",
        "name" => "Hawaiian"
    ],
    "he" => [
        "code" => "he",
        "autonym" => "עברית",
        "name" => "Hebrew"
    ],
    "hi" => [
        "code" => "hi",
        "autonym" => "हिन्दी",
        "name" => "Hindi"
    ],
    "hif" => [
        "code" => "hif",
        "autonym" => "Fiji Hindi",
        "name" => "Fiji Hindi"
    ],
    "ho" => [
        "code" => "ho",
        "autonym" => "Hiri Motu",
        "name" => "Hiri Motu"
    ],
    "hr" => [
        "code" => "hr",
        "autonym" => "Hrvatski",
        "name" => "Croatian"
    ],
    "hsb" => [
        "code" => "hsb",
        "autonym" => "Hornjoserbsce",
        "name" => "Upper Sorbian"
    ],
    "ht" => [
        "code" => "ht",
        "autonym" => "Krèyol ayisyen",
        "name" => "Haitian Creole"
    ],
    "hu" => [
        "code" => "hu",
        "autonym" => "Magyar",
        "name" => "Hungarian"
    ],
    "hy" => [
        "code" => "hy",
        "autonym" => "Հայերեն",
        "name" => "Armenian"
    ],
    "hyw" => [
        "code" => "hyw",
        "autonym" => "Արեւմտահայերէն",
        "name" => "Western Armenian"
    ],
    "hz" => [
        "code" => "hz",
        "autonym" => "Otsiherero",
        "name" => "Herero"
    ],
    "ia" => [
        "code" => "ia",
        "autonym" => "Interlingua",
        "name" => "Interlingua"
    ],
    "id" => [
        "code" => "id",
        "autonym" => "Bahasa Indonesia",
        "name" => "Indonesian"
    ],
    "ie" => [
        "code" => "ie",
        "autonym" => "Interlingue",
        "name" => "Interlingue"
    ],
    "ig" => [
        "code" => "ig",
        "autonym" => "Ìgbò",
        "name" => "Igbo"
    ],
    "ik" => [
        "code" => "ik",
        "autonym" => "Iñupiatun",
        "name" => "Inupiaq"
    ],
    "ilo" => [
        "code" => "ilo",
        "autonym" => "Ilokano",
        "name" => "Iloko"
    ],
    "inh" => [
        "code" => "inh",
        "autonym" => "ГӀалгӀай",
        "name" => "Ingush"
    ],
    "io" => [
        "code" => "io",
        "autonym" => "Ido",
        "name" => "Ido"
    ],
    "is" => [
        "code" => "is",
        "autonym" => "Íslenska",
        "name" => "Icelandic"
    ],
    "it" => [
        "code" => "it",
        "autonym" => "Italiano",
        "name" => "Italian"
    ],
    "iu" => [
        "code" => "iu",
        "autonym" => "ᐃᓄᒃᑎᑐᑦ",
        "name" => "Inuktitut"
    ],
    "ja" => [
        "code" => "ja",
        "autonym" => "日本語",
        "name" => "Japanese"
    ],
    "jam" => [
        "code" => "jam",
        "autonym" => "Jumiekan Kryuol",
        "name" => "Jamaican Creole English"
    ],
    "jbo" => [
        "code" => "jbo",
        "autonym" => "Lojban",
        "name" => "Lojban"
    ],
    "jv" => [
        "code" => "jv",
        "autonym" => "Basa Jawa",
        "name" => "Javanese"
    ],
    "ka" => [
        "code" => "ka",
        "autonym" => "ქართული",
        "name" => "Georgian"
    ],
    "kaa" => [
        "code" => "kaa",
        "autonym" => "Qaraqalpaqsha",
        "name" => "Kara-Kalpak"
    ],
    "kab" => [
        "code" => "kab",
        "autonym" => "Taqbaylit",
        "name" => "Kabyle"
    ],
    "kbd" => [
        "code" => "kbd",
        "autonym" => "Адыгэбзэ",
        "name" => "Kabardian"
    ],
    "kbp" => [
        "code" => "kbp",
        "autonym" => "Kabɩyɛ",
        "name" => "Kabiye"
    ],
    "kg" => [
        "code" => "kg",
        "autonym" => "Kikôngo",
        "name" => "Kongo"
    ],
    "ki" => [
        "code" => "ki",
        "autonym" => "Gĩkũyũ",
        "name" => "Kikuyu"
    ],
    "kj" => [
        "code" => "kj",
        "autonym" => "Kuanyama",
        "name" => "Kuanyama"
    ],
    "kk" => [
        "code" => "kk",
        "autonym" => "Қазақша",
        "name" => "Kazakh"
    ],
    "kl" => [
        "code" => "kl",
        "autonym" => "Kalaallisut",
        "name" => "Kalaallisut"
    ],
    "km" => [
        "code" => "km",
        "autonym" => "ភាសាខ្មែរ",
        "name" => "Khmer"
    ],
    "kn" => [
        "code" => "kn",
        "autonym" => "ಕನ್ನಡ",
        "name" => "Kannada"
    ],
    "ko" => [
        "code" => "ko",
        "autonym" => "한국어",
        "name" => "Korean"
    ],
    "koi" => [
        "code" => "koi",
        "autonym" => "Перем Коми",
        "name" => "Komi-Permyak"
    ],
    "kr" => [
        "code" => "kr",
        "autonym" => "Kanuri",
        "name" => "Kanuri"
    ],
    "krc" => [
        "code" => "krc",
        "autonym" => "Къарачай-Малкъар",
        "name" => "Karachay-Balkar"
    ],
    "ks" => [
        "code" => "ks",
        "autonym" => "कश्मीरी / كشميري",
        "name" => "Kashmiri"
    ],
    "ksh" => [
        "code" => "ksh",
        "autonym" => "Ripoarisch",
        "name" => "Colognian"
    ],
    "ku" => [
        "code" => "ku",
        "autonym" => "Kurdî / كوردی",
        "name" => "Kurdish"
    ],
    "kv" => [
        "code" => "kv",
        "autonym" => "Коми",
        "name" => "Komi"
    ],
    "kw" => [
        "code" => "kw",
        "autonym" => "Kernowek/Karnuack",
        "name" => "Cornish"
    ],
    "ky" => [
        "code" => "ky",
        "autonym" => "Кыргызча",
        "name" => "Kyrgyz"
    ],
    "la" => [
        "code" => "la",
        "autonym" => "Latina",
        "name" => "Latin"
    ],
    "lad" => [
        "code" => "lad",
        "autonym" => "Dzhudezmo",
        "name" => "Ladino"
    ],
    "lb" => [
        "code" => "lb",
        "autonym" => "Lëtzebuergesch",
        "name" => "Luxembourgish"
    ],
    "lbe" => [
        "code" => "lbe",
        "autonym" => "Лакку",
        "name" => "Lak"
    ],
    "lez" => [
        "code" => "lez",
        "autonym" => "Лезги чІал",
        "name" => "Lezghian"
    ],
    "lfn" => [
        "code" => "lfn",
        "autonym" => "Lingua franca nova",
        "name" => "Lingua Franca Nova"
    ],
    "lg" => [
        "code" => "lg",
        "autonym" => "Luganda",
        "name" => "Ganda"
    ],
    "li" => [
        "code" => "li",
        "autonym" => "Limburgs",
        "name" => "Limburgish"
    ],
    "lij" => [
        "code" => "lij",
        "autonym" => "Lìgure",
        "name" => "Ligurian"
    ],
    "lld" => [
        "code" => "lld",
        "autonym" => "Lingaz",
        "name" => "Ladin"
    ],
    "lmo" => [
        "code" => "lmo",
        "autonym" => "Lumbaart",
        "name" => "Lombard"
    ],
    "ln" => [
        "code" => "ln",
        "autonym" => "Lingala",
        "name" => "Lingala"
    ],
    "lo" => [
        "code" => "lo",
        "autonym" => "ລາວ",
        "name" => "Lao"
    ],
    "lrc" => [
        "code" => "lrc",
        "autonym" => "لۊری شومالی",
        "name" => "Northern Luri"
    ],
    "lt" => [
        "code" => "lt",
        "autonym" => "Lietuvių",
        "name" => "Lithuanian"
    ],
    "ltg" => [
        "code" => "ltg",
        "autonym" => "Latgaļu",
        "name" => "Latgalian"
    ],
    "lv" => [
        "code" => "lv",
        "autonym" => "Latviešu",
        "name" => "Latvian"
    ],
    "mad" => [
        "code" => "mad",
        "autonym" => "Madhurâ",
        "name" => "Madurese"
    ],
    "mai" => [
        "code" => "mai",
        "autonym" => "मैथिली",
        "name" => "Maithili"
    ],
    "map-bms" => [
        "code" => "map-bms",
        "autonym" => "Basa Banyumasan",
        "name" => "Basa Banyumasan"
    ],
    "mdf" => [
        "code" => "mdf",
        "autonym" => "Мокшень",
        "name" => "Moksha"
    ],
    "mg" => [
        "code" => "mg",
        "autonym" => "Malagasy",
        "name" => "Malagasy"
    ],
    "mh" => [
        "code" => "mh",
        "autonym" => "Ebon",
        "name" => "Marshallese"
    ],
    "mhr" => [
        "code" => "mhr",
        "autonym" => "Олык Марий",
        "name" => "Eastern Mari"
    ],
    "mi" => [
        "code" => "mi",
        "autonym" => "Māori",
        "name" => "Maori"
    ],
    "min" => [
        "code" => "min",
        "autonym" => "Minangkabau",
        "name" => "Minangkabau"
    ],
    "mk" => [
        "code" => "mk",
        "autonym" => "Македонски",
        "name" => "Macedonian"
    ],
    "ml" => [
        "code" => "ml",
        "autonym" => "മലയാളം",
        "name" => "Malayalam"
    ],
    "mn" => [
        "code" => "mn",
        "autonym" => "Монгол",
        "name" => "Mongolian"
    ],
    "mni" => [
        "code" => "mni",
        "autonym" => "ꯃꯤꯇꯩꯂꯣꯟ",
        "name" => "Manipuri"
    ],
    "mnw" => [
        "code" => "mnw",
        "autonym" => "မန်",
        "name" => "Mon"
    ],
    "mr" => [
        "code" => "mr",
        "autonym" => "मराठी",
        "name" => "Marathi"
    ],
    "mrj" => [
        "code" => "mrj",
        "autonym" => "Кырык Мары",
        "name" => "Western Mari"
    ],
    "ms" => [
        "code" => "ms",
        "autonym" => "Bahasa Melayu",
        "name" => "Malay"
    ],
    "mt" => [
        "code" => "mt",
        "autonym" => "Malti",
        "name" => "Maltese"
    ],
    "mus" => [
        "code" => "mus",
        "autonym" => "Muskogee",
        "name" => "Muscogee"
    ],
    "mwl" => [
        "code" => "mwl",
        "autonym" => "Mirandés",
        "name" => "Mirandese"
    ],
    "my" => [
        "code" => "my",
        "autonym" => "မြန်မာဘာသာ",
        "name" => "Burmese"
    ],
    "myv" => [
        "code" => "myv",
        "autonym" => "Эрзянь",
        "name" => "Erzya"
    ],
    "mzn" => [
        "code" => "mzn",
        "autonym" => "مَزِروني",
        "name" => "Mazanderani"
    ],
    "na" => [
        "code" => "na",
        "autonym" => "dorerin Naoero",
        "name" => "Nauru"
    ],
    "nah" => [
        "code" => "nah",
        "autonym" => "Nāhuatl",
        "name" => "Nāhuatl"
    ],
    "nap" => [
        "code" => "nap",
        "autonym" => "Nnapulitano",
        "name" => "Neapolitan"
    ],
    "nds" => [
        "code" => "nds",
        "autonym" => "Plattdüütsch",
        "name" => "Low German"
    ],
    "nds-nl" => [
        "code" => "nds-nl",
        "autonym" => "Nedersaksisch",
        "name" => "Low Saxon"
    ],
    "ne" => [
        "code" => "ne",
        "autonym" => "नेपाली",
        "name" => "Nepali"
    ],
    "new" => [
        "code" => "new",
        "autonym" => "नेपाल भाषा",
        "name" => "Newari"
    ],
    "ng" => [
        "code" => "ng",
        "autonym" => "Ndonga",
        "name" => "Ndonga"
    ],
    "nia" => [
        "code" => "nia",
        "autonym" => "Li Niha",
        "name" => "Nias"
    ],
    "nl" => [
        "code" => "nl",
        "autonym" => "Nederlands",
        "name" => "Dutch"
    ],
    "nn" => [
        "code" => "nn",
        "autonym" => "Nynorsk",
        "name" => "Norwegian Nynorsk"
    ],
    "no" => [
        "code" => "no",
        "autonym" => "Norsk",
        "name" => "Norwegian"
    ],
    "nov" => [
        "code" => "nov",
        "autonym" => "Novial",
        "name" => "Novial"
    ],
    "nqo" => [
        "code" => "nqo",
        "autonym" => "ߒߞߏ",
        "name" => "N’Ko"
    ],
    "nrm" => [
        "code" => "nrm",
        "autonym" => "Nouormand/Normaund",
        "name" => "Norman"
    ],
    "nso" => [
        "code" => "nso",
        "autonym" => "Sepedi",
        "name" => "Northern Sotho"
    ],
    "nv" => [
        "code" => "nv",
        "autonym" => "Diné bizaad",
        "name" => "Navajo"
    ],
    "ny" => [
        "code" => "ny",
        "autonym" => "Chichewa",
        "name" => "Nyanja"
    ],
    "oc" => [
        "code" => "oc",
        "autonym" => "Occitan",
        "name" => "Occitan"
    ],
    "olo" => [
        "code" => "olo",
        "autonym" => "Karjalan",
        "name" => "Livvi-Karelian"
    ],
    "om" => [
        "code" => "om",
        "autonym" => "Oromoo",
        "name" => "Oromo"
    ],
    "or" => [
        "code" => "or",
        "autonym" => "ଓଡ଼ିଆ",
        "name" => "Odia"
    ],
    "os" => [
        "code" => "os",
        "autonym" => "Иронау",
        "name" => "Ossetic"
    ],
    "pa" => [
        "code" => "pa",
        "autonym" => "ਪੰਜਾਬੀ",
        "name" => "Punjabi"
    ],
    "pag" => [
        "code" => "pag",
        "autonym" => "Pangasinan",
        "name" => "Pangasinan"
    ],
    "pam" => [
        "code" => "pam",
        "autonym" => "Kapampangan",
        "name" => "Pampanga"
    ],
    "pap" => [
        "code" => "pap",
        "autonym" => "Papiamentu",
        "name" => "Papiamento"
    ],
    "pcd" => [
        "code" => "pcd",
        "autonym" => "Picard",
        "name" => "Picard"
    ],
    "pdc" => [
        "code" => "pdc",
        "autonym" => "Deitsch",
        "name" => "Pennsylvania German"
    ],
    "pfl" => [
        "code" => "pfl",
        "autonym" => "Pälzisch",
        "name" => "Palatine German"
    ],
    "pi" => [
        "code" => "pi",
        "autonym" => "पाऴि",
        "name" => "Pali"
    ],
    "pih" => [
        "code" => "pih",
        "autonym" => "Norfuk",
        "name" => "Norfuk / Pitkern"
    ],
    "pl" => [
        "code" => "pl",
        "autonym" => "Polski",
        "name" => "Polish"
    ],
    "pms" => [
        "code" => "pms",
        "autonym" => "Piemontèis",
        "name" => "Piedmontese"
    ],
    "pnb" => [
        "code" => "pnb",
        "autonym" => "شاہ مکھی پنجابی",
        "name" => "Western Punjabi"
    ],
    "pnt" => [
        "code" => "pnt",
        "autonym" => "Ποντιακά",
        "name" => "Pontic"
    ],
    "ps" => [
        "code" => "ps",
        "autonym" => "پښتو",
        "name" => "Pashto"
    ],
    "pt" => [
        "code" => "pt",
        "autonym" => "Português",
        "name" => "Portuguese"
    ],
    "qu" => [
        "code" => "qu",
        "autonym" => "Runa Simi",
        "name" => "Quechua"
    ],
    "rm" => [
        "code" => "rm",
        "autonym" => "Rumantsch",
        "name" => "Romansh"
    ],
    "rmy" => [
        "code" => "rmy",
        "autonym" => "romani - रोमानी",
        "name" => "Vlax Romani"
    ],
    "rn" => [
        "code" => "rn",
        "autonym" => "Ikirundi",
        "name" => "Rundi"
    ],
    "ro" => [
        "code" => "ro",
        "autonym" => "Română",
        "name" => "Romanian"
    ],
    "roa-rup" => [
        "code" => "roa-rup",
        "autonym" => "Armãneashce",
        "name" => "Aromanian"
    ],
    "roa-tara" => [
        "code" => "roa-tara",
        "autonym" => "Tarandíne",
        "name" => "Tarantino"
    ],
    "ru" => [
        "code" => "ru",
        "autonym" => "Русский",
        "name" => "Russian"
    ],
    "rue" => [
        "code" => "rue",
        "autonym" => "Русиньскый",
        "name" => "Rusyn"
    ],
    "rw" => [
        "code" => "rw",
        "autonym" => "Ikinyarwanda",
        "name" => "Kinyarwanda"
    ],
    "sa" => [
        "code" => "sa",
        "autonym" => "संस्कृतम्",
        "name" => "Sanskrit"
    ],
    "sah" => [
        "code" => "sah",
        "autonym" => "Саха тыла",
        "name" => "Sakha"
    ],
    "sat" => [
        "code" => "sat",
        "autonym" => "ᱥᱟᱱᱛᱟᱲᱤ",
        "name" => "Santali"
    ],
    "sc" => [
        "code" => "sc",
        "autonym" => "Sardu",
        "name" => "Sardinian"
    ],
    "scn" => [
        "code" => "scn",
        "autonym" => "Sicilianu",
        "name" => "Sicilian"
    ],
    "sco" => [
        "code" => "sco",
        "autonym" => "Scots",
        "name" => "Scots"
    ],
    "sd" => [
        "code" => "sd",
        "autonym" => "سنڌي، سندھی ، सिन्ध",
        "name" => "Sindhi"
    ],
    "se" => [
        "code" => "se",
        "autonym" => "Sámegiella",
        "name" => "Northern Sami"
    ],
    "sg" => [
        "code" => "sg",
        "autonym" => "Sängö",
        "name" => "Sango"
    ],
    "sh" => [
        "code" => "sh",
        "autonym" => "Srpskohrvatski / Српскохрватски",
        "name" => "Serbo-Croatian"
    ],
    "shn" => [
        "code" => "shn",
        "autonym" => "လိၵ်ႈတႆး",
        "name" => "Shan"
    ],
    "si" => [
        "code" => "si",
        "autonym" => "සිංහල",
        "name" => "Sinhala"
    ],
    "simple" => [
        "code" => "simple",
        "autonym" => "Simple English",
        "name" => "Simple English"
    ],
    "sk" => [
        "code" => "sk",
        "autonym" => "Slovenčina",
        "name" => "Slovak"
    ],
    "skr" => [
        "code" => "skr",
        "autonym" => "سرائیکی",
        "name" => "Saraiki"
    ],
    "sl" => [
        "code" => "sl",
        "autonym" => "Slovenščina",
        "name" => "Slovenian"
    ],
    "sm" => [
        "code" => "sm",
        "autonym" => "Gagana Samoa",
        "name" => "Samoan"
    ],
    "smn" => [
        "code" => "smn",
        "autonym" => "Anarâškielâ",
        "name" => "Inari Sami"
    ],
    "sn" => [
        "code" => "sn",
        "autonym" => "chiShona",
        "name" => "Shona"
    ],
    "so" => [
        "code" => "so",
        "autonym" => "Soomaali",
        "name" => "Somali"
    ],
    "sq" => [
        "code" => "sq",
        "autonym" => "Shqip",
        "name" => "Albanian"
    ],
    "sr" => [
        "code" => "sr",
        "autonym" => "Српски / Srpski",
        "name" => "Serbian"
    ],
    "srn" => [
        "code" => "srn",
        "autonym" => "Sranantongo",
        "name" => "Sranan Tongo"
    ],
    "ss" => [
        "code" => "ss",
        "autonym" => "SiSwati",
        "name" => "Swati"
    ],
    "st" => [
        "code" => "st",
        "autonym" => "Sesotho",
        "name" => "Southern Sotho"
    ],
    "stq" => [
        "code" => "stq",
        "autonym" => "Seeltersk",
        "name" => "Saterland Frisian"
    ],
    "su" => [
        "code" => "su",
        "autonym" => "Basa Sunda",
        "name" => "Sundanese"
    ],
    "sv" => [
        "code" => "sv",
        "autonym" => "Svenska",
        "name" => "Swedish"
    ],
    "sw" => [
        "code" => "sw",
        "autonym" => "Kiswahili",
        "name" => "Swahili"
    ],
    "szl" => [
        "code" => "szl",
        "autonym" => "Ślůnski",
        "name" => "Silesian"
    ],
    "szy" => [
        "code" => "szy",
        "autonym" => "Sakizaya",
        "name" => "Sakizaya"
    ],
    "ta" => [
        "code" => "ta",
        "autonym" => "தமிழ்",
        "name" => "Tamil"
    ],
    "tay" => [
        "code" => "tay",
        "autonym" => "Tayal",
        "name" => "Tayal"
    ],
    "tcy" => [
        "code" => "tcy",
        "autonym" => "ತುಳು",
        "name" => "Tulu"
    ],
    "te" => [
        "code" => "te",
        "autonym" => "తెలుగు",
        "name" => "Telugu"
    ],
    "tet" => [
        "code" => "tet",
        "autonym" => "Tetun",
        "name" => "Tetum"
    ],
    "tg" => [
        "code" => "tg",
        "autonym" => "Тоҷикӣ",
        "name" => "Tajik"
    ],
    "th" => [
        "code" => "th",
        "autonym" => "ไทย",
        "name" => "Thai"
    ],
    "ti" => [
        "code" => "ti",
        "autonym" => "ትግርኛ",
        "name" => "Tigrinya"
    ],
    "tk" => [
        "code" => "tk",
        "autonym" => "Türkmen",
        "name" => "Turkmen"
    ],
    "tl" => [
        "code" => "tl",
        "autonym" => "Tagalog",
        "name" => "Tagalog"
    ],
    "tn" => [
        "code" => "tn",
        "autonym" => "Setswana",
        "name" => "Tswana"
    ],
    "to" => [
        "code" => "to",
        "autonym" => "faka Tonga",
        "name" => "Tongan"
    ],
    "tpi" => [
        "code" => "tpi",
        "autonym" => "Tok Pisin",
        "name" => "Tok Pisin"
    ],
    "tr" => [
        "code" => "tr",
        "autonym" => "Türkçe",
        "name" => "Turkish"
    ],
    "trv" => [
        "code" => "trv",
        "autonym" => "Taroko",
        "name" => "Taroko"
    ],
    "ts" => [
        "code" => "ts",
        "autonym" => "Xitsonga",
        "name" => "Tsonga"
    ],
    "tt" => [
        "code" => "tt",
        "autonym" => "Tatarça / Татарча",
        "name" => "Tatar"
    ],
    "tum" => [
        "code" => "tum",
        "autonym" => "chiTumbuka",
        "name" => "Tumbuka"
    ],
    "tw" => [
        "code" => "tw",
        "autonym" => "Twi",
        "name" => "Twi"
    ],
    "ty" => [
        "code" => "ty",
        "autonym" => "Reo Mā`ohi",
        "name" => "Tahitian"
    ],
    "tyv" => [
        "code" => "tyv",
        "autonym" => "Тыва",
        "name" => "Tuvinian"
    ],
    "udm" => [
        "code" => "udm",
        "autonym" => "Удмурт кыл",
        "name" => "Udmurt"
    ],
    "ug" => [
        "code" => "ug",
        "autonym" => "ئۇيغۇر تىلى",
        "name" => "Uyghur"
    ],
    "uk" => [
        "code" => "uk",
        "autonym" => "Українська",
        "name" => "Ukrainian"
    ],
    "ur" => [
        "code" => "ur",
        "autonym" => "اردو",
        "name" => "Urdu"
    ],
    "uz" => [
        "code" => "uz",
        "autonym" => "O‘zbek",
        "name" => "Uzbek"
    ],
    "ve" => [
        "code" => "ve",
        "autonym" => "Tshivenda",
        "name" => "Venda"
    ],
    "vec" => [
        "code" => "vec",
        "autonym" => "Vèneto",
        "name" => "Venetian"
    ],
    "vep" => [
        "code" => "vep",
        "autonym" => "Vepsän",
        "name" => "Veps"
    ],
    "vi" => [
        "code" => "vi",
        "autonym" => "Tiếng Việt",
        "name" => "Vietnamese"
    ],
    "vls" => [
        "code" => "vls",
        "autonym" => "West-Vlams",
        "name" => "West Flemish"
    ],
    "vo" => [
        "code" => "vo",
        "autonym" => "Volapük",
        "name" => "Volapük"
    ],
    "wa" => [
        "code" => "wa",
        "autonym" => "Walon",
        "name" => "Walloon"
    ],
    "war" => [
        "code" => "war",
        "autonym" => "Winaray",
        "name" => "Waray"
    ],
    "wo" => [
        "code" => "wo",
        "autonym" => "Wolof",
        "name" => "Wolof"
    ],
    "wuu" => [
        "code" => "wuu",
        "autonym" => "吴语",
        "name" => "Wu Chinese"
    ],
    "xal" => [
        "code" => "xal",
        "autonym" => "Хальмг",
        "name" => "Kalmyk"
    ],
    "xh" => [
        "code" => "xh",
        "autonym" => "isiXhosa",
        "name" => "Xhosa"
    ],
    "xmf" => [
        "code" => "xmf",
        "autonym" => "მარგალური",
        "name" => "Mingrelian"
    ],
    "yi" => [
        "code" => "yi",
        "autonym" => "ייִדיש",
        "name" => "Yiddish"
    ],
    "yo" => [
        "code" => "yo",
        "autonym" => "Yorùbá",
        "name" => "Yoruba"
    ],
    "za" => [
        "code" => "za",
        "autonym" => "Cuengh",
        "name" => "Zhuang"
    ],
    "zea" => [
        "code" => "zea",
        "autonym" => "Zeêuws",
        "name" => "Zeelandic"
    ],
    "zh" => [
        "code" => "zh",
        "autonym" => "中文",
        "name" => "Chinese"
    ],
    "zh-classical" => [
        "code" => "zh-classical",
        "autonym" => "古文 / 文言文",
        "name" => "Classical Chinese"
    ],
    "zh-min-nan" => [
        "code" => "zh-min-nan",
        "autonym" => "Bân-lâm-gú",
        "name" => "Chinese (Min Nan)"
    ],
    "zh-yue" => [
        "code" => "zh-yue",
        "autonym" => "粵語",
        "name" => "Cantonese"
    ],
    "zu" => [
        "code" => "zu",
        "autonym" => "isiZulu",
        "name" => "Zulu"
    ]
];

function test_print($s)
{
    if (print_te && gettype($s) == 'string') {
        echo "\n<br>\n$s";
    } elseif (print_te) {
        echo "\n<br>\n";
        print_r($s);
    }
}

function get_url_result_curl(string $url, array $params = null): string
{
    global $usr_agent;

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // curl_setopt($ch, CURLOPT_COOKIEJAR, "cookie.txt");
    // curl_setopt($ch, CURLOPT_COOKIEFILE, "cookie.txt");

    curl_setopt($ch, CURLOPT_USERAGENT, $usr_agent);

    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $output = curl_exec($ch);
    if ($output === FALSE) {
        echo ("<br>cURL Error: " . curl_error($ch) . "<br>$url");
    }

    curl_close($ch);

    return $output;
}

function get_names()
{
    $params  = [
        "action" => "query",
        "format" => "json",
        "meta" => "wbcontentlanguages",
        "formatversion" => "2",
        "wbclcontext" => "monolingualtext",
        "wbclprop" => "code|autonym|name"
    ];

    $url = "https://www.wikidata.org/w/api.php?" . http_build_query($params);

    $result = get_url_result_curl($url);

    $result = json_decode($result, true);

    return $result['query']['wbcontentlanguages'];
}
function get_langs_list()
{
    $url = "https://cxserver.wikimedia.org/v2/list/languagepairs";

    $pairs = get_url_result_curl($url);

    $results = json_decode($pairs, true);
    $source = $results['source'];
    $target = $results['target'];

    $results = array_merge($source, $target);
    $results = array_unique($results);

    sort($results);

    // del "simple" and "en"
    $results = array_diff($results, ['simple', 'en']);

    return $results;
};

function get_lang_names()
{
    global $lang_tables;

    return $lang_tables;
};

function get_lang_names_no()
{
    global $lang_tables;
    $pairs = get_langs_list();
    $names = get_names();

    $results = array();

    foreach ($pairs as $pair) {
        $data = ["code" => $pair, "autonym" => "", "name" => ""];

        $results[] = $names[$pair] ?? $lang_tables[$pair] ?? $data;
    };
    return $results;
};
