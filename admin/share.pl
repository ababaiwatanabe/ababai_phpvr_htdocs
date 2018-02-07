
my $IpFilename	= "./ip.txt";		# 生成するログインIP保存ファイル名
my $IpTimeout	= 60*60*12;		# IPが無効になるまでの秒


###############################################################################
###############################################################################
###############################################################################

# 端数切り上げ
sub ceil{
	my $num = shift;
	my $val = 0;

	$val = 1 if($num > 0 and $num != int($num));
	return int($num + $val);
}


# ファイルサイズ文字列
sub GetFileSize{
	my $file = shift;
	
	if( -d $file ){
		return "";
	}
	
	my $size = ( -s $file );
	$size = &ceil( $size/1024 ) . "";
	
	while($size =~ s/(.*\d)(\d\d\d)/$1,$2/){};
	
	$size = $size . " KB";
	
	return $size;
}

###############################################################################
###############################################################################
###############################################################################

# IPチェック
sub ip_ok{
	if( $IpFilename eq "" ){
		return 1;
	}
	
	if( !(-e $IpFilename) ){
		return 0;
	}
	
	my $ip;
	my $saved_time;
	
	open( DB , "< $IpFilename" );
	&FileLock( *DB );
	$ip = <DB>;
	$saved_time = <DB>;
	&FileUnlock( *DB );
	close( DB );
	
	chop( $ip );
	
	if( $ip ne $ENV{"REMOTE_ADDR"} ){
		return 0;
	}
	if( $IpTimeout ne "" && $IpTimeout < (time()-$saved_time) ){
		return 0;
	}
	return 1;
}

# IP消去
sub DelIP{
	set_ip("");
}

# IP保存
sub SaveIP{
	set_ip( $ENV{"REMOTE_ADDR"} );
}

# IP操作
sub set_ip{
	if( $IpFilename eq "" ){
		return;
	}
	
	my $ip = shift;
	
	open(DB,"> $IpFilename");
	chmod(0600,"$IpFilename");
	&FileLock( *DB );
	seek(DB,0,0);
	print DB "$ip\n";
	print DB time();
	truncate(DB , tell(DB));
	&FileUnlock( *DB );
	close(DB);
}


###############################################################################
### ファイル直接操作 ##########################################################
###############################################################################

# 配列をそのままデータファイルに保存
# argv(0):保存する配列
sub SaveLines{
	my $file = shift;
	my @data_list = @_;
	
	open(DB,"> $file");
	chmod(0600,"$file");
	&FileLock( *DB );
	seek(DB,0,0);
	foreach my $line( @data_list ){
		print DB "$line";
	}
	truncate(DB , tell(DB));
	&FileUnlock( *DB );
	close(DB);
}

# 新着情報をファイルから読み込んで配列でゲトる
sub GetLines{
	my $file = shift;
	my @data_list = ();
	
	open( DB , "< $file" );
	&FileLock( *DB );
	@data_list = <DB>;
	&FileUnlock( *DB );
	close( DB );
	
	return @data_list;
}

###############################################################################
### しょぼいファイルロック ####################################################
###############################################################################

# ファイルロック argv(0):ロックするファイルハンドル *FILE
sub FileLock{
	return 1;
	my $retry = 60*60;
	while( !mkdir("__lockdir__", 0700) ){
		if( --$retry <= 0 ){
			return 0;
		}
		sleep(1);
	}
	flock( $_[0] , 2 );
	return 1;
}

# ファイルアンロック argv(0):アンロックするファイルハンドル *FILE
sub FileUnlock{
	return 1;
	rmdir( "__lockdir__" );
	flock( $_[0] , 8 );
}

1;
