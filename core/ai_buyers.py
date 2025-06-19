"""
タイムトラベル仕入れゲーム - AIバイヤーシステム
オークションでの自動入札者を管理
"""

import random
from typing import Dict, List, Any, Tuple
from .item_system import ItemSystem


class AIBuyer:
    """個別のAIバイヤー"""
    
    def __init__(self, buyer_id: int, interested_genres: List[str], 
                 condition_preference: float, rarity_preference: float, 
                 price_sensitivity: float):
        """
        AIバイヤー初期化
        
        Args:
            buyer_id: バイヤーID
            interested_genres: 興味のあるジャンルリスト
            condition_preference: 状態への関心度 (0.5-1.0)
            rarity_preference: 希少性への関心度 (0.8-1.5)
            price_sensitivity: 価格感度 (0.5-1.2)
        """
        self.id = buyer_id
        self.interested_genres = interested_genres
        self.condition_preference = condition_preference
        self.rarity_preference = rarity_preference
        self.price_sensitivity = price_sensitivity
        self.bid_history = []
    
    def calculate_interest(self, item: Dict[str, Any], price: float) -> float:
        """商品への興味度を計算"""
        # ジャンルマッチング
        if item['genre'] not in self.interested_genres:
            return 0.0
        
        # 基本興味度
        interest = 1.0
        
        # 状態への評価
        condition_multiplier = ItemSystem.CONDITIONS[item['condition']]['multiplier']
        interest *= (condition_multiplier * self.condition_preference)
        
        # 希少性への評価
        rarity_score = item.get('rarity_multiplier', 1.0)
        interest *= (rarity_score * self.rarity_preference)
        
        # 価格評価（高すぎると興味が下がる）
        if price > 0:
            value_ratio = item['base_value'] / price
            price_factor = min(2.0, value_ratio * self.price_sensitivity)
            interest *= price_factor
        
        return round(interest, 3)
    
    def should_bid(self, item: Dict[str, Any], current_price: float, 
                   interest_threshold: float = 0.8) -> bool:
        """入札すべきかどうかを判定"""
        interest = self.calculate_interest(item, current_price)
        return interest >= interest_threshold
    
    def calculate_bid_amount(self, item: Dict[str, Any], current_price: float) -> float:
        """入札額を計算"""
        interest = self.calculate_interest(item, current_price)
        
        # 興味度に基づいて入札額を決定
        base_increase = current_price * random.uniform(0.05, 0.15)
        interest_multiplier = min(interest, 2.0)
        bid_increase = base_increase * interest_multiplier
        
        return round(current_price + bid_increase, 2)
    
    def record_bid(self, item_id: int, bid_amount: float, won: bool) -> None:
        """入札履歴を記録"""
        self.bid_history.append({
            'item_id': item_id,
            'bid_amount': bid_amount,
            'won': won,
            'timestamp': random.random()  # 簡易タイムスタンプ
        })
    
    def get_profile(self) -> Dict[str, Any]:
        """バイヤーのプロフィール情報を取得"""
        return {
            'id': self.id,
            'interested_genres': self.interested_genres,
            'preferences': {
                'condition_preference': self.condition_preference,
                'rarity_preference': self.rarity_preference,
                'price_sensitivity': self.price_sensitivity
            },
            'bid_count': len(self.bid_history),
            'wins': sum(1 for bid in self.bid_history if bid['won'])
        }


class AIBuyerManager:
    """AIバイヤー管理システム"""
    
    def __init__(self):
        """AIバイヤーマネージャー初期化"""
        self.buyers = []
        self.initialize_buyers()
    
    def initialize_buyers(self, count: int = 10) -> None:
        """AIバイヤーを初期化"""
        self.buyers = []
        
        for i in range(count):
            # 各AIは2-4個のジャンルに興味を持つ
            interested_genres = random.sample(
                ItemSystem.GENRES, 
                random.randint(2, 4)
            )
            
            # パラメータをランダム生成
            condition_preference = random.uniform(0.5, 1.0)
            rarity_preference = random.uniform(0.8, 1.5)
            price_sensitivity = random.uniform(0.5, 1.2)
            
            buyer = AIBuyer(
                buyer_id=i,
                interested_genres=interested_genres,
                condition_preference=condition_preference,
                rarity_preference=rarity_preference,
                price_sensitivity=price_sensitivity
            )
            
            self.buyers.append(buyer)
    
    def get_interested_buyers(self, item: Dict[str, Any], 
                            current_price: float) -> List[AIBuyer]:
        """商品に興味を持つバイヤーを取得"""
        interested = []
        for buyer in self.buyers:
            if buyer.should_bid(item, current_price):
                interested.append(buyer)
        return interested
    
    def simulate_bidding_round(self, item: Dict[str, Any], 
                              current_price: float) -> Tuple[bool, float, AIBuyer]:
        """入札ラウンドをシミュレート"""
        interested_buyers = self.get_interested_buyers(item, current_price)
        
        if not interested_buyers:
            return False, current_price, None
        
        # 最も高い入札額を計算
        best_buyer = None
        highest_bid = current_price
        
        for buyer in interested_buyers:
            bid_amount = buyer.calculate_bid_amount(item, current_price)
            if bid_amount > highest_bid:
                highest_bid = bid_amount
                best_buyer = buyer
        
        if best_buyer:
            return True, highest_bid, best_buyer
        
        return False, current_price, None
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """全バイヤーのプロフィール情報を取得"""
        return [buyer.get_profile() for buyer in self.buyers]
    
    def get_buyer_by_id(self, buyer_id: int) -> AIBuyer:
        """IDでバイヤーを取得"""
        for buyer in self.buyers:
            if buyer.id == buyer_id:
                return buyer
        return None
    
    def reset_all_histories(self) -> None:
        """全バイヤーの入札履歴をリセット"""
        for buyer in self.buyers:
            buyer.bid_history = []
    
    def get_statistics(self) -> Dict[str, Any]:
        """AIバイヤーシステムの統計情報を取得"""
        total_bids = sum(len(buyer.bid_history) for buyer in self.buyers)
        total_wins = sum(
            sum(1 for bid in buyer.bid_history if bid['won']) 
            for buyer in self.buyers
        )
        
        # ジャンル別興味統計
        genre_interest = {}
        for genre in ItemSystem.GENRES:
            interested_count = sum(
                1 for buyer in self.buyers 
                if genre in buyer.interested_genres
            )
            genre_interest[genre] = interested_count
        
        return {
            'total_buyers': len(self.buyers),
            'total_bids': total_bids,
            'total_wins': total_wins,
            'win_rate': round(total_wins / max(total_bids, 1) * 100, 2),
            'genre_interest': genre_interest,
            'average_genres_per_buyer': round(
                sum(len(buyer.interested_genres) for buyer in self.buyers) / len(self.buyers), 1
            )
        }


# シングルトンインスタンス
ai_buyer_manager = AIBuyerManager()