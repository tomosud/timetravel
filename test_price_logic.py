#!/usr/bin/env python3
"""
価格曲線ロジックの単体テスト
目標倍率と8回の投資でランダムウォークしながら到達する計算を検証
"""

import random
import math

def generate_price_curve_v1(target_multiplier, turns=8, random_min=0.5, random_max=1.8):
    """
    バージョン1: 各ターン倍率の平均が目標倍率になる方式
    """
    print(f"=== V1: 平均ベース方式 ===")
    print(f"目標倍率: {target_multiplier:.2f}x")
    
    # ランダム倍率生成
    raw_multipliers = []
    for i in range(turns):
        multiplier = random.uniform(random_min, random_max)
        if i == 0 and multiplier < 1.0:  # 初回は1.0以上
            multiplier = 1.0
        raw_multipliers.append(multiplier)
    
    # 平均が目標倍率になるよう正規化
    average = sum(raw_multipliers) / len(raw_multipliers)
    scale_factor = target_multiplier / average
    turn_multipliers = [m * scale_factor for m in raw_multipliers]
    
    print(f"生ランダム倍率: {[f'{x:.2f}' for x in raw_multipliers]}")
    print(f"平均: {average:.2f}, スケール係数: {scale_factor:.3f}")
    print(f"正規化後倍率: {[f'{x:.2f}' for x in turn_multipliers]}")
    print(f"実際の平均: {sum(turn_multipliers)/len(turn_multipliers):.2f}")
    
    # 投資シミュレーション
    total_investment = 0
    total_value = 0
    print("\n投資シミュレーション:")
    for i, multiplier in enumerate(turn_multipliers):
        investment = 100
        value = investment * multiplier
        total_investment += investment
        total_value += value
        print(f"  ターン{i+1}: {investment}円 × {multiplier:.2f}x = {value:.0f}円")
    
    final_multiplier = total_value / total_investment
    print(f"結果: {total_investment}円 → {total_value:.0f}円 (倍率: {final_multiplier:.2f}x)")
    print(f"目標達成: {'✅' if abs(final_multiplier - target_multiplier) < 0.1 else '❌'}")
    
    return turn_multipliers

def generate_price_curve_v2(target_multiplier, turns=8, random_min=0.5, random_max=1.8):
    """
    バージョン2: 累積乗算が目標倍率になる方式
    """
    print(f"\n=== V2: 累積乗算方式 ===")
    print(f"目標倍率: {target_multiplier:.2f}x")
    
    # ランダム倍率生成
    raw_multipliers = []
    for i in range(turns):
        multiplier = random.uniform(random_min, random_max)
        if i == 0 and multiplier < 1.0:  # 初回は1.0以上
            multiplier = 1.0
        raw_multipliers.append(multiplier)
    
    # 累積乗算が目標倍率になるよう正規化
    cumulative_product = 1.0
    for m in raw_multipliers:
        cumulative_product *= m
    
    scale_factor = target_multiplier / cumulative_product
    turn_multipliers = [m * scale_factor for m in raw_multipliers]
    
    print(f"生ランダム倍率: {[f'{x:.2f}' for x in raw_multipliers]}")
    print(f"累積積: {cumulative_product:.2f}, スケール係数: {scale_factor:.3f}")
    print(f"正規化後倍率: {[f'{x:.2f}' for x in turn_multipliers]}")
    
    # 累積値計算
    cumulative = 1.0
    cumulative_values = []
    for m in turn_multipliers:
        cumulative *= m
        cumulative_values.append(cumulative)
    
    print(f"累積値: {[f'{x:.2f}' for x in cumulative_values]}")
    print(f"最終累積値: {cumulative_values[-1]:.2f}")
    print(f"目標達成: {'✅' if abs(cumulative_values[-1] - target_multiplier) < 0.01 else '❌'}")
    
    return turn_multipliers, cumulative_values

def generate_price_curve_v3(target_multiplier, turns=8, random_min=0.5, random_max=1.8):
    """
    バージョン3: 各ターンで1円投資し続けた場合の最終資産が目標倍率になる方式
    """
    print(f"\n=== V3: 継続投資資産成長方式 ===")
    print(f"目標倍率: {target_multiplier:.2f}x")
    
    # 試行錯誤で目標倍率に近づける
    best_multipliers = None
    best_error = float('inf')
    
    for attempt in range(1000):  # 1000回試行
        # ランダム倍率生成
        raw_multipliers = []
        for i in range(turns):
            multiplier = random.uniform(random_min, random_max)
            if i == 0 and multiplier < 1.0:
                multiplier = 1.0
            raw_multipliers.append(multiplier)
        
        # 継続投資シミュレーション
        total_investment = 0
        total_assets = 0
        
        for i, multiplier in enumerate(raw_multipliers):
            # 毎ターン1円投資
            investment = 1
            value = investment * multiplier
            total_investment += investment
            total_assets += value
        
        final_multiplier = total_assets / total_investment
        error = abs(final_multiplier - target_multiplier)
        
        if error < best_error:
            best_error = error
            best_multipliers = raw_multipliers.copy()
    
    print(f"最適解探索完了 (誤差: {best_error:.4f})")
    print(f"最適倍率: {[f'{x:.2f}' for x in best_multipliers]}")
    
    # 検証
    total_investment = 0
    total_assets = 0
    print("\n継続投資シミュレーション:")
    
    for i, multiplier in enumerate(best_multipliers):
        investment = 1
        value = investment * multiplier
        total_investment += investment
        total_assets += value
        print(f"  ターン{i+1}: {investment}円 × {multiplier:.2f}x = {value:.2f}円 (累計資産: {total_assets:.2f}円)")
    
    final_multiplier = total_assets / total_investment
    print(f"結果: {total_investment}円 → {total_assets:.2f}円 (倍率: {final_multiplier:.2f}x)")
    print(f"目標達成: {'✅' if abs(final_multiplier - target_multiplier) < 0.1 else '❌'}")
    
    return best_multipliers

def test_all_approaches():
    """全てのアプローチをテスト"""
    target_multipliers = [2.5, 5.0, 7.5, 10.0]
    
    for target in target_multipliers:
        print("=" * 80)
        print(f"目標倍率: {target}倍でのテスト")
        print("=" * 80)
        
        # 3つの方式を比較
        v1_result = generate_price_curve_v1(target)
        v2_result = generate_price_curve_v2(target)
        v3_result = generate_price_curve_v3(target)
        
        print(f"\n{'='*50}")
        print(f"目標{target}倍のテスト完了")
        print(f"{'='*50}\n")

if __name__ == "__main__":
    print("価格曲線ロジック単体テスト")
    print("3つの異なるアプローチで目標倍率達成を検証")
    print()
    
    # 固定シードで再現性確保
    random.seed(42)
    
    test_all_approaches()