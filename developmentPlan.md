# 開発計画・進行管理

## 開発の再開時に確認すること

1. 現在の開発状況（下記の進行状況を確認）
2. 次に取り組むべき項目（開発計画セクションを確認）
3. 開発環境のセットアップ状況（[CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)参照）

## 開発の全体的な進行イメージ

### 基本方針
- **ゲームロジックとUIの完全分離**: 将来的なUI切り替えを容易にするため
- **最小限のインターフェースでゲームサイクル確立**: 演出は後から実装
- **機能の小分け・整理**: 段階的な開発で品質を保つ

### アーキテクチャ設計
- **ゲームロジック**: 辞書などのデータ構造で入出力を管理
- **UI層**: Flask Web版 ⇔ pyxel版への切り替えを容易に
- **データ層**: 現在はメモリ上、将来的にはファイル/DB永続化を検討

### 開発ステップ
1. **コア機能の確立** (完了済みフェーズ0-4)
2. **ロジックとUIの分離リファクタリング** (今後実装)
3. **演出・UI改善** (フェーズ6以降)
4. **LLM連携** (フェーズ5)

## 現在の開発状況

**最終更新日**: 2025-06-20

### 完了済みフェーズ
- ✅ **フェーズ0**: 基盤構築（Flask、HTML/CSS/JavaScript、バッチファイル）
- ✅ **フェーズ1**: 買うモードのコスト計算と商品生成ロジック
- ✅ **フェーズ2**: 売るモードの価格評価とオークション結果判定
- ✅ **フェーズ3**: 収益・資金管理とループ処理
- ✅ **フェーズ4**: 商品保持・再出品ロジック

### 最近の作業内容
- 仮想環境のクロスプラットフォーム対応完了
  - WSL/Linux用: `venv`
  - Windows用: `venv_win`
- requirements.txt英語コメント対応
- run.batの英語化・仮想環境名更新
- .gitignoreにvenv_win追加
- [README.md](./README.md)開発ガイトライン更新

## 次の開発計画

### 優先度: 高
- **ロジック・UI分離リファクタリング**
  - 現在のFlaskアプリをゲームロジック層とUI層に分離
  - 辞書形式での入出力インターフェース設計
  - pyxel版への切り替え準備

### 優先度: 中
- **フェーズ5**: LLM導入準備
  - 商品名・説明文の自動生成システム
  - LLM API連携の基盤実装

- **フェーズ6**: UIの改善
  - pyxelなどによるリッチなインターフェース実装
  - ユーザビリティ向上

### 優先度: 低
- パフォーマンス最適化
- データ永続化（ファイル/DB）
- コードリファクタリング

## 開発上の注意点

### 開発環境
- [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)に従った環境で開発
- WSL/Linux（venv）とWindows（venv_win）の両環境対応を維持

### 仮想環境管理
**2つの仮想環境を使い分け:**

- **venv** (WSL/Linux環境用)
  - WSL上のClaude Codeが使用
  - 存在しない場合は自動作成: `python3 -m venv venv`
  - 新しいパッケージが必要な場合：
    1. `source venv/bin/activate`
    2. `pip install [パッケージ名]`
    3. [requirements.txt](./requirements.txt)に手動で記述追加（英語コメントのみ）
    4. Windows環境で[run.bat](./run.bat)実行テスト

- **venv_win** (Windows環境用)
  - Windows環境で`run.bat`実行時に使用
  - [requirements.txt](./requirements.txt)を参照して自動インストール
  - 直接パッケージ追加は行わず、[requirements.txt](./requirements.txt)の内容に従う

### コーディング規約
- **ファイル分割**: 1ファイル約400行以内で機能分割
- **クロスプラットフォーム対応**: Unixコマンド（`&&`等）使用禁止
- **エンコーディング問題回避**: 英語コメント推奨、日本語コメント禁止
- **ロジックとUIの分離**: 辞書等のデータ構造で入出力を管理
- **ドキュメント更新**: 仕様や計画変更時は[README.md](./README.md)、[developmentPlan.md](./developmentPlan.md)を更新

## 技術的課題・検討事項

### 現在の課題
- なし（基本機能は完成済み）

### 将来の検討事項
- LLM API選定（OpenAI GPT-4、Anthropic Claude等）
- UI/UXライブラリの選定
- データ永続化（現在はメモリ上のみ）

## 開発履歴

### 2025-06-20
- クロスプラットフォーム対応セットアップ完了
- 開発環境ドキュメント整備
- [developmentPlan.md](./developmentPlan.md)作成

### それ以前
- フェーズ0～4の基本ゲーム機能実装完了
- Flask Webアプリケーション完成
- AIオークションシステム実装

## 参考ドキュメント

- **[README.md](./README.md)**: 成果物の仕様・使用方法
- **[CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)**: 開発環境セットアップ手順
- **[requirements.txt](./requirements.txt)**: 依存パッケージリスト