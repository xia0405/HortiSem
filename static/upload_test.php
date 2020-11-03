<?php
header("Access-Control-Allow-Origin: *");

$success=false;
$size = 0;
$name = '[upload failed]';

if (!empty($_FILES["file"])) {
    $name = $_FILES["file"]["name"];
    $size = filesize($_FILES["file"]["tmp_name"]);
    if (!empty($size)) {
        $success=true;
    }
}

echo json_encode([
    'filename'=>$name,
    'file_size_in_bytes'=>$size
]);
