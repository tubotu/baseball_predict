# baseball_predict

 http://npb.jp を対象にクローイング・スクレイピングを行い、得られたデータを基に日本のプロ野球の勝敗予測を行う。
 予測に使える情報はその予測する試合の前日までの試合の情報とする。
 現在は下のデータを用いて学習用のデータセットを作成中。
 
## game_result_yyyy.csv
その年のすべての試合結果に関するcsv。game_result_crawling.pyで取得。
2018以降ページの構成が少し変わっているので2018以降は2018の方を用いる。
headerの説明に関してはheader_explanation.txtを参照。

## personal_achivements2.csv
プレイヤーの個人成績に関するcsv。player_crawling.pyで取得。

## Untitled.ipynb
適当に分析しているnotebook。乱雑で成形されてないです、ごめんなさい。
そもそもipynb投げてるのあかんのわかっているので近いうちに消してモジュールごとにちゃんと分けた.pyファイルにします。
