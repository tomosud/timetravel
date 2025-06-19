"""
タイムトラベル仕入れゲーム - ゲーム状態API
ゲーム状態の取得・操作をJSON形式で提供
"""

from typing import Dict, Any
from core.game_engine import game_engine
from core.item_system import item_system


class GameAPI:
    """ゲーム状態API"""
    
    @staticmethod
    def get_game_state() -> Dict[str, Any]:
        """ゲーム状態を取得"""
        return {
            'success': True,
            'data': game_engine.get_state()
        }
    
    @staticmethod
    def get_game_summary() -> Dict[str, Any]:
        """ゲーム状態のサマリーを取得"""
        return {
            'success': True,
            'data': game_engine.get_summary()
        }
    
    @staticmethod
    def reset_game() -> Dict[str, Any]:
        """ゲームをリセット"""
        try:
            game_engine.reset_game()
            return {
                'success': True,
                'message': 'ゲームがリセットされました',
                'data': game_engine.get_state()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_inventory() -> Dict[str, Any]:
        """在庫一覧を取得"""
        state = game_engine.get_state()
        inventory = state['inventory']
        
        # 在庫アイテムに表示用情報を追加
        enhanced_inventory = [
            item_system.get_item_display_info(item)
            for item in inventory
        ]
        
        return {
            'success': True,
            'data': {
                'inventory': enhanced_inventory,
                'summary': item_system.get_inventory_summary(inventory)
            }
        }
    
    @staticmethod
    def get_auction_items() -> Dict[str, Any]:
        """出品中のアイテム一覧を取得"""
        state = game_engine.get_state()
        return {
            'success': True,
            'data': {
                'auction_items': state['auction_items']
            }
        }
    
    @staticmethod
    def save_game(filepath: str) -> Dict[str, Any]:
        """ゲーム状態を保存"""
        try:
            game_engine.save_state(filepath)
            return {
                'success': True,
                'message': f'ゲーム状態を {filepath} に保存しました'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'保存に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def load_game(filepath: str) -> Dict[str, Any]:
        """ゲーム状態を読み込み"""
        try:
            success = game_engine.load_state(filepath)
            if success:
                return {
                    'success': True,
                    'message': f'ゲーム状態を {filepath} から読み込みました',
                    'data': game_engine.get_state()
                }
            else:
                return {
                    'success': False,
                    'error': 'ファイルの読み込みに失敗しました'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'読み込みに失敗しました: {str(e)}'
            }
    
    @staticmethod
    def export_game_json() -> Dict[str, Any]:
        """ゲーム状態をJSONとして出力"""
        try:
            json_data = game_engine.export_state_json()
            return {
                'success': True,
                'data': json_data
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'JSON出力に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def import_game_json(json_data: str) -> Dict[str, Any]:
        """JSON文字列からゲーム状態を読み込み"""
        try:
            success = game_engine.import_state_json(json_data)
            if success:
                return {
                    'success': True,
                    'message': 'ゲーム状態をインポートしました',
                    'data': game_engine.get_state()
                }
            else:
                return {
                    'success': False,
                    'error': 'JSONデータが無効です'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'インポートに失敗しました: {str(e)}'
            }
    
    @staticmethod
    def get_item_by_id(item_id: int) -> Dict[str, Any]:
        """IDでアイテムを取得"""
        try:
            # 在庫から検索
            item = game_engine.get_inventory_item(item_id)
            if item:
                return {
                    'success': True,
                    'data': {
                        'item': item_system.get_item_display_info(item),
                        'location': 'inventory'
                    }
                }
            
            # オークション中から検索
            auction_item = game_engine.get_auction_item(item_id)
            if auction_item:
                return {
                    'success': True,
                    'data': {
                        'item': item_system.get_item_display_info(auction_item['item']),
                        'location': 'auction',
                        'auction_info': {
                            'start_price': auction_item['start_price'],
                            'current_price': auction_item['current_price'],
                            'bid_count': auction_item['bid_count']
                        }
                    }
                }
            
            return {
                'success': False,
                'error': f'ID {item_id} のアイテムが見つかりません'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'アイテム検索に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """統計情報を取得"""
        try:
            state = game_engine.get_state()
            summary = game_engine.get_summary()
            
            return {
                'success': True,
                'data': {
                    'game_summary': summary,
                    'turn_based_stats': {
                        'turn_count': state['statistics']['turn_count'],
                        'money_per_turn': round(
                            summary['current_money'] / max(state['statistics']['turn_count'], 1), 2
                        ),
                        'profit_per_turn': round(
                            summary['total_profit'] / max(state['statistics']['turn_count'], 1), 2
                        )
                    },
                    'inventory_stats': item_system.get_inventory_summary(state['inventory'])
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'統計情報の取得に失敗しました: {str(e)}'
            }


# APIインスタンス
game_api = GameAPI()