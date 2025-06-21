# タイムトラベル仕入れ・オークションゲーム

**更新条件**: ゲームの概要・クイックスタート方法・基本ゲームフローの変更時

https://deepwiki.com/tomosud/timetravel

## 概要

プレイヤーが過去にタイムトラベルして商品を仕入れ、現代のオークションで売却して利益を得るWebゲームです。
AIを使ったコーディングの学習のために開発中ですよ。
Privateで公開する価値のないリポジトリですが、よくわかんなくなったのでDeepwikiで読んでみたいので一旦公開しています。

**📋 開発状況**: [DEVELOPMENT_ENTRY.md](./DEVELOPMENT_ENTRY.md) | **🛠️ 開発ガイド**: [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)

## クイックスタート

```cmd
run.bat
```

自動で環境構築してゲーム開始。ブラウザで `http://127.0.0.1:5000` にアクセス。

## 動作環境

- Python 3.7以上
- Windows（`venv_win`）/ WSL・Linux（`venv`）対応

## セットアップ・実行方法

### クイック実行
```cmd
run.bat
```

詳細なセットアップ手順: [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)

## 使用方法

1. `./run.bat` を実行
2. ブラウザで `http://127.0.0.1:5000` にアクセス（自動で購買ページにリダイレクト）
3. ゲーム開始！

## ゲームの流れ

### 基本ループ
1. **購買**: 過去にタイムトラベルして商品取得
2. **売却**: AIオークションで売却益獲得  
3. **成長**: 価格倍率曲線により**1～10倍**の可変成長

### 現在の特徴
- **大ターン・子ターンシステム**: 8子ターン単位で価格変動
- **価格倍率曲線**: ランダムな緩急で単調性を回避
- **動的AIバイヤー**: 15人が各オークションで新規生成
- **コスト計算**: `年数 × 距離`

### ゲームオーバー
- 所持金0円 かつ 在庫なし
- 10%確率でタイムトラベル失敗（お金のみ失う）※現状は一時停止


## 技術仕様

### アーキテクチャ
3層分離設計（core/api/templates）による将来のUI切り替え対応

**詳細仕様**: [CURRENT_SPECIFICATIONS.md](./CURRENT_SPECIFICATIONS.md)

## ドキュメント構成

### 📖 プレイヤー・初回利用者向け
1. **README.md** (このファイル) - プロジェクト概要・クイックスタート

### 📖 開発者向け - 読む順序
1. **[DEVELOPMENT_ENTRY.md](./DEVELOPMENT_ENTRY.md)** - 開発の入り口・現在状況
2. **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)** - 開発方針・ルール・環境構築
3. **[CURRENT_SPECIFICATIONS.md](./CURRENT_SPECIFICATIONS.md)** - 現在の実装仕様詳細

### 📖 参考資料
- **[DEVELOPMENT_HISTORY.md](./DEVELOPMENT_HISTORY.md)** - 完了フェーズの開発履歴
- **[CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)** - 環境構築詳細

### 🔧 開発ツール
- **[tools/](./tools/)** - テスト・デバッグ・分析ツール

---
