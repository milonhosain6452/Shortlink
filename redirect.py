<?php
$data = json_decode(file_get_contents("data.json"), true);
$code = trim($_GET["code"]);

if (!isset($data['links'][$code])) {
    echo "Invalid or expired link.";
    exit;
}

$data['links'][$code]['clicks'] += 1;
file_put_contents("data.json", json_encode($data, JSON_PRETTY_PRINT));

header("Location: " . $data['links'][$code]['url']);
exit;
?>
