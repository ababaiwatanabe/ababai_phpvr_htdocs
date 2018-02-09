<!DOCTYPE html>
<html lang="ja">
<?php include_once("include_parts/common.php"); ?>
<?php $companyname = '会社名'; ?>
<?php $titletext = '123タイトル'; ?>
<?php $descriptiontext = 'ディスクリプション'; ?>
<?php $keywordstext = 'キーワード'; ?>
<?php $h1text = 'h1テキスト'; ?>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<?php include_once("include_parts/common_meta.php"); ?>
<!--▼　topのみ　下層は削除　▼-->
<meta property="og:type" content="website">
<!--▼　下層はこちら article を使用　▼-->
<!--<meta property="og:type" content="article">-->
<link href="css/page-top.css" rel="stylesheet">

<?php include_once("include_parts/Google_Tag_Manager-A.php"); ?>
</head>


<body>
<?php include_once("include_parts/Google_Tag_Manager-B.php"); ?>


<?php include_once("include_parts/common_header.php"); ?>
<!-- header -->

<?php include_once("include_parts/common_gnavi.php"); ?>
<!-- glnavi -->

<nav class="seo_bread_list clearfix">
<ul class="clearfix" itemscope itemtype="http:/schema.org/BreadcrumbList/">
<li itemprop="itemListElement" itemscope itemtype="http:/schema.org/ListItem/">
<a itemprop="item" href="<?php echo siteURL; ?>/"><span itemprop="name">HOME</span></a>
<meta itemprop="position" content="1" />
</li>
<li itemprop="itemListElement" itemscope itemtype="http:/schema.org/ListItem/">
<link itemprop="item" href="<?php echo pageURL; ?>"><span itemprop="name">&nbsp;>&nbsp;</span>
<meta itemprop="position" content="2" />
</li>
</ul>
</nav> 

<main>
<?php include_once("include_parts/common_side-menu.php"); ?>

	<?php include_once("include_parts/end-bnr.php"); ?>
	
</main><!-- /main -->

<?php include_once("include_parts/common_footer.php"); ?>
<?php include_once("include_parts/common_js.php"); ?>
</body>
</html>