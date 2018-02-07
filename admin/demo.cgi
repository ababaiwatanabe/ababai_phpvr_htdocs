#!/usr/bin/perl -w

# ���ޤ��ʤ�
$| = 1;

# �⥸�塼���ɤ߹���
use strict;
use warnings;
use CGI;
use Encode;
use File::Copy;
use File::Basename;
use HTML::Template;
use Image::Magick;

require "./share.pl";

# ����
my $ScriptTitle		= "ABABAI �ǡ����١������������ƥ�";
my $ScriptVersion	= "10.04.20";

# �С������
# 09.07.16	����
# 09.07.30	�ܺ�html�������� ¸��̵ͭʬ������
# 09.08.03	�����������̥ե����벽 �ѥ�᡼���������Ϥ�층��
# 09.08.06	��������å���̵���� �����ǧɽ��
# 09.09.28	���������魯�줿
# 09.12.03	���Ϲ������꤬�ʤ󤫼�ͳ�ˤʤä� ����ʸ���к�
# 09.12.09	����ɽ�������������������ڤ���Ȥ��ǤϤʤ�����˼����ꥵ����
# 09.12.10	�ե����륵����ɽ����ǽ���롼�ײ��ɽ����ǽ
# 09.12.18	���쥯�Ȼ��Ѳġ���������������äȼ�ͳ����������ջ��������
# 09.12.24	�����å��ܥå����ҤȤޤȤᲽ�����ѥ졼���ʲ�
# 10.01.05	�������̤��¤��ؤ���ñ����ɽ���ե��륿��Ĥ��������Σɣġ����Σɣ�
# 10.02.01	ʣ���ʥƥ����Ⱥ�ä���
# 10.04.12	�ե�����Ȳ����ν��������ؤ���ǽ
# 10.04.20	jcode.pm����encode.pm��
# ��&rarr;	�������̿ʲ�
#		��ɽ�����Ĵ���ȥڡ����ڤ��ؤ�
#		����祽���ȡ�ID���������
#		�����Խ�
#		��checkbox��select��������
#		�ǡ����ե����뼫ư�Хå����å�
#		���������������ɤ��줤�˽�ľ������

###############################################################################
# �������
#�������ܺ٥ե������ȥե����
#��ȥե�����˼�ư��������ǡ����ե����
#�����ƥ�ץ�ե�����̾
#�����ե�����̾
#�ܺ٥ƥ�ץ�ե�����̾
#�ܺ٥ե�����̾

#----------------------------------------------PC�ѥ���ǥå�������----------------------------------------------
my $IndexHTML	= "../index.php";				# �������륤��ǥå����ե�����̾
my $IndexTMPL	= "../demo_tmpl.php";			# ����ǥå����ƥ�ץ졼�ȥե�����̾
my $IndexAnchor	= "demo_body";						# ����ǥå��������ᤸ�뤷
my $IndexMax	= 3;							# ����ǥå������������

#----------------------------------------------PC���Ǥ��Ф�2����----------------------------------------------
my $IndexHTML2	= "../demo/index.php";				# �������륤��ǥå����ե�����̾
my $IndexTMPL2	= "../demo/demo_tmpl.php";			# ����ǥå����ƥ�ץ졼�ȥե�����̾
my $IndexAnchor2	= "demo_body_002";						# ����ǥå��������ᤸ�뤷
my $IndexMax2	= 6;							# ����ǥå������������

#----------------------------------------------SP�ѥ���ǥå�������----------------------------------------------
my $IndexSPHTML	= "../mob/index.php";				# �������륤��ǥå����ե�����̾
my $IndexSPTMPL	= "../mob/demo_tmpl.php";			# ����ǥå����ƥ�ץ졼�ȥե�����̾
my $IndexSPAnchor	= "demo";						# ����ǥå��������ᤸ�뤷
my $IndexSPMax	= 1;							# ����ǥå������������

#--------------------------------------------------PC�Ѱ�������--------------------------------------------------
my $ListHTML	= "../demo/index.php";			# ������������ե�����̾
my $ListTMPL	= "../demo/index_tmpl.php";	# �����ƥ�ץ졼�ȥե�����̾
my $ListMax		= 9999;							# �������������

#--------------------------------------------------SP�Ѱ�������--------------------------------------------------
my $ListSPHTML	= "../mob/demo/index.php";			# ������������ե�����̾
my $ListSPTMPL	= "../mob/demo/index_tmpl.php";	# �����ƥ�ץ졼�ȥե�����̾
my $ListSPMax		= 9999;							# �������������

#--------------------------------------------------PC�Ѿܺ�����--------------------------------------------------
my $DetailHTML_PRE	= "../demo/detail";					# ��������ܺ٥ե�����̾��������
my $DetailHTML_PST	= ".php";					# ��������ܺ٥ե�����̾������
my $DetailTMPL	= "../demo/detail_tmpl.php";		# �ܺ٥ƥ�ץ졼�ȥե�����̾

#--------------------------------------------------SP�Ѿܺ�����--------------------------------------------------
my $DetailSPHTML_PRE	= "../mob/demo/detail";					# ��������ܺ٥ե�����̾��������
my $DetailSPHTML_PST	= ".php";					# ��������ܺ٥ե�����̾������
my $DetailSPTMPL	= "../mob/demo/detail_tmpl.php";		# �ܺ٥ƥ�ץ졼�ȥե�����̾

#--------------------------------------------------�ե������ѥѥ�����--------------------------------------------------
my $FilePath	= "./uploads/";							# ��������У��ѥե����뤫�鸫�����åץ��ɥե�����ؤ����Хѥ�
my $FilePathSP	= "../../demo/uploads/";							# �������륹�ޥ��ѥե����뤫�鸫�����åץ��ɥե�����ؤ����Хѥ�
my $FileSavePath= "../demo/uploads/";					# ���Υ�����ץȤ��鸫�����åץ��ɥե�������¸��
my $DataFilename= "./demo.txt";		# ���Υ�����ץȤ��鸫���ǡ�����¸�ե�����̾


my $DispTrg		= -1;							# ����ɽ������� ɽ���ե饰���إѥ�᡼���ֹ�	�ޥ��ʥ�������
my $DateJoint	= "/";						# ��ư�������դĤʤ�����
my $GoogleMapTrg= -1;							# ��������ޥå��ֹ�	�ޥ��ʥ�������
my $GenreSort	= 0;							# �����륽����
my @Genre		=(								# ������̾
	"�����룱"
	);
my @Param		=(
	# �ѥ�᡼��̾,			ñ��,	���ϻ���ս�,	��������ɽ��,	�����뤴�Ȼ��Ѳ��Բ�,	���ϥ�����,���֥ѥ�᡼��
	"separator","",
	"�ᥤ�����",			"",		"",			1,		1,		"photo",650,670,354,236,
	"����",				"",		"",			1,		1,		"date",
	"������������",			"",		"",		1,		1,			"select",2,"on","off",
	"�ϰ�",				"",		"�㡧������������",	1,		1,		"text",
	"������̾",			"",		"�㡧A��",		1,		1,		"text",
	"�����ȥ�",			"",		"",			1,		1,		"text",
	"������ʸ",			"",		"",			0,		1,		"wysiwyg",
	"��Ϣ����(PDF)",		"",		"",		0,		1,			"file",
	"̵�����̲񥢥�����",		"",		"",		1,		1,			"checkbox",1,'��',
	"�Ͽޤ�������",		"",		"",			0,		1,		"gmaps",
	"�����꡼",			"",		"",			0,		1,		"photos",
	"�����꡼�ʥ���ץ�����դ���",			"",		"",			0,		1,		"photos_with_comment",650,670,354,236,
	);


###############################################################################
# ����ޤ�������ʤ��Ƥ⤤���������
my $BackToMenu	= "./index.cgi";						# �����

###############################################################################

# �ѥ�᡼����,�ѿ��ִ�
my $GnrCount= (1+$#Genre);
my $PrmCount= 0;
my @PrmName = ();
my @PrmUnit = ();
my @PrmNotice = ();
my @PrmDisp = ();
my @PrmEnable = ();
my @PrmType = ();
my @PrmSub = ();
my @Separator = ();
my @SepText = ();
my @PrmMulti = ();
my $SepCount = 0;
while( @Param ){
	$SepCount++;
	my $name = shift(@Param);
	# �Խ������ѥ��ѥ졼��
	if( $name eq "separator" ){
		push( @Separator , $SepCount );
		push( @SepText , shift(@Param) );
		$SepCount = -1;
		next;
	}
	push( @PrmName , $name );
	push( @PrmUnit , shift(@Param) );
	push( @PrmNotice , shift(@Param) );
	push( @PrmDisp , shift(@Param) );
	for( my $j=0 ; $j<$GnrCount ; $j++ ){
		push( @{$PrmEnable[$PrmCount]} , shift(@Param) );
	}
	my $type =  shift(@Param);
	push( @PrmType , $type );
	# ¿�ʥƥ����Ȥ���̾����
	if( $type =~ /(texts_set)/i ){
		my $max = shift(@Param)*2;
		for( my $i=0 ; $i<$max ; $i++ ){
			push( @{$PrmSub[$PrmCount]} , shift(@Param) );
		}
	}
	# �����ϥ���������
	if( $type =~ /(photo)/i ){
		push( @{$PrmSub[$PrmCount]} , shift(@Param) );
		push( @{$PrmSub[$PrmCount]} , shift(@Param) );
		push( @{$PrmSub[$PrmCount]} , shift(@Param) );
		push( @{$PrmSub[$PrmCount]} , shift(@Param) );
	}
	# �����å��ȥ��쥯�ȤϹ���̾
	if( $type =~ /(select)/i or $type =~ /(checkbox)/i ){
		my $max = shift(@Param);
		for( my $i=0 ; $i<$max ; $i++ ){
			push( @{$PrmSub[$PrmCount]} , shift(@Param) );
		}
	}
	$PrmCount++;
}

# �����ꥪ�֥������Ⱥ���
my $query = new CGI;

# ��ǽʬ��
if( &ip_ok() ){
	# ������
	if( $query->param("mode") eq "sort" ){		&Sort();	}
	# ȿ��
	elsif( $query->param("mode") eq "update" ){	&Update();	}
	# ��¸
	elsif( $query->param("mode") eq "apply" ){	&Apply();	}
	# �Խ�
	elsif( $query->param("mode") eq "edit" ){	&Edit();	}
	# �ɲ�
	elsif( $query->param("mode") eq "add" ){	&Add(); }
	# ���
	elsif( $query->param("mode") eq "del" ){	&Del(); }
	# ɽ��
	else{										&List();	}
}else{
	print "Location: $BackToMenu\n\n";
}

exit;


##############################################################################################################################################################
### ��ǽ���� #################################################################################################################################################
##############################################################################################################################################################

# ȿ��
sub Update{
	&UpdateTmpl();
	&PrintHeader();
	&PrintList("�����Ȥ�ȿ�Ǥ��ޤ�����");
	&PrintFooter();
}

# ����ɽ��
sub List{
	&PrintHeader();
	&PrintList();
	&PrintFooter();
}

# ��¸
sub Apply{
	&SaveLine();
	&PrintHeader();
	&PrintList("�ǡ�������¸���ޤ�����");
	&PrintFooter();
}

# �Խ�
sub Edit{
	&PrintHeader();
	&PrintEdit( $query->param("line") );
	&PrintFooter();
}

# �ɲ�
sub Add{
	&AddLine();
	&PrintHeader();
	&PrintList("��Ƭ��1�ԥǡ������ɲä��ޤ�����");
	&PrintFooter();
}


# ���
sub Del{
	&DeleteLine( $query->param("line") );
	&PrintHeader();
	&PrintList("�ǡ�����1�Ժ�����ޤ�����");
	&PrintFooter();
}

# ������
sub Sort{
	&SortList( $query->param("line") );
	&PrintHeader();
	&PrintList("�ǡ����ν������¸���ޤ�����");
	&PrintFooter();
}


##############################################################################################################################################################
### ɽ����ʬ #################################################################################################################################################
##############################################################################################################################################################

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
	<script type="text/javascript" src="./share.js"></script>
	
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
</body>

</html>
END_OF_HTML
}

##############################################################################################################################################################

# ����ɽ���ʤ���
sub PrintListPanel{
	print <<END_OF_HTML;

	<script type="text/javascript" src="./jquery-1.3.2.min.js"></script>
	<script type="text/javascript" src="./jquery.tablednd_0_5.js"></script>


	<div style="float:left">
		<div class="cmd" onclick="add();"><img src="./images/icon_add.png" alt=""> ����</div>
		<div class="cmd" onclick="sort('list');"><img src="./images/icon_apply.png" alt=""> �������¸</div>
		<div class="cmd" onclick="update();"><img src="./images/icon_update.png" alt=""> �����Ȥ�ȿ��</div>
		<div class="cmd" onclick="window.open('$ListHTML');"><img src="./images/icon_check.png" alt=""> �����Ȥ��ǧ</div>
	</div>
END_OF_HTML
}
sub PrintListHeader{
	print "<thead><tr class=\"nodrop nodrag\"><th>ID</th>\n";
	
	# ������
	if( 1<$GnrCount ){
		print "<th>����</th>\n";
	}
	# �ѥ�᡼��
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		if( $PrmDisp[$i] != 0 ){
			print "<th>$PrmName[$i]</th>\n";
		}
	}
	# ���ܥ���
	print "<th width=\"20\">��<br>��</th>";
	print "<th width=\"20\">��<br>��</th>";
	
	print "</tr></thead><tbody>\n";
}
sub PrintList{
	
	# ��å�����
	my $message = shift;
	if( $message ne "" ){
		print "<p class=\"error_message\">$message</p>\n";
	}
	
	my @lines = &GetLines( $DataFilename );
	
	# �����ܥ���
	&PrintListPanel();
	
	# �إå�����
	print <<END_OF_HTML;
	<div align="right">
		������<input style="width:20em;" type="text" onchange="search('list',this.value);">
	</div>
END_OF_HTML
	print "<table id=\"list\">";
	&PrintListHeader();
	
	my $i=0;
	foreach my $line ( @lines ){
		my %data = &LineToHash( $line );
		
		# ��Ƭ
		print "<tr id=\"line".$i."\"><td>".$data{"id"}."</td>";
		
		# ������
		if( 1<$GnrCount ){
			my $genre_text = $Genre[$data{"genre"}];
			print "<td>".$genre_text."</td>";
		}
		
		# �ѥ�᡼��
		for( my $i=0 ; $i<$PrmCount ; $i++ ){
			my $str = "";
			if( $PrmDisp[$i] != 0 ){
				my $type = $PrmType[$i];
				# �����å��ܥå���
				if( $type eq "checkbox" ){
					my @check = split( /,/ , $data{"param".$i} );
					my $c_max = 1+$#{$PrmSub[$i]};
					for( my $c=0 ; $c<$c_max ; $c++ ){
						if( $check[$c] == 1 ){
							$str .= $PrmSub[$i][$c]." ";
						}
					}
					chop( $str );
				}


				# �ƥ�����
				elsif( $type eq "text" ){		$str = $data{"param".$i};	}
				# ����,google maps,color picker		wada�ɲ�
				elsif( $type eq "date" or $type eq "gmaps" or $type eq "color"){		$str = $data{"param".$i};	}
				# �ƥ����ȥ��ꥢ
				elsif( $type eq "textarea" or $type eq "wysiwyg" or $type eq "station"){	$str = $data{"param".$i};	$str =~ s/\r\n/\n/g;$str =~ s/\r/\n/g;$str =~ s/\n/<br>/g;	}
				# �ƥ����ȥ��å�
				elsif( $type eq "texts_set" ){	$str = $data{"param".$i}."����";	}
				# ���쥯��
				elsif( $type eq "select" ){		$str = $PrmSub[$i][$data{"param".$i}];	}
				# �ե�����
				elsif( $type eq "file" ){		$str = $data{"param".$i};	}
				# �ե�����ʣ��
				elsif( $type eq "files" or $type eq "files_with_comment" ){		$str = $data{"param".$i."_0"};	}
				# �̿�
				elsif( $type eq "photo" ){		$str = "<img src=\"".$FileSavePath.$data{"param".$i}."?".int(rand(1000000000))."\" height=\"64\">";		}
				# �̿�ʣ��
				elsif( $type eq "photos" or $type eq "photos_with_comment" ){	$str = "<img src=\"".$FileSavePath.$data{"param".$i."_0"}."?".int(rand(1000000000))."\" height=\"64\">";	}
			print <<END_OF_HTML;
				<td>$str</td>
END_OF_HTML
			}
		}
		
		# ���ܥ���
		print <<END_OF_HTML;
				<td>
					<div class="cmd" onclick="edit($i);"><img src="./images/icon_edit.png" alt=""></div>
				</td><td>
					<div class="cmd" onclick="del($i);"><img src="./images/icon_del.png" alt=""></div>
				</td>
			</tr>
END_OF_HTML
		$i++;
	}
	print "</tbody></table><input type=\"hidden\" id=\"max\" value=\"".$i."\">\n";
	
	print <<END_OF_HTML;
	<script type="text/javascript">
	\$(document).ready(function(){
		\$("#list").tableDnD({
			onDragClass: "drag"
		});
	});
	</script>
END_OF_HTML
	
	# �����ܥ���
	&PrintListPanel();
	
	print <<END_OF_HTML;
	<div align="right" style="clear:both;">
		<a href="$BackToMenu">��˥塼�����</a>
	</div>
	
	<form action="demo.cgi" method="post" name="sender" id="sender" style="display:none;"></form>
END_OF_HTML
	
}

##############################################################################################################################################################

# �Խ�����
sub PrintEdit{
	my $number = shift;
	my @lines = &GetLines( $DataFilename );
	my %data = &LineToHash( $lines[$number] );
	my $textarea_param = 9999;
	
	# �������ѥǡ���
	my $enable;
	print <<END_OF_HTML;

	<script type="text/javascript" src="./scripts/jquery-1.7.2.min.js"></script>
	<script type="text/javascript" src="./scripts/jquery.ui.core.min.js"></script>
	<script type="text/javascript" src="./scripts/jquery.ui.datepicker.min.js"></script>
	<script type="text/javascript" src="./scripts/jquery.ui.datepicker-ja.js"></script>
	<link rel="stylesheet" type="text/css" href="./scripts/jquery.ui.base.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="./scripts/jquery.ui.theme.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="./scripts/jquery.ui.datepicker.css" media="screen" />
	<script type="text/javascript" src="./scripts/jquery.mousewheel-3.0.6.pack.js"></script>
	<script type="text/javascript" src="./scripts/jquery.fancybox.pack.js"></script>
	<link rel="stylesheet" type="text/css" href="./scripts/jquery.fancybox.css" media="screen" />
	<script type="text/javascript" src="./scripts/my_func.js"></script>

	<script src="./scripts/jquery.excolor.min.js" type="text/javascript"></script>
	<link rel="stylesheet" type="text/css" href="./scripts/excolor.css" />

	<script type="text/javascript">
		\$(document).ready(function() {
			\$('.fancybox').fancybox({
				maxWidth	: 800,
				maxHeight	: 400,
				fitToView	: false,
				width		: 800,
				height		: 400,
				autoSize	: false,
				closeClick	: false,
				openEffect	: 'none',
				closeEffect	: 'none'
			});
		});
	</script>
	<script type="text/javascript" src="./ckeditor/ckeditor.js"></script>

	<script type="text/javascript"><!--
		var param_count = $PrmCount;
		var enable = new Array($PrmCount);
		var wysiwygid = new Array();
END_OF_HTML
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		print <<END_OF_HTML;
		enable[$i] = new Array($GnrCount);
END_OF_HTML
		for( my $j=0 ; $j<$GnrCount ; $j++){
			my $v = $PrmEnable[$i][$j]-0;
			print <<END_OF_HTML;
		enable[$i][$j] = $v;
END_OF_HTML
		}
	}
	print <<END_OF_HTML;
	// --></script>
END_OF_HTML
	
	
	# �ơ��֥�إå�
	my $id = $data{"id"};
	print <<END_OF_HTML;
	
	<form id="detail" name="detail" action="demo.cgi" method="post" enctype="multipart/form-data">
	<table>
		<tbody>
			<tr><th>ID</th><td>$data{"id"}<input type="hidden" name="id" id="id" value="$id"></td></tr>
END_OF_HTML
	
	# ������
	if( 1<$GnrCount ){
		print <<END_OF_HTML;
			<tr><th>����</th><td>
				<select name="genre" id="genre" onchange="genre_change();">
END_OF_HTML
		for( my $i=0 ; $i<$GnrCount ; $i++ ){
			my $genre_name = $Genre[$i];
			my $selected = "";
			if( $data{"genre"} eq $i ){
				$selected = " selected";
			}
			print <<END_OF_HTML;
					<option value="$i"$selected>$genre_name</option>
END_OF_HTML
		}
		print <<END_OF_HTML;
				</select>
			</td></tr>
END_OF_HTML
	}
	
	# �ѥ�᡼��
	my $separator = shift( @Separator );
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		
		if( 0<$separator ){
			$separator--;
			if( 0 == $separator ){
				my $caption = shift( @SepText );
				if( $caption ne "" ){ $caption = "<caption>".$caption."</caption>"; }
				print "</tbody></table><table>$caption<tbody>";
				$separator = shift( @Separator );
			}
		}
		
		my $type = $PrmType[$i];
		my $name = $PrmName[$i];
		my $value = $data{"param$i"};
		my $unit = $PrmUnit[$i];
		my $notice = "<p class='notice'>".$PrmNotice[$i]."</p>";	#//wada �ѹ�
		if( $notice ne "" ){
#			$notice .= "<br>";	//wada �ɲ�
		}
		print <<END_OF_HTML;
			<tr id="line$i"><th>$name</th><td>$notice
END_OF_HTML
		
		### �����å��ܥå���
		if( $type eq "checkbox" ){
			my @checks = split( /,/ , $value );
			my $max = 1+$#{$PrmSub[$i]};
			for( my $c=0 ; $c<$max ; $c++ ){
				my $val = $PrmSub[$i][$c];
				my $checked = "";
				if( $checks[$c] eq "1" ){ $checked = "checked"; }
				my $str = "param".$i."_".$c;
				print <<END_OF_HTML;
			<label><input type="checkbox" name="$str" id="$str" value="1" $checked>$val</label>
END_OF_HTML
			}
		}
		
		### ���쥯��
		elsif( $type eq "select" ){
			print <<END_OF_HTML;
			<select name="param$i" id="param$i">
END_OF_HTML
			my $max = 1+$#{$PrmSub[$i]};
			for( my $s=0 ; $s<$max ; $s++ ){
				my $val = $PrmSub[$i][$s];
				my $selected = "";
				if( $s == $value ){
					$selected = "selected";
				}
				print <<END_OF_HTML;
				<option value="$s" $selected>$val</option>
END_OF_HTML
			}
			print <<END_OF_HTML;
			</select>$unit
END_OF_HTML
		}
		
		### �ƥ����ȥ��ꥢ
		elsif( $type eq "textarea" ){
			print <<END_OF_HTML;
			<textarea cols="40" rows="5" name="param$i" id="param$i" onchange="ReplaceInvalidCode(this);">$value</textarea>$unit
END_OF_HTML
		}
		### �Ǵ���
		elsif( $type eq "station" ){
			print <<END_OF_HTML;
			<textarea cols="40" rows="5" name="param$i" id="param$i" onchange="ReplaceInvalidCode(this);" class="result_station">$value</textarea><p class="get_station" style="border:1px solid #DDDDDD;padding:5px 10px;text-align:center;width:100px;">�Ǵ��ظ���</span>$unit
END_OF_HTML
		}

		### �ƥ����ȥ��ꥢ(wysiwyg)
		elsif( $type eq "wysiwyg" ){
			$textarea_param = "param$i";
			print <<END_OF_HTML;
			<textarea name="param$i" id="param$i" class="ckeditor">$value</textarea>$unit
END_OF_HTML
		}
		
		### �ƥ�����
		elsif( $type eq "text" ){
			print <<END_OF_HTML;
			<input size="50" type="text" name="param$i" id="param$i" value="$value" onchange="ReplaceInvalidCode(this);">$unit
END_OF_HTML
		}
		
		### ���� wada�ɲ�
		elsif( $type eq "date" ){
			print <<END_OF_HTML;
			<input size="20" type="text" name="param$i" id="param$i" value="$value" onchange="ReplaceInvalidCode(this);" style="width:120px;">$unit
			<script type="text/javascript">jQuery("#param$i").datepicker();</script>
END_OF_HTML
		}
		
		### gmap wada�ɲ�
		elsif( $type eq "gmaps" ){
			print <<END_OF_HTML;
			<a href="./my_googlemaps.php?id=param$i" class="fancybox" data-fancybox-type="iframe" style="padding-right:20px;"><img src="./images/icon_gmap.jpg" style="vertical-align:middle;"/></a>
			<input size="50" type="text" name="param$i" id="param$i" value="$value" style="width:260px;" class="cord">
END_OF_HTML
		}

		### color picker wada�ɲ�
		elsif( $type eq "color" ){
			print <<END_OF_HTML;
			<input size="50" type="text" name="param$i" id="param$i" value="$value" style="width:260px;" class="cord">
			<script type="text/javascript">jQuery('#param$i').excolor({root_path: 'img/'});</script>

END_OF_HTML
		}

		### �ƥ����ȥ��å�
		elsif( $type eq "texts_set" ){
			my $v = $value-1;
			my $c_max = ( 1+$#{$PrmSub[$i]} )/2;
			print <<END_OF_HTML;
				<input type="hidden" name="param_add_count$i" id="param_add_count$i" value="$value">
				<div id="area$i">
END_OF_HTML
			for( my $c=0 ; $c<$c_max ; $c++ ){
				my $name = $PrmSub[$i][$c];
				my $width = ($PrmSub[$i][$c+$c_max])."px";
				print <<END_OF_HTML;
					<div class="narrow" style="width:$width;float:left;border:1px solid white;padding:0 3px;">$name</div>
END_OF_HTML
			}
			print <<END_OF_HTML;
				<br>
END_OF_HTML
			for( my $j=0 ; $j<$value ; $j++ ){
				for( my $c=0 ; $c<$c_max ; $c++ ){
					my $text = "param".$i."_".$j."_".$c;
					my $text_value = $data{"param".$i."_".$j."_".$c};
					my $width = ($PrmSub[$i][$c+$c_max])."px";
					print <<END_OF_HTML;
					<input class="narrow" style="width:$width;" type="text" name="$text" id="$text" value="$text_value">
END_OF_HTML
				}
				print <<END_OF_HTML;
				<br>
END_OF_HTML
			}
			for( my $c = 0 ; $c<$c_max ; $c++ ){
				my $text = "param".$i."_".$value."_".$c;
				my $width = ($PrmSub[$i][$c+$c_max])."px";
				print <<END_OF_HTML;
				<input class="narrow" style="width:$width;" type="text" name="$text" id="$text" value="" onChange="column_add($i,$value,$c_max);">
END_OF_HTML
			}
			print <<END_OF_HTML;
			</div>
END_OF_HTML
		}
		
		### �ե�����
		elsif( $type eq "file" ){
			my $del = "param".$i."_del";
			print <<END_OF_HTML;
				<a href="$FileSavePath$value">$value</a><br>
				<input size="140" type="file" name="param$i" id="param$i" class="file_up" onchange="Byte2Check($i,-1);">
				<label><input type="checkbox" name="$del" id="$del" value="del">�������</label>
END_OF_HTML
		}
		
		### ����
		elsif( $type eq "photo" ){
			my $del = "param".$i."_del";
			my $img = $FileSavePath.$value."?".int(rand(1000000000));
			print <<END_OF_HTML;
				<img src="$img" width="80"><br>
				<input size="140" type="file" name="param$i" id="param$i" class="file_up" onchange="Byte2Check($i,-1);">
				<label><input type="checkbox" name="$del" id="$del" value="del">�������</label>
END_OF_HTML
		}
		### �ե�����ʣ��
		elsif( $type eq "files" ){
			print <<END_OF_HTML;
				<input type="hidden" name="param_add_count$i" id="param_add_count$i" value="0">
				<div id="area$i">
END_OF_HTML
			for( my $j = 0 ; $j<$value ; $j++ ){
				my $id = "file".$i."_".$j;
				my $file = $data{"param".$i."_".$j};
				my $file_id = "param".$i."_".$j."_file";
				my $del = "param".$i."_".$j."_del";
				print <<END_OF_HTML;
				<div>
					<a id="$id" href="$FileSavePath$file">$file</a><br>
					<input type="hidden" id="$file_id" name="$file_id" value="$file">
					<label><input type="checkbox" id="$del" name="$del" value="del">�������</label>
					<span onClick="file_swap($i,$j);">�ҤȤľ�ȸ�</span><br><br>
				</div>
END_OF_HTML
			}
			if( 0<$value ){
				print <<END_OF_HTML;
				<hr>
				<p style="font-weight:bold;">�ɲ�</p>
END_OF_HTML
			}
			my $id = "param".$i."_add0";
			print <<END_OF_HTML;
				<input type="file" id="$id" name="$id" size="140" onChange="upload_add($i,0,0);" class="file_up">
				</div>
END_OF_HTML
		}
		
		### ����ʣ��
		elsif( $type eq "photos" ){
			print <<END_OF_HTML;
				<input type="hidden" name="param_add_count$i" id="param_add_count$i" value="0">
				<div id="area$i">
END_OF_HTML
			for( my $j = 0 ; $j<$value ; $j++ ){
				my $id = "file".$i."_".$j;
				my $img = $FileSavePath.$data{"param".$i."_".$j}."?".int(rand(1000000000));
				my $file = $data{"param".$i."_".$j};
				my $file_id = "param".$i."_".$j."_file";
				my $del = "param".$i."_".$j."_del";
				print <<END_OF_HTML;
				<div>
					<img id="$id" src="$img" width="80"><br>
					<input type="hidden" id="$file_id" name="$file_id" value="$file">
					<label><input type="checkbox" id="$del" name="$del" value="del">�������</label>
					<span onClick="file_swap($i,$j);">�ҤȤľ�ȸ�</span><br><br>
				</div>
END_OF_HTML
			}
			if( 0<$value ){
				print <<END_OF_HTML;
				<hr>
				<p style="font-weight:bold;">�ɲ�</p>
END_OF_HTML
			}
			my $id = "param".$i."_add0";
			print <<END_OF_HTML;
				<input type="file" id="$id" name="$id" size="140" onChange="upload_add($i,0,0);" class="file_up">
				</div>
END_OF_HTML
		}
		
######################################################################################################################texts
		### texts
		elsif( $type eq "texts" ){
			print <<END_OF_HTML;
				<input type="hidden" name="param_add_count$i" id="param_add_count$i" value="0">
				<div id="area$i">
END_OF_HTML
			for( my $j = 0 ; $j<$value ; $j++ ){
				my $text_value1 = $data{"param".$i."_".$j."t1"};
				my $text_value2 = $data{"param".$i."_".$j."t2"};
				my $text1 = "param".$i."_".$j."t1";
				my $text2 = "param".$i."_".$j."t2";
				my $del = "param".$i."_".$j."_del";
				print <<END_OF_HTML;
				<div style="clear:both;margin-bottom:20px;">
					<input size="50" type="text" name="$text1" id="$text1" value="$text_value1"><br>
					<input size="50" type="text" name="$text2" id="$text2" value="$text_value2">
					<label style="float:none;display:inline;"><input type="checkbox" id="$del" name="$del" value="del">�������</label>
				</div>
END_OF_HTML
			}
			if( 0<$value ){
				print <<END_OF_HTML;
				<hr>
				<p style="font-weight:bold;">�ɲ�</p>
END_OF_HTML
			}
			my $id = "param".$i."_add0";
			my $text1 = "param".$i."_add0t1";
			my $text2 = "param".$i."_add0t2";
			print <<END_OF_HTML;
				<input size="50" type="text" name="$text1" id="$text1">
				<input size="50" type="text" name="$text2" id="$text2">
				</div>
END_OF_HTML
		}

		### �ե�����ʣ���ȥ�����
		elsif( $type eq "files_with_comment" ){
			print <<END_OF_HTML;
				<input type="hidden" name="param_add_count$i" id="param_add_count$i" value="0">
				<div id="area$i">
END_OF_HTML
			for( my $j = 0 ; $j<$value ; $j++ ){
				my $file = $data{"param".$i."_".$j};
				my $file_id = "param".$i."_".$j."_file";
				my $text_value = $data{"param".$i."_".$j."t"};
				my $text = "param".$i."_".$j."t";
				my $del = "param".$i."_".$j."_del";
				print <<END_OF_HTML;
				<div>
					<a href="$FileSavePath$file">$file</a><br>
					<input size="50" type="text" name="$text" id="$text" value="$text_value"><br>
					<input type="hidden" id="$file_id" name="$file_id" value="$file">
					<label><input type="checkbox" id="$del" name="$del" value="del">�������</label>
					<span onClick="file_swap($i,$j);">�ҤȤľ�ȸ�</span><br><br>
				</div>
END_OF_HTML
			}
			if( 0<$value ){
				print <<END_OF_HTML;
				<hr>
				<p style="font-weight:bold;">�ɲ�</p>
END_OF_HTML
			}
			my $id = "param".$i."_add0";
			my $text = "param".$i."_add0t";
			print <<END_OF_HTML;
				<input type="file" id="$id" name="$id" size="140" onChange="upload_add($i,0,1);" class="file_up">
				<input size="50" type="text" name="$text" id="$text">
				</div>
END_OF_HTML
		}
		
		### ����ʣ���ȥ�����
		elsif( $type eq "photos_with_comment" ){
			print <<END_OF_HTML;
				<input type="hidden" name="param_add_count$i" id="param_add_count$i" value="0">
				<div id="area$i">
END_OF_HTML
			for( my $j = 0 ; $j<$value ; $j++ ){
				my $id = "file".$i."_".$j;
				my $img = $FileSavePath.$data{"param".$i."_".$j}."?".int(rand(1000000000));
				my $file = $data{"param".$i."_".$j};
				my $file_id = "param".$i."_".$j."_file";
				my $text_value = $data{"param".$i."_".$j."t"};
				my $text = "param".$i."_".$j."t";
				my $del = "param".$i."_".$j."_del";
				print <<END_OF_HTML;
				<div>
					<img id="$id" src="$img" width="80"><br>
					<input size="50" type="text" name="$text" id="$text" value="$text_value"><br>
					<input type="hidden" id="$file_id" name="$file_id" value="$file">
					$FileSavePath$data{"param".$i."_".$j}<br />
					<label><input type="checkbox" id="$del" name="$del" value="del">�������</label>

					<span onClick="file_swap($i,$j);">�ҤȤľ�ȸ�</span><br><br>
					<br><br>
				</div>
END_OF_HTML
			}
			if( 0<$value ){
				print <<END_OF_HTML;
				<hr>
				<p style="font-weight:bold;">�ɲ�</p>
END_OF_HTML
			}
			my $id = "param".$i."_add0";
			my $text = "param".$i."_add0t";
			print <<END_OF_HTML;
				<input type="file" id="$id" name="$id" size="140" onChange="upload_add($i,0,1);" class="file_up">
				<input size="50" type="text" name="$text" id="$text">
				</div>
END_OF_HTML
		}
		
		print <<END_OF_HTML;
			</td></tr>
END_OF_HTML
	}
	
	
	print <<END_OF_HTML;
		</tbody>
	</table>
	<input type="hidden" name="line" id="line" value="$number">
	<input type="hidden" name="mode" id="mode" value="apply">
	</form>
	<script type="text/javascript"><!--
END_OF_HTML

	print <<END_OF_HTML;
	// --></script>
	<div align="center">
		<div class="cmd" onclick="cancel();"><img src="./images/icon_cancel.png" alt=""> ����󥻥�</div>
		<div class="cmd" onclick="apply($number);"><img src="./images/icon_apply.png" alt=""> Ŭ��</div>
	</div>
	
	<form action="demo.cgi" method="post" name="sender" id="sender" style="display:none;">
		<input type="hidden" name="mode" id="mode">
		<input type="hidden" name="line" id="line">
	</form>
	<script type="text/javascript"><!--
	genre_change();
	// --></script>
	
END_OF_HTML
	
}



##############################################################################################################################################################
### �ƥ�ץ졼�ȹ�������ɤ� #################################################################################################################################
##############################################################################################################################################################

# �ϥå�������
sub LineToTmplHash{
	my $line = shift;
	my %data = &LineToHash( $line );
	
	my $path = encode( 'utf-8', decode( 'euc-jp', $FilePath ) );
	my $path_sp = encode( 'utf-8', decode( 'euc-jp', $FilePathSP ) );
	my $list = encode( 'utf-8', decode( 'euc-jp', $ListHTML ) );
	my $pre = encode( 'utf-8', decode( 'euc-jp', $DetailHTML_PRE ) );
	my $pst = encode( 'utf-8', decode( 'euc-jp', $DetailHTML_PST ) );
	my $sp_pre = encode( 'utf-8', decode( 'euc-jp', $DetailSPHTML_PRE ) );
	my $sp_pst = encode( 'utf-8', decode( 'euc-jp', $DetailSPHTML_PST ) );

	
	my %tmpl_hash;
	
	$tmpl_hash{"ID"} = $data{"id"};
	
	$tmpl_hash{"LIST_URL"} = $list;
	$tmpl_hash{"DETAIL_URL"} = $pre.$data{"id"}.$pst;
	$tmpl_hash{"DETAIL_SP_URL"} = $sp_pre.$data{"id"}.$sp_pst;
	
	$tmpl_hash{"GENRE_ID"} = $data{"genre"};
	$tmpl_hash{"GENRE"} = encode( 'utf-8', decode( 'euc-jp', $Genre[$data{"genre"}] ) );
	$tmpl_hash{"GENRE".$data{"genre"}} = 1;
	
	if( -1<$GoogleMapTrg ){
		my $gm = $data{"param".$GoogleMapTrg};
		if( $gm ne "" ){
			my $bgn = index( $gm , "sll=" );
			my $end = index( $gm , "sspn=" );
			my $loc = substr( $gm , $bgn+4 , $end-$bgn-4-1 );
			my @loc_spl = split( /,/ , $loc );
			$tmpl_hash{"MAP_LON"} = $loc_spl[0];
			$tmpl_hash{"MAP_LAT"} = $loc_spl[1];
		}
	}
	
	# �ѥ�᡼������
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		# ʣ���ƥ�����
		if( $PrmType[$i] eq "texts_set" ){
			my @loop_data = ();
			my $count = $data{"param".$i};
			my $c_max = ( 1+$#{$PrmSub[$i]} )/2;
			if( 0<$count ){	$tmpl_hash{"PRM_EXIST".$i} = 1; }
			for( my $j=0 ; $j<$count ; $j++ ){
				my %files;
				if( $j==0 ){		$files{"FIRST"} = 1;	}
				if( $j%2==0 ){		$files{"EVEN"} = 1;		}
				if( $j==$count-1 ){	$files{"FINAL"} = 1;	}
				$files{"INDEX"} = encode( 'utf-8', decode( 'euc-jp' , $j ) );
				for( my $c=0 ; $c<$c_max ; $c++ ){
					$files{"COL".$c} = encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j."_".$c} ) );
$files{"COL".$c} =~ s/\r\n/\n/g;$files{"COL".$c} =~ s/\r/\n/g;$files{"COL".$c} =~ s/\n/<br>/g;
#					$files{"COL".$c} =~ s/\n/<br>/g;
				}
				push(@loop_data, \%files);
			}
			$tmpl_hash{"PRM_LOOP".$i} = \@loop_data;
		}
######################################################################################################################texts

		# �ƥ�����ʣ�����
		elsif($PrmType[$i] eq "texts"){
			my @loop_data = ();
			my $count = $data{"param".$i};
			if( 0<$count ){	$tmpl_hash{"PRM_EXIST".$i} = 1; }
			for( my $j=0 ; $j<$count ; $j++ ){
				my %files;
				if( $j==0 ){		$files{"FIRST"} = 1;	}
				if( $j%2==0 ){		$files{"EVEN"} = 1;		}
				if( $j==$count-1 ){	$files{"FINAL"} = 1;	}
				$files{"INDEX"} = encode( 'utf-8', decode( 'euc-jp' , $j ) );
				$files{"TEXT1"} = encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j."t1"} ) );
				$files{"TEXT2"} = encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j."t2"} ) );
				push(@loop_data, \%files);
			}
			$tmpl_hash{"PRM_LOOP".$i} = \@loop_data;
		}

		# ʣ�����
		elsif( $PrmType[$i] eq "files" or $PrmType[$i] eq "files_with_comment" or $PrmType[$i] eq "photos" or $PrmType[$i] eq "photos_with_comment" ){
			my @loop_data = ();
			my $count = $data{"param".$i};
			if( 0<$count ){	$tmpl_hash{"PRM_EXIST".$i} = 1; }
			for( my $j=0 ; $j<$count ; $j++ ){
				my %files;
				if( $j==0 ){		$files{"FIRST"} = 1;	}
				if( $j%2==0 ){		$files{"EVEN"} = 1;		}
				if( $j==$count-1 ){	$files{"FINAL"} = 1;	}
				$files{"INDEX"} = encode( 'utf-8', decode( 'euc-jp' , $j ) );
				$files{"FILENAME"} = encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j} ) );
				$files{"PATH"} = $path.encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j} ) );
				$files{"PATH_SP"} = $path_sp.encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j} ) );
				$files{"PATH_S"} = $path.encode( 'utf-8', decode( 'euc-jp' , "s_".$data{"param".$i."_".$j} ) );
				$files{"PATH_S_SP"} = $path_sp.encode( 'utf-8', decode( 'euc-jp' , "s_".$data{"param".$i."_".$j} ) );
				$files{"SIZE"} = encode( 'utf-8', decode( 'euc-jp' , &GetFileSize( $FileSavePath.$data{"param".$i."_".$j} ) ) );
				$files{"TEXT"} = encode( 'utf-8', decode( 'euc-jp' , $data{"param".$i."_".$j."t"} ) );
				$files{"TARGET_ID"} = $data{"id"};
				push(@loop_data, \%files);
			}
			$tmpl_hash{"PRM_LOOP".$i} = \@loop_data;
		}
		# ñ�ʤ��
		else{
			$tmpl_hash{"PRM_NAME".$i} = encode( 'utf-8', decode( 'euc-jp' , $PrmName[$i] ) );
			my $var = $data{"param".$i};
$var =~ s/\r\n/\n/g;$var =~ s/\r/\n/g;$var =~ s/\n/<br>/g;
#			$var =~ s/\n/<br>/g;
			my $unit = $PrmUnit[$i];
			
			if( $var ne "" ){
				$tmpl_hash{"PRM_EXIST".$i} = 1;
			}
			# ���쥯�Ȥξ������ƥƥ����Ȥ��ֹ�
			if( $PrmType[$i] eq "select" ){
				$tmpl_hash{"PRM_VAR".$i} = encode( 'utf-8', decode( 'euc-jp' , $PrmSub[$i][$var].$unit ) );
				$tmpl_hash{"PRM_VAR".$i."_INDEX".$var} = 1;
				$tmpl_hash{"PRM_INDEX".$i} = encode( 'utf-8', decode( 'euc-jp' , $var ) );
			}
			# �����å��ܥå����ξ��Ϥʤ󤫤�����
			elsif( $PrmType[$i] eq "checkbox" ){
				my $c_max = 1+$#{$PrmSub[$i]};
				my @checks = split( /,/ , $var );
				my $str = "";
				my $ex = 0;
				for( my $c=0 ; $c<$c_max ; $c++ ){
					if( $checks[$c] eq "1" ){
						$str .= encode( 'utf-8', decode( 'euc-jp' , $PrmSub[$i][$c] ) ).",";
						$tmpl_hash{"PRM_VAR".$i."_INDEX".$c} = 1;
						$ex = 1;
					}
				}
				chop( $str );
				$tmpl_hash{"PRM_VAR".$i} = $str;
				$tmpl_hash{"PRM_EXIST".$i} = $ex;
			}
			# �ե�����ξ��ϥѥ��ȥ�����
			elsif( $PrmType[$i] eq "file" or $PrmType[$i] eq "photo" ){
				$tmpl_hash{"PRM_VAR".$i} = $path.encode( 'utf-8', decode( 'euc-jp' , $var ) );
				$tmpl_hash{"PRM_VAR_SP".$i} = $path_sp.encode( 'utf-8', decode( 'euc-jp' , $var ) );
				$tmpl_hash{"PRM_VAR_S".$i} = $path.encode( 'utf-8', decode( 'euc-jp' , "s_".$var ) );
				$tmpl_hash{"PRM_VAR_S_SP".$i} = $path_sp.encode( 'utf-8', decode( 'euc-jp' , "s_".$var ) );
				$tmpl_hash{"PRM_SIZE".$i} = encode( 'utf-8', decode( 'euc-jp' , &GetFileSize( $FileSavePath.$var ) ) );
			}
			# ����¾
			else{
				$tmpl_hash{"PRM_VAR".$i} = encode( 'utf-8', decode( 'euc-jp' , $var.$unit ) );
			}
		}
	}
	
	return %tmpl_hash;
}

# PC�ѥ���ǥå����ե�����
sub UpdateIndexTmpl{
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$IndexTMPL"
	);
	
	# �ǡ����ե������ɤ߹���
	my @data_list = &GetLines( $DataFilename );
	
	my @lines_data = ();
	my @count = ();
	my $count_max = 1+$#data_list;
	
	my $order = 0;
	foreach my $line ( @data_list ){
		# �ϥå�����Ѵ�
		my %tmpl_hash = &LineToTmplHash( $line );
		
		my $g = $tmpl_hash{"GENRE_ID"};
		
		$tmpl_hash{"ORDER"} = $order;
		
		# ����
		$count[$g]++;
		if( $count[$g]%2 == 0 ){
			$tmpl_hash{"EVEN"} = 1;
		}
		if( $count[$g] == 1 ){
			$tmpl_hash{"FIRST"} = 1;
		}
		
		# ������ɲ�
		push( @{$lines_data[$g]} , \%tmpl_hash );
		
		# �����
		if( $DispTrg<0 or $tmpl_hash{"PRM_VAR".$DispTrg} ne "" ){
			$IndexMax--;
		}
		if( $IndexMax == 0 ){
			last;
		}
		
		$order++;
	}
	# �ƥ�ץ졼�Ȥ�����
	for( my $i=0 ; $i<$GnrCount ; $i++ ){
		if( 0<=$#{$lines_data[$i]} ){
			$lines_data[$i][$#{$lines_data[$i]}]{"FINAL"} = 1;
		}
		my $var = "GENRE".$i;
		$template->param( $var => \@{$lines_data[$i]} );
	}
	
	# ����ʸ����
	my $tmpl = $template->output;
	$tmpl =~ s/\n//g;
	
	# HTML��������
	
	# �ɹ�
	open( FILE , "< $IndexHTML" );
	&FileLock( *FILE );
	my @file_lines = <FILE>;
	&FileUnlock( *FILE );
	close(FILE);
	
	#�ե����볫��
	open( DB ,"+> $IndexHTML");
	&FileLock( *DB );
	# �ִ�����
	foreach my $line ( @file_lines ){
		if( 0<=index($line,"<!-- $IndexAnchor -->") ){
			print DB "<!-- $IndexAnchor -->$tmpl\n";
		}else{
			print DB "$line";
		}
	}
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
}

# PC�ѥ���ǥå����ե�����002
sub UpdateIndexTmpl2{
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$IndexTMPL2"
	);
	
	# �ǡ����ե������ɤ߹���
	my @data_list = &GetLines( $DataFilename );
	
	my @lines_data = ();
	my @count = ();
	my $count_max = 1+$#data_list;
	
	my $order = 0;
	foreach my $line ( @data_list ){
		# �ϥå�����Ѵ�
		my %tmpl_hash = &LineToTmplHash( $line );
		
		my $g = $tmpl_hash{"GENRE_ID"};
		
		$tmpl_hash{"ORDER"} = $order;
		
		# ����
		$count[$g]++;
		if( $count[$g]%2 == 0 ){
			$tmpl_hash{"EVEN"} = 1;
		}
		if( $count[$g] == 1 ){
			$tmpl_hash{"FIRST"} = 1;
		}
		
		# ������ɲ�
		push( @{$lines_data[$g]} , \%tmpl_hash );
		
		# �����
		if( $DispTrg<0 or $tmpl_hash{"PRM_VAR".$DispTrg} ne "" ){
			$IndexMax2--;
		}
		if( $IndexMax2 == 0 ){
			last;
		}
		
		$order++;
	}
	# �ƥ�ץ졼�Ȥ�����
	for( my $i=0 ; $i<$GnrCount ; $i++ ){
		if( 0<=$#{$lines_data[$i]} ){
			$lines_data[$i][$#{$lines_data[$i]}]{"FINAL"} = 1;
		}
		my $var = "GENRE".$i;
		$template->param( $var => \@{$lines_data[$i]} );
	}
	
	# ����ʸ����
	my $tmpl = $template->output;
	$tmpl =~ s/\n//g;
	
	# HTML��������
	
	# �ɹ�
	open( FILE , "< $IndexHTML2" );
	&FileLock( *FILE );
	my @file_lines = <FILE>;
	&FileUnlock( *FILE );
	close(FILE);
	
	#�ե����볫��
	open( DB ,"+> $IndexHTML2");
	&FileLock( *DB );
	# �ִ�����
	foreach my $line ( @file_lines ){
		if( 0<=index($line,"<!-- $IndexAnchor2 -->") ){
			print DB "<!-- $IndexAnchor2 -->$tmpl\n";
		}else{
			print DB "$line";
		}
	}
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
}

# SP�ѥ���ǥå����ե�����
sub UpdateSPIndexTmpl{
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$IndexSPTMPL"
	);
	
	# �ǡ����ե������ɤ߹���
	my @data_list = &GetLines( $DataFilename );
	
	my @lines_data = ();
	my @count = ();
	my $count_max = 1+$#data_list;
	
	my $order = 0;
	foreach my $line ( @data_list ){
		# �ϥå�����Ѵ�
		my %tmpl_hash = &LineToTmplHash( $line );
		
		my $g = $tmpl_hash{"GENRE_ID"};
		
		$tmpl_hash{"ORDER"} = $order;
		
		# ����
		$count[$g]++;
		if( $count[$g]%2 == 0 ){
			$tmpl_hash{"EVEN"} = 1;
		}
		if( $count[$g] == 1 ){
			$tmpl_hash{"FIRST"} = 1;
		}
		
		# ������ɲ�
		push( @{$lines_data[$g]} , \%tmpl_hash );
		
		# �����
		if( $DispTrg<0 or $tmpl_hash{"PRM_VAR".$DispTrg} ne "" ){
			$IndexSPMax--;
		}
		if( $IndexSPMax == 0 ){
			last;
		}
		
		$order++;
	}
	# �ƥ�ץ졼�Ȥ�����
	for( my $i=0 ; $i<$GnrCount ; $i++ ){
		if( 0<=$#{$lines_data[$i]} ){
			$lines_data[$i][$#{$lines_data[$i]}]{"FINAL"} = 1;
		}
		my $var = "GENRE".$i;
		$template->param( $var => \@{$lines_data[$i]} );
	}
	
	# ����ʸ����
	my $tmpl = $template->output;
	$tmpl =~ s/\n//g;
	
	# HTML��������
	
	# �ɹ�
	open( FILE , "< $IndexSPHTML" );
	&FileLock( *FILE );
	my @file_lines = <FILE>;
	&FileUnlock( *FILE );
	close(FILE);
	
	#�ե����볫��
	open( DB ,"+> $IndexSPHTML");
	&FileLock( *DB );
	# �ִ�����
	foreach my $line ( @file_lines ){
		if( 0<=index($line,"<!-- $IndexSPAnchor -->") ){
			print DB "<!-- $IndexSPAnchor -->$tmpl\n";
		}else{
			print DB "$line";
		}
	}
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
}


# PC�����ե�����
sub UpdateListTmpl{
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$ListTMPL"
	);
	
	# �ǡ����ե������ɤ߹���
	my @data_list = &GetLines( $DataFilename );
	
	
	my @lines_data = ();
	my @count = ();
	my $count_max = 1+$#data_list;
	
	my $order = 0;
	foreach my $line ( @data_list ){
		# �ϥå�����Ѵ�
		my %tmpl_hash = &LineToTmplHash( $line );
		
		my $g = $tmpl_hash{"GENRE_ID"};
		
		$tmpl_hash{"ORDER"} = $order;
		
		# ����
		$count[$g]++;
		if( $count[$g]%2 == 0 ){
			$tmpl_hash{"EVEN"} = 1;
		}
		if( $count[$g] == 1 ){
			$tmpl_hash{"FIRST"} = 1;
		}
		
		# ������ɲ�
		push( @{$lines_data[$g]} , \%tmpl_hash );
		
		# �����
		if( $DispTrg<0 or $tmpl_hash{"PRM_VAR".$DispTrg} ne "" ){
			$ListMax--;
		}
		if( $ListMax == 0 ){
			last;
		}
		
		$order++;
	}
	# �ƥ�ץ졼�Ȥ�����
	for( my $i=0 ; $i<$GnrCount ; $i++ ){
		if( 0<=$#{$lines_data[$i]} ){
			$lines_data[$i][$#{$lines_data[$i]}]{"FINAL"} = 1;
		}
		my $var = "GENRE".$i;
		$template->param( $var => \@{$lines_data[$i]} );
	}
	
	# HTML��������
	#�ե����볫��
	open( DB ,"> $ListHTML");
	&FileLock( *DB );
	#�񤭹���
	print DB $template->output;
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
}


# SP�����ե�����
sub UpdateListSPTmpl{
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$ListSPTMPL"
	);
	
	# �ǡ����ե������ɤ߹���
	my @data_list = &GetLines( $DataFilename );
	
	
	my @lines_data = ();
	my @count = ();
	my $count_max = 1+$#data_list;
	
	my $order = 0;
	foreach my $line ( @data_list ){
		# �ϥå�����Ѵ�
		my %tmpl_hash = &LineToTmplHash( $line );
		
		my $g = $tmpl_hash{"GENRE_ID"};
		
		$tmpl_hash{"ORDER"} = $order;
		
		# ����
		$count[$g]++;
		if( $count[$g]%2 == 0 ){
			$tmpl_hash{"EVEN"} = 1;
		}
		if( $count[$g] == 1 ){
			$tmpl_hash{"FIRST"} = 1;
		}
		
		# ������ɲ�
		push( @{$lines_data[$g]} , \%tmpl_hash );
		
		# �����
		if( $DispTrg<0 or $tmpl_hash{"PRM_VAR".$DispTrg} ne "" ){
			$ListSPMax--;
		}
		if( $ListSPMax == 0 ){
			last;
		}
		
		$order++;
	}
	# �ƥ�ץ졼�Ȥ�����
	for( my $i=0 ; $i<$GnrCount ; $i++ ){
		if( 0<=$#{$lines_data[$i]} ){
			$lines_data[$i][$#{$lines_data[$i]}]{"FINAL"} = 1;
		}
		my $var = "GENRE".$i;
		$template->param( $var => \@{$lines_data[$i]} );
	}
	
	# HTML��������
	#�ե����볫��
	open( DB ,"> $ListSPHTML");
	&FileLock( *DB );
	#�񤭹���
	print DB $template->output;
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
}




# PC�ܺ٥ե�����
sub UpdateDetailTMPL{
	my $line = shift;
	my $prv = shift;
	my $nxt = shift;
	my %data = LineToHash( $line );
	my $id = $data{"id"};
	my $genre = $data{"genre"};
	
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$DetailTMPL"
	);
	
	# �ϥå�����Ѵ�
	my %tmpl_hash = &LineToTmplHash( $line );
	my $pre = encode( 'utf-8', decode( 'euc-jp' , $DetailHTML_PRE ) );
	my $pst = encode( 'utf-8', decode( 'euc-jp' , $DetailHTML_PST ) );
	
	if( 0<=$prv ){
		$tmpl_hash{"PREV_PAGE_EXIST"} = 1;
		$tmpl_hash{"PREV_PAGE"} = $pre.$prv.$pst;
	}
	if( 0<=$nxt ){
		$tmpl_hash{"NEXT_PAGE_EXIST"} = 1;
		$tmpl_hash{"NEXT_PAGE"} = $pre.$nxt.$pst;
	}
	
	# �ƥ�ץ졼�Ȥ�����
	my $var = "GENRE".$genre;
	$template->param( $var => 1 );
	
	$template->param( \%tmpl_hash );
	
	# HTML��������
	my $file = $DetailHTML_PRE.$id.$DetailHTML_PST;
	#�ե����볫��
	open( DB ,"> $file");
	&FileLock( *DB );
	#�񤭹���
	print DB $template->output;
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
	chmod(0644,"$file");
}



# PC�ܺ٥ե�����
sub UpdateDetailSPTMPL{
	my $line = shift;
	my $prv = shift;
	my $nxt = shift;
	my %data = LineToHash( $line );
	my $id = $data{"id"};
	my $genre = $data{"genre"};
	
	# �ƥ�ץ졼���ɤ߹���
	my $template = HTML::Template->new(
		die_on_bad_params => 0,
		filename => "$DetailSPTMPL"
	);
	
	# �ϥå�����Ѵ�
	my %tmpl_hash = &LineToTmplHash( $line );
	my $pre = encode( 'utf-8', decode( 'euc-jp' , $DetailSPHTML_PRE ) );
	my $pst = encode( 'utf-8', decode( 'euc-jp' , $DetailSPHTML_PST ) );
	
	if( 0<=$prv ){
		$tmpl_hash{"PREV_PAGE_EXIST"} = 1;
		$tmpl_hash{"PREV_PAGE"} = $pre.$prv.$pst;
	}
	if( 0<=$nxt ){
		$tmpl_hash{"NEXT_PAGE_EXIST"} = 1;
		$tmpl_hash{"NEXT_PAGE"} = $pre.$nxt.$pst;
	}
	
	# �ƥ�ץ졼�Ȥ�����
	my $var = "GENRE".$genre;
	$template->param( $var => 1 );
	
	$template->param( \%tmpl_hash );
	
	# HTML��������
	my $file = $DetailSPHTML_PRE.$id.$DetailSPHTML_PST;
	#�ե����볫��
	open( DB ,"> $file");
	&FileLock( *DB );
	#�񤭹���
	print DB $template->output;
	#�ե������Ĥ���
	&FileUnlock( *DB );
	close( DB );
	chmod(0644,"$file");
}

# �ƥ�ץ졼��ȿ�ǣ���
sub UpdateTmpl{
	#PC�ѥ���ǥå���
	if( $IndexTMPL ne "" and -f $IndexTMPL ){
		&UpdateIndexTmpl();
	}
	#PC�ѥ���ǥå���002
	if( $IndexTMPL2 ne "" and -f $IndexTMPL2 ){
		&UpdateIndexTmpl2();
	}
	#SP�ѥ���ǥå���
	if( $IndexSPTMPL ne "" and -f $IndexSPTMPL ){
		&UpdateSPIndexTmpl();
	}
	#PC�Ѱ���
	if( $ListTMPL ne "" and -f $ListTMPL ){
		&UpdateListTmpl();
	}
	#SP�Ѱ���
	if( $ListSPTMPL ne "" and -f $ListSPTMPL ){
		&UpdateListSPTmpl();
	}
	#PC�Ѿܺ�
	if( $DetailTMPL ne "" and -f $DetailTMPL ){
		my @data_list = &GetLines( $DataFilename );
		my $lines_max = 1+$#data_list;
		my @ids = ();
		for( my $i=0 ; $i<$lines_max ; $i++ ){
			my @spl = split( /<>/ , $data_list[$i] );
			push( @ids , shift(@spl) );
		}
		for( my $i=0 ; $i<$lines_max ; $i++ ){
			my $prv = $i==0 ? -1 : $ids[$i-1];
			my $nxt = $i==$lines_max-1 ? -1 : $ids[$i+1];
			&UpdateDetailTMPL( $data_list[$i] , $prv , $nxt );
		}
	}

	#SP�Ѿܺ�
	if( $DetailSPTMPL ne "" and -f $DetailSPTMPL ){
		my @data_list = &GetLines( $DataFilename );
		my $lines_max = 1+$#data_list;
		my @ids = ();
		for( my $i=0 ; $i<$lines_max ; $i++ ){
			my @spl = split( /<>/ , $data_list[$i] );
			push( @ids , shift(@spl) );
		}
		for( my $i=0 ; $i<$lines_max ; $i++ ){
			my $prv = $i==0 ? -1 : $ids[$i-1];
			my $nxt = $i==$lines_max-1 ? -1 : $ids[$i+1];
			&UpdateDetailSPTMPL( $data_list[$i] , $prv , $nxt );
		}
	}
}



##############################################################################################################################################################
### ���åץ��� #############################################################################################################################################
##############################################################################################################################################################

sub Upload{
	( my $upfile , my $fh , my $type , my $PhotoW , my $PhotoH , my $PhotoW_S , my $PhotoH_S )= @_;
	
	# �ե�����̾�ȳ�ĥ��
	my $name = "";
	my $ext = "";
	{
		my @token = split( /\\/ , $upfile );
		my $f = pop( @token );
		my @ft = split( /\./ , $f );
		$ext = pop( @ft );
		$name = pop( @ft );
		
		$ext =~ tr/[A-Z]/[a-z]/;
	}
	
	# ���Ѥ�̵��
	if( $name =~ /[\x80-\xff]/ ){
		return "";
	}
	
	# ��¸��
	my $filename = $name.".".$ext;
	my $savefile = $FileSavePath.$filename;
	my $joint = "";
	while( -f $savefile ){
		$joint .= "_";
		$filename = $name.$joint.".".$ext;
		$savefile = $FileSavePath.$filename;
	}
	
	# �ե�����Ǥ�
	if( $type =~ /(file)/i ){
		# ���åץ��ɤ��줿�ե�����Υե�ѥ�
		my $temp_path = $query->tmpFileName($fh);
		
		# File::Copy �� move�᥽�åɤǰ�ư
		move($temp_path, $savefile);
		
		close($fh);
	}
	# �����Ǥ�
	elsif( $type =~ /(photo)/i and $ext =~ /(jpg|gif|bmp|png)/i ){
		binmode($fh);
		my $img = new Image::Magick;
		my $binary = join ("", <$fh>);
		
		# �ե�����ϥ�ɥ뤫��Х��ʥ��
		$img->BlobToImage($binary);
		
		# ����������Ĵ��
		my ( $x, $y ) = $img->Get( 'width', 'height' );
		if( $PhotoW<$x or $PhotoH<$y ){
			$img->Resize( geometry => $PhotoW."x".$PhotoH );
		}
#		if ( $x > $y * $PhotoW / $PhotoH ) {
#			$img->Resize( width => $x * $PhotoH / $y, height => $PhotoH );
#			$img->Crop( width => $PhotoW, height => $PhotoH, x => ( $x * $PhotoH / $y - $PhotoW ) / 2, y => 0 );
#		}
#		else {
#			$img->Resize( width => $PhotoW, height => $y * $PhotoW / $x );
#			$img->Crop( width => $PhotoW, height => $PhotoH, x => 0, y => ( $y * $PhotoW / $x - $PhotoH ) / 2 );
#		}
		
		# ��¸
		$img->Write("$ext:$savefile");
		
		# ����ͥ����̲����ˤ�����
		if( $PhotoW_S != 0 and $PhotoH_S != 0 ){
			my $savefile_s = $FileSavePath."s_".$filename;
			
			# ����������Ĵ��
			if ( $x > $y * $PhotoW_S / $PhotoH_S ) {
				$img->Resize( width => $x * $PhotoH_S / $y, height => $PhotoH_S );
				$img->Crop( width => $PhotoW_S, height => $PhotoH_S, x => ( $x * $PhotoH_S / $y - $PhotoW_S ) / 2, y => 0 );
			}
			else {
				$img->Resize( width => $PhotoW_S, height => $y * $PhotoW_S / $x );
				$img->Crop( width => $PhotoW_S, height => $PhotoH_S, x => 0, y => ( $y * $PhotoW_S / $x - $PhotoH_S ) / 2 );
			}
			
			# ��¸
			$img->Write("$ext:$savefile_s");
		}
		
	}else{
		$filename = "";
	}
	
	return $filename;
}

##############################################################################################################################################################
### ������� #################################################################################################################################################
##############################################################################################################################################################

# �ǡ���ʬ��
# argv(0):ʬ�䤷�����ǡ���,<>��ʬ�䵭��
sub LineToHash{
	
	my $line = shift;
	my @data_array = split( /<>/ , $line );
	my %data_hash;
	
	# id
	$data_hash{"id"} = sprintf( "%04d" , shift(@data_array) );
	
	# ������
	$data_hash{"genre"} = shift( @data_array );
	
	# �ѥ�᡼��
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		my $type = $PrmType[$i];
		$data_hash{"param".$i} = shift( @data_array );
		# ���Ԥ����浭�����
		if( $type eq "text" or $type eq "textarea" or $type eq "station" ){
			$data_hash{"param".$i} =~ s/<br>/\n/g;
			$data_hash{"param".$i} =~ s/&lt;/</g;
			$data_hash{"param".$i} =~ s/&gt;/>/g;
		}
		elsif($type eq "wysiwyg"){
			$data_hash{"param".$i} =~ s/&lt;/</g;
			$data_hash{"param".$i} =~ s/&gt;/>/g;
		}
		# ʣ��
		elsif( $type eq "files" or $type eq "photos" ){
			my $count = $data_hash{"param".$i};
			for( my $j=0 ; $j<$count ; $j++ ){
				$data_hash{"param".$i."_".$j} = shift(@data_array);
			}
		}
######################################################################################################################texts

		# texts
		elsif( $type eq "texts" ){
			my $count = $data_hash{"param".$i};
			for( my $j=0 ; $j<$count ; $j++ ){
				$data_hash{"param".$i."_".$j."t1"} = shift(@data_array);
				$data_hash{"param".$i."_".$j."t2"} = shift(@data_array);
			}
		}

		# ʸ�ϤĤ���ʣ��
		elsif( $type eq "files_with_comment" or $type eq "photos_with_comment" ){
			my $count = $data_hash{"param".$i};
			for( my $j=0 ; $j<$count ; $j++ ){
				$data_hash{"param".$i."_".$j} = shift(@data_array);
				$data_hash{"param".$i."_".$j."t"} = shift(@data_array);
			}
		}
		# ʸ�Ϥ�ʣ��
		elsif( $type eq "texts_set" ){
			my $count = $data_hash{"param".$i};
			my $c_max = ( 1+$#{$PrmSub[$i]} )/2;
			for( my $r=0 ; $r<$count ; $r++ ){
				for( my $c=0 ; $c<$c_max ; $c++ ){
					$data_hash{"param".$i."_".$r."_".$c} = shift(@data_array);
				}
			}
		}
		
	}
	
	return %data_hash;
}


##############################################################################################################################################################
### �ե����������� #########################################################################################################################################
##############################################################################################################################################################

# ������ǣ��Ծ����¸
sub SaveLine{
	my @data_list = &GetLines( $DataFilename );
	my %data = &LineToHash( $data_list[$query->param("line")] );
	
	
	# ��¸�ѿ�
	my $line = "";
	
	# ��¸�Ժ���
	
	# ID
	$line = $line.$query->param("id")."<>";
	
	# ������
	$line = $line.$query->param("genre")."<>";
	
	# �ѥ�᡼��
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		my $param = $query->param("param".$i);
		my $type = $PrmType[$i];
		
		# �ƥ����ȡ��ƥ����ȥ��ꥢ�����쥯�ȡ�����
		if( $type eq "text" or $type eq "textarea" or $type eq "station" or $type eq "select" or $type eq "date" or $type eq "gmaps" or $type eq "color"){
			$param =~ s/\r\n/\n/g;
			$param =~ s/\r/\n/g;
			$param =~ s/</&lt;/g;
			$param =~ s/>/&gt;/g;
			$param =~ s/\n/<br>/g;
			$line .= $param."<>";
		}elsif( $type eq "wysiwyg"){
			$param =~ s/\r\n/\n/g;
			$param =~ s/\r/\n/g;
			$param =~ s/\n//g;
			$param =~ s/</&lt;/g;
			$param =~ s/>/&gt;/g;
			$line .= $param."<>";
		}
		# ¿�ʥƥ�����
		elsif( $type eq "texts_set" ){
			my $c_max = ( 1+$#{$PrmSub[$i]} )/2;
			my $r_max = $query->param("param_add_count".$i);
			my $rows = 0;
			my $str = "";
			for( my $r=0 ; $r<$r_max ; $r++ ){
				if( $query->param("param".$i."_".$r."_0") eq "" ){
					next;
				}
				$rows++;
				for( my $c=0 ; $c<$c_max ; $c++ ){
					$param = $query->param("param".$i."_".$r."_".$c);
					$param =~ s/\r\n/\n/g;
					$param =~ s/\r/\n/g;
					$param =~ s/</&lt;/g;
					$param =~ s/>/&gt;/g;
					$param =~ s/\n/<br>/g;
					$str .= $param."<>";
				}
			}
			$line .= $rows."<>".$str;
		}
		# �����å��ܥå���
		elsif( $type eq "checkbox" ){
			my @checks = ();
			my $c_max = 1+$#{$PrmSub[$i]};
			for( my $c=0 ; $c<$c_max ; $c++ ){
				if( $query->param("param".$i."_".$c) ){
					push( @checks , "1" );
				}else{
					push( @checks , "0" );
				}
			}
			$param = join( "," , @checks );
			$line .= $param."<>";
		}
		
		# �ե����롦�̿�
		if( $type eq "file" or $type eq "photo" ){
			my $filename = $data{"param".$i};
			# �õ���
			if( $query->param("param".$i."_del") eq "del" ){
				unlink( $FileSavePath.$data{"param".$i} );
				unlink( $FileSavePath."s_".$data{"param".$i} );
				$filename = "";
			}
			# ���åץ���
			if( $query->param("param".$i) ne "" ){
				unlink( $FileSavePath.$data{"param".$i} );
				unlink( $FileSavePath."s_".$data{"param".$i} );
				if( $type =~ /(photo)/i ){
					$filename = &Upload( $query->param("param".$i) , $query->upload("param".$i) , "photo" , $PrmSub[$i][0] , $PrmSub[$i][1] , $PrmSub[$i][2] , $PrmSub[$i][3] );
				}else{
					$filename = &Upload( $query->param("param".$i) , $query->upload("param".$i) , "file" );
					chmod(0777,"$FileSavePath$filename");
				}
			}
			$line .= $filename."<>";
		}
		
		# �ե�����ʣ�����̿�ʣ��
		if( $type eq "files" or $type eq "photos" ){
			my $filename = "";
			my $files = 0;
			my $str = "";
			# �õ���
			my $svcount = $data{"param".$i};
			for( my $j=0 ; $j<$svcount ; $j++ ){
				if( $query->param("param".$i."_".$j."_del") eq "del" ){
					unlink( $FileSavePath.$query->param("param".$i."_".$j."_file") );
					unlink( $FileSavePath."s_".$query->param("param".$i."_".$j."_file") );
				}else{
					$files++;
					$str .= $query->param("param".$i."_".$j."_file")."<>";
				}
			}
			# ���åץ���
			my $upcount = $query->param("param_add_count".$i);
			for( my $j=0 ; $j<$upcount ; $j++ ){
				if( $query->param("param".$i."_add".$j) ne "" ){
					if( $type =~ /(photo)/i ){
						$filename = &Upload( $query->param("param".$i."_add".$j) , $query->upload("param".$i."_add".$j) , "photo" , $PrmSub[$i][0] , $PrmSub[$i][1] , $PrmSub[$i][2] , $PrmSub[$i][3] );
					}else{
						$filename = &Upload( $query->param("param".$i."_add".$j) , $query->upload("param".$i."_add".$j) , "file" );
						chmod(0777,"$FileSavePath$filename");
					}
				}
				if( $filename ne "" ){
					$files++;
					$str .= $filename."<>";
				}
			}
			$line .= $files."<>".$str;
		}
######################################################################################################################texts
		# �ƥ�����ʣ��
		if( $type eq "texts" ){
			my $filename = "";
			my $files = 0;
			my $str = "";
			# �õ���
			my $svcount = $data{"param".$i};
			for( my $j=0 ; $j<$svcount ; $j++ ){
				if( $query->param("param".$i."_".$j."_del") eq "del" ){
				}else{
					$files++;
					$str .= $query->param("param".$i."_".$j."t1")."<>";
					$str .= $query->param("param".$i."_".$j."t2")."<>";
				}
			}
			# ���åץ���
			my $upcount = $query->param("param_add_count".$i);
#			for( my $j=0 ; $j<$upcount ; $j++ ){
			if( $query->param("param".$i."_add0t1") ne "" or $query->param("param".$i."_add0t1") ne "" ){
#				if( $filename ne "" ){
					$files++;
					$str .= $query->param("param".$i."_add0t1")."<>".$query->param("param".$i."_add0t2")."<>";
#				}
			}
			$line .= $files."<>".$str;
		}


		# �ե�����ʣ���ȥ����ȡ��̿�ʣ���ȥ�����
		if( $type eq "files_with_comment" or $type eq "photos_with_comment" ){
			my $filename = "";
			my $files = 0;
			my $str = "";
			# �õ���
			my $svcount = $data{"param".$i};
			for( my $j=0 ; $j<$svcount ; $j++ ){
				if( $query->param("param".$i."_".$j."_del") eq "del" ){
					unlink( $FileSavePath.$data{"param".$i."_".$j} );
					unlink( $FileSavePath."s_".$data{"param".$i."_".$j} );
				}else{
					$files++;
					$str .= $query->param("param".$i."_".$j."_file")."<>";
					$str .= $query->param("param".$i."_".$j."t")."<>";
				}
			}
			# ���åץ���
			my $upcount = $query->param("param_add_count".$i);
			for( my $j=0 ; $j<$upcount ; $j++ ){
				if( $query->param("param".$i."_add".$j) ne "" ){
					if( $type =~ /(photo)/i ){
						$filename = &Upload( $query->param("param".$i."_add".$j) , $query->upload("param".$i."_add".$j) , "photo" , $PrmSub[$i][0] , $PrmSub[$i][1] , $PrmSub[$i][2] , $PrmSub[$i][3] );
					}else{
						$filename = &Upload( $query->param("param".$i."_add".$j) , $query->upload("param".$i."_add".$j) , "file" );
						chmod(0755,"$FileSavePath$filename");
					}
				}
				if( $filename ne "" ){
					$files++;
					$str .= $filename."<>".$query->param("param".$i."_add".$j."t")."<>";
				}
			}
			$line .= $files."<>".$str;
		}
	}
	
	$line .= "\n";
	
	$data_list[$query->param("line")] = $line;
	
	# ��¸
	&SaveLines( $DataFilename , @data_list );
}

# �¤��ؤ�����¸
sub SortList{
	my @order = split( /,/ , shift );
	
	# ��������
	my @data_list = &GetLines( $DataFilename );
	
	my @new_order = ();
	
	while( @order ){
		push( @new_order , $data_list[ shift(@order) ] );
	}
	
	# ��¸
	&SaveLines( $DataFilename , @new_order );
}

# �����ؤ�����¸
sub SwapList{
	my $src = shift;
	my $offset = shift;
	
	# ��������
	my @data_list = &GetLines( $DataFilename );
	
	# ̵�����ä��齪λ
	if( $src+$offset < 0 ){
		return;
	}elsif( $#data_list< $src+$offset ){
		return;
	}
	
	# �����ؤ�
	my $tmp = $data_list[$src+$offset];
	$data_list[$src+$offset] = $data_list[$src];
	$data_list[$src] = $tmp;
	
	# ��¸
	&SaveLines( $DataFilename , @data_list );
}

# ��Ժ��������¸
# argv(0):���������ֹ�
sub DeleteLine{
	my $delete_target = shift;
	my @data_list = &GetLines( $DataFilename );
	
	# �ե�������
	my %data = &LineToHash( $data_list[$delete_target] );
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		my $type = $PrmType[$i];
		if( $type eq "file" ){
			unlink( $FileSavePath.$data{"param".$i} );
		}elsif( $type eq "files" or $type eq "files_with_comment" ){
			my $items = $data{"param".$i};
			for( my $j=0 ; $j<$items ; $j++ ){
				unlink( $FileSavePath.$data{"param".$i."_".$j} );
			}
		}elsif( $type eq "photo" ){
			unlink( $FileSavePath.$data{"param".$i} );
			unlink( $FileSavePath."s_".$data{"param".$i} );
		}elsif( $type eq "photos" or $type eq "files_with_comment" ){
			my $items = $data{"param".$i};
			for( my $j=0 ; $j<$items ; $j++ ){
				unlink( $FileSavePath.$data{"param".$i."_".$j} );
				unlink( $FileSavePath."s_".$data{"param".$i."_".$j} );
			}
		}
	}
	
	# �ǡ������
	splice( @data_list , $delete_target , 1 );
	
	# ��¸
	&SaveLines( $DataFilename , @data_list );
}

# ����ɲä�����¸
sub AddLine{
	my @data_list = &GetLines( $DataFilename );
	
	my $line = "";
	
	# ID
	my $max_id = 0;
	my $list_max = $#data_list;
	if( 0<=$list_max ){
		foreach my $data_line ( @data_list ){
			my %data = &LineToHash( $data_line );
			if( $max_id < $data{"id"}-0 ){
				$max_id = $data{"id"}-0;
			}
		}
		$max_id = $max_id+1;
	}
	$max_id = sprintf( "%04d" , $max_id );
	$line = $max_id."<>";
	
	# ������
	$line = $line."0<>";
	
	# �ѥ�᡼��
	for( my $i=0 ; $i<$PrmCount ; $i++ ){
		my $type = $PrmType[$i];
		#����
		if($type eq "date"){
			$ENV{'TZ'} = "JST-9";
			my $time = time();
			(my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday) = localtime($time);
			my $date = sprintf("%04d$DateJoint%02d$DateJoint%02d",$year + 1900, $mon + 1, $mday);
			$line = $line.$date."<>";

		# ʣ��
		}elsif( $type eq "files" or $type eq "files_with_comment" or $type eq "photos" or $type eq "photos_with_comment" ){
			$line = $line."0<>";
		# �����å��ܥå���
		}elsif( $type eq "checkbox" ){
			my $c_max = 1+$#{$PrmSub[$i]};
			for( my $c=0 ; $c<$c_max ; $c++ ){
				$line .= "0,";
			}
			chop( $line );
			$line .= "<>";
		# ¿�ʥƥ�����
		}elsif( $type eq "texts_set" ){
			$line .= "0<>";
		# ñ��
		}else{
			$line = $line."<>";
		}
	}
	
	# �����
	$line = $line."\n";
	
	# �ɲ�
	unshift( @data_list , $line );
	
	&SaveLines( $DataFilename , @data_list );
}

