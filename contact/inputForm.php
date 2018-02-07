<!DOCTYPE html>
<html lang="ja">
<head></head>

<body>

<form action="index.php?" method="post">
<input type="hidden" name="act" value="confirm">
<table id="mailform" class="contact_form mb55">

<tr>
<th class="special">資料請求の有無 <span class="red">【必須】</span></th>
<td>
<label><input type="radio" value="有り" name="document" <?php checked('document', '有り')?> />有り</label>
<label><input type="radio" value="無し" name="document" <?php checked('document', '無し')?> />無し</label>
<span class="red"><?php err('document')?></span>
</td>
</tr>

<tr>
<th>お名前 <span class="red">【必須】</span> </th>
<td><input type="text" class="textform01" name="name" value="<?php eh('name')?>"><span class="red"><?php err('name')?></span></td>
</tr>

<tr>
<th>ふりがな <span class="red">【必須】</span></th>
<td><input type="text" class="textform01" name="hira" value="<?php eh('hira')?>"><span class="red"><?php err('hira')?></span></td>
</tr>

<tr>
<th>メールアドレス <span class="red">【必須】</span> </th>
<td><input type="email" class="textform01" name="email1" value="<?php eh('email1')?>"><span class="red"><?php err('email1')?></span></td>
</tr>

<tr>
<th>郵便番号 </th>
<td><input type="text" name="zip" value="<?php eh('zip')?>" onkeyup="AjaxZip3.zip2addr(this,'','address','address');"></td>
</tr>

<tr>
<th>住所</th>
<td><input type="text" class="textform01" name="address" value="<?php eh('address')?>"><br><div class="rei"></div></td>
</tr>

<tr>
<th>お電話番号 </th>
<td><input type="tel" class="textform01" name="tel" value="<?php eh('tel')?>"></td>
</tr>

<tr>
<th>ご希望の連絡方法 <span class="red">【必須】</span></th>
<td>
<label><input type="radio" value="メール" name="how"<?php checked('how', 'メール')?>>メール</label>
<label><input type="radio" value="電話" name="how"<?php checked('how', '電話')?>>電話</label>
<label><input type="radio" value="どちらでも" name="how"<?php checked('how', 'どちらでも')?>>どちらでも</label><?php err('how')?></td>
</tr>

<tr>
<th class="bdb">お問い合わせ内容</th>
<td><textarea name="body" rows="15" class="maileform" value="<?php eh('body')?>"><?php eh('body')?></textarea><br><span class="red"><?php err('body')?></span></td>
</tr>
</table>

<p class="ta_c mb40"><input class="contanct_btn" type="image" id="contact-confirmation" value="入力内容を確認する" alt="入力内容を確認する" src="../images/contact/btn_index.jpg"></p>
</form>


</body>
</html>