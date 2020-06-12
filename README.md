画像の人の部分にモザイクをかけるアプリです。PythonのHTTPサーバーで動きます。

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

png画像を受け取り、256×256のサイズのモザイク処理済画像を出力します。
