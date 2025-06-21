# フェーズ2.3 価格倍率システム設計

## 概要

フェーズ2.3で実装された価格倍率曲線システムの設計仕様。目標倍率に基づく動的価格決定により戦略性を実現。

**最終更新**: 2025-06-21 - フェーズ2.3完了後

## システム仕様

### 基本原則
```
商品価値 = 投資コスト × 価格倍率曲線
目標倍率 = 1.0～10.0倍（大ターン開始時決定）
```

### 主要コンポーネント

#### 1. 投資コスト計算
```
投資コスト = 年数 × 距離
固定費 = 資産 × 5%（UFO代金）
```

#### 2. 価格倍率曲線
```
目標倍率 = 1.0～10.0倍（ランダム決定）
各ターン乗数 = 0.5～2.0倍（8ターン分）
累積達成倍率 ≒ 目標倍率（誤差±0.05）
```

#### 3. 商品生成
```
商品数 = 2～5個（ランダム）
総価値 = 投資コスト × 価格倍率
個別価値 = 総価値 / 商品数（±10%バリエーション）
```

## 実装アルゴリズム

### 価格倍率曲線生成
```python
def generate_multipliers(target):
    multipliers = []
    current = 1.0
    
    for i in range(8):  # 8子ターン
        remaining = 8 - i
        ideal = pow(target / current, 1.0 / remaining)
        factor = ideal * (0.6 + random() * 0.8)  # 60%-140%揺らぎ
        factor = clamp(factor, 0.5, 2.0)  # 0.5-2.0制限
        multipliers.append(factor)
        current *= factor
    
    return multipliers
```

### 商品価値計算
```python
def calculate_item_value(investment_cost, price_multiplier, num_items):
    total_value = investment_cost * price_multiplier
    base_value = total_value / num_items
    variation = base_value * (0.9 + random() * 0.2)  # ±10%
    return variation
```

## 戦略的要素

### プレイヤー判断ポイント
1. **目標倍率確認**: 現在の大ターンの目標倍率をUI表示
2. **投資判断**: 高倍率時は積極投資、低倍率時は控えめ
3. **資産管理**: 固定費を考慮したゲームオーバー回避

### システムの利点
- **予測可能性**: 目標倍率による期待値計算
- **戦略性**: 倍率に基づく投資判断
- **バランス**: 長期的な成長保証

## 設計目標達成状況

### ✅ 達成済み
- 目標倍率の正確な実現（誤差±0.05）
- 戦略的投資判断の導入
- 固定費による資産管理要素
- UFOサイズ廃止による簡素化

### 将来拡張可能性
- 市場予測ヒントの表示
- より複雑な倍率決定ロジック
- 複数大ターンの相関性

---

**注意**: このファイルはフェーズ2.3完了後の現在実装仕様です。過去の設計案や実装経緯は DEVELOPMENT_HISTORY.md を参照してください。