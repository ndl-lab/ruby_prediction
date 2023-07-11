# ruby_prediction(NDLOCR(ver.2)用漢字読み推定モジュール)

NDLOCR(ver.2)用のテキストの漢字の読みを推定するモジュールのリポジトリです。

本プログラムは、全文検索用途のテキスト化のために開発した[ver.1](https://github.com/ndl-lab/ndlocr_cli/tree/ver.1)に対して、視覚障害者等の読み上げ用途にも利用できるよう、国立国会図書館が外部委託して追加開発したプログラムです（委託業者：株式会社モルフォAIソリューションズ）。


事業の詳細については、[令和4年度NDLOCR追加開発事業及び同事業成果に対する改善作業](https://lab.ndl.go.jp/data_set/r4ocr/r4_software/)をご覧ください。

本プログラムは、国立国会図書館がCC BY 4.0ライセンスで公開するものです。詳細については LICENSEをご覧ください。

## 漢字の読み推定
形態素解析器kyteaを用いた漢字の読み推定機能を提供しています。

kyteaのPythonラッパーを使用しているため、kyteaを先にインストールしておく必要があります。
kyteaの導入はhttp://www.phontron.com/kytea/index-ja.html
を参照してください。

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

