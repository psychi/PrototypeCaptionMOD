# PrototypeCaptionMOD users manual in japanese

## PrototypeCaptionMODの機能と目的
PrototypeCaptionMODは、Activision社から発売されているWindows用ビデオゲーム『PROTOTYPE』で使う字幕ファイルとフォントファイルを書き換えることができます。英語字幕から日本語字幕に書き換えることを、主な目的としています。

## PrototypeCaptionMODの使用上の注意
**PrototypeCaptionMODの動作はまだ十分に検証されていない**ため、取り返しのつかないトラブルを発生させてしまうことがあるかもしれません。**動作の結果を自己責任で対応**できる方のみ、PrototypeCaptionMODを使用してください。

## PrototypeCaptionMODのインストールの手順

### 1. 『PROTOTYPE』のインストール
Windows用『PROTOTYPE』を任意のディレクトリにインストールしてください。以後このディレクトリを"**Prototype/**"と表記します。

### 2. Prototype日本語化MODの入手
[Prototype（プロトタイプ）@wiki - MOD導入方法](http://www19.atwiki.jp/protot/pages/92.html)から、[日本語化MOD](http://www.mediafire.com/?9b5z68bljjttddv)をダウンロードして下さい。
ダウンロードした圧縮ファイルを任意のディレクトリに展開してください。以後このディレクトリを"**Prototype日本語化MOD/**"と表記します。

### 3. 『PROTOTYPE』データファイルの展開
『PROTOTYPE』が読み込むデータを編集できるようにするため、以下に示したパスにある8個のrcfファイルを展開してください。

* "Prototype/00audio.rcf"
* "Prototype/00woi.rcf"
* "Prototype/01audio.rcf"
* "Prototype/01woi.rcf"
* "Prototype/02woi.rcf"
* "Prototype/03woi.rcf"
* "Prototype/art.rcf"
* "Prototype/movies.rcf"

rcfファイルを展開するには、以下の手順に従ってください。

1. "Prototype日本語化MOD/ScarfaceExplorer/ScarfaceExplorer.exe"を、ファイルエクスプローラでダブルクリックし、起動してください。
2. ScarfaceExplorerのメニューバーから「File」→「Open」を選択し、ファイルダイアログでrcfファイルを選択してください。
3. ScarfaceExplorerのメニューバーから「Extract」→「All Files」を選択し、ファイルダイアログで"**Prototype/**"を選択してください。
4. 展開した元のrcfファイルのファイル名を変更してください。元のrcfファイルがなければ、展開されたファイルを読み込むようになるからです。

8個すべてのrcfファイルを展開しファイル名を変更した状態で、『PROTOTYPE』が起動するのを確認してください。

### 4. 虐杀原形 素材编辑工具第二版の入手
虐杀原形 素材编辑工具第二版は、『PROTOTYPE』のデータ全般を書き換えるためのツールのようですが、詳細は不明です。  
[《虐杀原形》素材编辑工具第二版下载_游戏工具_4391单机网](http://www.4391.com/9/2529.html)にあるリンク「电信下载1」から、圧縮ファイル"[《虐杀原形》素材编辑工具第二版.rar](http://2.4391.com/%E6%B8%B8%E6%88%8F%E5%B7%A5%E5%85%B7/%E3%80%8A%E8%99%90%E6%9D%80%E5%8E%9F%E5%BD%A2%E3%80%8B%E7%B4%A0%E6%9D%90%E7%BC%96%E8%BE%91%E5%B7%A5%E5%85%B7%E7%AC%AC%E4%BA%8C%E7%89%88.rar)"をダウンロードできるようです。  
ダウンロードした圧縮ファイルを任意のディレクトリに展開してください。以後このディレクトリを"**《虐杀原形》素材编辑工具第二版/**"と表記します。

### 5. PrototypeCaptionMODの入手
[PrototypeCaptionMOD - GitHub](https://github.com/psychi/PrototypeCaptionMOD)にある「Download」ボタンを押して、圧縮ファイルをダウンロードして下さい。  
ダウンロードする圧縮ファイルはzip形式とtar.gz形式を選べますが、どちらをダウンロードしても構いません。  
ダウンロードした圧縮ファイルを任意のディレクトリに展開してください。以後このディレクトリを"**PrototypeCaptionMOD/**"と表記します。

### 6. PrototypeCaptionMODに必要なファイルをコピー
以下に示したパスにある6個のファイルを、"**PrototypeCaptionMOD/**"の直下にコピーしてください。

* "Prototype日本語化MOD/offzip/**offzip.exe**"
* "Prototype日本語化MOD/ProtoLE/**ProtoLE.exe**"
* "Prototype日本語化MOD/フォント/フォント作成用/**swfmill.exe**"
* "Prototype日本語化MOD/フォント/フォント作成用/**ipagp.ttf**"
* "Prototype日本語化MOD/フォント/フォント作成用/**IPAPGothic_Bold.ttf**"
* "《虐杀原形》素材编辑工具第二版/Prototype_DDS_Trainer/**PackageManager.exe**"

以上で、PrototypeCaptionMODのインストールは完了です。

## 『PROTOTYPE』の字幕を日本語化する手順

### 1. データをコピー
以下に示したパスにある3個のディレクトリを、"**PrototypeCaptionMOD/**"の直下にコピーしてください。

* "Prototype/**art**"
* "Prototype/**Audio**"
* "Prototype/**movie**"

### 2. 字幕のテキストとフォントを日本語に書き換える
"PrototypeCaptionMOD/BuildCaptionsAndFonts.bat"をファイルエクスプローラでダブルクリックし、実行が終了するまで待機してください。

### 3. 書き換えたデータをコピー
以下に示したパスにある3個のディレクトリを、"**Prototype/**"の直下にコピーしてください。

* "PrototypeCaptionMOD/**art**"
* "PrototypeCaptionMOD/**Audio**"
* "PrototypeCaptionMOD/**movie**"

以上で、『PROTOTYPE』の字幕が日本語で表示されるようになります。『PROTOTYPE』を起動し、ゲーム設定で字幕の表示をONにするのを忘れないでください。

## 『PROTOTYPE』の字幕を日本語に翻訳する作業のお願い
現在、『PROTOTYPE』の字幕を日本語に翻訳する作業は途中となっています。

より多くの方に翻訳作業を手伝っていただけるよう、原文と訳文の一覧を記述したスプレッドシートを[PrototypeCaptionMOD - Google ドキュメント](https://docs.google.com/spreadsheet/ccc?key=0AgVoxoyqR4aEdGFDVzVFRVVUdENDaUp6RGszX19kR3c&hl=ja#gid=1)に用意し、どなたにでも編集できる状態にしています。翻訳に協力していただける方は、このスプレッドシートを編集して、英文を日本語に翻訳してみてください。

編集したスプレッドシートは、以下の手順で『PROTOTYPE』に反映させることができます。

1. Googleドキュメントのスプレッドシートの下部にある「captions」タグを選択してください。
2. Googleドキュメントのメニューバーにある「ファイル」から、「形式を指定してダウンロード」→「CSV（現在のシート）」を選択し、CSVファイルをダウンロードして下さい。
3. ダウンロードしたCSVファイルを、"PrototypeCaptionMOD/PrototypeCaptionMOD.csv"にコピーしてください。
4. 前節の**『PROTOTYPE』の字幕を日本語化する手順**に従って作業をしてください。
