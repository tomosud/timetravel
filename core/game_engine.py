"""
タイムトラベル仕入れゲーム - ゲームエンジン
ゲーム状態の管理とゲーム進行ロジックを担当
"""

import json
from typing import Dict, List, Any, Optional
import time


class GameEngine:
    """ゲーム状態管理とコアロジック"""
    
    def __init__(self):
        """ゲーム初期化"""
        self.reset_game()
    
    def reset_game(self) -> None:
        """ゲーム状態をリセット"""
        self.state = {
            'money': 1000,
            'inventory': [],
            'auction_items': [],
            'game_over': False,
            'turn_count': 0,
            'total_profit': 0,
            'total_spent': 0
        }
    
    def get_state(self) -> Dict[str, Any]:
        """現在のゲーム状態を取得"""
        # ゲームオーバー判定を更新
        self.state['game_over'] = self.check_game_over()
        
        return {
            'money': self.state['money'],
            'inventory': self.state['inventory'].copy(),
            'auction_items': self.state['auction_items'].copy(),
            'game_over': self.state['game_over'],
            'statistics': {
                'turn_count': self.state['turn_count'],
                'total_profit': self.state['total_profit'],
                'total_spent': self.state['total_spent'],
                'inventory_count': len(self.state['inventory']),
                'auction_count': len(self.state['auction_items'])
            }
        }
    
    def check_game_over(self) -> bool:
        """ゲームオーバー判定：所持金0円かつ在庫なし"""
        return self.state['money'] <= 0 and len(self.state['inventory']) == 0
    
    def spend_money(self, amount: float) -> bool:
        """お金を消費（成功時True、残高不足時False）"""
        if self.state['money'] >= amount:
            self.state['money'] -= amount
            self.state['total_spent'] += amount
            return True
        return False
    
    def earn_money(self, amount: float) -> None:
        """お金を獲得"""
        self.state['money'] += amount
        self.state['total_profit'] += amount
    
    def add_to_inventory(self, items: List[Dict[str, Any]]) -> None:
        """アイテムを在庫に追加"""
        self.state['inventory'].extend(items)
    
    def remove_from_inventory(self, item_id: int) -> Optional[Dict[str, Any]]:
        """在庫からアイテムを削除して返す"""
        for i, item in enumerate(self.state['inventory']):
            if item['id'] == item_id:
                return self.state['inventory'].pop(i)
        return None
    
    def get_inventory_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """在庫からアイテムを検索"""
        for item in self.state['inventory']:
            if item['id'] == item_id:
                return item
        return None
    
    def add_to_auction(self, auction_item: Dict[str, Any]) -> None:
        """オークションに出品"""
        self.state['auction_items'].append(auction_item)
    
    def remove_from_auction(self, item_id: int) -> Optional[Dict[str, Any]]:
        """オークションから取り下げ"""
        for i, auction_item in enumerate(self.state['auction_items']):
            if auction_item['item']['id'] == item_id:
                removed = self.state['auction_items'].pop(i)
                # 在庫に戻す
                self.state['inventory'].append(removed['item'])
                return removed
        return None
    
    def clear_sold_auction_items(self) -> None:
        """売却済みのオークションアイテムをクリア"""
        self.state['auction_items'] = [
            auction_item for auction_item in self.state['auction_items']
            if not auction_item.get('sold', False)
        ]
    
    def get_auction_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """オークションアイテムを検索"""
        for auction_item in self.state['auction_items']:
            if auction_item['item']['id'] == item_id:
                return auction_item
        return None
    
    def update_auction_item(self, item_id: int, updates: Dict[str, Any]) -> bool:
        """オークションアイテムの情報を更新"""
        auction_item = self.get_auction_item(item_id)
        if auction_item:
            auction_item.update(updates)
            return True
        return False
    
    def increment_turn(self) -> None:
        """ターン数を増加"""
        self.state['turn_count'] += 1
    
    def save_state(self, filepath: str) -> None:
        """ゲーム状態をファイルに保存"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ゲーム状態の保存に失敗: {e}")
    
    def load_state(self, filepath: str) -> bool:
        """ファイルからゲーム状態を読み込み"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
            return True
        except Exception as e:
            print(f"ゲーム状態の読み込みに失敗: {e}")
            return False
    
    def export_state_json(self) -> str:
        """ゲーム状態をJSON文字列として出力"""
        return json.dumps(self.get_state(), ensure_ascii=False, indent=2)
    
    def import_state_json(self, json_str: str) -> bool:
        """JSON文字列からゲーム状態を読み込み"""
        try:
            imported_state = json.loads(json_str)
            
            # 必要なキーの存在確認
            required_keys = ['money', 'inventory', 'auction_items']
            if all(key in imported_state for key in required_keys):
                self.state.update(imported_state)
                return True
            return False
        except Exception as e:
            print(f"JSON状態の読み込みに失敗: {e}")
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """ゲーム状態のサマリーを取得"""
        state = self.get_state()
        
        # 在庫の価値計算
        inventory_value = sum(item.get('base_value', 0) for item in state['inventory'])
        
        # オークション中の価値計算
        auction_value = sum(
            auction_item.get('current_price', auction_item.get('start_price', 0))
            for auction_item in state['auction_items']
        )
        
        return {
            'current_money': state['money'],
            'inventory_count': len(state['inventory']),
            'inventory_value': round(inventory_value, 2),
            'auction_count': len(state['auction_items']),
            'auction_value': round(auction_value, 2),
            'total_assets': round(state['money'] + inventory_value + auction_value, 2),
            'game_over': state['game_over'],
            'turn_count': state['statistics']['turn_count'],
            'total_profit': state['statistics']['total_profit'],
            'total_spent': state['statistics']['total_spent'],
            'net_profit': round(state['statistics']['total_profit'] - state['statistics']['total_spent'], 2)
        }


# シングルトンインスタンス
game_engine = GameEngine()