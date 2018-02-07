#!/usr/bin/perl -w

# おまじない
$| = 1;

# モジュール読み込み
use strict;
use warnings;
use CGI;

require "./share.pl";

# 情報
my $ScriptTitle     = "ABABAI システム管理画面";
my $ScriptVersion   = "11.05.26";

# バージョン
# 09.09.18  即日誕生

###############################################################################
# 初期設定
my $Password    = "ababai";                     # パスワード
my @Menus		=(	
	"./demo.cgi",		"デモ",							# URL、タイトル
);
###############################################################################

# クエリオブジェクト作成
my $query = new CGI;

# メニューデータ処理
my $MenuCount= (1+$#Menus)/2;
my @MenuURL		= ();
my @MenuName	= ();
for( my $i=0 ; $i<$MenuCount ; $i++ ){
	push( @MenuURL , $Menus[$i*2+0] );
	push( @MenuName , $Menus[$i*2+1] );
}

# 機能分岐
if( &ip_ok() ){
    # ログアウト
    if( $query->param("mode") eq "exit" ){      &Logout();  }
    # 表示
    else{                                       &List();    }
}else{
    if( !$query->param("password") ){
        # ログイン画面
        &Login();
    }elsif( $query->param("password") ne $Password ){
        # ログイン失敗
        &LoginError();
    }else{
        # ログイン成功
        &LoginSuccess();
    }
}

exit;


###############################################################################
### 入り口 ####################################################################
###############################################################################

# ログイン
sub Login{
    &PrintHeader();
    &PrintLogin("");
    &PrintFooter();
}

# ログイン失敗
sub LoginError{
    &PrintHeader();
    &PrintLogin("認証に失敗しました。パスワードをもう一度入力して下さい。");
    &PrintFooter();
}

# ログイン成功
sub LoginSuccess{
    &SaveIP();
    &PrintHeader();
    &PrintList();
    &PrintFooter();
}

###############################################################################
### 機能たち ##################################################################
###############################################################################

# ログアウト
sub Logout{
    &PrintHeader();
    &DelIP();
    &PrintLogin("ログアウトしました。");
    &PrintFooter();
}

# 一覧表示
sub List{
    &PrintHeader();
    &PrintList();
    &PrintFooter();
}

###############################################################################
### 表示気分 ##################################################################
###############################################################################

# 開始定型文
sub PrintHeader{
    print "Content-type: text/html\n";
	print "Pragma: no-cache", "\n\n";
    print <<END_OF_HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html lang="ja">

<head>
    <meta http-equiv="content-type" content="text/html; charset=euc-jp">
    <meta http-equiv="content-language" content="ja">
    <meta http-equiv="content-style-type" content="text/css">
    <meta http-equiv="content-script-type" content="text/javascript">
    <link rel="stylesheet" href="./share.css" type="text/css">
    <script src="./share.js"></script>
    
    <title>$ScriptTitle</title>
    
</head>

<body>
<div id="whole">
    <hr>
END_OF_HTML
}

###############################################################################

# 終了定型文
sub PrintFooter{
    print <<END_OF_HTML;
    <hr>
    <address>$ScriptTitle ver $ScriptVersion</address>
</div>

<form action="./index.cgi" method="post" name="sender" id="sender" style="display:none;"></form>

</body>

</html>
END_OF_HTML
}

###############################################################################

# ログイン画面
sub PrintLogin{
    print <<END_OF_HTML;
    <form action="./index.cgi" method="post" id="login">
        <input type="text" name="password" id="password" value="">
        <input type="submit" value="ログイン" class="btn" id="btn">
    </form>
END_OF_HTML
    my $error_message = shift;
    if( $error_message ){
        print <<END_OF_HTML;
    <p class="error_message">$error_message</p>
END_OF_HTML
    }
}

###############################################################################

# 一覧表示ながい
sub PrintList{
    
    print <<END_OF_HTML;
    
	<table>
END_OF_HTML
	for( my $i=0 ; $i<$MenuCount ; $i++ ){
		my $url = $MenuURL[$i];
		my $name = $MenuName[$i];
		print <<END_OF_HTML;
		<tr><td><div class="cmd" onclick="move('$url');">$name &gt;&gt;</td></tr>
END_OF_HTML
	}
    print <<END_OF_HTML;
	</table>
    
    <div align="right">
        <div class="cmd" onclick="logout();"><img src="./images/icon_exit.png" alt=""> ログアウト</div>
    </div>
    
END_OF_HTML
    
}

