#!/usr/bin/perl -w

# ���ޤ��ʤ�
$| = 1;

# �⥸�塼���ɤ߹���
use strict;
use warnings;
use CGI;

require "./share.pl";

# ����
my $ScriptTitle     = "ABABAI �����ƥ��������";
my $ScriptVersion   = "11.05.26";

# �С������
# 09.09.18  ¨������

###############################################################################
# �������
my $Password    = "ababai";                     # �ѥ����
my @Menus		=(	
	"./demo.cgi",		"�ǥ�",							# URL�������ȥ�
);
###############################################################################

# �����ꥪ�֥������Ⱥ���
my $query = new CGI;

# ��˥塼�ǡ�������
my $MenuCount= (1+$#Menus)/2;
my @MenuURL		= ();
my @MenuName	= ();
for( my $i=0 ; $i<$MenuCount ; $i++ ){
	push( @MenuURL , $Menus[$i*2+0] );
	push( @MenuName , $Menus[$i*2+1] );
}

# ��ǽʬ��
if( &ip_ok() ){
    # ��������
    if( $query->param("mode") eq "exit" ){      &Logout();  }
    # ɽ��
    else{                                       &List();    }
}else{
    if( !$query->param("password") ){
        # ���������
        &Login();
    }elsif( $query->param("password") ne $Password ){
        # ��������
        &LoginError();
    }else{
        # ����������
        &LoginSuccess();
    }
}

exit;


###############################################################################
### ����� ####################################################################
###############################################################################

# ������
sub Login{
    &PrintHeader();
    &PrintLogin("");
    &PrintFooter();
}

# ��������
sub LoginError{
    &PrintHeader();
    &PrintLogin("ǧ�ڤ˼��Ԥ��ޤ������ѥ���ɤ�⤦�������Ϥ��Ʋ�������");
    &PrintFooter();
}

# ����������
sub LoginSuccess{
    &SaveIP();
    &PrintHeader();
    &PrintList();
    &PrintFooter();
}

###############################################################################
### ��ǽ���� ##################################################################
###############################################################################

# ��������
sub Logout{
    &PrintHeader();
    &DelIP();
    &PrintLogin("�������Ȥ��ޤ�����");
    &PrintFooter();
}

# ����ɽ��
sub List{
    &PrintHeader();
    &PrintList();
    &PrintFooter();
}

###############################################################################
### ɽ����ʬ ##################################################################
###############################################################################

# �����귿ʸ
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

# ��λ�귿ʸ
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

# ���������
sub PrintLogin{
    print <<END_OF_HTML;
    <form action="./index.cgi" method="post" id="login">
        <input type="text" name="password" id="password" value="">
        <input type="submit" value="������" class="btn" id="btn">
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

# ����ɽ���ʤ���
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
        <div class="cmd" onclick="logout();"><img src="./images/icon_exit.png" alt=""> ��������</div>
    </div>
    
END_OF_HTML
    
}

