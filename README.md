画像の人の部分にモザイクをかけるアプリです。HTTPサーバーで動かしています。
png画像を受け取り、256×256のサイズのモザイク処理済画像を出力します。

![1](https://user-images.githubusercontent.com/45190789/84501767-0db12e00-acf2-11ea-992b-b8dacf15a7df.jpg)
![2](https://user-images.githubusercontent.com/45190789/84501774-10ac1e80-acf2-11ea-84b6-327ea56d6613.jpg)

# Requirements

```
torch
torchvision
argparse
numpy
```

# Overview

## サーバーの起動
```python
python app.py
```

## ページへのアクセス
```
localhost:8000/index
```

## セグメンテーション
pascal_vocデータセットをセマンティックセグメンテーションするように学習されたモデル(``model.pth``、  https://github.com/Tatsuya1112/pytorch_VOC_Segmentation　のコードを実行することにより得られるモデル)を使用して、一度入力画像をセマンティックセグメンテーション(21分類)します。その後21分類から人か人以外かの2分類に変換します。

## モザイク
人に分類されたピクセルは近傍のピクセルの平均値に置き換えられます。
