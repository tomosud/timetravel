#!/usr/bin/env python3
"""
ターンシステムテスト - 価格曲線と成長保証の検証
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.turn_system import turn_system, configure_turn_system
from api.travel_api import travel_api
from api.game_api import game_api


def test_price_curve_generation():
    """価格曲線生成テスト"""
    print("=== 価格曲線生成テスト ===")
    
    # 複数の価格曲線を生成してテスト
    for test_round in range(3):
        print(f"\n--- テストラウンド {test_round + 1} ---")
        turn_system.major_turn = test_round + 1
        turn_system.minor_turn = 1
        curve = turn_system.generate_new_price_curve()
        
        # 最終値が目標倍率に近いかチェック
        final_multiplier = curve[-1]
        target = turn_system.TARGET_GROWTH_MULTIPLIER
        error = abs(final_multiplier - target) / target * 100
        
        print(f"最終倍率: {final_multiplier:.2f} (目標: {target:.2f}, 誤差: {error:.3f}%)")
        print(f"変動パターン: {[f'{curve[i]/curve[i-1]:.2f}' if i > 0 else '1.00' for i in range(len(curve))]}")


def test_turn_progression():
    """ターン進行テスト"""
    print("\n=== ターン進行テスト ===")
    
    # ゲームリセット
    game_api.reset_game()
    
    print("8回の子ターンを実行して大ターン完了をテスト")
    
    for turn in range(12):  # 1.5大ターン分
        print(f"\n--- 購買 {turn + 1} ---")
        
        # 現在のターン情報
        turn_info = turn_system.get_turn_info()
        print(f"実行前: 大ターン{turn_info['major_turn']}, 子ターン{turn_info['minor_turn']}")
        
        # タイムトラベル実行（コストが安くなるよう調整）
        try:
            result = travel_api.execute_travel(5, 20, 1.0)
            if result['success'] and not result.get('failed', False):
                print(f"✅ タイムトラベル成功: {result['data']['item_count']}個取得")
            elif result.get('failed', False):
                print(f"⚠️ タイムトラベル失敗（確率的失敗）")
            else:
                print(f"❌ タイムトラベルエラー: {result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"❌ 例外エラー: {e}")
        
        # 実行後のターン情報
        turn_info_after = turn_system.get_turn_info()
        print(f"実行後: 大ターン{turn_info_after['major_turn']}, 子ターン{turn_info_after['minor_turn']}")


def test_long_term_growth():
    """長期成長テスト"""
    print("\n=== 長期成長テスト ===")
    
    # 設定を調整（テスト用に簡素化）
    configure_turn_system(
        minor_turns_per_major=4,  # 短縮
        target_growth=5.0,        # 低い目標
        random_range=(0.8, 1.5)   # 安定した範囲
    )
    
    game_api.reset_game()
    initial_money = 1000
    
    print(f"初期資金: {initial_money}円")
    print("2大ターン分（8回の購買）を実行して成長を確認")
    
    growth_history = []
    
    for turn in range(8):
        state_before = game_api.get_game_state()['data']
        money_before = state_before['money']
        
        # 安価なタイムトラベル
        result = travel_api.execute_travel(3, 10, 1.0)
        
        if result['success'] and not result.get('failed', False):
            state_after = game_api.get_game_state()['data']
            money_after = state_after['money']
            items = result['data']['item_count']
            
            # 取得アイテムの価値を概算
            if items > 0:
                # 最初のアイテムの推定価格から全体価値を推測
                inventory = game_api.get_inventory()['data']['inventory']
                if len(inventory) > 0:
                    avg_price = sum(item['estimated_price'] for item in inventory[-items:]) / items
                    total_value = avg_price * items
                    
                    growth_ratio = total_value / (money_before - money_after)
                    growth_history.append(growth_ratio)
                    
                    print(f"ターン{turn + 1}: 投資{money_before - money_after}円 → 価値{int(total_value)}円 (倍率: {growth_ratio:.2f})")
    
    # 成長傾向の分析
    if growth_history:
        avg_growth = sum(growth_history) / len(growth_history)
        print(f"\n平均成長倍率: {avg_growth:.2f}")
        print(f"成長履歴: {[f'{x:.2f}' for x in growth_history]}")
        
        if avg_growth > 1.0:
            print("✅ 長期成長が確認されました")
        else:
            print("⚠️ 成長が不十分です")


def test_configuration():
    """設定変更テスト"""
    print("\n=== 設定変更テスト ===")
    
    print("設定変更前:")
    turn_system._debug_current_state()
    
    # 設定変更
    configure_turn_system(
        minor_turns_per_major=6,
        target_growth=15.0,
        random_range=(0.4, 2.2),
        trend_settings={'enable': True, 'strength': 0.2}
    )
    
    print("\n設定変更後:")
    turn_system._debug_current_state()
    
    # 元の設定に戻す
    configure_turn_system(
        minor_turns_per_major=8,
        target_growth=10.0,
        random_range=(0.5, 1.8),
        trend_settings={'enable': True, 'strength': 0.1}
    )


def run_all_tests():
    """全テスト実行"""
    print("ターンシステム・価格曲線テスト開始\n")
    
    tests = [
        test_price_curve_generation,
        test_configuration,
        test_turn_progression,
        test_long_term_growth,
    ]
    
    for test in tests:
        try:
            test()
            print()
        except Exception as e:
            print(f"❌ {test.__name__} でエラー: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("🎉 全テスト完了！")


if __name__ == "__main__":
    run_all_tests()