# 買う機能バランス分析ツール

## 概要

タイムトラベルゲームの「買う」機能における3つのパラメータ（年数・距離・UFOサイズ）の影響を可視化・分析するツールです。

## 実行方法

### Windows環境
```cmd
cd analysis
run_analysis.bat
```

### WSL/Linux環境  
```bash
cd analysis
./run_analysis.sh
```

## 生成される可視化

### 1. cost_3d.png
**3Dコスト表面プロット**
- 年数×距離でのコスト変化を3D表示
- コスト爆発の傾向を視覚的に確認

### 2. roi_heatmap.png
**ROI（投資収益率）ヒートマップ**
- 年数×距離の組み合わせでの投資効率
- 緑：高収益、赤：低収益・損失

### 3. ufo_size_analysis.png
**UFOサイズ効率分析**
- UFOサイズに対する利益・アイテム数・コストの変化
- 最適なUFOサイズの特定

### 4. rarity_bonus.png
**レア度ボーナス曲線**
- 年数・距離がレア度に与える影響
- ボーナス上限の確認

### 5. optimal_strategies.png
**予算別最適戦略テーブル**
- 予算制約下での最適パラメータ組み合わせ
- 期待利益とROIの表示

## 分析対象パラメータ

### 年数（Years）
- **範囲**: 1～1000年
- **影響**: コスト増加 + レア度向上（上限2.0倍）

### 距離（Distance）  
- **範囲**: 0～50,000km
- **影響**: コスト増加 + レア度向上（上限1.5倍）

### UFOサイズ
- **範囲**: 1.0～10.0倍
- **影響**: コスト倍率 + アイテム数（最大8個）

## 計算式

### コスト
```
総コスト = (年数 × 距離) × UFOサイズ
```

### レア度倍率
```
レア度倍率 = 1.0 + year_bonus + distance_bonus + combo_bonus
year_bonus = min(年数 × 0.02, 2.0)
distance_bonus = min(距離 × 0.001, 1.5)  
combo_bonus = min((年数 × 距離) × 0.00001, 1.0)
```

### 期待利益
```
期待利益 = (期待売却額 × 成功率 × 売却効率) - 投資コスト
成功率 = 90% (失敗率10%)
売却効率 = 80% (手数料等)
```

## ファイル構成

```
analysis/
├── README.md                 # この説明ファイル
├── buy_balance_analysis.md   # 詳細分析レポート
├── buy_visualizer.py         # メイン可視化スクリプト
├── run_analysis.bat          # Windows実行スクリプト
├── run_analysis.sh           # Linux実行スクリプト
└── plots/                    # 生成される画像ファイル
    ├── cost_3d.png
    ├── roi_heatmap.png
    ├── ufo_size_analysis.png
    ├── rarity_bonus.png
    └── optimal_strategies.png
```

## 注意事項

- 初回実行時は必要なパッケージ（matplotlib, seaborn等）が自動インストールされます
- 実行には数分かかる場合があります
- 生成された画像は`plots/`フォルダに保存されます