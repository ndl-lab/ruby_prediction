# ruby_prediction

NDLOCR(version2)用のテキストの漢字の読みを推定するモジュールのリポジトリです。

本プログラムは、国立国会図書館が株式会社モルフォAIソリューションズに委託して作成したものです。

本プログラムは、国立国会図書館がCC BY 4.0ライセンスで公開するものです。詳細については LICENSEをご覧ください。

## 漢字の読み推定
形態素解析器kyteaを用いた漢字の読み推定。
kyteaの導入はhttp://www.phontron.com/kytea/index-ja.html こちらを参照。
pythonラッパーでkyteaを使用しているため、kyteaを先にインストールしておく必要がある.

```
python output_ruby.py path/to/hogehoge.xml 
```

## 対応入力形式

* xmlファイル　
* xmlファイルが入ったディレクトリ。
#### ディレクトリで入力する時のファイル構成
```
input_directory
├── hogehoge0.xml 
├── hogehoge1.xml
... 
```
## オプション

-t,--timetest
 処理速度測定

使用しているライブラリはrequirments.txtを参照。
