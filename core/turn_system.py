"""
タイムトラベル仕入れゲーム - ターンシステム
大ターン・子ターン管理と価格倍率曲線生成
"""

import random
from typing import List, Dict, Any
import time


class TurnSystem:
    """大ターン・子ターンシステムと価格倍率曲線管理"""
    
    # 設定可能な変数
    MINOR_TURNS_PER_MAJOR = 8      # 大ターンあたりの子ターン数
    TARGET_GROWTH_MULTIPLIER = 10.0  # 大ターン終了時の目標倍率
    RANDOM_MIN = 0.5               # 乱数の最小値
    RANDOM_MAX = 1.8               # 乱数の最大値
    FIRST_TURN_MIN = 1.0           # 最初の子ターンの最小倍率
    ENABLE_TREND_BIAS = True       # トレンド要素の有効化
    TREND_STRENGTH = 0.1           # トレンド要素の強度
    
    def __init__(self):
        """ターンシステム初期化"""
        self.major_turn = 1
        self.minor_turn = 1
        self.price_curve = []
        self.generate_new_price_curve()
        
        print(f"[TurnSystem] 初期化完了")
        print(f"  設定: 子ターン数={self.MINOR_TURNS_PER_MAJOR}, 目標倍率={self.TARGET_GROWTH_MULTIPLIER}")
        print(f"  乱数範囲: {self.RANDOM_MIN}～{self.RANDOM_MAX}")
        self._debug_current_state()
    
    def generate_new_price_curve(self) -> List[float]:
        """新しい価格倍率曲線を生成"""
        print(f"\n[TurnSystem] 大ターン{self.major_turn} - 新しい価格曲線を生成中...")
        
        # トレンド要素の決定
        trend_bias = 0.0
        if self.ENABLE_TREND_BIAS:
            trend_type = random.choice(['up', 'neutral', 'down'])
            trend_bias = {
                'up': self.TREND_STRENGTH,
                'neutral': 0.0,
                'down': -self.TREND_STRENGTH
            }[trend_type]
            print(f"  トレンド: {trend_type} (バイアス: {trend_bias:+.2f})")
        
        # ランダム乗数の生成
        raw_multipliers = []
        for i in range(self.MINOR_TURNS_PER_MAJOR):
            base_random = random.uniform(self.RANDOM_MIN, self.RANDOM_MAX)
            multiplier = base_random + trend_bias
            
            # 最初の子ターンは必ず1.0以上
            if i == 0 and multiplier < self.FIRST_TURN_MIN:
                multiplier = self.FIRST_TURN_MIN
            
            raw_multipliers.append(multiplier)
        
        print(f"  生ランダム乗数: {[f'{x:.2f}' for x in raw_multipliers]}")
        
        # 累積乗算
        cumulative_values = []
        current_value = 1.0
        for multiplier in raw_multipliers:
            current_value *= multiplier
            cumulative_values.append(current_value)
        
        print(f"  累積値: {[f'{x:.2f}' for x in cumulative_values]}")
        
        # 正規化（最終値を目標倍率に調整）
        final_value = cumulative_values[-1]
        scale_factor = self.TARGET_GROWTH_MULTIPLIER / final_value
        
        self.price_curve = [value * scale_factor for value in cumulative_values]
        
        print(f"  最終値: {final_value:.2f} → スケール係数: {scale_factor:.3f}")
        print(f"  正規化済み曲線: {[f'{x:.2f}' for x in self.price_curve]}")
        print(f"  変化率: {[f'{(self.price_curve[i]/self.price_curve[i-1]-1)*100:+.1f}%' if i > 0 else '+0.0%' for i in range(len(self.price_curve))]}")
        
        return self.price_curve
    
    def get_current_price_multiplier(self) -> float:
        """現在の子ターンの価格倍率を取得"""
        if not self.price_curve or self.minor_turn < 1 or self.minor_turn > len(self.price_curve):
            print(f"[TurnSystem] WARNING: 無効な子ターン {self.minor_turn}")
            return 1.0
        
        multiplier = self.price_curve[self.minor_turn - 1]
        print(f"[TurnSystem] 現在の価格倍率: {multiplier:.2f} (大ターン{self.major_turn}, 子ターン{self.minor_turn})")
        return multiplier
    
    def advance_minor_turn(self) -> bool:
        """子ターンを進める"""
        print(f"\n[TurnSystem] 子ターン進行: {self.minor_turn} → {self.minor_turn + 1}")
        
        if self.minor_turn >= self.MINOR_TURNS_PER_MAJOR:
            # 大ターン終了、新しい大ターン開始
            self.major_turn += 1
            self.minor_turn = 1
            self.generate_new_price_curve()
            
            print(f"[TurnSystem] 🎉 大ターン{self.major_turn - 1}完了！新しい大ターン{self.major_turn}開始")
            self._debug_current_state()
            return True
        else:
            # 子ターン進行
            self.minor_turn += 1
            self._debug_current_state()
            return False
    
    def get_turn_info(self) -> Dict[str, Any]:
        """現在のターン情報を取得"""
        return {
            'major_turn': self.major_turn,
            'minor_turn': self.minor_turn,
            'minor_turns_total': self.MINOR_TURNS_PER_MAJOR,
            'current_multiplier': self.get_current_price_multiplier(),
            'price_curve': self.price_curve.copy(),
            'progress_ratio': self.minor_turn / self.MINOR_TURNS_PER_MAJOR,
            'is_major_turn_complete': self.minor_turn >= self.MINOR_TURNS_PER_MAJOR
        }
    
    def reset_turns(self):
        """ターンシステムをリセット"""
        print(f"\n[TurnSystem] ターンシステムリセット")
        self.major_turn = 1
        self.minor_turn = 1
        self.price_curve = []
        self.generate_new_price_curve()
        self._debug_current_state()
    
    def _debug_current_state(self):
        """デバッグ用現在状態表示"""
        print(f"[TurnSystem] 現在状態:")
        print(f"  大ターン: {self.major_turn}")
        print(f"  子ターン: {self.minor_turn}/{self.MINOR_TURNS_PER_MAJOR}")
        print(f"  現在倍率: {self.get_current_price_multiplier():.2f}x")
        
        # 価格曲線の進行状況表示
        progress_bar = ""
        for i in range(self.MINOR_TURNS_PER_MAJOR):
            if i + 1 < self.minor_turn:
                progress_bar += "✓"
            elif i + 1 == self.minor_turn:
                progress_bar += "●"
            else:
                progress_bar += "○"
        print(f"  進行状況: {progress_bar}")
        
        # 今後の倍率予告（デバッグ用）
        if len(self.price_curve) >= self.minor_turn:
            upcoming = self.price_curve[self.minor_turn - 1:min(self.minor_turn + 2, len(self.price_curve))]
            print(f"  今後の倍率: {[f'{x:.2f}' for x in upcoming]}")


# グローバルインスタンス
turn_system = TurnSystem()


# 設定変更用の関数群
def configure_turn_system(
    minor_turns_per_major: int = None,
    target_growth: float = None,
    random_range: tuple = None,
    trend_settings: dict = None
):
    """ターンシステムの設定を変更"""
    global turn_system
    
    if minor_turns_per_major is not None:
        turn_system.MINOR_TURNS_PER_MAJOR = minor_turns_per_major
        print(f"[Config] 子ターン数を {minor_turns_per_major} に変更")
    
    if target_growth is not None:
        turn_system.TARGET_GROWTH_MULTIPLIER = target_growth
        print(f"[Config] 目標成長倍率を {target_growth} に変更")
    
    if random_range is not None:
        turn_system.RANDOM_MIN, turn_system.RANDOM_MAX = random_range
        print(f"[Config] 乱数範囲を {random_range[0]}～{random_range[1]} に変更")
    
    if trend_settings is not None:
        if 'enable' in trend_settings:
            turn_system.ENABLE_TREND_BIAS = trend_settings['enable']
        if 'strength' in trend_settings:
            turn_system.TREND_STRENGTH = trend_settings['strength']
        print(f"[Config] トレンド設定を変更: {trend_settings}")
    
    # 設定変更後は新しい曲線を生成
    turn_system.generate_new_price_curve()