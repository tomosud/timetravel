# 開発ガイド

**更新条件**: 開発方針・アーキテクチャルール・コーディング規約の変更時

## 開発再開時のチェックリスト

1. **現在の状況確認**: [DEVELOPMENT_ENTRY.md](./DEVELOPMENT_ENTRY.md)
2. **環境セットアップ**: [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)
3. **詳細仕様確認**: [CURRENT_SPECIFICATIONS.md](./CURRENT_SPECIFICATIONS.md)

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

## 開発計画の管理

具体的な開発計画は [DEVELOPMENT_ENTRY.md](./DEVELOPMENT_ENTRY.md) を参照してください。

## 開発上の注意点

### 開発環境
- [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)に従った環境で開発
- WSL/Linux（venv）とWindows（venv_win）の両環境対応を維持

### 環境管理
詳細な環境セットアップ手順は [CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md) を参照してください。

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

開発履歴詳細は [DEVELOPMENT_HISTORY.md](./DEVELOPMENT_HISTORY.md) を参照してください。

## 参考ドキュメント

- **[README.md](./README.md)**: 成果物の仕様・使用方法
- **[CROSS_PLATFORM_PYTHON_SETUP.md](./CROSS_PLATFORM_PYTHON_SETUP.md)**: 開発環境セットアップ手順
- **[requirements.txt](./requirements.txt)**: 依存パッケージリスト