# 📖 ドキュメント読み方ガイド

## 目的別読み方

### 🚀 初回セットアップ・ゲーム体験
1. **[README.md](./README.md)** - プロジェクト概要とクイックスタート
2. **[CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)** - 環境構築（必要時のみ）

### 📊 現在の開発状況を知りたい
1. **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - 開発状況の全体像
2. **[features/](./features/)** - 機能別の詳細進捗

### 🔧 開発に参加したい
1. **[README.md](./README.md)** - プロジェクト概要
2. **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - 現在の状況
3. **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)** - 開発方針・ルール
4. **[GAME_SPECIFICATIONS.md](./GAME_SPECIFICATIONS.md)** - 詳細仕様

### 🎮 ゲーム仕様を詳しく知りたい
1. **[README.md](./README.md)** - 基本ルール
2. **[GAME_SPECIFICATIONS.md](./GAME_SPECIFICATIONS.md)** - 詳細仕様・変更履歴
3. **[features/game_cycle_system.md](./features/game_cycle_system.md)** - 価格曲線システム

### 🐛 バグ修正・機能改善
1. **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - 未解決課題確認
2. **[features/](./features/)** - 該当機能の詳細仕様
3. **[analysis/](./analysis/)** - 関連分析資料

---

## ファイル役割一覧

### レベル1: エントリーポイント
| ファイル | 役割 | 読者 |
|---------|------|------|
| **README.md** | プロジェクト概要・使い方 | 全員 |

### レベル2: 開発者向け
| ファイル | 役割 | 読者 |
|---------|------|------|
| **PROJECT_STATUS.md** | 開発状況の一元管理 | 開発者 |
| **DEVELOPMENT_GUIDE.md** | 開発方針・ルール・環境 | 開発者 |

### レベル3: 詳細仕様
| ファイル | 役割 | 読者 |
|---------|------|------|
| **GAME_SPECIFICATIONS.md** | ゲーム仕様・変更履歴 | 実装者 |
| **features/game_cycle_system.md** | 価格曲線システム詳細 | 実装者 |

### レベル4: 技術・分析資料
| ファイル | 役割 | 読者 |
|---------|------|------|
| **CROSS_PLATFORM_PYTHON_SETUP.md** | 環境構築専用 | 開発者 |
| **analysis/buy_balance_analysis.md** | バランス分析・改善履歴 | 設計者 |
| **CLAUDE.md** | 開発時の技術メモ | 開発者 |

---

## 更新頻度と責任

### 高頻度更新（開発時毎回）
- **PROJECT_STATUS.md** - 開発進捗・課題状況
- **features/○○.md** - 機能実装状況

### 中頻度更新（仕様変更時）
- **README.md** - ゲーム基本仕様
- **GAME_SPECIFICATIONS.md** - 詳細仕様

### 低頻度更新（方針変更時）
- **DEVELOPMENT_GUIDE.md** - 開発方針・ルール

### 単発更新
- **CROSS_PLATFORM_PYTHON_SETUP.md** - 環境構築手順

---

## 情報の一元化ルール

### ✅ 単一責任
- 1つの情報は1つのファイルで管理
- 他ファイルは参照リンクのみ

### ✅ 階層化
- 概要 → 詳細の順で情報を配置
- レベル別にファイルを分離

### ✅ 最新性
- 仕様変更時は関連ファイルを同期更新
- 古い情報は削除またはアーカイブ化

---

**最終更新**: 2025-06-21  
**次回更新予定**: ドキュメント構造変更時