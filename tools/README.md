# 開発ツール

このフォルダには開発・デバッグ・分析用のツールが含まれています。

## フォルダ構成

### 📁 tests/
**用途**: テスト・検証スクリプト  
**対象**: 開発者・テスター

- `auto_invest_test.py` - 自動投資テスト
- `test_phase2_pricing.py` - フェーズ2価格システムテスト  
- `test_price_logic.py` - 価格ロジック単体テスト

### 📁 debug/
**用途**: デバッグ・開発支援ツール  
**対象**: 開発者

- `run_test.py` - テスト実行ツール
- `test_game.py` - ゲーム動作テスト
- `test_turn_system.py` - ターンシステムテスト

### 📁 analysis/
**用途**: ゲームバランス分析・設計資料  
**対象**: 設計者・バランス調整者

- `buy_balance_analysis.md` - 購買システム分析
- `new_balance_design.md` - システム設計仕様
- `buy_visualizer.py` - データ可視化ツール

## 実行方法

### テスト実行
```bash
# 仮想環境でテスト実行
source venv/bin/activate  # Linux/WSL
# または
venv_win\Scripts\activate.bat  # Windows

python tools/tests/test_price_logic.py
python tools/debug/run_test.py
```

### 分析ツール
```bash
python tools/analysis/buy_visualizer.py
```

## 注意事項

- **本番環境から分離**: これらのツールは本番ゲームとは独立しています
- **仮想環境必須**: 実行時は必ず仮想環境をアクティベートしてください
- **パス調整**: tools/移動後のインポートパス調整が必要な場合があります

---

**メンテナンス**: 新しいテストやツールはこのフォルダ構成に従って配置してください