"""
タイムトラベル仕入れゲーム - アイテムシステム
商品の生成、管理、評価ロジックを担当
"""

import random
import time
from typing import Dict, List, Any, Tuple
from .turn_system import turn_system


class ItemSystem:
    """商品システム管理"""
    
    # 10ジャンルのハードコード
    GENRES = [
        "家電", "玩具", "服飾", "書籍", "美術品",
        "楽器", "スポーツ用品", "工具", "食器", "アクセサリー"
    ]
    
    # 状態の定義
    CONDITIONS = {
        'A': {'name': '新品', 'multiplier': 1.0},
        'B': {'name': '良品', 'multiplier': 0.8},
        'C': {'name': '劣化', 'multiplier': 0.6}
    }
    
    def __init__(self):
        """アイテムシステム初期化"""
        pass
    
    @staticmethod
    def calculate_travel_cost(years: int, distance: int, ufo_size: float) -> float:
        """タイムトラベルコストを計算"""
        return (years * distance) * ufo_size
    
    @staticmethod
    def calculate_rarity_multiplier(years: int, distance: int) -> float:
        """距離と年数に基づいてレア度倍率を計算"""
        # 基本倍率
        base_multiplier = 1.0
        
        # 年数ボーナス（古いほど希少）
        year_bonus = min(years * 0.02, 2.0)  # 最大2.0倍まで
        
        # 距離ボーナス（遠いほど希少）
        distance_bonus = min(distance * 0.001, 1.5)  # 最大1.5倍まで
        
        # 組み合わせボーナス（年数と距離の相乗効果）
        combo_bonus = (years * distance) * 0.00001
        combo_bonus = min(combo_bonus, 1.0)  # 最大1.0倍まで
        
        total_multiplier = base_multiplier + year_bonus + distance_bonus + combo_bonus
        return round(total_multiplier, 2)
    
    @staticmethod
    def get_rarity_name(multiplier: float) -> str:
        """倍率に応じてレア度名を返す"""
        if multiplier < 1.5:
            return 'コモン'
        elif multiplier < 2.5:
            return 'レア'
        elif multiplier < 4.0:
            return 'ウルトラレア'
        elif multiplier < 5.5:
            return '伝説'
        else:
            return '神話'
    
    @classmethod
    def generate_item_with_predetermined_value(cls, actual_value: float, years: int, distance: int) -> Dict[str, Any]:
        """事前決定された価値でアイテムを生成（新仕様）"""
        genre = random.choice(cls.GENRES)
        
        # 年代が古いほど劣化しやすい（表示用）
        condition_weights = {
            'A': max(0.1, 1.0 - years * 0.01),
            'B': 0.5,
            'C': min(0.9, years * 0.01)
        }
        condition = random.choices(
            list(condition_weights.keys()), 
            weights=list(condition_weights.values())
        )[0]
        
        # 距離と年数に基づいてレア度倍率を計算（表示用）
        rarity_multiplier = cls.calculate_rarity_multiplier(years, distance)
        rarity_name = cls.get_rarity_name(rarity_multiplier)
        
        # 表示用基本価値（逆算）
        condition_mult = cls.CONDITIONS[condition]['multiplier']
        display_base_value = actual_value / (condition_mult * rarity_multiplier)
        
        # 一意のIDを生成
        item_id = int(time.time() * 1000000 + random.randint(0, 999999))
        
        return {
            'id': item_id,
            'genre': genre,
            'condition': condition,
            'condition_name': cls.CONDITIONS[condition]['name'],
            'rarity': rarity_name,
            'rarity_multiplier': rarity_multiplier,
            'base_value': round(actual_value, 2),  # 実際の価値を使用
            'display_base_value': round(display_base_value, 2),  # 表示用
            'years': years,
            'distance': distance,
            'created_at': time.time()
        }

    @classmethod
    def generate_item(cls, years: int, distance: int) -> Dict[str, Any]:
        """年代と距離に基づいて商品を生成（旧仕様・互換性維持）"""
        genre = random.choice(cls.GENRES)
        
        # 年代が古いほど劣化しやすい
        condition_weights = {
            'A': max(0.1, 1.0 - years * 0.01),
            'B': 0.5,
            'C': min(0.9, years * 0.01)
        }
        condition = random.choices(
            list(condition_weights.keys()), 
            weights=list(condition_weights.values())
        )[0]
        
        # 距離と年数に基づいてレア度倍率を計算
        rarity_multiplier = cls.calculate_rarity_multiplier(years, distance)
        rarity_name = cls.get_rarity_name(rarity_multiplier)
        
        # 基本価値を計算
        base_value = random.uniform(100, 1000)
        base_value *= cls.CONDITIONS[condition]['multiplier']
        base_value *= rarity_multiplier
        
        # 一意のIDを生成
        item_id = int(time.time() * 1000000 + random.randint(0, 999999))
        
        return {
            'id': item_id,
            'genre': genre,
            'condition': condition,
            'condition_name': cls.CONDITIONS[condition]['name'],
            'rarity': rarity_name,
            'rarity_multiplier': rarity_multiplier,
            'base_value': round(base_value, 2),
            'years': years,
            'distance': distance,
            'created_at': time.time()
        }
    
    @classmethod
    def generate_items(cls, years: int, distance: int, count: int) -> List[Dict[str, Any]]:
        """複数のアイテムを生成"""
        return [cls.generate_item(years, distance) for _ in range(count)]
    
    @classmethod
    def calculate_estimated_selling_price(cls, item: Dict[str, Any]) -> float:
        """アイテムの推定売却価格を計算"""
        # 基本価値の80%を推定売却価格とする
        return round(item['base_value'] * 0.8, 2)
    
    @classmethod
    def get_item_display_info(cls, item: Dict[str, Any]) -> Dict[str, Any]:
        """アイテムの表示用情報を取得"""
        return {
            'id': item['id'],
            'genre': item['genre'],
            'condition': item['condition'],
            'condition_name': item.get('condition_name', cls.CONDITIONS[item['condition']]['name']),
            'rarity': item['rarity'],
            'rarity_multiplier': item['rarity_multiplier'],
            'base_value': item['base_value'],
            'estimated_price': cls.calculate_estimated_selling_price(item),
            'years': item['years'],
            'distance': item['distance'],
            'acquisition_info': {
                'years_ago': item['years'],
                'distance_km': item['distance'],
                'rarity_score': item['rarity_multiplier']
            }
        }
    
    @classmethod
    def validate_travel_parameters(cls, years: int, distance: int, ufo_size: float) -> Tuple[bool, str]:
        """タイムトラベルパラメータの妥当性をチェック"""
        if years < 1 or years > 1000000:
            return False, "年数は1〜1000000年の範囲で指定してください"
        
        if distance < 0 or distance > 50000:
            return False, "距離は0〜50000kmの範囲で指定してください"
        
        if ufo_size < 1.0 or ufo_size > 10.0:
            return False, "UFOサイズは1.0〜10.0倍の範囲で指定してください"
        
        return True, ""
    
    @classmethod
    def simulate_travel_failure(cls) -> bool:
        """タイムトラベル失敗をシミュレート（10%の確率）"""
        return random.random() < 0.1
    
    @classmethod
    def distribute_value_across_items(cls, target_total: float, num_items: int) -> List[float]:
        """目標総価値をアイテム間で分配（新仕様）"""
        if num_items <= 0:
            return []
        
        base_value = target_total / num_items
        values = []
        remaining_total = target_total
        
        for i in range(num_items - 1):
            # ±40%のバリエーションを持たせる
            min_val = max(base_value * 0.6, 100)  # 最小100円
            max_val = min(base_value * 1.4, remaining_total * 0.8)
            
            if max_val <= min_val:
                max_val = min_val * 1.1
            
            item_value = random.uniform(min_val, max_val)
            values.append(item_value)
            remaining_total -= item_value
        
        # 最後のアイテムは残り全額（最小100円保証）
        values.append(max(remaining_total, 100))
        return values

    @classmethod
    def get_travel_result(cls, years: int, distance: int, ufo_size: float, 
                         available_money: float) -> Dict[str, Any]:
        """タイムトラベルの結果を取得（新仕様）"""
        # パラメータ検証
        valid, error_message = cls.validate_travel_parameters(years, distance, ufo_size)
        if not valid:
            return {
                'success': False,
                'error': error_message
            }
        
        # コスト計算
        cost = cls.calculate_travel_cost(years, distance, ufo_size)
        
        # 資金チェック
        if cost > available_money:
            return {
                'success': False,
                'error': f"資金が不足しています。必要: {cost}円, 所持金: {available_money}円"
            }
        
        # 失敗判定
        failed = cls.simulate_travel_failure()
        
        if failed:
            return {
                'success': True,
                'failed': True,
                'cost': cost,
                'items': [],
                'message': "タイムトラベルに失敗しました。お金は消費されましたが、商品は取得できませんでした。"
            }
        
        # 新仕様: アイテム数を2-5個固定
        item_count = random.randint(2, 5)
        
        # 新仕様: 目標総価値（投資額±10%）
        variance = random.uniform(0.9, 1.1)
        target_total_value = cost * variance
        
        # 価値分配
        individual_values = cls.distribute_value_across_items(target_total_value, item_count)
        
        # アイテム生成
        items = []
        for actual_value in individual_values:
            item = cls.generate_item_with_predetermined_value(actual_value, years, distance)
            items.append(item)
        
        return {
            'success': True,
            'failed': False,
            'cost': cost,
            'items': items,
            'item_count': len(items),
            'total_value': round(sum(item['base_value'] for item in items), 2),
            'message': f"タイムトラベルに成功！{len(items)}個のアイテムを取得しました。"
        }
    
    @classmethod
    def get_inventory_summary(cls, inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """在庫のサマリー情報を取得"""
        if not inventory:
            return {
                'total_items': 0,
                'total_value': 0,
                'genre_breakdown': {},
                'rarity_breakdown': {},
                'condition_breakdown': {}
            }
        
        total_value = sum(item['base_value'] for item in inventory)
        
        # ジャンル別集計
        genre_breakdown = {}
        for item in inventory:
            genre = item['genre']
            if genre not in genre_breakdown:
                genre_breakdown[genre] = {'count': 0, 'value': 0}
            genre_breakdown[genre]['count'] += 1
            genre_breakdown[genre]['value'] += item['base_value']
        
        # レア度別集計
        rarity_breakdown = {}
        for item in inventory:
            rarity = item['rarity']
            if rarity not in rarity_breakdown:
                rarity_breakdown[rarity] = {'count': 0, 'value': 0}
            rarity_breakdown[rarity]['count'] += 1
            rarity_breakdown[rarity]['value'] += item['base_value']
        
        # 状態別集計
        condition_breakdown = {}
        for item in inventory:
            condition = item['condition']
            if condition not in condition_breakdown:
                condition_breakdown[condition] = {'count': 0, 'value': 0}
            condition_breakdown[condition]['count'] += 1
            condition_breakdown[condition]['value'] += item['base_value']
        
        return {
            'total_items': len(inventory),
            'total_value': round(total_value, 2),
            'average_value': round(total_value / len(inventory), 2),
            'genre_breakdown': genre_breakdown,
            'rarity_breakdown': rarity_breakdown,
            'condition_breakdown': condition_breakdown
        }


# シングルトンインスタンス
item_system = ItemSystem()