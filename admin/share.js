
function Id(id){
	return document.getElementById(id);
}

var sending = 0;

/*** うー ******************************************************************/

// IE
if (window.attachEvent){
	window.attachEvent("onload", function(){Initialize();});
}

// それ以外
if (window.addEventListener){
	window.addEventListener("load", function(){Initialize();}, false);
}

function Initialize(){
	window.document.onkeydown = function(){
		if( event.keyCode==116 || event.keyCode==86 ){
			//event.keyCode = null;
			//return false;
		}
	}
}

/*** 送信ボタン ************************************************************/

function submit(mode,line){
	if( sending==1 )
		return;
	
	sending = 1;
	
	var arg = [];
	arg.push.apply(arg, arguments);
	
	var form = Id("sender");
	while( arg.length ){
		var input = document.createElement("input");
		input.name = arg.shift();
		input.value = arg.shift();
		form.appendChild(input);
	}
	form.submit();
}

/*** 管理 ******************************************************************/

function move(cgi){
	Id("sender").action = cgi;
	submit();
}


function logout(){
	submit("mode","exit");
}



/*** 各自 ******************************************************************/

/*** 新規 ***/
function add(){
	submit("mode","add");
}

/*** ソート ***/
function sort(id){
	var rows = Id(id).tBodies[0].rows;
	var length = rows.length;
	var str = "";
	for( var i=0 ; i<length ; i++ ){
		str += rows[i].id.substring(4)+",";
	}
	str = str.substr(0,str.length-1);
	
	submit("mode","sort","line",str);
}

/*** 上へ ***/
function up(line){
	if( line==0 )
		return;
	
	submit("mode","up","line",line);
}

/*** 下へ ***/
function down(line){
	if( line==Number(Id("max").value)-1 )
		return;
	
	submit("mode","down","line",line);
}

/*** 削除 ***/
function del(line){
	if( window.confirm("削除してよろしいですか？") ){
		submit("mode","del","line",line);
	}
}

/*** 編集 ***/
function edit(line){
	submit("mode","edit","line",line);
}

/*** 終了 ***/
function exit(){
	submit("mode","exit");
}

/*** 反映 ***/
function update(){
	if( window.confirm("サイトに反映してよろしいですか？") ){
		submit("mode","update");
	}
}

/*** キャンセル ***/
function cancel(){
	submit();
}

/*** 適用 ***/
function apply(line){
	Id("detail").submit();
}



/*** 検索 ***/
function search(table_id,word){
	
	var rows = Id(table_id).tBodies[0].rows;
	var length = rows.length;
	for( var i=0 ; i<length ; i++ ){
		if( rows[i].innerHTML.indexOf(word) < 0 ){
			rows[i].setAttribute("class","unsearched");
			rows[i].className="unsearched";
		}else{
			rows[i].setAttribute("class","");
			rows[i].className="";
		}
	}
	
}

/*** 機種依存文字チェック ***/
function ReplaceInvalidCode( obj ){
	var str = obj.value;
	
    var ngchr = [
        '��','��','��','��','��','��','��','��','��','��','��','��','��','��','��',
        '��','��','��','��','��','��','��','��','��','��','��','��','��','��','��',
        '��','��','��','��','��','��','��','��','��','��','��','��','��','��','��','��',
        '��','��','��','��','��','��','��','��',
        '��','��','��','��','��','��','��','��','��','��','��','��','��','��','��','��','‐','−'
    ];
    var trnchr = [
        '(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)','(10)','(11)','(12)','(13)','(14)','(15)',
        '(16)','(17)','(18)','(19)','(20)','I','II','III','IV','V','VI','VII','VIII','IX','X',
        'ミリ','キロ','センチ','メートル','グラム','トン','アール','ヘクタール','リットル','ワット','カロリー','ドル','セント','パーセント','ミリバール','ページ',
        'mm','cm','km','mg','kg','cc','m2','平成',
        '「','」','No.','K.K.','TEL','(上)','(中)','(下)','(左)','(右)','(株)','(有)','(代)','明治','大正','昭和','-','-'
    ];
    for(var i=0; i<ngchr.length;i++){
    	var regexp = new RegExp( ngchr[i] , 'gm' );
        str = str.replace( regexp , trnchr[i] );
    }
    
    obj.value = str;
}

/*** ジャンル切り替え時 ***/
function genre_change(){
	var genre = Id("genre").value;
	for( var i=0 ; i<param_count ; i++ ){
		var obj = Id("param"+i);
		// 単品
		if( obj!=null ){
			if( enable[i][genre] ){
				obj.disabled = false;
				obj.style.backgroundColor = "white";
			}else{
				obj.disabled = true;
				obj.style.backgroundColor = "silver";
				if( obj.type=="checkbox" )	obj.checked = false;
				else						obj.value = "";
			}
		// 複数
		}else{
			var j=0;
			while( null!=(obj=Id("param"+i+"_add"+j)) ){
				if( enable[i][genre] ){
					obj.disabled = false;
					obj.style.backgroundColor = "white";
				}else{
					obj.disabled = true;
					obj.style.backgroundColor = "silver";
					obj.value = "";
				}
				j++;
			}
			j=0;
			while( null!=(obj=Id("param"+i+"_add"+j+"t")) ){
				if( enable[i][genre] ){
					obj.disabled = false;
					obj.style.backgroundColor = "white";
				}else{
					obj.disabled = true;
					obj.style.backgroundColor = "silver";
					obj.value = "";
				}
				j++;
			}
			j=0;
			while( null!=(obj=Id("param"+i+"_"+j)) ){
				if( enable[i][genre] ){
					obj.disabled = false;
					obj.style.backgroundColor = "white";
				}else{
					obj.disabled = true;
					obj.style.backgroundColor = "silver";
					obj.checked = false;
				}
				j++;
			}
		}
		var line = Id("line"+i);
		if( enable[i][genre] ){
			line.style.display = "";
		}else{
			line.style.display = "none";
		}
	}
}

/*** カラム追加時 ***/
function column_add(line,index,cols){
	if( Id("param"+line+"_"+index+"_"+"0").value == "" )
		return;
	
	Id("param_add_count"+line).value = Number( Id("param_add_count"+line).value )+1;
	
	for( var i=0 ; i<cols ; i++ )
		Id("param"+line+"_"+index+"_"+i).onchange = null;
	
	var new_index = index-0+1;
	
	var br = document.createElement("br");
	Id("area"+line).appendChild(br);
	
	for( var i=0 ; i<cols ; i++ ){
		var f = document.createElement("input");
		f.id = "param"+line+"_"+new_index+"_"+i;
		f.name = "param"+line+"_"+new_index+"_"+i;
		f.setAttribute("type","text");
		f.setAttribute("size","20");
		
		f.style.width = Id("param"+line+"_"+index+"_"+i).style.width;
		
		(function(l,m,n){
			f.onchange = function(){
				column_add(l,m,n);
			};
		})(line,new_index,cols);
		
		Id("area"+line).appendChild(f);
		
		var newText = document.createTextNode("\n");
		Id("area"+line).appendChild(newText);
	}
}

/*** ファイル追加時 ***/
function upload_add(line,index,text){
	if( Byte2Check(line,index) )
		return;
	
	if( Id("param"+line+"_add"+index).value == "" )
		return;
	
	Id("param_add_count"+line).value = Number( Id("param_add_count"+line).value )+1;
	
	Id("param"+line+"_add"+index).onchange = null;
	
	var new_index = index-0+1;
	
	var f = document.createElement("input");
	f.id = "param"+line+"_add"+new_index;
	f.name = "param"+line+"_add"+new_index;
	f.setAttribute("type","file");
	f.setAttribute("size","140");
	f.setAttribute("class","file_up");
	f.setAttribute("className","file_up");
	
	(function(l,m,n){
		f.onchange = function(){
			upload_add(l,m,n);
		};
	})(line,new_index,text);
	
	Id("area"+line).appendChild(f);
	
	if( !text )
		return;
	
	var t = document.createElement("input");
	t.id = "param"+line+"_add"+new_index+"t";
	t.name = "param"+line+"_add"+new_index+"t";
	t.setAttribute("type","text");
	t.setAttribute("size","50");
	
	Id("area"+line).appendChild(t);
}

/*** 全角チェック ***/
function CheckLength(str,flg) {
	for (var i = 0; i < str.length; i++) {
		var c = str.charCodeAt(i);
		if ( (c >= 0x0 && c < 0x81) || (c == 0xf8f0) || (c >= 0xff61 && c < 0xffa0) || (c >= 0xf8f1 && c < 0xf8f4)) {
			if(!flg) return true;
		}else{
			if(flg) return true;
		}
	}
	return false;
}

function Byte2Check(param,index){
	var obj;
	if( index<0 ){
		obj = Id("param"+param);
	}else{
		obj = Id("param"+param+"_add"+index);
	}
	
	var check = obj.value.split( "\\" ).pop();
	
	if( CheckLength(check,1) ){
		alert("全角文字を含むファイルはアップロードできません。\nファイル名を半角文字に変更してください。");
		obj.value = "";
		return true;
	}
	return false;
}

function AppendInput(src,countbox_id){
	src.onchange = null;
	var id = src.id;
	var next_index = Id(countbox_id).value;
	var append_to = src.parentElement;
	
	var separate = id.match(/(\D+)(\d+)(\D+)(\d+)/);
	var id_str = RegExp.$1+RegExp.$2+RegExp.$3;
	
	var input = document.createElement("input");
	input.id = id_str+next_index;
	input.name = id_str+next_index;
	input.setAttribute("type","text");
	input.setAttribute("size","50");
	(function(l,m){
		input.onchange = function(){
			AppendInput(l,m);
		};
	})(input,countbox);
	
	
	append_to.appendChild(input);
	
	next_index++;
	Id(countbox_id).value = next_index;
	
}

/* ファイル順序 */

function file_swap(param,src_index){
	
	if( src_index==0 )
		return;
	
	var dst_index = src_index-1;
	
	var src_file;
	var dst_file;
	var src_text;
	var dst_text;
	
	if( document.getElementById("file"+param+"_"+src_index).tagName.match(/img/i) ){
		src_file = document.getElementById("file"+param+"_"+src_index).src;
		dst_file = document.getElementById("file"+param+"_"+dst_index).src;
		document.getElementById("file"+param+"_"+src_index).src = dst_file;
		document.getElementById("file"+param+"_"+dst_index).src = src_file;
	}else{
		src_file = document.getElementById("file"+param+"_"+src_index).href;
		dst_file = document.getElementById("file"+param+"_"+dst_index).href;
		src_text = document.getElementById("file"+param+"_"+src_index).innerHTML;
		dst_text = document.getElementById("file"+param+"_"+dst_index).innerHTML;
		document.getElementById("file"+param+"_"+src_index).href = dst_file;
		document.getElementById("file"+param+"_"+dst_index).href = src_file;
		document.getElementById("file"+param+"_"+src_index).innerHTML = dst_text;
		document.getElementById("file"+param+"_"+dst_index).innerHTML = src_text;
	}
	if( document.getElementById("param"+param+"_"+src_index+"t") ){
		var src_comment = document.getElementById("param"+param+"_"+src_index+"t").value;
		var dst_comment = document.getElementById("param"+param+"_"+dst_index+"t").value;
		document.getElementById("param"+param+"_"+src_index+"t").value = dst_comment;
		document.getElementById("param"+param+"_"+dst_index+"t").value = src_comment;
	}
	
	var src_data = document.getElementById("param"+param+"_"+src_index+"_file").value;
	var dst_data = document.getElementById("param"+param+"_"+dst_index+"_file").value;
	document.getElementById("param"+param+"_"+src_index+"_file").value = dst_data;
	document.getElementById("param"+param+"_"+dst_index+"_file").value = src_data;
}

/*** SEO *********************************************************************/

function edit_flag(index){
	document.getElementById("e"+index).value = "1";
	
}


/*** カレンダー **************************************************************/


/*** 買い物籠 ****************************************************************/

/*** 規格追加 ***/
function ver_add(obj,line){
	if( obj.value == "" )
		return;
	
	Id("ver_count").value = Number( Id("ver_count").value )+1;
	
	var new_line = line-0+1;
	
	add_input("veriety",new_line);
	add_input("price",new_line);
	add_input("stock",new_line).value="999999";
	add_input("order",new_line).value="0";
	add_input("point",new_line).value="0";
}

function add_input(type,new_line){
	
	var old=new_line-1;
	Id(type+old).onchange = null;
	
	var input = document.createElement("input");
	
	var input = document.createElement("input");
	(function(n){
		input.onchange = function(){
			ver_add(input,n);
		};
	})(new_line);
	
	input.setAttribute("type","input");
	input.style.width = "60px";
	
	input.id = type+new_line;
	input.name = type+new_line;
	Id(type+"_area").appendChild( document.createTextNode("\n") );
	Id(type+"_area").appendChild(input);
	
	return input;
}


/*** メルマガ ****************************************************************/


/*** 追加 ***/
function add_user(){
	Id("add_user").submit();
}

/*** 削除 ***/
function del_user(line){
	if( window.confirm("削除してよろしいですか？") ){
		submit("mode","del_user","line",line);
	}
}

function mail_edit(line){
	submit("mode","edit_mail","line",line);
}

function mail_del(line){
	if( window.confirm("削除してよろしいですか？") ){
		submit("mode","del_mail","line",line);
	}
}

function sendmail_del(line){
	if( window.confirm("削除してよろしいですか？") ){
		submit("mode","del_sendmail","line",line);
	}
}

function mail_save(){
	var error = "";
	
	if( Id("title").value == "" ){
		error += "タイトルが入力されていません\n";
	}
	if( Id("header").value == "" ){
		error += "ヘッダが入力されていません\n";
	}
	if( Id("content").value == "" ){
		error += "本文が入力されていません\n";
	}
	if( Id("footer").value == "" ){
		error += "フッタが入力されていません\n";
	}
	
	var ry = Id("reserve_y").value;
	var rm = Id("reserve_m").value;
	var rd = Id("reserve_d").value;
	var rh = Id("reserve_h").value;
	if( ry.length+rm.length+rd.length+rh.length != 0 ){
		if( ry.length*rm.length*rd.length*rh.length == 0 ){
			error += "未入力の日時があります\n";
		}
		if( isNaN(ry) || isNaN(rm) || isNaN(rd) || isNaN(rh) ){
			error += "日時が数字になっていません\n";
		}
	}
	
	if( error != "" ){
		alert( error );
	}else{
		Id("mail_save").submit();
	}
	
}

function birth_save(){
	Id("mail_birth").submit();
}
