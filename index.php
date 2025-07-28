<?php
$filename = 'data.json';
if (!file_exists($filename)) {
    file_put_contents($filename, json_encode([
        'links' => [],
        'generated_count' => 0
    ]));
}

$data = json_decode(file_get_contents($filename), true);
$total_clicks = 0;

foreach ($data['links'] as $link) {
    $total_clicks += $link['clicks'];
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Shortlink Stats</title>
</head>
<body>
    <h1>Welcome to Shortlink Service</h1>
    <p>Total shortlinks: <?= $data['generated_count'] ?></p>
    <p>Total clicks: <?= $total_clicks ?></p>
</body>
</html>
