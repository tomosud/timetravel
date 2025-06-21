#!/usr/bin/env python3
"""
タイムトラベル仕入れゲーム - 自動テスト
APIの動作確認とデバッグ用
"""

import sys
import os
import json

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """インポートテスト"""
    print("=== インポートテスト ===")
    try:
        from core.game_engine import game_engine
        print("✅ game_engine インポート成功")
        
        from core.item_system import item_system
        print("✅ item_system インポート成功")
        
        from core.ai_buyers import ai_buyer_manager
        print("✅ ai_buyer_manager インポート成功")
        
        from core.auction_system import auction_system
        print("✅ auction_system インポート成功")
        
        from api.game_api import game_api
        print("✅ game_api インポート成功")
        
        from api.travel_api import travel_api
        print("✅ travel_api インポート成功")
        
        from api.auction_api import auction_api
        print("✅ auction_api インポート成功")
        
        return True
        
    except Exception as e:
        print(f"❌ インポートエラー: {e}")
        return False

def test_game_state():
    """ゲーム状態テスト"""
    print("\n=== ゲーム状態テスト ===")
    try:
        from api.game_api import game_api
        
        # 初期状態取得
        result = game_api.get_game_state()
        print(f"✅ ゲーム状態取得: {result['success']}")
        print(f"   所持金: {result['data']['money']}円")
        print(f"   在庫数: {len(result['data']['inventory'])}個")
        
        # リセットテスト
        reset_result = game_api.reset_game()
        print(f"✅ ゲームリセット: {reset_result['success']}")
        
        return True
        
    except Exception as e:
        print(f"❌ ゲーム状態テストエラー: {e}")
        return False

def test_travel():
    """タイムトラベルテスト"""
    print("\n=== タイムトラベルテスト ===")
    try:
        from api.travel_api import travel_api
        
        # コスト計算テスト
        cost_result = travel_api.calculate_travel_cost(10, 100, 1.0)
        print(f"✅ コスト計算: {cost_result['success']}")
        if cost_result['success']:
            print(f"   コスト: {cost_result['data']['cost']}円")
        
        # タイムトラベル実行テスト
        travel_result = travel_api.execute_travel(10, 100, 1.0)
        print(f"✅ タイムトラベル実行: {travel_result['success']}")
        if travel_result['success'] and not travel_result.get('failed', False):
            print(f"   取得アイテム数: {travel_result['data']['item_count']}個")
            print(f"   残り所持金: {travel_result['data']['new_money']}円")
        elif travel_result.get('failed', False):
            print("   ⚠️ タイムトラベル失敗（10%の確率）")
        
        return True
        
    except Exception as e:
        print(f"❌ タイムトラベルテストエラー: {e}")
        return False

def test_auction():
    """オークションテスト"""
    print("\n=== オークションテスト ===")
    try:
        from api.auction_api import auction_api
        from api.game_api import game_api
        
        # 在庫確認
        inventory_result = game_api.get_inventory()
        if not inventory_result['success']:
            print("❌ 在庫取得エラー")
            return False
            
        inventory = inventory_result['data']['inventory']
        if len(inventory) == 0:
            print("⚠️ 在庫がないためオークションテストをスキップ")
            return True
        
        # オークション設定テスト
        auction_items = []
        for i, item in enumerate(inventory[:2]):  # 最大2個でテスト
            auction_items.append({
                'item_id': item['id'],
                'start_price': int(item['estimated_price'])
            })
        
        setup_result = auction_api.setup_auction(auction_items)
        print(f"✅ オークション設定: {setup_result['success']}")
        if setup_result['success']:
            print(f"   出品数: {setup_result['data']['total_items']}個")
        
        # オークション実行テスト
        start_result = auction_api.start_auction()
        print(f"✅ オークション実行: {start_result['success']}")
        if start_result['success']:
            print(f"   売却数: {start_result['data']['summary']['sold_items']}個")
            print(f"   総利益: {start_result['data']['summary']['total_profit']}円")
        
        return True
        
    except Exception as e:
        print(f"❌ オークションテストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_flow():
    """完全フローテスト"""
    print("\n=== 完全フローテスト ===")
    try:
        from api.game_api import game_api
        from api.travel_api import travel_api
        from api.auction_api import auction_api
        
        # ゲームリセット
        game_api.reset_game()
        print("✅ ゲームリセット")
        
        # アイテム取得（成功するまで最大5回試行）
        items_acquired = False
        for attempt in range(5):
            travel_result = travel_api.execute_travel(20, 200, 2.0)
            if travel_result['success'] and not travel_result.get('failed', False):
                print(f"✅ タイムトラベル成功（試行{attempt + 1}回目）")
                print(f"   取得アイテム: {travel_result['data']['item_count']}個")
                items_acquired = True
                break
            elif travel_result.get('failed', False):
                print(f"   試行{attempt + 1}: 失敗")
        
        if not items_acquired:
            print("⚠️ 5回試行してもアイテム取得に失敗（運が悪い）")
            return True
        
        # オークション実行
        inventory_result = game_api.get_inventory()
        inventory = inventory_result['data']['inventory']
        
        if len(inventory) > 0:
            auction_items = [{
                'item_id': inventory[0]['id'],
                'start_price': int(inventory[0]['estimated_price'] * 0.8)
            }]
            
            auction_api.setup_auction(auction_items)
            start_result = auction_api.start_auction()
            
            if start_result['success']:
                print(f"✅ オークション完了")
                print(f"   結果: {start_result['data']['summary']}")
        
        # 最終状態確認
        final_state = game_api.get_game_state()
        print(f"✅ 最終状態確認")
        print(f"   所持金: {final_state['data']['money']}円")
        print(f"   在庫数: {len(final_state['data']['inventory'])}個")
        
        return True
        
    except Exception as e:
        print(f"❌ 完全フローテストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """全テストを実行"""
    print("タイムトラベル仕入れゲーム - 自動テスト開始\n")
    
    tests = [
        test_imports,
        test_game_state,
        test_travel,
        test_auction,
        test_complete_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} 失敗")
        except Exception as e:
            print(f"❌ {test.__name__} 例外: {e}")
    
    print(f"\n=== テスト結果 ===")
    print(f"合格: {passed}/{total}")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 全テスト合格！")
    else:
        print("⚠️ 一部テストが失敗しました")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)