<?php
/*
 * Kontaktformular von Gandert. Webdesign
 * Läuft auf jedem Hosting mit PHP und mail() (z. B. Hostinger).
 *
 * VOR DEM LIVEGANG: Empfänger und Absender unten eintragen.
 * Der Absender muss eine Adresse der eigenen Domain sein, sonst landen
 * die Mails im Spam.
 */

$EMPFAENGER = '[E-MAIL]';
$ABSENDER   = 'formular@[DOMAIN]';

$ist_ajax = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;

function antworten($ok, $fehler = '')
{
    global $ist_ajax;
    if ($ist_ajax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'fehler' => $fehler]);
    } else {
        header('Location: ' . ($ok ? 'danke.html' : 'index.html#kontakt'), true, 303);
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    antworten(false, 'Ungültige Anfrage.');
}

// Honigtopf: Menschen sehen dieses Feld nicht, Bots füllen es aus.
if (!empty($_POST['website'])) {
    antworten(true);
}

function feld($name, $max)
{
    $wert = isset($_POST[$name]) ? trim((string) $_POST[$name]) : '';
    // Zeilenumbrüche in einzeiligen Feldern entfernen (Schutz gegen Header-Injection)
    if ($name !== 'nachricht') {
        $wert = preg_replace('/[\r\n]+/', ' ', $wert);
    }
    return mb_substr($wert, 0, $max);
}

$name        = feld('name', 120);
$betrieb     = feld('betrieb', 160);
$email       = feld('email', 200);
$telefon     = feld('telefon', 60);
$paket       = feld('paket', 60);
$nachricht   = feld('nachricht', 5000);
$einwilligung = isset($_POST['einwilligung']) && $_POST['einwilligung'] === 'ja';

if ($name === '' || $nachricht === '') {
    antworten(false, 'Bitte füllen Sie Name und Nachricht aus.');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    antworten(false, 'Bitte geben Sie eine gültige E-Mail-Adresse an.');
}
if (!$einwilligung) {
    antworten(false, 'Bitte bestätigen Sie die Einwilligung zur Datenverarbeitung.');
}

$betreff = 'Neue Anfrage über die Website: ' . $name;
$text = "Neue Anfrage über das Kontaktformular\n\n"
      . "Name:     $name\n"
      . "Betrieb:  " . ($betrieb !== '' ? $betrieb : '–') . "\n"
      . "E-Mail:   $email\n"
      . "Telefon:  " . ($telefon !== '' ? $telefon : '–') . "\n"
      . "Interesse: $paket\n\n"
      . "Nachricht:\n$nachricht\n\n"
      . "Einwilligung zur Datenverarbeitung: ja (" . date('d.m.Y H:i') . ")\n";

$kopf = [
    'From: Gandert. Website <' . $ABSENDER . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];

$gesendet = mail(
    $EMPFAENGER,
    '=?UTF-8?B?' . base64_encode($betreff) . '?=',
    $text,
    implode("\r\n", $kopf)
);

antworten($gesendet, 'Die Anfrage konnte nicht gesendet werden. Bitte schreiben Sie mir direkt eine E-Mail.');
