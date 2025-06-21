"""
フェーズ2: 資産管理・固定費・ゲームオーバー管理システム
"""

import random
from typing import Dict, List, Any, Tuple
from .phase2_config import (
    TARGET_MULTIPLIER_MIN, TARGET_MULTIPLIER_MAX, 
    FIXED_COST_RATE, INVENTORY_SELL_RATE, ENABLE_GAME_OVER
)


class AssetManager:
    """資産・固定費・ゲーム状態管理"""
    
    @classmethod
    def calculate_assets(cls, money: float, inventory: List[Dict[str, Any]]) -> float:
        """
        総資産を計算
        資産 = 現金 + 在庫価値合計
        """
        cash = float(money)
        
        # 在庫価値の合計（base_valueを使用）
        inventory_value = 0.0
        for item in inventory:
            if 'base_value' in item:
                inventory_value += float(item['base_value'])
        
        total_assets = cash + inventory_value
        
        print(f"[AssetManager] 資産計算:")
        print(f"  現金: {cash:.2f}円")
        print(f"  在庫価値: {inventory_value:.2f}円 ({len(inventory)}個)")
        print(f"  総資産: {total_assets:.2f}円")
        
        return round(total_assets, 2)
    
    @classmethod
    def calculate_fixed_cost(cls, assets: float) -> float:
        """
        固定費（UFO代金）を計算
        固定費 = 資産 × 5%
        """
        fixed_cost = assets * FIXED_COST_RATE
        
        print(f"[AssetManager] 固定費計算:")
        print(f"  資産: {assets:.2f}円")
        print(f"  固定費率: {FIXED_COST_RATE*100:.1f}%")
        print(f"  UFO代金: {fixed_cost:.2f}円")
        
        return round(fixed_cost, 2)
    
    @classmethod
    def check_game_over(cls, assets: float, fixed_cost: float) -> bool:
        """
        ゲームオーバー判定
        資産 < 固定費 = ゲームオーバー
        """
        if not ENABLE_GAME_OVER:
            return False
            
        is_game_over = assets < fixed_cost
        
        print(f"[AssetManager] ゲームオーバー判定:")
        print(f"  資産: {assets:.2f}円")
        print(f"  必要固定費: {fixed_cost:.2f}円")
        print(f"  結果: {'ゲームオーバー' if is_game_over else '継続可能'}")
        
        return is_game_over
    
    @classmethod
    def can_afford_purchase(cls, assets: float, fixed_cost: float, investment: float) -> Tuple[bool, str]:
        """
        購入可能性判定
        資産 >= 固定費 + 投資額
        """
        required_total = fixed_cost + investment
        can_afford = assets >= required_total
        
        if not can_afford:
            shortage = required_total - assets
            message = f"資金不足: {shortage:.2f}円足りません（必要: {required_total:.2f}円、保有: {assets:.2f}円）"
        else:
            remaining = assets - required_total
            message = f"購入可能（購入後残高: {remaining:.2f}円）"
        
        print(f"[AssetManager] 購入可能性判定:")
        print(f"  資産: {assets:.2f}円")
        print(f"  固定費: {fixed_cost:.2f}円")
        print(f"  投資額: {investment:.2f}円")
        print(f"  必要合計: {required_total:.2f}円")
        print(f"  結果: {message}")
        
        return can_afford, message
    
    @classmethod
    def generate_target_multiplier(cls) -> float:
        """
        目標倍率をランダム生成
        0.1倍 ～ 10.0倍
        """
        # 対数スケールでより自然な分布
        import math
        log_min = math.log(TARGET_MULTIPLIER_MIN)
        log_max = math.log(TARGET_MULTIPLIER_MAX)
        log_value = random.uniform(log_min, log_max)
        multiplier = math.exp(log_value)
        
        # 小数点2桁で丸める
        multiplier = round(multiplier, 2)
        
        print(f"[AssetManager] 目標倍率生成:")
        print(f"  範囲: {TARGET_MULTIPLIER_MIN:.1f}倍 ～ {TARGET_MULTIPLIER_MAX:.1f}倍")
        print(f"  生成値: {multiplier:.2f}倍")
        
        return multiplier
    
    @classmethod
    def get_multiplier_description(cls, multiplier: float) -> str:
        """
        目標倍率の説明テキスト生成
        """
        if multiplier >= 7.0:
            return f"🚀 超高成長期待 ({multiplier:.1f}倍) - 積極投資推奨"
        elif multiplier >= 5.0:
            return f"📈 高成長期待 ({multiplier:.1f}倍) - 積極投資"
        elif multiplier >= 3.0:
            return f"📊 成長期待 ({multiplier:.1f}倍) - 適度な投資"
        elif multiplier >= 2.0:
            return f"⚖️ 堅実成長 ({multiplier:.1f}倍) - 安定投資"
        else:
            return f"🔒 保守期間 ({multiplier:.1f}倍) - 慎重な投資"
    
    @classmethod
    def calculate_inventory_sell_value(cls, inventory: List[Dict[str, Any]]) -> float:
        """
        在庫の売却可能価値を計算
        売却価値 = base_value × 100%
        """
        total_sell_value = 0.0
        
        for item in inventory:
            if 'base_value' in item:
                sell_value = float(item['base_value']) * INVENTORY_SELL_RATE
                total_sell_value += sell_value
        
        print(f"[AssetManager] 在庫売却価値計算:")
        print(f"  在庫数: {len(inventory)}個")
        print(f"  売却率: {INVENTORY_SELL_RATE*100:.0f}%")
        print(f"  売却可能価値: {total_sell_value:.2f}円")
        
        return round(total_sell_value, 2)
    
    @classmethod
    def get_asset_info(cls, money: float, inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        資産情報の詳細を取得
        """
        assets = cls.calculate_assets(money, inventory)
        fixed_cost = cls.calculate_fixed_cost(assets)
        sell_value = cls.calculate_inventory_sell_value(inventory)
        is_game_over = cls.check_game_over(assets, fixed_cost)
        
        return {
            'assets': assets,
            'cash': float(money),
            'inventory_value': assets - float(money),
            'inventory_count': len(inventory),
            'fixed_cost': fixed_cost,
            'fixed_cost_rate': FIXED_COST_RATE,
            'sell_value': sell_value,
            'is_game_over': is_game_over,
            'can_continue': assets >= fixed_cost
        }