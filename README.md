# タイムトラベル仕入れ・オークションゲーム

https://deepwiki.com/tomosud/timetravel

## 概要

プレイヤーが過去にタイムトラベルして商品を仕入れ、現代のオークションで売却して利益を得るWebゲームです。
AIを使ったコーディングの学習をもとに開発中ですよ。

**📋 開発状況**: [PROJECT_STATUS.md](./PROJECT_STATUS.md) | **🛠️ 開発ガイド**: [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)

## クイックスタート

```cmd
run.bat
```

自動で環境構築してゲーム開始。ブラウザで `http://127.0.0.1:5000` にアクセス。

## 動作環境

- Python 3.7以上
- Windows（`venv_win`）/ WSL・Linux（`venv`）対応

## セットアップ・実行方法

### 1. 簡単実行（推奨）

```cmd
run.bat
```

この単一コマンドで以下が自動実行されます：
- 仮想環境の作成（初回のみ）
- 必要パッケージのインストール
- ゲームサーバーの起動

### 2. 手動セットアップ

**Windows環境:**
```cmd
# 仮想環境作成
python -m venv venv_win

# 仮想環境アクティベート
venv_win\Scripts\activate.bat

# 依存関係インストール
pip install -r ./requirements.txt

# ゲーム実行
python ./entry.py
```

**WSL/Linux環境:**
```bash
# 仮想環境作成
python3 -m venv venv

# 仮想環境アクティベート
source venv/bin/activate

# 依存関係インストール
pip install -r ./requirements.txt

# ゲーム実行
python ./entry.py
```

## 使用方法

1. `./run.bat` を実行
2. ブラウザで `http://127.0.0.1:5000` にアクセス
3. ゲーム開始！

## ゲームの流れ

### 基本ループ
1. **購買**: 過去にタイムトラベルして商品取得
2. **売却**: AIオークションで売却益獲得  
3. **成長**: 長期的に投資額の10倍成長を保証

### 現在の特徴
- **大ターン・子ターンシステム**: 8子ターン単位で価格変動
- **価格倍率曲線**: ランダムな緩急で単調性を回避
- **動的AIバイヤー**: 15人が各オークションで新規生成
- **コスト計算**: `(年数 × 距離) × UFOサイズ`

### ゲームオーバー
- 所持金0円 かつ 在庫なし
- 10%確率でタイムトラベル失敗（お金のみ失う）


## 技術仕様

### アーキテクチャ
```
timetravel/
├── core/           # ゲームロジック層
├── api/            # JSON API層
├── web/            # Flask UI層
└── features/       # 機能別詳細仕様
```

### 主要システム
- **3層分離設計**: ロジック・API・UI完全分離
- **価格倍率曲線**: 8子ターンで10倍成長保証
- **動的AIオークション**: 毎回15人の新規バイヤー生成
- **商品システム**: 10ジャンル×3状態×動的レア度

**詳細仕様**: [GAME_SPECIFICATIONS.md](./GAME_SPECIFICATIONS.md)

## ドキュメント構成

### 📖 読む順序
1. **README.md** (このファイル) - プロジェクト概要
2. **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - 現在の開発状況
3. **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)** - 開発方針・環境構築
4. **[GAME_SPECIFICATIONS.md](./GAME_SPECIFICATIONS.md)** - 詳細仕様
5. **[features/](./features/)** - 機能別設計書

### 🔧 開発者向け
- 環境構築: [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)
- 分析資料: [analysis/](./analysis/)
- 技術メモ: [CLAUDE.md](./CLAUDE.md)

---

**バージョン**: v2.0 - フェーズ1完全完了（長期成長保証システム）  
**ライセンス**: MIT  
**次フェーズ**: フェーズ2 - 攻略性・戦略要素導入
