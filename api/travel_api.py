"""
タイムトラベル仕入れゲーム - タイムトラベルAPI
タイムトラベルと商品取得の処理をJSON形式で提供
"""

from typing import Dict, Any
from core.game_engine import game_engine
from core.item_system import item_system
from core.asset_manager import AssetManager
import random


class TravelAPI:
    """タイムトラベルAPI"""
    
    @staticmethod
    def calculate_travel_cost(years: int, distance: int) -> Dict[str, Any]:
        """タイムトラベルコストを計算（フェーズ2: UFOサイズ廃止）"""
        try:
            # パラメータ検証
            valid, error_message = item_system.validate_travel_parameters(years, distance)
            if not valid:
                return {
                    'success': False,
                    'error': error_message
                }
            
            # 投資コスト計算
            investment_cost = item_system.calculate_travel_cost(years, distance)
            
            # 現在のゲーム状態取得
            current_state = game_engine.get_state()
            current_money = current_state['money']
            current_inventory = current_state['inventory']
            
            # 資産・固定費計算
            assets = AssetManager.calculate_assets(current_money, current_inventory)
            fixed_cost = AssetManager.calculate_fixed_cost(assets)
            
            # 購入可能性判定
            can_afford, afford_message = AssetManager.can_afford_purchase(assets, fixed_cost, investment_cost)
            
            return {
                'success': True,
                'data': {
                    'investment_cost': investment_cost,
                    'fixed_cost': fixed_cost,
                    'total_cost': investment_cost + fixed_cost,
                    'parameters': {
                        'years': years,
                        'distance': distance
                    },
                    'assets': assets,
                    'current_money': current_money,
                    'affordable': can_afford,
                    'afford_message': afford_message,
                    'estimated_items': random.randint(2, 5),  # 新仕様: 2-5個固定
                    'rarity_multiplier': item_system.calculate_rarity_multiplier(years, distance)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'コスト計算に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def preview_travel(years: int, distance: int) -> Dict[str, Any]:
        """タイムトラベルの事前プレビュー（フェーズ2: UFOサイズ廃止）"""
        try:
            # コスト計算
            cost_result = TravelAPI.calculate_travel_cost(years, distance)
            if not cost_result['success']:
                return cost_result
            
            # 新仕様: 期待値計算
            investment_cost = cost_result['data']['investment_cost']
            estimated_items = random.randint(2, 5)  # 2-5個固定
            
            # 新仕様: 投資額±10%の期待値
            expected_min_total = investment_cost * 0.9
            expected_max_total = investment_cost * 1.1
            expected_avg_total = investment_cost
            
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
                            'min': round(expected_min_total - investment_cost, 2),
                            'max': round(expected_max_total - investment_cost, 2),
                            'avg': round(expected_avg_total - investment_cost, 2)
                        }
                    },
                    'risk_assessment': {
                        'failure_rate': 0.1,  # 10%失敗率
                        'high_risk': cost_result['data']['total_cost'] > cost_result['data']['assets'] * 0.8,
                        'recommendation': TravelAPI._get_travel_recommendation(
                            cost_result['data']['total_cost'], 
                            expected_avg_total, 
                            cost_result['data']['assets']
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
    def execute_travel(years: int, distance: int) -> Dict[str, Any]:
        """タイムトラベルを実行（フェーズ2: UFOサイズ廃止・固定費統合）"""
        try:
            current_state = game_engine.get_state()
            current_money = current_state['money']
            current_inventory = current_state['inventory']
            
            # 事前チェック: 資産・固定費・購入可能性
            assets = AssetManager.calculate_assets(current_money, current_inventory)
            fixed_cost = AssetManager.calculate_fixed_cost(assets)
            investment_cost = item_system.calculate_travel_cost(years, distance)
            
            can_afford, afford_message = AssetManager.can_afford_purchase(assets, fixed_cost, investment_cost)
            if not can_afford:
                return {
                    'success': False,
                    'error': afford_message
                }
            
            # タイムトラベル結果を取得
            travel_result = item_system.get_travel_result(years, distance, current_money)
            
            if not travel_result['success']:
                return travel_result
            
            # フェーズ2: 固定費徴収
            total_cost = investment_cost + fixed_cost
            if not game_engine.spend_money(total_cost):
                return {
                    'success': False,
                    'error': '資金が不足しています（固定費含む）'
                }
            
            print(f"[TravelAPI] 資金消費完了: 投資{investment_cost}円 + UFO代金{fixed_cost}円 = 合計{total_cost}円")
            
            # 失敗時の処理
            if travel_result['failed']:
                # ゲームオーバー判定
                new_state = game_engine.get_state()
                new_assets = AssetManager.calculate_assets(new_state['money'], new_state['inventory'])
                new_fixed_cost = AssetManager.calculate_fixed_cost(new_assets)
                is_game_over = AssetManager.check_game_over(new_assets, new_fixed_cost)
                
                return {
                    'success': True,
                    'failed': True,
                    'data': {
                        'investment_cost': investment_cost,
                        'fixed_cost': fixed_cost,
                        'total_cost': total_cost,
                        'items': [],
                        'message': travel_result['message'],
                        'new_money': new_state['money'],
                        'new_assets': new_assets,
                        'game_over': is_game_over
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
            
            # 最終状態とゲームオーバー判定
            final_state = game_engine.get_state()
            final_assets = AssetManager.calculate_assets(final_state['money'], final_state['inventory'])
            final_fixed_cost = AssetManager.calculate_fixed_cost(final_assets)
            is_game_over = AssetManager.check_game_over(final_assets, final_fixed_cost)
            
            return {
                'success': True,
                'failed': False,
                'data': {
                    'investment_cost': investment_cost,
                    'fixed_cost': fixed_cost,
                    'total_cost': total_cost,
                    'items': display_items,
                    'item_count': len(items),
                    'total_value': travel_result['total_value'],
                    'message': travel_result['message'],
                    'new_money': final_state['money'],
                    'new_assets': final_assets,
                    'new_inventory_count': len(final_state['inventory']),
                    'game_over': is_game_over,
                    'travel_info': {
                        'years': years,
                        'distance': distance,
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
            
            # 現在の資産状況取得
            current_state = game_engine.get_state()
            assets = AssetManager.calculate_assets(current_money, current_state['inventory'])
            
            # 低コスト・安全志向
            safe_params = {'years': 10, 'distance': 100}
            safe_cost = item_system.calculate_travel_cost(**safe_params)
            safe_fixed_cost = AssetManager.calculate_fixed_cost(assets)
            safe_total = safe_cost + safe_fixed_cost
            
            if safe_total <= assets:
                recommendations.append({
                    'type': '安全志向',
                    'description': '低コスト・低リスクでの商品取得',
                    'parameters': safe_params,
                    'investment_cost': safe_cost,
                    'fixed_cost': safe_fixed_cost,
                    'total_cost': safe_total,
                    'risk_level': 'Low'
                })
            
            # バランス型
            balanced_params = {'years': 30, 'distance': 500}
            balanced_cost = item_system.calculate_travel_cost(**balanced_params)
            balanced_total = balanced_cost + safe_fixed_cost  # 固定費は同じ
            
            if balanced_total <= assets:
                recommendations.append({
                    'type': 'バランス型',
                    'description': '適度なコストでより良い商品を狙う',
                    'parameters': balanced_params,
                    'investment_cost': balanced_cost,
                    'fixed_cost': safe_fixed_cost,
                    'total_cost': balanced_total,
                    'risk_level': 'Medium'
                })
            
            # 高リスク・高リターン
            if assets >= 1000:
                risky_params = {'years': 100, 'distance': 2000}
                risky_cost = item_system.calculate_travel_cost(**risky_params)
                risky_total = risky_cost + safe_fixed_cost
                
                if risky_total <= assets * 0.8:  # 資産の80%以下
                    recommendations.append({
                        'type': '高リスク・高リターン',
                        'description': '高コストだが希少な商品が期待できる',
                        'parameters': risky_params,
                        'investment_cost': risky_cost,
                        'fixed_cost': safe_fixed_cost,
                        'total_cost': risky_total,
                        'risk_level': 'High'
                    })
            
            return {
                'success': True,
                'data': {
                    'recommendations': recommendations,
                    'current_money': current_money,
                    'current_assets': assets,
                    'fixed_cost_rate': AssetManager.calculate_fixed_cost(assets) / assets if assets > 0 else 0
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'おすすめの取得に失敗しました: {str(e)}'
            }
    
    @staticmethod
    def _get_travel_recommendation(total_cost: float, expected_value: float, assets: float) -> str:
        """タイムトラベルの推奨度を判定（フェーズ2: 資産ベース）"""
        if total_cost > assets:
            return "資産不足"
        elif total_cost > assets * 0.9:
            return "危険: 資産のほとんどを消費"
        elif expected_value < total_cost:
            return "非推奨: 損失の可能性が高い"
        elif expected_value > total_cost * 1.5:
            return "推奨: 良好な利益が期待できる"
        else:
            return "普通: 適度な利益が期待できる"


# APIインスタンス
travel_api = TravelAPI()