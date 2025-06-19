"""
タイムトラベル仕入れゲーム - タイムトラベルAPI
タイムトラベルと商品取得の処理をJSON形式で提供
"""

from typing import Dict, Any
from ..core.game_engine import game_engine
from ..core.item_system import item_system


class TravelAPI:
    """タイムトラベルAPI"""
    
    @staticmethod
    def calculate_travel_cost(years: int, distance: int, ufo_size: float) -> Dict[str, Any]:
        """タイムトラベルコストを計算"""
        try:
            # パラメータ検証
            valid, error_message = item_system.validate_travel_parameters(years, distance, ufo_size)
            if not valid:
                return {
                    'success': False,
                    'error': error_message
                }
            
            cost = item_system.calculate_travel_cost(years, distance, ufo_size)
            current_money = game_engine.get_state()['money']
            
            return {
                'success': True,
                'data': {
                    'cost': cost,
                    'parameters': {
                        'years': years,
                        'distance': distance,
                        'ufo_size': ufo_size
                    },
                    'current_money': current_money,
                    'affordable': cost <= current_money,
                    'estimated_items': max(1, int(ufo_size)),
                    'rarity_multiplier': item_system.calculate_rarity_multiplier(years, distance)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'コスト計算に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def preview_travel(years: int, distance: int, ufo_size: float) -> Dict[str, Any]:
        """タイムトラベルの事前プレビュー"""
        try:
            # コスト計算
            cost_result = TravelAPI.calculate_travel_cost(years, distance, ufo_size)
            if not cost_result['success']:
                return cost_result
            
            # 期待値計算
            rarity_multiplier = item_system.calculate_rarity_multiplier(years, distance)
            estimated_items = max(1, int(ufo_size))
            
            # 期待値範囲（概算）
            min_value_per_item = 100 * 0.6 * rarity_multiplier  # 最低値×劣化×レア度
            max_value_per_item = 1000 * 1.0 * rarity_multiplier  # 最高値×新品×レア度
            
            expected_min_total = min_value_per_item * estimated_items
            expected_max_total = max_value_per_item * estimated_items
            expected_avg_total = (expected_min_total + expected_max_total) / 2
            
            return {
                'success': True,
                'data': {
                    'cost_info': cost_result['data'],
                    'expected_outcome': {
                        'item_count': estimated_items,
                        'min_total_value': round(expected_min_total, 2),
                        'max_total_value': round(expected_max_total, 2),
                        'avg_total_value': round(expected_avg_total, 2),
                        'estimated_profit_range': {
                            'min': round(expected_min_total - cost_result['data']['cost'], 2),
                            'max': round(expected_max_total - cost_result['data']['cost'], 2),
                            'avg': round(expected_avg_total - cost_result['data']['cost'], 2)
                        }
                    },
                    'risk_assessment': {
                        'failure_rate': 0.1,  # 10%失敗率
                        'high_risk': cost_result['data']['cost'] > game_engine.get_state()['money'] * 0.8,
                        'recommendation': TravelAPI._get_travel_recommendation(
                            cost_result['data']['cost'], 
                            expected_avg_total, 
                            game_engine.get_state()['money']
                        )
                    }
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'プレビュー計算に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def execute_travel(years: int, distance: int, ufo_size: float) -> Dict[str, Any]:
        """タイムトラベルを実行"""
        try:
            current_state = game_engine.get_state()
            
            # タイムトラベル結果を取得
            travel_result = item_system.get_travel_result(
                years, distance, ufo_size, current_state['money']
            )
            
            if not travel_result['success']:
                return travel_result
            
            # お金を消費
            cost = travel_result['cost']
            if not game_engine.spend_money(cost):
                return {
                    'success': False,
                    'error': '資金が不足しています'
                }
            
            # ターン数を増加
            game_engine.increment_turn()
            
            # 失敗時の処理
            if travel_result['failed']:
                return {
                    'success': True,
                    'failed': True,
                    'data': {
                        'cost': cost,
                        'items': [],
                        'message': travel_result['message'],
                        'new_money': game_engine.get_state()['money'],
                        'game_over': game_engine.check_game_over()
                    }
                }
            
            # 成功時の処理
            items = travel_result['items']
            game_engine.add_to_inventory(items)
            
            # 表示用のアイテム情報を生成
            display_items = [
                item_system.get_item_display_info(item)
                for item in items
            ]
            
            return {
                'success': True,
                'failed': False,
                'data': {
                    'cost': cost,
                    'items': display_items,
                    'item_count': len(items),
                    'total_value': travel_result['total_value'],
                    'message': travel_result['message'],
                    'new_money': game_engine.get_state()['money'],
                    'new_inventory_count': len(game_engine.get_state()['inventory']),
                    'game_over': game_engine.check_game_over(),
                    'travel_info': {
                        'years': years,
                        'distance': distance,
                        'ufo_size': ufo_size,
                        'rarity_multiplier': item_system.calculate_rarity_multiplier(years, distance)
                    }
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'タイムトラベルの実行に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def get_travel_history() -> Dict[str, Any]:
        """タイムトラベル履歴を取得（将来の機能）"""
        # TODO: 実装予定
        return {
            'success': True,
            'data': {
                'history': [],
                'message': 'タイムトラベル履歴機能は実装予定です'
            }
        }
    
    @staticmethod
    def get_travel_recommendations() -> Dict[str, Any]:
        """おすすめのタイムトラベル先を取得"""
        try:
            current_money = game_engine.get_state()['money']
            
            recommendations = []
            
            # 低コスト・安全志向
            safe_params = {'years': 10, 'distance': 100, 'ufo_size': 1.0}
            safe_cost = item_system.calculate_travel_cost(**safe_params)
            if safe_cost <= current_money:
                recommendations.append({
                    'type': '安全志向',
                    'description': '低コスト・低リスクでの商品取得',
                    'parameters': safe_params,
                    'cost': safe_cost,
                    'risk_level': 'Low'
                })
            
            # バランス型
            balanced_params = {'years': 30, 'distance': 500, 'ufo_size': 2.0}
            balanced_cost = item_system.calculate_travel_cost(**balanced_params)
            if balanced_cost <= current_money:
                recommendations.append({
                    'type': 'バランス型',
                    'description': '適度なコストでより良い商品を狙う',
                    'parameters': balanced_params,
                    'cost': balanced_cost,
                    'risk_level': 'Medium'
                })
            
            # 高リスク・高リターン
            if current_money >= 1000:
                risky_params = {'years': 100, 'distance': 2000, 'ufo_size': 3.0}
                risky_cost = item_system.calculate_travel_cost(**risky_params)
                if risky_cost <= current_money * 0.8:  # 資金の80%以下
                    recommendations.append({
                        'type': '高リスク・高リターン',
                        'description': '高コストだが希少な商品が期待できる',
                        'parameters': risky_params,
                        'cost': risky_cost,
                        'risk_level': 'High'
                    })
            
            return {
                'success': True,
                'data': {
                    'recommendations': recommendations,
                    'current_money': current_money
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'おすすめの取得に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def _get_travel_recommendation(cost: float, expected_value: float, current_money: float) -> str:
        """タイムトラベルの推奨度を判定"""
        if cost > current_money:
            return "資金不足"
        elif cost > current_money * 0.9:
            return "危険: 資金のほとんどを消費"
        elif expected_value < cost:
            return "非推奨: 損失の可能性が高い"
        elif expected_value > cost * 1.5:
            return "推奨: 良好な利益が期待できる"
        else:
            return "普通: 適度な利益が期待できる"


# APIインスタンス
travel_api = TravelAPI()