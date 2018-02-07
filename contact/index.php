<?php
header("P3P: CP='UNI CUR OUR'");
//ini_set('display_errors', '1');
//error_reporting(0);
//error_reporting(E_ALL);
// --- 設定部 ------------------------------------------------------------------
// --- 必ず書き換える項目 ------------------------------------------------------
// --- メールの送信先 ----------------------------------------------------------
$mail_to = 's.matsuzaki@ababai.co.jp';
$return_path = '';
$subject = '【】お問い合わせを受け付けました';
$default_encode = 'UTF-8';

// --- 必要に応じて書き換える項目 ----------------------------------------------
// 送信完了ページを別ページにリダイレクトする場合はURLを書いてください。
// このスクリプトで送信完了ページを出力する場合は空欄です（デフォルト 空欄）
$redirect = '';

// --- プログラム部 ------------------------------------------------------------
// --- 初期化 ------------------------------------------------------------------
$prefArray = array('選択してください',
'北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県',
'東京都','神奈川県','埼玉県','千葉県','茨城県','栃木県','群馬県','山梨県',
'新潟県','長野県','富山県','石川県','福井県',
'愛知県','岐阜県','静岡県','三重県',
'大阪府','兵庫県','京都府','滋賀県','奈良県','和歌山県',
'鳥取県','島根県','岡山県','広島県','山口県',
'徳島県','香川県','愛媛県','高知県',
'福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県'
);

session_start();

// magic quotes
if (get_magic_quotes_gpc()) {
	foreach($_POST as $key => $val) {
		$_POST[$key] = stripslashes($val);
	}
}


$vars = array();
$errors = array();

if (isset($_POST['act']) && $_POST['act'] == 'confirm'){
	$vars =& $_POST;
	convertVars();
	validateVars();
	if (count($errors) > 0) {
		$view = 'input';
	} else {
		$_SESSION = $vars;
		$view = 'confirm';
	}

} else if (isset($_POST['act']) && $_POST['act'] == 'done') {
	$vars =& $_SESSION;
	if (($_POST['back_to_input'] == 1) || $_POST['ssid'] != session_id()) {
		$view = 'input';
	} else {
		validateVars();
		if (count($errors) > 0) {
			$view = 'input';
		} else {
					/** 
 		            * メール送信処理 
 		            * 　▼添付ファイルを付ける、送信先を複数にする等、カスタマイズする場合は下記ページを参考にしてください。 
 		            * 　https://github.com/Synchro/PHPMailer#a-simple-example 
 		            */
					
			// --- メール送信ライブラリを読み込み
 		    require_once(dirname(__FILE__) . DIRECTORY_SEPARATOR . 'lib' . DIRECTORY_SEPARATOR . 'PHPMailer' . DIRECTORY_SEPARATOR . 'PHPMailerAutoload.php');

			// --- 受付メール送信
			$mail = new PHPMailer();
			
			$mail->CharSet = $default_encode;
			$mail->setFrom($vars['email1']);
			$mail->addAddress($mail_to);
			if ($return_path) {
				$mail->addReplyTo($return_path); 
			}
			if (isset($_POST['copy'])) { 
 		    	$mail->addCC($_POST['copy']); 
 		    }
			$mail->addBCC('inquiry@ababai.co.jp'); 
 		    $mail->Subject = $subject; 
 		    $mail->Body = createBody();
 		    if ( ! $mail->send()) {
 		        die('メール送信に失敗しました。'); 
			}

			// --- 自動メール返信
			$mail = new PHPMailer();
			$mail->CharSet = $default_encode;
			$mail->setFrom($mail_to);
			$mail->addAddress($vars['email1']);
			
			if ($return_path) {
				$mail->addReplyTo($return_path); 
			}
			$mail->Subject = '【】お問い合わせを送信しました';
			$mail->Body = createBodyReturn();
			if ( ! $mail->send()) {
				die('メール送信に失敗しました。');
			}

			$_SESSION = array();
			if ( $redirect != '' ) {
				header( "Location: $redirect" );
				exit;
			} else {
				$view = 'done';
			}
		}
	}
} else {
	$view = 'input';
	$vars = $_SESSION;
}
//-------------------------------------------------------------------------------------------------------------includeフォームhtml
?>
<?php if ($view == 'input'):?>
	<?php include('inputForm.php')?>
<?php elseif($view == 'confirm'):?>
	<?php include('confirm.php')?>
<?php else:?>
	<?php include('complete.php')?>
<?php endif;?>
<?php
//-------------------------------------------------------------------------------------------------------------function群
/**
 * 入力値の変換
 */
function convertVars() {
	global $vars;
	global $default_encode;

	$vars['mail'] = mb_convert_kana($vars['mail'], "a", $default_encode);
}

function validateVars() {
	global $vars;
	global $errors;

		if (!validateNotEmpty('name')) {
		$errors['name'] = 'お名前が入力されていません';
	}
		if (!validateNotEmpty('hira')) {
		$errors['hira'] = 'ふりがなが入力されていません';
	}
		if (!validateNotEmpty('email1')) {
		$errors['email1'] = 'メールアドレスが入力されていません';
	}		


		if (!validateNotEmpty('how')) {
		$errors['how'] = 'ご希望の連絡方法が選択されていません';
	}


}




function _h($value) {
	global $default_encode;
	return htmlspecialchars($value, ENT_QUOTES, $default_encode);
}

/**
 * postで送られた値を出力
 * @param unknown_type $key
 */
function eh($key) {
	global $vars;
	global $default_encode;
	if (isset($vars[$key])) {
		echo htmlspecialchars($vars[$key], ENT_QUOTES, $default_encode);
	}
}

/**
 * checked出力
 * @param unknown_type $key
 * @param unknown_type $value
 */
function checked($key, $value) {
	global $vars;
	if (isset($vars[$key])) {
		if (is_array($vars[$key]) && in_array($value, $vars[$key])) {
			echo ' checked="checked"';
		} else if ($vars[$key] == $value) {
			echo ' checked="checked"';
		}
	}
}

/**
 * selected出力
 * @param unknown_type $key
 * @param unknown_type $value
 */
function selected($key, $value) {
	global $vars;
	if (isset($vars[$key]) && $vars[$key] == $value) {
		echo ' selected="selected"';
	}
}

/**
 * エラー出力
 * @param unknown_type $key
 */
function err($key) {
	global $errors;
	global $default_encode;
	if (isset($errors[$key])) {
		echo '<div class="error">' . htmlspecialchars($errors[$key], ENT_QUOTES, $default_encode) . '</div>';
	}
}


/**
 * 必須項目検証
 * @param string $key 項目キー
 */
function validateNotEmpty($key) {
	global $vars;
	if (empty($vars[$key])) {
		return false;
	}
	return true;
}

/**
 * メールアドレス検証
 * @param string $key 項目キー
 */
function validateEmail($key) {
	global $vars;
	$email = isset($vars[$key])? $vars[$key]: '';
	if (preg_match("/^([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+\.([a-zA-Z0-9\._-]+)+$/", $email)) {
		return true;
	}
	return false;
}

/**
 * カタカナ検証
 * @param string $key
 */
function validateKana($key) {
	global $vars;
	global $default_encode;
	switch($default_encode){
		case 'EUC-JP':
		case 'euc-jp':
			$conv = "/^(\xa5[\xa1-\xf6]|\xa1[\xb3\xb4\xbc])+$/";
			break;
		case 'utf-8':
		case 'UTF-8':
			$conv = "/^[ァ-ヶー　]+$/u";
	}
	$value = isset($vars[$key])? $vars[$key]: '';
	if(preg_match($conv,$value)){
		return true;
	}
	return false;
}
/**
 * ひらがな検証
 * @param string $key
 */
function validateHira($key) {
	global $vars;
	global $default_encode;
	switch($default_encode){
		case 'EUC-JP':
		case 'euc-jp':
			$conv = "/^(\xa5[\xa1-\xf6]|\xa1[\xb3\xb4\xbc])+$/";
			break;
		case 'utf-8':
		case 'UTF-8':
			$conv = "/^[ぁ-ゞー　]+$/u";
	}
	$value = isset($vars[$key])? $vars[$key]: '';
	if(preg_match($conv,$value)){
		return true;
	}
	return false;
}

/**
 * 郵便番号検証
 * @param string $key
 */
function validateZip($key) {
	global $vars;
	$value = isset($vars[$key])? $vars[$key]: '';
	if (preg_match("/^\d{3}\-\d{4}$/", $value)) {
		return true;
	}
	return false;
}

/**
 * 電話番号検証
 * @param string $key
 */
function validateTel($key) {
	global $vars;
	$value = isset($vars[$key])? $vars[$key]: '';
	if (preg_match("/^\d{2,5}-?\d{1,4}-?\d{2,4}$/", $value)) {
		return true;
	}
	return false;
}


/**
 * メール本文を生成
 */
function createBody() {
	global $vars;

	$body = "


-----------------------------------------

■ お名前・・・{$vars['name']} ({$vars['hira']})

■ メールアドレス・・・{$vars['email1']}
■ お電話番号・・・{$vars['tel']}


――お問合わせ本文――――――――――――――――――――――――――

{$vars['body']}

―――――――――――――――――――――――――――――――――――
";

	return $body;
}
function createBodyReturn(){
  $body = createBody();
  $body = "

本文


―――――――――――――――――――――――――――――――――――
".$body."


==========================================

署名

==========================================



";

return $body;
}

?>