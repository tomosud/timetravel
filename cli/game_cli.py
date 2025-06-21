#!/usr/bin/env python3
"""
タイムトラベル仕入れゲーム - CLI版インターフェース
コマンドライン操作とJSON API経由の制御を提供
"""

import sys
import os
import json
import time
import argparse

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.game_api import game_api
from api.travel_api import travel_api
from api.auction_api import auction_api


class GameCLI:
    """CLI版ゲームインターフェース"""
    
    def __init__(self):
        self.running = True
    
    def show_game_state(self):
        """ゲーム状態表示"""
        result = game_api.get_game_state()
        if not result['success']:
            print(f"Error getting game state: {result.get('error', 'Unknown error')}")
            return
        
        state = result['data']
        stats = state['statistics']
        
        print(f"\n=== ゲーム状態 ===")
        print(f"所持金: {state['money']}円")
        print(f"在庫数: {stats['inventory_count']}個")
        print(f"出品数: {stats['auction_count']}個")
        print(f"ターン数: {stats['turn_count']}")
        print(f"総利益: {stats['total_profit']}円")
        print(f"総支出: {stats['total_spent']}円")
        
        if state['game_over']:
            print("❌ ゲームオーバー")
        else:
            print("✅ ゲーム継続中")
    
    def show_inventory(self):
        """在庫表示"""
        result = game_api.get_inventory()
        if not result['success']:
            print(f"Error getting inventory: {result.get('error', 'Unknown error')}")
            return
        
        inventory = result['data']['inventory']
        if len(inventory) == 0:
            print("在庫がありません")
            return
        
        print(f"\n=== 在庫一覧 ({len(inventory)}個) ===")
        for i, item in enumerate(inventory):
            print(f"{i+1:2d}. {item['genre']} ({item['condition']}) "
                  f"レア度:{item['rarity_tier']} 推定価格:{item['estimated_price']}円")
    
    def show_auction_items(self):
        """出品商品表示"""
        result = game_api.get_auction_items()
        if not result['success']:
            print(f"Error getting auction items: {result.get('error', 'Unknown error')}")
            return
        
        auction_items = result['data']['auction_items']
        if len(auction_items) == 0:
            print("出品商品がありません")
            return
        
        print(f"\n=== 出品商品一覧 ({len(auction_items)}個) ===")
        for i, auction_item in enumerate(auction_items):
            item = auction_item['item']
            print(f"{i+1:2d}. {item['genre']} ({item['condition']}) "
                  f"開始価格:{auction_item['start_price']}円")
    
    def execute_travel(self, years=None, distance=None, ufo_size=None):
        """タイムトラベル実行"""
        if years is None:
            years = int(input("年数差 (1-10000000): "))
        if distance is None:
            distance = int(input("距離 (1-20000): "))
        if ufo_size is None:
            ufo_size = float(input("UFOサイズ倍率 (1.0-100.0): "))
        
        # コスト計算
        cost_result = travel_api.calculate_travel_cost(years, distance, ufo_size)
        if not cost_result['success']:
            print(f"コスト計算エラー: {cost_result.get('error', 'Unknown error')}")
            return False
        
        cost = cost_result['data']['cost']
        print(f"必要コスト: {cost}円")
        
        state = game_api.get_game_state()['data']
        if cost > state['money']:
            print("❌ 資金不足です")
            return False
        
        # 実行確認
        confirm = input(f"実行しますか？ (y/N): ").lower().strip()
        if confirm != 'y':
            print("キャンセルしました")
            return False
        
        # タイムトラベル実行
        result = travel_api.execute_travel(years, distance, ufo_size)
        if not result['success']:
            print(f"タイムトラベルエラー: {result.get('error', 'Unknown error')}")
            return False
        
        if result.get('failed', False):
            print("❌ タイムトラベルに失敗しました（10%の確率）")
            print(f"失ったお金: {cost}円")
        else:
            data = result['data']
            print(f"✅ タイムトラベル成功！")
            print(f"取得アイテム: {data['item_count']}個")
            print(f"残り所持金: {data['new_money']}円")
        
        return True
    
    def setup_auction(self):
        """オークション設定"""
        inventory_result = game_api.get_inventory()
        inventory = inventory_result['data']['inventory']
        
        if len(inventory) == 0:
            print("在庫がありません")
            return False
        
        self.show_inventory()
        
        auction_items = []
        print("\n出品する商品を選択してください（最大8個、0で終了）:")
        
        for slot in range(8):
            try:
                choice = input(f"出品スロット{slot+1} (商品番号 1-{len(inventory)}, 0で終了): ")
                choice = int(choice)
                
                if choice == 0:
                    break
                
                if choice < 1 or choice > len(inventory):
                    print("無効な番号です")
                    continue
                
                item = inventory[choice - 1]
                start_price = int(input(f"開始価格 (推奨: {item['estimated_price']}円): "))
                
                auction_items.append({
                    'item_id': item['id'],
                    'start_price': start_price
                })
                
            except ValueError:
                print("数値を入力してください")
                continue
            except KeyboardInterrupt:
                print("\nキャンセルしました")
                return False
        
        if len(auction_items) == 0:
            print("出品商品がありません")
            return False
        
        # オークション設定
        result = auction_api.setup_auction(auction_items)
        if not result['success']:
            print(f"オークション設定エラー: {result.get('error', 'Unknown error')}")
            return False
        
        print(f"✅ {len(auction_items)}個の商品を出品設定しました")
        return True
    
    def start_auction(self):
        """オークション開始"""
        result = auction_api.start_auction()
        if not result['success']:
            print(f"オークション開始エラー: {result.get('error', 'Unknown error')}")
            return False
        
        print("🔨 1分間オークション開始...")
        time.sleep(1)  # 短縮版
        
        data = result['data']
        summary = data['summary']
        
        print(f"\n=== オークション結果 ===")
        print(f"売却数: {summary['sold_items']}/{summary['total_items']}個")
        print(f"総売上: {summary['total_revenue']}円")
        print(f"手数料: {summary['total_fees']}円")
        print(f"純利益: {summary['total_profit']}円")
        
        # 個別結果表示
        for auction_result in data['results']:
            item = auction_result['item']
            if auction_result['sold']:
                print(f"✅ {item['genre']} - {auction_result['final_price']}円で売却")
            else:
                print(f"❌ {item['genre']} - 売れ残り")
        
        return True
    
    def reset_game(self):
        """ゲームリセット"""
        confirm = input("ゲームをリセットしますか？ (y/N): ").lower().strip()
        if confirm != 'y':
            print("キャンセルしました")
            return
        
        result = game_api.reset_game()
        if result['success']:
            print("✅ ゲームをリセットしました")
        else:
            print(f"リセットエラー: {result.get('error', 'Unknown error')}")
    
    def show_help(self):
        """ヘルプ表示"""
        print("""
=== コマンド一覧 ===
s, state      - ゲーム状態表示
i, inventory  - 在庫表示
a, auction    - 出品商品表示
b, buy        - タイムトラベル（商品購入）
o, sell       - オークション設定
r, run        - オークション実行
reset         - ゲームリセット
h, help       - このヘルプ
q, quit       - 終了
""")
    
    def run_interactive(self):
        """対話モード実行"""
        print("タイムトラベル仕入れゲーム - CLI版")
        print("ヘルプは 'h' を入力してください")
        
        self.show_game_state()
        
        while self.running:
            try:
                command = input("\n> ").lower().strip()
                
                if command in ['q', 'quit']:
                    print("ゲームを終了します")
                    self.running = False
                    
                elif command in ['s', 'state']:
                    self.show_game_state()
                    
                elif command in ['i', 'inventory']:
                    self.show_inventory()
                    
                elif command in ['a', 'auction']:
                    self.show_auction_items()
                    
                elif command in ['b', 'buy']:
                    self.execute_travel()
                    
                elif command in ['o', 'sell']:
                    self.setup_auction()
                    
                elif command in ['r', 'run']:
                    self.start_auction()
                    
                elif command == 'reset':
                    self.reset_game()
                    
                elif command in ['h', 'help']:
                    self.show_help()
                    
                elif command == '':
                    continue
                    
                else:
                    print(f"不明なコマンド: {command}")
                    print("ヘルプは 'h' を入力してください")
                    
            except KeyboardInterrupt:
                print("\n\nゲームを終了します")
                self.running = False
            except EOFError:
                print("\n\nゲームを終了します")
                self.running = False
            except Exception as e:
                print(f"エラー: {e}")


def run_command_mode(args):
    """コマンドモード実行（自動テスト用）"""
    cli = GameCLI()
    
    if args.command == 'state':
        cli.show_game_state()
    elif args.command == 'inventory':
        cli.show_inventory()
    elif args.command == 'buy':
        if args.years and args.distance and args.ufo_size:
            cli.execute_travel(args.years, args.distance, args.ufo_size)
        else:
            print("Error: --years, --distance, --ufo-size required for buy command")
            return False
    elif args.command == 'reset':
        result = game_api.reset_game()
        print("Game reset" if result['success'] else f"Error: {result.get('error')}")
    else:
        print(f"Unknown command: {args.command}")
        return False
    
    return True


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Time Travel Trading Game CLI')
    parser.add_argument('--command', '-c', help='Command to execute (for automation)')
    parser.add_argument('--years', type=int, help='Years for travel')
    parser.add_argument('--distance', type=int, help='Distance for travel')
    parser.add_argument('--ufo-size', type=float, help='UFO size multiplier')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    args = parser.parse_args()
    
    if args.command:
        # コマンドモード（自動化用）
        success = run_command_mode(args)
        sys.exit(0 if success else 1)
    else:
        # 対話モード
        cli = GameCLI()
        cli.run_interactive()


if __name__ == "__main__":
    main()