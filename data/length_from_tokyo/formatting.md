raw_dataフォルダのdataを整形するToolを作成してここに置く
このフォルダに整形したdataを置く。

-----
整形する

raw_data\worldcities.csv
上記を読み。Tokyoからの距離（km）と都市名など整形と項目を削減したcsvにする。

距離（length）はlat　lng　の値を緯度経度として取得し、Tokyoのそれからの距離を計算してkmを数値として入れる。小数点以下は切り捨てる。

項目と内容は後述する。

結果をこのフォルダに、length_from_tokyo.csvとして書き出す。


■data構造
"city","city_ascii","lat","lng","country","iso2","iso3","admin_name","capital","population","id"
"Tokyo","Tokyo","35.6850","139.7514","Japan","JP","JPN","Tōkyō","primary","35676000","1392685764"
"New York","New York","40.6943","-73.9249","United States","US","USA","New York","","19354922.0","1840034016"
"Mexico City","Mexico City","19.4424","-99.1310","Mexico","MX","MEX","Ciudad de México","primary","19028000","1484247881"
"Mumbai","Mumbai","19.0170","72.8570","India","IN","IND","Mahārāshtra","admin","18978000","1356226629"
"São Paulo","Sao Paulo","-23.5587","-46.6250","Brazil","BR","BRA","São Paulo","admin","18845000","1076532519"
-----

■項目と内容
length:計算して作成。
city_ascii：そのまま使用する
country：そのまま使用する
population：そのまま使用する

書き出すデータはlengthでソートしてから出力する事。