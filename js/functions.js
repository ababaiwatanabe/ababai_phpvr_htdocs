/*+++++-----------------------------------
   ページ内スクロール
-----------------------------------+++++*/


$(function(){
   // #で始まるアンカーをクリックした場合に処理
   $('a[href^=#]').click(function() {
      // スクロールの速度
      var speed = 800; // ミリ秒
      // アンカーの値取得
      var href= $(this).attr("href");
      // 移動先を取得
      var target = $(href == "#" || href == "" ? 'html' : href);
      // 移動先を数値で取得
      var position = target.offset().top;
      // スムーススクロール
      $('body,html').animate({scrollTop:position}, speed, 'swing');
      return false;
   });
});


// remap jQuery to $
(function($){

	$(function(){
	$('a img').hover(
		function(){$(this).fadeTo(200, 0.8).fadeTo(400, 0.8);},
		function(){$(this).fadeTo('fast', 1.0);}
	);	
});

	
/* スマホ tel */
$(function(){
var device = navigator.userAgent;
if((device.indexOf('iPhone') > 0 && device.indexOf('iPad') == -1) || device.indexOf('iPod') > 0 || device.indexOf('Android') > 0){
$(".sp-tel-link").wrap('<a href="tel:0120-00-0000"></a>');
}
});
	

/* page-top */
$(document).ready(function(){
    var showFlag = false;
    var topBtn = $('#pagetop');    
    topBtn.css('bottom', '-200px');
    var showFlag = false;
    //スクロールが100に達したらボタン表示
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            if (showFlag == false) {
                showFlag = true;
                topBtn.stop().animate({'bottom' : '90px'}, 200); 
            }
        } else {
            if (showFlag) {
                showFlag = false;
                topBtn.stop().animate({'bottom' : '-200px'}, 200); 
            }
        }
    });
    //スクロールしてトップ
    topBtn.click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 500);
        return false;
    });
});

})(window.jQuery);