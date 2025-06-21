#!/usr/bin/env python3
"""
自動投資テスト用スクリプト - ターン進行の確認
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from core.game_engine import game_engine
from core.turn_system import turn_system
from core.asset_manager import AssetManager
from api.travel_api import travel_api

def display_game_status():
    """現在のゲーム状態を表示"""
    state = game_engine.get_state()
    turn_info = turn_system.get_turn_info()
    asset_info = AssetManager.get_asset_info(state['money'], state['inventory'])
    
    print("=" * 60)
    print("🎮 現在のゲーム状態")
    print("=" * 60)
    print(f"💰 所持金: {state['money']:.0f}円")
    print(f"📦 在庫数: {len(state['inventory'])}個")
    print(f"💎 総資産: {asset_info['assets']:.0f}円")
    print(f"🛸 UFO代金: {asset_info['fixed_cost']:.0f}円 ({asset_info['fixed_cost_rate']*100:.1f}%)")
    print()
    print(f"🔄 大ターン: {turn_info['major_turn']}")
    print(f"⏱️  子ターン: {turn_info['minor_turn']}/{turn_info['minor_turns_total']}")
    print(f"📊 目標倍率: {turn_info['target_multiplier']:.2f}倍")
    print(f"📈 現在価格倍率: {turn_info['current_multiplier']:.2f}x")
    print(f"⚠️  ゲーム状況: {'ゲームオーバー' if asset_info['is_game_over'] else '継続可能'}")
    print()
    
    # 価格曲線の進行状況表示
    progress_bar = ""
    for i in range(turn_info['minor_turns_total']):
        if i + 1 < turn_info['minor_turn']:
            progress_bar += "✓"
        elif i + 1 == turn_info['minor_turn']:
            progress_bar += "●"
        else:
            progress_bar += "○"
    
    print(f"📊 子ターン進行: {progress_bar}")
    print(f"📈 価格曲線: {[f'{x:.2f}' for x in turn_info['price_curve']]}")
    print("=" * 60)

def auto_invest_test(turns=10):
    """自動投資テスト"""
    print("🤖 自動投資テスト開始")
    print(f"計画: {turns}回の投資を実行")
    print()
    
    # 初期状態表示
    display_game_status()
    
    for i in range(turns):
        print(f"\n🔄 投資ラウンド {i+1}/{turns}")
        print("-" * 40)
        
        # 現在の状態取得
        state = game_engine.get_state()
        asset_info = AssetManager.get_asset_info(state['money'], state['inventory'])
        
        # ゲームオーバーチェック
        if asset_info['is_game_over']:
            print("❌ ゲームオーバーのため投資停止")
            break
        
        # 投資額決定（現金の20%）
        investment_base = max(100, state['money'] * 0.2)
        years = min(10, max(1, int(investment_base / 10)))
        distance = min(10, max(1, int(investment_base / years)))
        
        print(f"📝 投資計画: {years}年前, {distance}km, 投資額={years * distance}円")
        
        # 投資実行
        try:
            result = travel_api.execute_travel(years, distance)
            
            if result['success']:
                if result.get('failed', False):
                    print(f"💥 タイムトラベル失敗（確率的失敗）")
                    print(f"   費用支払い: {result['data']['total_cost']:.0f}円")
                else:
                    data = result['data']
                    print(f"✅ タイムトラベル成功")
                    print(f"   投資額: {data['investment_cost']}円")
                    print(f"   UFO代金: {data['fixed_cost']:.0f}円")
                    print(f"   総費用: {data['total_cost']:.0f}円")
                    print(f"   取得商品: {data['item_count']}個")
                    
                    if data['item_count'] > 0:
                        total_value = sum(item['base_value'] for item in data['items'])
                        profit_ratio = total_value / data['investment_cost']
                        print(f"   商品価値: {total_value:.0f}円")
                        print(f"   投資倍率: {profit_ratio:.2f}x")
            else:
                print(f"❌ 投資失敗: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ 例外エラー: {e}")
        
        # 投資後の状態表示（簡易版）
        state_after = game_engine.get_state()
        turn_info_after = turn_system.get_turn_info()
        
        print(f"📊 投資後状態:")
        print(f"   所持金: {state['money']:.0f}円 → {state_after['money']:.0f}円")
        print(f"   在庫数: {len(state['inventory'])}個 → {len(state_after['inventory'])}個")
        print(f"   ターン: {turn_info_after['major_turn']}-{turn_info_after['minor_turn']}")
        print(f"   価格倍率: {turn_info_after['current_multiplier']:.2f}x")
    
    print("\n🎉 自動投資テスト完了")
    print("\n最終状態:")
    display_game_status()

def reset_and_test():
    """ゲームリセットしてテスト実行"""
    print("🔄 ゲームリセット実行")
    game_engine.reset_game()
    turn_system.reset_turns()
    
    print("✅ リセット完了")
    auto_invest_test(8)  # 1大ターン分テスト

if __name__ == "__main__":
    reset_and_test()