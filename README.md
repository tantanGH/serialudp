# serialudp

RS232C/UART serial communication gateway over UDP

---

## About This

これはPythonで実装された RS232C/UART シリアル通信を UDP を使ってIPネットワーク越しに転送するためのゲートウェイサーバアプリケーションです。
主たるユースケースとして、RS232Cクロス通信を使うレトロPCの通信対戦ゲームをLAN、あるいはインターネット越しに実現することを想定しています。

Pythonで書かれているため、IPネットワークに接続されたPythonが動作する環境であればLinux,macOSなどOSを問わずに動かすことができます。
ただし、Windows OSでは動作しないかもしれません。(selectorsを使っているため)

以下の説明では X680x0 のRS232Cクロス接続対戦ゲームを Raspberry Pi を使用してIPネットワーク越しに行う前提で記述してあります。適宜読み替えてください。

---

## 準備するもの

以下の構成が通信相手と自分と双方に必要です。

- ケーブル
  - RS232Cクロスケーブル(25pin-9pin)
  - USB-Serial変換ケーブル

- Raspberry Pi 3A+/3B+/4B のいずれか (2/Zeroは所有していないので未検証)
  - Raspberry Pi OS が導入済であること (最新の32bit OS Liteでのみ検証)
  - インターネットに接続されていること
  - USB-SerialおyびRS232CクロスケーブルでX680x0実機と接続されていること
  - `/dev/ttyUSB0` が見えていること

- X680x0 実機
  - RS232CクロスケーブルおよびUSB-SerialケーブルでRaspberry Piと接続されていること
  - 通信対戦をサポートした市販ゲームソフト(以下ではポピュラスを使用)

---

## インストール

Raspberry Pi にpiユーザでloginし、pipが導入されていなければ導入する。

    sudo apt-get install python3-pip

serialudp をこのGitリポジトリから導入する。

    pip install git+https://github.com/tantanGH/serialudp.git

コマンドラインで `serialudp` が使えることを確認する。

    serialudp -h

同じことを双方の Raspberry Pi で実施しておく。

---

## 使い方 (X680x0 ポピュラスの例)



---

## 変更履歴

- 0.1.0 (2023/07/23) ... 初版

