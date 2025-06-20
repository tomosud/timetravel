# 新バランス仕様設計

## 概要

現在のランダム性の高い価値計算システムを、投資額に対してほぼ同額（±10%）が戻ってくる予測可能なシステムに変更する。

## 新仕様

### 基本原則
```
期待価値合計 ≒ 投資コスト ± 10%
```

### 主要変更点

1. **投資コスト計算**: 現在と同じ
   ```
   投資コスト = (年数 × 距離) × UFOサイズ
   ```

2. **アイテム数**: UFOサイズに依存せず固定範囲
   ```
   アイテム数 = 2～5個（ランダム）
   ```

3. **価値計算**: 投資額から逆算
   ```
   目標総価値 = 投資コスト × (0.9 ～ 1.1)
   個別価値 = 目標総価値をアイテム数で分配
   ```

## 実装設計

### 1. 新しい計算フロー

```python
def calculate_new_travel_result(years, distance, ufo_size):
    # Step 1: 投資コスト計算（現在と同じ）
    investment_cost = (years * distance) * ufo_size
    
    # Step 2: アイテム数決定（新仕様）
    num_items = random.randint(2, 5)
    
    # Step 3: 目標総価値計算（±10%）
    target_total_value = investment_cost * random.uniform(0.9, 1.1)
    
    # Step 4: 価値分配
    individual_values = distribute_value_across_items(target_total_value, num_items)
    
    # Step 5: 装飾的属性付与（表示用）
    items = []
    for value in individual_values:
        item = create_item_with_predetermined_value(value, years, distance)
        items.append(item)
    
    return items
```

### 2. 価値分配アルゴリズム

```python
def distribute_value_across_items(target_total, num_items):
    """目標総価値をアイテム間で分配"""
    
    # 基本等分値
    base_value = target_total / num_items
    
    # ±40%のバリエーションを持たせつつ総合計を維持
    values = []
    remaining_total = target_total
    
    for i in range(num_items - 1):
        # 最小値: base_value * 0.6
        # 最大値: base_value * 1.4 または remaining_total * 0.8の小さい方
        min_val = base_value * 0.6
        max_val = min(base_value * 1.4, remaining_total * 0.8)
        
        item_value = random.uniform(min_val, max_val)
        values.append(item_value)
        remaining_total -= item_value
    
    # 最後のアイテムは残り全額
    values.append(remaining_total)
    
    return values
```

### 3. 装飾的属性システム

現在の状態・レア度・ジャンルシステムは**表示用として維持**し、実際の価値には影響させない。

```python
def create_item_with_predetermined_value(actual_value, years, distance):
    """事前決定された価値でアイテムを作成"""
    
    # ジャンル（ランダム）
    genre = random.choice(GENRES)
    
    # 状態（年数に基づく確率、表示用）
    condition_weights = {
        'A': max(0.1, 1.0 - years * 0.01),
        'B': 0.5,
        'C': min(0.9, years * 0.01)
    }
    condition = random.choices(['A', 'B', 'C'], 
                              weights=list(condition_weights.values()))[0]
    
    # レア度（距離・年数から計算、表示用）
    rarity_multiplier = calculate_rarity_multiplier(years, distance)
    rarity_name = get_rarity_name(rarity_multiplier)
    
    # 表示用基本価値（逆算）
    condition_mult = CONDITIONS[condition]['multiplier']
    display_base_value = actual_value / (condition_mult * rarity_multiplier)
    
    return {
        'actual_value': actual_value,  # 実際の価値（これを使用）
        'genre': genre,
        'condition': condition,
        'condition_name': CONDITIONS[condition]['name'],
        'rarity': rarity_name,
        'rarity_multiplier': rarity_multiplier,
        'display_base_value': display_base_value,  # 表示用
        'name': generate_item_name(genre, condition, rarity_name)
    }
```

## 変更が必要なファイル

### 1. core/item_system.py
- `get_travel_result()` メソッドの完全リファクタリング
- `generate_item()` メソッドの修正
- 新しい価値分配メソッド追加

### 2. 表示ロジック（必要に応じて）
- 既存の表示形式を維持しつつ、actual_valueを使用

## 期待される効果

### メリット
1. **予測可能性**: 投資額に対する戻りが安定
2. **戦略性向上**: プレイヤーが計算しやすい
3. **バランス安定**: 極端な損益が発生しない
4. **開発しやすさ**: 後段のロジック追加が容易

### ゲーム性の維持
1. **UFOサイズの意味**: コスト倍率として機能継続
2. **年数・距離の意味**: コスト増加要因として継続
3. **状態・レア度**: 視覚的な楽しさとして継続
4. **オークション**: 実際の価値で売却判定

## 実装手順

1. **新価値計算システム実装**
2. **既存アイテム生成ロジック修正**  
3. **表示互換性確保**
4. **テスト・バランス調整**
5. **次段階の増減ロジック設計準備**

この設計により、元手とそんなに増減しない安定した基盤ができ、次の段階で大きな増減を作るロジックを追加しやすくなる。