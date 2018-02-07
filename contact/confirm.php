<!DOCTYPE html>
<html lang="ja">
<head></head>


<body>


<form action="index.php" method="post">
<input type="hidden"name="act" value="done">
<input type="hidden" name="ssid" value="<?php echo _h(session_id())?>">
<table id="mailform" class="contact_form mb55">
<tr>
<th class="special">資料請求の有無 <span class="red">【必須】</span></th>
<td><?php eh('document')?></td>
</tr>
<tr><th>お名前 </th><td><?php eh('name')?></td></tr>
<tr><th>ふりがな</th><td><?php eh('hira')?></td></tr>
<tr><th>メールアドレス</th><td><?php eh('email1')?></td></tr>
<tr><th>郵便番号</th><td><?php eh('zip')?></td></tr>
<tr><th>住所</th><td><?php eh('address')?></td></tr>
<tr><th>お電話番号</th><td><?php eh('tel')?></td></tr>
<tr><th>ご希望の連絡方法</th><td><?php eh('how')?></td></tr>
<tr><th class="bdb">お問い合わせ内容</th><td><?php eh('body')?></td></tr>
</table>


<input type="hidden" name="back_to_input" id="back_to_input" value="">
<div class="clearfix btn-Box mb40">
<p class="fl_l"><input type="image" id="contact-histryback" value="入力画面に戻る" src="../images/contact/btn_back.jpg" onclick="document.getElementById('back_to_input').value=1"></p>
<p class="fl_r"><input type="image" value="送信" src="../images/contact/btn_send.jpg" id="contact-complete" onclick="javascript:ga('send', 'pageview', {'page': '/complete/', 'title': 'Contact Completion'});"></p>
</div>


</form>
</body>
</html>