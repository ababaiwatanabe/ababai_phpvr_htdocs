<?php //エラー表示切り替え　非表示：0　表示：1
 ini_set('display_errors', 0); ?>
<?php
/*サイトurlを取得：吐き出しは<?php echo siteURL; ?>*/
//define (siteURL, ('http://ababai.net/test/html'));
define (siteURL, (empty($_SERVER['HTTPS']) ? 'http://' : 'https://').$_SERVER['HTTP_HOST']);
/*ページurlを取得：吐き出しは<?php echo pageURL; ?>*/
define (pageURL, (empty($_SERVER['HTTPS']) ? 'http://' : 'https://').$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);
?>
