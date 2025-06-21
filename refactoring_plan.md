# ドキュメント・コード整理計画

**作成日**: 2025-06-21  
**目的**: ドキュメントと実装の乖離解消、開発再開の容易化  
**完了時**: このファイルは削除する

## 整理対象の問題

### 1. 重大な乖離
- **UFOサイズシステム**: ドキュメントに詳細記載、実装では完全廃止済み
- **開発フェーズ**: ドキュメント「フェーズ1完了」、実装「フェーズ2.3完了」
- **価格システム**: ドキュメント「固定10倍」、実装「可変1-10倍+固定費」

### 2. ファイル散乱
- テストファイルがルートディレクトリに散乱
- 古い不要ファイル（run_cli.*）が残存
- ドキュメントが多数あり階層が不明確

## 作業順序

### フェーズ1: 緊急修正（HIGH優先度）
1. ✅ **refactoring_plan.md作成** - 作業記録用
2. ⏳ **UFOサイズ関連記述の完全削除**
3. ⏳ **フェーズ進捗状況の正確な更新**
4. ⏳ **価格・固定費システムの記述統一**

### フェーズ2: 構造整理（MEDIUM優先度）
5. ⏳ **テストファイルのdebug/フォルダ移動**
6. ⏳ **ドキュメント構造の再編成**

### フェーズ3: 最終整理（LOW優先度）
7. ⏳ **refactoring_plan.mdの削除**

## 決定事項記録

### コーディングルール
- **現状の実装を各文書に記載する**（実装優先）
- 重複記述は統一・削除
- 実装と矛盾する記述は実装に合わせて修正
- 古い仕様は履歴として残すが現在仕様と明確に分離

### 例外ファイル（そのまま残す）
- CROSS_PLATFORM_PYTHON_SETUP.md

### ドキュメント方針
- **現在仕様**: 1つのファイルに集約
- **開発履歴**: 別ファイルでアーカイブ
- **開発ガイド**: 手順・環境構築のみ

## 全ドキュメント分析

### レベル1: エントリーポイント
| ファイル | 現状 | 問題 | 提案 |
|---------|------|------|------|
| **README.md** | プロジェクト概要 | UFOサイズ記述あり | 現在実装に更新 |

### レベル2: 開発者向け
| ファイル | 現状 | 問題 | 提案 |
|---------|------|------|------|
| **PROJECT_STATUS.md** | フェーズ1完了状況 | フェーズ2.3未反映 | 最新状況に更新 |
| **DEVELOPMENT_GUIDE.md** | 開発方針・環境 | 確認が必要 | 内容確認後判断 |
| **READING_GUIDE.md** | ドキュメント構造 | 良い構造 | 参考にして整理 |

### レベル3: 詳細仕様
| ファイル | 現状 | 問題 | 提案 |
|---------|------|------|------|
| **GAME_SPECIFICATIONS.md** | 詳細仕様 | UFOサイズ等古い仕様 | 現在仕様に整理 |
| **features/game_cycle_system.md** | 価格曲線詳細 | フェーズ1仕様 | フェーズ2.3仕様に更新 |
| **features/game_cycle_phase2.md** | フェーズ2仕様 | 内容確認必要 | 確認後統合検討 |

### レベル4: 履歴・完了サマリー
| ファイル | 現状 | 問題 | 提案 |
|---------|------|------|------|
| **PHASE1_COMPLETION_SUMMARY.md** | フェーズ1完了記録 | 履歴として価値あり | アーカイブ化 |
| **PHASE2_3_COMPLETION_SUMMARY.md** | フェーズ2.3完了記録 | 最新完了記録 | アーカイブ化 |

### レベル5: 技術・分析資料
| ファイル | 現状 | 問題 | 提案 |
|---------|------|------|------|
| **CROSS_PLATFORM_PYTHON_SETUP.md** | 環境構築 | そのまま | 例外として保持 |
| **analysis/*** | 分析資料群 | UFOサイズ前提多数 | 古いコード更新/削除 |

## ドキュメント整理最終案（改訂版）

### 提案: 5つのカテゴリに整理（意図を組んだ改良版）

#### 1. **現在情報** (4ファイル)
1. **README.md** - 概要・クイックスタート＋ドキュメントガイド
   - プレイヤー向け：ゲーム概要・操作方法
   - 開発者向け：他文書の役割説明・全体ガイド
   
2. **CURRENT_SPECIFICATIONS.md** - 最新仕様統合（新規作成）
   - 現在実装されているシステム詳細
   - パラメータ・設定値・数式
   - ゲームロジック・アーキテクチャ
   
3. **DEVELOPMENT_GUIDE.md** - 開発ガイド（仕様以外）
   - 開発環境・ルール・方針
   - コーディング規約・ファイル構成
   
4. **CROSS_PLATFORM_PYTHON_SETUP.md** - 環境構築（固定）

#### 2. **開発現状** (1ファイル)
5. **DEVELOPMENT_ENTRY.md** - 開発エントリー（新規作成）
   - 文書冒頭でDEVELOPMENT_GUIDE.md参照指示
   - 開発フェーズ全体像
   - 現在進行中の開発内容
   - 今後のフェーズ計画（粗い）
   - 完了フェーズ概要（詳細は履歴へ）

#### 3. **開発履歴** (1ファイル)  
6. **DEVELOPMENT_HISTORY.md** - 完了サマリー統合（新規作成）
   - 過去の開発経緯・変更理由
   - 大きな仕様変更の記録
   - 完了フェーズの詳細記録

#### 4. **開発用ツール** (既存フォルダ整理）
7. **tools/** (新規フォルダ)
   - tools/README.md作成（ツール群の用途説明）
   - analysis/ → tools/analysis/ に移動
   - debug/ → tools/debug/ に移動  
   - test関連ファイル → tools/tests/ に移動
   - 各サブフォルダにREADME.md追加
   - rootのREADME.mdからtools/への案内追加

#### 5. **削除対象**
- features/フォルダ → 内容を統合後削除
- PHASE*_COMPLETION_SUMMARY.md → 履歴に統合後削除
- PROJECT_STATUS.md → DEVELOPMENT_ENTRY.mdに統合後削除
- GAME_SPECIFICATIONS.md → CURRENT_SPECIFICATIONS.mdに統合後削除
- READING_GUIDE.md → README.mdに統合後削除

### features/フォルダ整理方針

#### 内容分析結果：
- **game_cycle_system.md**: フェーズ1詳細（完了済み・履歴価値）
- **game_cycle_phase2.md**: フェーズ2詳細（完了済み・履歴価値）

#### 統合方針：
- **技術詳細** → CURRENT_SPECIFICATIONS.mdに統合
- **開発経緯** → DEVELOPMENT_HISTORY.mdに統合
- **フォルダ削除** → featuresフォルダ自体を削除

## 作業ログ

### 2025-06-21 作業開始
- refactoring_plan.md作成
- 作業計画策定
- TodoList設定完了
- 全ドキュメント分析完了
- 改訂版整理案策定（5カテゴリ + tools/）
- DEVELOPMENT_ENTRY.md（旧DEVELOPMENT_NOW.md）に名称変更
- tools/README.md追加、rootからの案内追加を決定

### UFOサイズ削除作業方針
- **履歴価値あり**: PHASE2_3_COMPLETION_SUMMARY.md, features/game_cycle_phase2.md → 保持
- **混乱を招く**: analysis/古い分析資料 → 削除・更新

### UFOサイズ削除実行
- ✅ README.md:88 UFOサイズ記述削除 → 「年数 × 距離」に修正
- ✅ GAME_SPECIFICATIONS.md:35-36,239,244 UFOサイズ仕様削除
- ✅ PHASE2_3_COMPLETION_SUMMARY.md - 履歴として保持（削除不要）
- ✅ analysis/buy_balance_analysis.md - 現在仕様に完全書き換え
- ✅ analysis/new_balance_design.md - フェーズ2.3仕様に完全書き換え
- ✅ features/game_cycle_phase2.md - 履歴として保持（削除不要）

### フェーズ進捗更新作業
- ✅ PROJECT_STATUS.md:4 フェーズ2.3完了に更新
- ✅ PROJECT_STATUS.md:25-30 フェーズ2.3完了内容追加
- ✅ PROJECT_STATUS.md:32-38 次ステップをフェーズ2.4以降に更新

### 価格・固定費システム記述統一
- ✅ README.md:82 「10倍成長保証」→「1～10倍可変成長」に修正
- ✅ README.md:108 「10倍成長保証」→「1～10倍可変目標倍率」に修正
- ✅ PROJECT_STATUS.md:22 「10倍成長保証」→「基礎システム」に修正
- ✅ PROJECT_STATUS.md:53 「10倍成長保証」→「1～10倍戦略的成長」に修正
- ✅ PROJECT_STATUS.md:90,94 成長保証表記を可変成長に統一
- ✅ PROJECT_STATUS.md:96 固定費説明追加

### テストファイルtools/移動作業
- ✅ tools/フォルダ作成
- ✅ tools/tests/フォルダ作成
- ✅ auto_invest_test.py → tools/tests/に移動
- ✅ test_phase2_pricing.py → tools/tests/に移動
- ✅ test_price_logic.py → tools/tests/に移動
- ✅ debug/フォルダ → tools/debug/に移動
- ✅ analysis/フォルダ → tools/analysis/に移動
- ✅ run_cli.py, run_cli.bat削除
- ✅ tools/README.md作成（ツール用途説明）
- ✅ root README.mdにtools/案内追加

---

**注意**: 作業中に矛盾や不明点があれば都度質問・決定を記録する