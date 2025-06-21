#!/usr/bin/env python3
"""
フェーズ2 価格システムの自動テスト
大フェーズ目標倍率と子フェーズ価格倍率の検証
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.turn_system import turn_system
from core.asset_manager import AssetManager
from core.item_system import item_system
from core.game_engine import game_engine


def test_target_multiplier_generation():
    """大フェーズ目標倍率の生成テスト"""
    print("=== 大フェーズ目標倍率生成テスト ===")
    
    for i in range(10):
        multiplier = AssetManager.generate_target_multiplier()
        print(f"生成 {i+1}: {multiplier:.2f}倍")
        
        # 範囲チェック
        if multiplier < 0.1 or multiplier > 10.0:
            print(f"❌ 範囲外: {multiplier}倍 (0.1～10.0の範囲外)")
        else:
            print(f"✅ 範囲内: {multiplier}倍")
    
    print()


def test_price_curve_generation():
    """子フェーズ価格倍率の生成テスト"""
    print("=== 子フェーズ価格倍率生成テスト ===")
    
    # 新しいターンシステムを生成して価格曲線をテスト
    turn_system.reset_turns()
    
    target = turn_system.get_target_multiplier()
    curve = turn_system.price_curve.copy()
    
    print(f"大フェーズ目標倍率: {target:.2f}倍")
    print(f"子フェーズ価格倍率: {[f'{x:.2f}' for x in curve]}")
    print(f"最終値: {curve[-1]:.2f}倍")
    print(f"目標との差: {abs(curve[-1] - target):.4f}")
    
    # 最終値が目標倍率と一致するかチェック
    if abs(curve[-1] - target) < 0.01:
        print("✅ 最終値が目標倍率と一致")
    else:
        print(f"❌ 最終値が目標倍率と不一致: 目標{target:.2f} vs 実際{curve[-1]:.2f}")
    
    print()
    return target, curve


def test_investment_simulation():
    """投資シミュレーションテスト"""
    print("=== 投資シミュレーションテスト ===")
    
    # 初期設定
    initial_money = 1000
    investment_per_turn = 100
    
    print(f"初期資金: {initial_money}円")
    print(f"毎ターン投資額: {investment_per_turn}円")
    
    # ゲームリセット
    game_engine.reset_game()
    game_engine.state['money'] = initial_money
    
    target_multiplier = turn_system.get_target_multiplier()
    print(f"大フェーズ目標倍率: {target_multiplier:.2f}倍")
    
    total_investment = 0
    total_fixed_cost = 0
    total_item_value = 0
    
    # 8ターン（1大フェーズ）投資シミュレーション
    for turn in range(8):
        current_state = game_engine.get_state()
        current_money = current_state['money']
        current_inventory = current_state['inventory']
        
        # 資産・固定費計算
        assets = AssetManager.calculate_assets(current_money, current_inventory)
        fixed_cost = AssetManager.calculate_fixed_cost(assets)
        
        # 投資可能かチェック
        total_cost = investment_per_turn + fixed_cost
        if assets < total_cost:
            print(f"ターン {turn+1}: 資金不足でスキップ")
            continue
        
        # 現在の価格倍率取得
        current_multiplier = turn_system.get_current_price_multiplier()
        
        print(f"ターン {turn+1}:")
        print(f"  子フェーズ価格倍率: {current_multiplier:.2f}x")
        print(f"  投資額: {investment_per_turn}円")
        print(f"  固定費: {fixed_cost:.2f}円")
        print(f"  総費用: {total_cost:.2f}円")
        
        # タイムトラベル実行
        travel_result = item_system.get_travel_result(10, 10, current_money)
        
        if travel_result['success'] and not travel_result['failed']:
            # 成功時の処理
            items = travel_result['items']
            item_values = [item['base_value'] for item in items]
            turn_item_value = sum(item_values)
            
            print(f"  取得アイテム数: {len(items)}個")
            print(f"  取得アイテム価値: {turn_item_value:.2f}円")
            print(f"  期待価値倍率: {turn_item_value / investment_per_turn:.2f}x")
            
            # ゲーム状態更新
            game_engine.spend_money(total_cost)
            game_engine.add_to_inventory(items)
            
            total_investment += investment_per_turn
            total_fixed_cost += fixed_cost
            total_item_value += turn_item_value
        else:
            print(f"  ❌ タイムトラベル失敗")
        
        print()
    
    # 最終結果
    print("=== 大フェーズ完了結果 ===")
    print(f"総投資額: {total_investment}円")
    print(f"総固定費: {total_fixed_cost:.2f}円")
    print(f"総費用: {total_investment + total_fixed_cost:.2f}円")
    print(f"取得アイテム総価値: {total_item_value:.2f}円")
    
    if total_investment > 0:
        actual_multiplier = total_item_value / total_investment
        print(f"実際の投資倍率: {actual_multiplier:.2f}x")
        print(f"目標倍率: {target_multiplier:.2f}x")
        print(f"倍率差: {abs(actual_multiplier - target_multiplier):.2f}")
        
        if abs(actual_multiplier - target_multiplier) < 0.5:
            print("✅ 実際の倍率が目標倍率に近い")
        else:
            print("❌ 実際の倍率が目標倍率から乖離")
    
    print()


def test_price_curve_consistency():
    """価格曲線の一貫性テスト"""
    print("=== 価格曲線一貫性テスト ===")
    
    # 複数回テストして一貫性を確認
    for test_num in range(3):
        print(f"\n--- テスト {test_num + 1} ---")
        
        # 新しい価格曲線生成
        turn_system.reset_turns()
        target = turn_system.get_target_multiplier()
        curve = turn_system.price_curve.copy()
        
        print(f"大フェーズ目標倍率: {target:.2f}倍")
        print(f"価格曲線: {[f'{x:.2f}' for x in curve]}")
        
        # 各ターンでの価格倍率をチェック
        for i in range(len(curve)):
            turn_system.minor_turn = i + 1
            current_multiplier = turn_system.get_current_price_multiplier()
            expected_multiplier = curve[i]
            
            print(f"  ターン {i+1}: 取得倍率={current_multiplier:.2f}, 期待倍率={expected_multiplier:.2f}")
            
            if abs(current_multiplier - expected_multiplier) > 0.01:
                print(f"    ❌ 不一致: {current_multiplier:.2f} != {expected_multiplier:.2f}")
            else:
                print(f"    ✅ 一致")


def test_item_generation_with_multiplier():
    """倍率による商品生成テスト"""
    print("=== 倍率による商品生成テスト ===")
    
    investment = 100
    years = 10
    distance = 10
    
    # 異なる価格倍率でテスト
    test_multipliers = [0.5, 1.0, 2.0, 5.0]
    
    for multiplier in test_multipliers:
        print(f"\n--- 価格倍率 {multiplier:.1f}x テスト ---")
        
        # 価格倍率を手動設定（テスト用）
        turn_system.price_curve = [multiplier] * 8
        turn_system.minor_turn = 1
        
        # 商品生成
        travel_result = item_system.get_travel_result(years, distance, 1000)
        
        if travel_result['success'] and not travel_result['failed']:
            items = travel_result['items']
            total_value = sum(item['base_value'] for item in items)
            
            print(f"投資額: {investment}円")
            print(f"取得商品価値: {total_value:.2f}円")
            print(f"実際倍率: {total_value / investment:.2f}x")
            print(f"期待倍率: {multiplier:.2f}x")
            
            # 商品の estimated_price をチェック
            for i, item in enumerate(items):
                base_value = item['base_value']
                estimated_price = item.get('estimated_price', 0)
                price_multiplier = estimated_price / base_value if base_value > 0 else 0
                
                print(f"  商品{i+1}: base_value={base_value:.2f}, estimated_price={estimated_price:.2f}, 倍率={price_multiplier:.2f}x")


if __name__ == "__main__":
    print("フェーズ2 価格システム自動テスト開始\n")
    
    # テスト実行
    test_target_multiplier_generation()
    target, curve = test_price_curve_generation()
    test_price_curve_consistency()
    test_item_generation_with_multiplier()
    test_investment_simulation()
    
    print("テスト完了")