"""
タイムトラベル仕入れゲーム - オークションシステム
オークションの実行とログ出力を担当
"""

import time
from typing import Dict, List, Any, Tuple
from core.ai_buyers import ai_buyer_manager
from core.item_system import ItemSystem


class AuctionSystem:
    """オークションシステム管理"""
    
    def __init__(self):
        """オークションシステム初期化"""
        self.auction_fee_rate = 0.1  # 手数料10%
        self.auction_duration_rounds = 10  # 1分間を10ラウンドでシミュレート
        self.bid_threshold = 0.8  # 入札の興味度閾値
    
    def create_auction_item(self, item: Dict[str, Any], start_price: float) -> Dict[str, Any]:
        """オークション出品アイテムを作成"""
        return {
            'item': item,
            'start_price': start_price,
            'current_price': start_price,
            'bid_count': 0,
            'sold': False,
            'winner_id': None,
            'bid_history': [],
            'created_at': time.time()
        }
    
    def validate_auction_setup(self, auction_items: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """オークション設定の妥当性をチェック"""
        if len(auction_items) == 0:
            return False, "出品する商品がありません"
        
        if len(auction_items) > 8:
            return False, "同時出品は最大8個までです"
        
        for auction_item in auction_items:
            if auction_item['start_price'] <= 0:
                return False, "開始価格は0円より大きくしてください"
        
        return True, ""
    
    def simulate_auction(self, auction_items: List[Dict[str, Any]], 
                        verbose: bool = True) -> List[Dict[str, Any]]:
        """オークションをシミュレート（詳細ログ付き）"""
        if verbose:
            print(f"\n{'='*50}")
            print(f"オークション開始 - {len(auction_items)}個の商品")
            print(f"{'='*50}")
        
        results = []
        
        for auction_item in auction_items:
            if verbose:
                print(f"\n--- 商品 ID:{auction_item['item']['id']} のオークション ---")
                print(f"ジャンル: {auction_item['item']['genre']}")
                print(f"状態: {auction_item['item']['condition']} ({auction_item['item'].get('condition_name', '')})")
                print(f"レア度: {auction_item['item']['rarity']} (倍率: {auction_item['item']['rarity_multiplier']})")
                print(f"基本価値: {auction_item['item']['base_value']}円")
                print(f"開始価格: {auction_item['start_price']}円")
            
            # 1分間のオークションをシミュレート
            result = self._simulate_single_auction(auction_item, verbose)
            results.append(result)
            
            if verbose:
                if result['sold']:
                    profit = result['final_price'] * (1 - self.auction_fee_rate)
                    print(f"🎉 売却成功! 最終価格: {result['final_price']}円")
                    print(f"💰 手取り: {profit:.2f}円 (手数料{self.auction_fee_rate*100}%差引後)")
                    print(f"🏆 落札者: AIバイヤー #{result['winner_id']}")
                else:
                    print(f"❌ 売却失敗 (入札: {result['bid_count']}回)")
        
        if verbose:
            print(f"\n{'='*50}")
            print("オークション終了")
            self._print_auction_summary(results)
            print(f"{'='*50}")
        
        return results
    
    def _simulate_single_auction(self, auction_item: Dict[str, Any], 
                                verbose: bool = True) -> Dict[str, Any]:
        """単一商品のオークションをシミュレート"""
        item = auction_item['item']
        current_price = auction_item['start_price']
        bid_count = 0
        winner_buyer = None
        bid_history = []
        
        if verbose:
            print(f"入札開始...")
        
        # 10ラウンドの入札シミュレート
        for round_num in range(1, self.auction_duration_rounds + 1):
            had_bid, new_price, winning_buyer = ai_buyer_manager.simulate_bidding_round(
                item, current_price
            )
            
            if had_bid and new_price > current_price:
                bid_count += 1
                previous_price = current_price
                current_price = new_price
                winner_buyer = winning_buyer
                
                # 入札履歴を記録
                bid_record = {
                    'round': round_num,
                    'bidder_id': winning_buyer.id,
                    'bid_amount': new_price,
                    'previous_price': previous_price
                }
                bid_history.append(bid_record)
                
                if verbose:
                    interest = winning_buyer.calculate_interest(item, previous_price)
                    print(f"  R{round_num}: AIバイヤー#{winning_buyer.id} が {new_price:.2f}円で入札 "
                          f"(+{new_price - previous_price:.2f}円, 興味度: {interest:.2f})")
            elif verbose and round_num <= 3:
                print(f"  R{round_num}: 入札なし")
        
        # オークション結果を決定
        sold = bid_count > 0
        final_price = current_price
        
        # 結果を構築
        result = {
            'item_id': item['id'],
            'sold': sold,
            'final_price': final_price,
            'start_price': auction_item['start_price'],
            'bid_count': bid_count,
            'winner_id': winner_buyer.id if winner_buyer else None,
            'profit': round(final_price * (1 - self.auction_fee_rate), 2) if sold else 0,
            'bid_history': bid_history
        }
        
        # 勝者の入札履歴に記録
        if winner_buyer:
            winner_buyer.record_bid(item['id'], final_price, True)
        
        if verbose:
            if not sold:
                print(f"❌ 売却失敗 (入札: {bid_count}回)")
                print(f"💡 商品はオークションに残り続けます")
        
        return result
    
    def _print_auction_summary(self, results: List[Dict[str, Any]]) -> None:
        """オークション結果のサマリーを出力"""
        total_items = len(results)
        sold_items = sum(1 for r in results if r['sold'])
        total_revenue = sum(r['final_price'] for r in results if r['sold'])
        total_profit = sum(r['profit'] for r in results if r['sold'])
        total_bids = sum(r['bid_count'] for r in results)
        
        print(f"📊 オークション結果サマリー:")
        print(f"   出品数: {total_items}個")
        print(f"   売却数: {sold_items}個 ({sold_items/total_items*100:.1f}%)")
        print(f"   総売上: {total_revenue:.2f}円")
        print(f"   手取り: {total_profit:.2f}円")
        print(f"   総入札: {total_bids}回")
        
        if sold_items > 0:
            print(f"   平均売値: {total_revenue/sold_items:.2f}円")
        
        # 最高額と最低額
        if results:
            sold_results = [r for r in results if r['sold']]
            if sold_results:
                max_price = max(r['final_price'] for r in sold_results)
                min_price = min(r['final_price'] for r in sold_results)
                print(f"   最高売値: {max_price:.2f}円")
                print(f"   最低売値: {min_price:.2f}円")
    
    def calculate_fee(self, sale_price: float) -> float:
        """手数料を計算"""
        return round(sale_price * self.auction_fee_rate, 2)
    
    def calculate_profit(self, sale_price: float) -> float:
        """手数料差引後の利益を計算"""
        return round(sale_price * (1 - self.auction_fee_rate), 2)
    
    def get_auction_statistics(self) -> Dict[str, Any]:
        """オークション統計情報を取得"""
        return {
            'fee_rate': self.auction_fee_rate,
            'auction_duration_rounds': self.auction_duration_rounds,
            'bid_threshold': self.bid_threshold,
            'ai_buyer_stats': ai_buyer_manager.get_statistics()
        }
    
    def update_settings(self, fee_rate: float = None, duration_rounds: int = None, 
                       bid_threshold: float = None) -> None:
        """オークション設定を更新"""
        if fee_rate is not None:
            self.auction_fee_rate = max(0.0, min(1.0, fee_rate))
        
        if duration_rounds is not None:
            self.auction_duration_rounds = max(1, min(20, duration_rounds))
        
        if bid_threshold is not None:
            self.bid_threshold = max(0.1, min(2.0, bid_threshold))
    
    def preview_auction(self, auction_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """オークションの事前予測を実行"""
        preview_results = []
        
        for auction_item in auction_items:
            item = auction_item['item']
            start_price = auction_item['start_price']
            
            # 興味を持つバイヤー数を計算
            interested_buyers = ai_buyer_manager.get_interested_buyers(item, start_price)
            
            # 予想最終価格を計算（簡易）
            if interested_buyers:
                max_interest = max(
                    buyer.calculate_interest(item, start_price) 
                    for buyer in interested_buyers
                )
                estimated_final = start_price * (1 + max_interest * 0.2)
            else:
                estimated_final = start_price
            
            preview_results.append({
                'item_id': item['id'],
                'start_price': start_price,
                'interested_buyers': len(interested_buyers),
                'estimated_final_price': round(estimated_final, 2),
                'estimated_profit': round(estimated_final * (1 - self.auction_fee_rate), 2),
                'confidence': 'High' if len(interested_buyers) >= 3 else 
                            'Medium' if len(interested_buyers) >= 1 else 'Low'
            })
        
        return {
            'previews': preview_results,
            'total_estimated_revenue': sum(p['estimated_final_price'] for p in preview_results),
            'total_estimated_profit': sum(p['estimated_profit'] for p in preview_results)
        }


# シングルトンインスタンス
auction_system = AuctionSystem()