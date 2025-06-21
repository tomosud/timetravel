"""
タイムトラベル仕入れゲーム - ターンシステム
大ターン・子ターン管理と価格倍率曲線生成
"""

import random
from typing import List, Dict, Any
import time
from .asset_manager import AssetManager


class TurnSystem:
    """大ターン・子ターンシステムと価格倍率曲線管理"""
    
    # 設定可能な変数
    MINOR_TURNS_PER_MAJOR = 8      # 大ターンあたりの子ターン数
    # TARGET_GROWTH_MULTIPLIER = 10.0  # フェーズ2で可変化のため廃止
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
        self.turn_multipliers = []  # 各ターンの倍率
        self.target_multiplier = AssetManager.generate_target_multiplier()  # フェーズ2: 目標倍率
        self.generate_new_price_curve()
        
        print(f"[TurnSystem] 初期化完了")
        print(f"  設定: 子ターン数={self.MINOR_TURNS_PER_MAJOR}, 目標倍率={self.target_multiplier:.2f}倍")
        print(f"  乱数範囲: {self.RANDOM_MIN}～{self.RANDOM_MAX}")
        self._debug_current_state()
    
    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """値を最小～最大に収めるユーティリティ"""
        return max(min_val, min(max_val, value))
    
    def _generate_multipliers(self, target: float) -> List[float]:
        """目標値targetを8ステップで達成するための乗数を作成"""
        multipliers = []
        current = 1.0
        
        for i in range(self.MINOR_TURNS_PER_MAJOR):
            remaining = self.MINOR_TURNS_PER_MAJOR - i
            # 残りステップで目標値に到達するのに必要な理想的な乗数
            ideal = pow(target / current, 1.0 / remaining)
            # 60%-140%の揺らぎを加える
            factor = ideal * (0.6 + random.random() * 0.8)
            # 0.5-2.0の範囲に制限
            factor = self._clamp(factor, 0.5, 2.0)
            
            multipliers.append(factor)
            current *= factor
            
        
        return multipliers
    
    def _calc_cumulative(self, multipliers: List[float]) -> List[float]:
        """乗数配列から各ステップ後の累積値を求める"""
        cumulative = 1.0
        result = []
        for m in multipliers:
            cumulative *= m
            result.append(cumulative)
        return result

    def generate_new_price_curve(self) -> List[float]:
        """新しい価格倍率曲線を生成（JSサンプル移植版）"""
        print(f"\n[TurnSystem] 大ターン{self.major_turn} - 新しい価格曲線を生成中...")
        print(f"  目標倍率: {self.target_multiplier:.2f}倍")
        
        # 複数回試行して最も良い結果を採用
        best_multipliers = None
        best_error = float('inf')
        
        for attempt in range(10):  # 10回試行
            multipliers = self._generate_multipliers(self.target_multiplier)
            cumulative_values = self._calc_cumulative(multipliers)
            final_value = cumulative_values[-1]
            error = abs(final_value - self.target_multiplier)
            
            if error < best_error:
                best_error = error
                best_multipliers = multipliers
        
        # 最良の結果を採用
        self.turn_multipliers = best_multipliers
        self.price_curve = self._calc_cumulative(best_multipliers)
        
        print(f"  各ターン乗数: {[f'{x:.2f}x' for x in self.turn_multipliers]}")
        print(f"  累積値: {[f'{x:.2f}' for x in self.price_curve]}")
        print(f"  最終到達値: {self.price_curve[-1]:.2f} (目標: {self.target_multiplier:.2f})")
        print(f"  誤差: {best_error:.3f} (10回試行での最良値)")
        
        return self.price_curve
    
    def get_target_multiplier(self) -> float:
        """現在の目標倍率を取得（フェーズ2）"""
        return self.target_multiplier
    
    def get_current_price_multiplier(self) -> float:
        """現在の子ターンの価格倍率を取得（各ターンの倍率）"""
        if not self.turn_multipliers or self.minor_turn < 1 or self.minor_turn > len(self.turn_multipliers):
            print(f"[TurnSystem] WARNING: 無効な子ターン {self.minor_turn}")
            return 1.0
        
        multiplier = self.turn_multipliers[self.minor_turn - 1]
        print(f"[TurnSystem] 現在のターン倍率: {multiplier:.2f}x (大ターン{self.major_turn}, 子ターン{self.minor_turn})")
        return multiplier
    
    def get_current_cumulative_multiplier(self) -> float:
        """現在の子ターンの累積価格倍率を取得（商品生成用）"""
        if not self.price_curve or self.minor_turn < 1 or self.minor_turn > len(self.price_curve):
            print(f"[TurnSystem] WARNING: 無効な子ターン {self.minor_turn}")
            return 1.0
        
        multiplier = self.price_curve[self.minor_turn - 1]
        print(f"[TurnSystem] 現在の累積倍率: {multiplier:.2f} (商品生成用)")
        return multiplier
    
    def advance_minor_turn(self) -> bool:
        """子ターンを進める"""
        print(f"\n[TurnSystem] 子ターン進行: {self.minor_turn} → {self.minor_turn + 1}")
        
        if self.minor_turn >= self.MINOR_TURNS_PER_MAJOR:
            # 大ターン終了、新しい大ターン開始
            self.major_turn += 1
            self.minor_turn = 1
            # フェーズ2: 新しい目標倍率を生成
            self.target_multiplier = AssetManager.generate_target_multiplier()
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
            'target_multiplier': self.target_multiplier,  # フェーズ2: 目標倍率追加
            'price_curve': self.price_curve.copy(),
            'turn_multipliers': self.turn_multipliers.copy(),  # 各ターンの倍率追加
            'progress_ratio': self.minor_turn / self.MINOR_TURNS_PER_MAJOR,
            'is_major_turn_complete': self.minor_turn >= self.MINOR_TURNS_PER_MAJOR
        }
    
    def reset_turns(self):
        """ターンシステムをリセット"""
        print(f"\n[TurnSystem] ターンシステムリセット")
        self.major_turn = 1
        self.minor_turn = 1
        self.price_curve = []
        self.turn_multipliers = []
        # フェーズ2: 新しい目標倍率を生成
        self.target_multiplier = AssetManager.generate_target_multiplier()
        self.generate_new_price_curve()
        self._debug_current_state()
    
    def _debug_current_state(self):
        """デバッグ用現在状態表示"""
        print(f"[TurnSystem] 現在状態:")
        print(f"  大ターン: {self.major_turn}")
        print(f"  子ターン: {self.minor_turn}/{self.MINOR_TURNS_PER_MAJOR}")
        print(f"  目標倍率: {self.target_multiplier:.2f}倍")
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