# 開発ガイド

## 開発再開時のチェックリスト

1. **現在の状況確認**: [PROJECT_STATUS.md](./PROJECT_STATUS.md)
2. **環境セットアップ**: [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)
3. **詳細仕様確認**: [GAME_SPECIFICATIONS.md](./GAME_SPECIFICATIONS.md)

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

## 開発方針

### アーキテクチャ原則
- **3層分離設計**: core(ロジック) / api(JSON) / web(UI)
- **UI独立性**: Flask ⇔ CLI ⇔ pyxel等への切り替えを容易に
- **段階的実装**: 機能を小分けして品質を保つ

### 技術選択
- **Backend**: Python + Flask
- **Frontend**: HTML/CSS/JavaScript (将来pyxel等に切り替え予定)
- **State**: メモリ上管理 (将来DB化検討)
- **API**: JSON形式でUI層と分離

## 次の開発計画

### 優先度: 高
- **フェーズ4.5**: ゲームサイクル実証・継続性向上
  - ゲームバランス調整とプレイ体験向上
  - プレイヤーの継続意欲を高める要素の実装
  - 演出なしでのゲーム性確立
  - 長期プレイ可能性の検証

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