<?php
$filename = 'data.json';
if (!file_exists($filename)) {
    header("Location: https://google.com");
    exit;
}

$data = json_decode(file_get_contents($filename), true);

if (isset($_GET['r'])) {
    $code = $_GET['r'];
    foreach ($data['links'] as &$link) {
        if ($link['code'] === $code) {
            $link['clicks'] += 1;
            file_put_contents($filename, json_encode($data, JSON_PRETTY_PRINT));
            header("Location: " . $link['url']);
            exit;
        }
    }
}

header("Location: https://google.com");
?>
