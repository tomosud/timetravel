"""
タイムトラベル仕入れゲーム - オークションAPI
オークション機能をJSON形式で提供
"""

from typing import Dict, Any, List
from ..core.game_engine import game_engine
from ..core.auction_system import auction_system
from ..core.item_system import item_system


class AuctionAPI:
    """オークションAPI"""
    
    @staticmethod
    def setup_auction(auction_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """オークション出品を設定"""
        try:
            # 既存のオークション出品をクリア
            game_engine.state['auction_items'] = []
            
            # 新しい出品を設定
            valid_items = []
            for item_data in auction_items:
                item_id = item_data.get('item_id')
                start_price = item_data.get('start_price')
                
                if not item_id or not start_price:
                    continue
                
                # インベントリから商品を検索
                item = game_engine.remove_from_inventory(item_id)
                if item:
                    auction_item = auction_system.create_auction_item(item, float(start_price))
                    game_engine.add_to_auction(auction_item)
                    valid_items.append({
                        'item_id': item_id,
                        'start_price': start_price,
                        'item_info': item_system.get_item_display_info(item)
                    })
            
            return {
                'success': True,
                'data': {
                    'auction_items': valid_items,
                    'total_items': len(valid_items),
                    'message': f'{len(valid_items)}個の商品を出品設定しました'
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'オークション設定に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def start_auction() -> Dict[str, Any]:
        """オークションを開始"""
        try:
            current_auction_items = game_engine.get_state()['auction_items']
            
            if not current_auction_items:
                return {
                    'success': False,
                    'error': '出品する商品がありません'
                }
            
            # オークション設定の妥当性をチェック
            valid, error_message = auction_system.validate_auction_setup(current_auction_items)
            if not valid:
                return {
                    'success': False,
                    'error': error_message
                }
            
            # オークションを実行（詳細ログ付き）
            results = auction_system.simulate_auction(current_auction_items, verbose=True)
            
            # 結果を処理
            total_revenue = 0
            total_profit = 0
            sold_count = 0
            
            for result in results:
                if result['sold']:
                    sold_count += 1
                    revenue = result['final_price']
                    profit = auction_system.calculate_profit(revenue)
                    total_revenue += revenue
                    total_profit += profit
                    
                    # お金を獲得
                    game_engine.earn_money(profit)
                    
                    # オークションアイテムを売却済みにマーク
                    game_engine.update_auction_item(result['item_id'], {
                        'sold': True,
                        'final_price': revenue,
                        'winner_id': result['winner_id']
                    })
            
            # 売却済みアイテムをクリア
            game_engine.clear_sold_auction_items()
            
            return {
                'success': True,
                'data': {
                    'results': results,
                    'summary': {
                        'total_items': len(results),
                        'sold_items': sold_count,
                        'success_rate': round(sold_count / len(results) * 100, 1),
                        'total_revenue': round(total_revenue, 2),
                        'total_profit': round(total_profit, 2),
                        'average_sale_price': round(total_revenue / max(sold_count, 1), 2) if sold_count > 0 else 0
                    },
                    'new_money': game_engine.get_state()['money'],
                    'remaining_auction_items': len(game_engine.get_state()['auction_items'])
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'オークション実行に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def cancel_auction_item(item_id: int) -> Dict[str, Any]:
        """オークション出品を取り消し"""
        try:
            auction_item = game_engine.remove_from_auction(item_id)
            
            if auction_item:
                return {
                    'success': True,
                    'data': {
                        'item_id': item_id,
                        'message': '出品を取り消しました',
                        'returned_to_inventory': True
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'ID {item_id} の出品商品が見つかりません'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'出品取り消しに失敗しました: {str(e)}'
            }
    
    @staticmethod
    def preview_auction(auction_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """オークションの事前予測"""
        try:
            # 仮の出品アイテムを作成
            temp_auction_items = []
            for item_data in auction_items:
                item_id = item_data.get('item_id')
                start_price = item_data.get('start_price')
                
                if not item_id or not start_price:
                    continue
                
                item = game_engine.get_inventory_item(item_id)
                if item:
                    auction_item = auction_system.create_auction_item(item, float(start_price))
                    temp_auction_items.append(auction_item)
            
            if not temp_auction_items:
                return {
                    'success': False,
                    'error': '有効な出品商品がありません'
                }
            
            # 予測を実行
            preview_result = auction_system.preview_auction(temp_auction_items)
            
            return {
                'success': True,
                'data': preview_result
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'オークション予測に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def get_auction_status() -> Dict[str, Any]:
        """現在のオークション状況を取得"""
        try:
            state = game_engine.get_state()
            auction_items = state['auction_items']
            
            # 各出品アイテムの詳細情報
            detailed_items = []
            for auction_item in auction_items:
                item_info = item_system.get_item_display_info(auction_item['item'])
                detailed_items.append({
                    'auction_info': {
                        'start_price': auction_item['start_price'],
                        'current_price': auction_item['current_price'],
                        'bid_count': auction_item['bid_count'],
                        'sold': auction_item.get('sold', False)
                    },
                    'item_info': item_info
                })
            
            return {
                'success': True,
                'data': {
                    'auction_items': detailed_items,
                    'total_items': len(auction_items),
                    'total_start_value': sum(item['start_price'] for item in auction_items),
                    'total_current_value': sum(item['current_price'] for item in auction_items),
                    'active': len(auction_items) > 0
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'オークション状況の取得に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def get_auction_history() -> Dict[str, Any]:
        """オークション履歴を取得（将来の機能）"""
        # TODO: 実装予定
        return {
            'success': True,
            'data': {
                'history': [],
                'message': 'オークション履歴機能は実装予定です'
            }
        }
    
    @staticmethod
    def get_auction_statistics() -> Dict[str, Any]:
        """オークション統計情報を取得"""
        try:
            stats = auction_system.get_auction_statistics()
            
            return {
                'success': True,
                'data': {
                    'auction_settings': {
                        'fee_rate': stats['fee_rate'],
                        'duration_rounds': stats['auction_duration_rounds'],
                        'bid_threshold': stats['bid_threshold']
                    },
                    'ai_buyer_statistics': stats['ai_buyer_stats']
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'統計情報の取得に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def update_auction_settings(fee_rate: float = None, duration_rounds: int = None, 
                               bid_threshold: float = None) -> Dict[str, Any]:
        """オークション設定を更新"""
        try:
            auction_system.update_settings(fee_rate, duration_rounds, bid_threshold)
            
            updated_stats = auction_system.get_auction_statistics()
            
            return {
                'success': True,
                'data': {
                    'message': 'オークション設定を更新しました',
                    'new_settings': {
                        'fee_rate': updated_stats['fee_rate'],
                        'duration_rounds': updated_stats['auction_duration_rounds'],
                        'bid_threshold': updated_stats['bid_threshold']
                    }
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'設定更新に失敗しました: {str(e)}'
            }


# APIインスタンス
auction_api = AuctionAPI()