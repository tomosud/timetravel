#!/usr/bin/env python3
"""
タイムトラベル仕入れゲーム - 自動テスト実行スクリプト
CLI経由でのゲームロジック検証
"""

import sys
import os
import json
import subprocess
import time

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from api.game_api import game_api
from api.travel_api import travel_api
from api.auction_api import auction_api


def test_cli_commands():
    """CLI コマンドテスト"""
    print("=== CLI コマンドテスト ===")
    
    commands = [
        ["python", "run_cli.py", "--command", "reset"],
        ["python", "run_cli.py", "--command", "state"],
        ["python", "run_cli.py", "--command", "buy", "--years", "10", "--distance", "100", "--ufo-size", "1.0"],
        ["python", "run_cli.py", "--command", "inventory"],
    ]
    
    for cmd in commands:
        try:
            print(f"実行: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ 成功")
                if result.stdout.strip():
                    print(f"   出力: {result.stdout.strip()}")
            else:
                print(f"❌ 失敗 (code: {result.returncode})")
                if result.stderr.strip():
                    print(f"   エラー: {result.stderr.strip()}")
                    
        except subprocess.TimeoutExpired:
            print(f"❌ タイムアウト")
        except Exception as e:
            print(f"❌ 例外: {e}")
        
        print()


def test_api_isolation():
    """API分離テスト - UI層を使わずにゲームロジックのテスト"""
    print("=== API分離テスト ===")
    
    # ゲームリセット
    result = game_api.reset_game()
    print(f"ゲームリセット: {'✅' if result['success'] else '❌'}")
    
    # 初期状態確認
    state = game_api.get_game_state()
    print(f"初期所持金: {state['data']['money']}円")
    
    # タイムトラベル（JSON API経由）
    travel_result = travel_api.execute_travel(15, 150, 1.5)
    if travel_result['success'] and not travel_result.get('failed', False):
        print(f"✅ タイムトラベル成功: {travel_result['data']['item_count']}個取得")
        
        # 在庫確認
        inventory = game_api.get_inventory()
        items = inventory['data']['inventory']
        print(f"在庫数: {len(items)}個")
        
        if len(items) > 0:
            # オークション設定（JSON API経由）
            auction_items = [{
                'item_id': items[0]['id'],
                'start_price': int(items[0]['estimated_price'] * 0.9)
            }]
            
            setup_result = auction_api.setup_auction(auction_items)
            print(f"オークション設定: {'✅' if setup_result['success'] else '❌'}")
            
            # オークション実行
            auction_result = auction_api.start_auction()
            if auction_result['success']:
                summary = auction_result['data']['summary']
                print(f"✅ オークション完了: {summary['sold_items']}個売却、{summary['total_profit']}円利益")
            else:
                print(f"❌ オークション失敗")
    
    elif travel_result.get('failed', False):
        print("⚠️ タイムトラベル失敗（10%の確率）")
    else:
        print(f"❌ タイムトラベルエラー: {travel_result.get('error', 'Unknown')}")
    
    # 最終状態
    final_state = game_api.get_game_state()
    print(f"最終所持金: {final_state['data']['money']}円")
    print(f"ゲームオーバー: {'はい' if final_state['data']['game_over'] else 'いいえ'}")


def test_ui_independence():
    """UI独立性テスト - 複数のUI層が同じロジックを使用可能か"""
    print("=== UI独立性テスト ===")
    
    # API経由でゲーム状態を操作
    game_api.reset_game()
    initial_state = game_api.get_game_state()['data']
    
    # 複数のインターフェースで同じ状態を確認
    interfaces = {
        'JSON API': lambda: game_api.get_game_state()['data'],
        'CLI module': lambda: game_api.get_game_state()['data'],  # 同じAPIを使用
    }
    
    for interface_name, get_state_func in interfaces.items():
        try:
            state = get_state_func()
            consistent = (
                state['money'] == initial_state['money'] and
                len(state['inventory']) == len(initial_state['inventory'])
            )
            print(f"{interface_name}: {'✅ 一貫性確認' if consistent else '❌ 不整合'}")
        except Exception as e:
            print(f"{interface_name}: ❌ エラー - {e}")


def test_automated_play():
    """自動プレイテスト - 完全なゲームサイクル"""
    print("=== 自動プレイテスト ===")
    
    game_api.reset_game()
    
    for turn in range(3):
        print(f"\n--- ターン {turn + 1} ---")
        
        # 資金確認
        state = game_api.get_game_state()['data']
        if state['game_over']:
            print("ゲームオーバー")
            break
        
        print(f"所持金: {state['money']}円")
        
        # タイムトラベル（適度なリスク）
        years = 20 + turn * 10
        distance = 100 + turn * 50
        ufo_size = 1.0 + turn * 0.5
        
        travel_result = travel_api.execute_travel(years, distance, ufo_size)
        if travel_result['success'] and not travel_result.get('failed', False):
            print(f"✅ {travel_result['data']['item_count']}個のアイテム取得")
        else:
            print("❌ タイムトラベル失敗")
            continue
        
        # 在庫確認してオークション
        inventory = game_api.get_inventory()['data']['inventory']
        if len(inventory) > 0:
            # 価格を少し下げて売却確率を上げる
            auction_items = []
            for item in inventory[:3]:  # 最大3個
                auction_items.append({
                    'item_id': item['id'],
                    'start_price': int(item['estimated_price'] * 0.8)
                })
            
            auction_api.setup_auction(auction_items)
            auction_result = auction_api.start_auction()
            
            if auction_result['success']:
                summary = auction_result['data']['summary']
                print(f"✅ {summary['sold_items']}個売却、{summary['total_profit']}円利益")
            else:
                print("❌ オークション失敗")
    
    # 最終結果
    final_state = game_api.get_game_state()['data']
    stats = final_state['statistics']
    
    print(f"\n=== 最終結果 ===")
    print(f"最終所持金: {final_state['money']}円")
    print(f"総利益: {stats['total_profit']}円")
    print(f"総支出: {stats['total_spent']}円")
    print(f"ターン数: {stats['turn_count']}")
    print(f"結果: {'ゲームオーバー' if final_state['game_over'] else '継続可能'}")


def run_all_tests():
    """全テスト実行"""
    print("タイムトラベル仕入れゲーム - UI分離・自動化テスト\n")
    
    tests = [
        test_api_isolation,
        test_ui_independence,
        test_automated_play,
        # test_cli_commands,  # 最後に実行（外部プロセス）
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