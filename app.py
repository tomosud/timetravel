from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import random
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'timetravel_game_secret_key'

# ゲーム状態を保持するグローバル変数（本来はセッションやDBで管理）
game_state = {
    'money': 1000,
    'inventory': [],
    'auction_items': [],
    'game_over': False
}

def check_game_over():
    """ゲームオーバー判定：所持金0円かつ在庫なし"""
    return game_state['money'] <= 0 and len(game_state['inventory']) == 0

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

def calculate_rarity_multiplier(years, distance):
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

def get_rarity_name(multiplier):
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

# AIバイヤーの定義
AI_BUYERS = []

def initialize_ai_buyers():
    """AIバイヤーを初期化"""
    global AI_BUYERS
    AI_BUYERS = []
    
    for i in range(10):
        # 各AIは2-4個のジャンルに興味を持つ
        interested_genres = random.sample(GENRES, random.randint(2, 4))
        
        ai_buyer = {
            'id': i,
            'interested_genres': interested_genres,
            'condition_preference': random.uniform(0.5, 1.0),  # 状態への関心度
            'rarity_preference': random.uniform(0.8, 1.5),     # 希少性への関心度
            'price_sensitivity': random.uniform(0.5, 1.2)      # 価格感度
        }
        AI_BUYERS.append(ai_buyer)

def calculate_travel_cost(years, distance, ufo_size):
    """タイムトラベルコストを計算"""
    return (years * distance) * ufo_size

def generate_item(years, distance):
    """年代と距離に基づいて商品を生成"""
    genre = random.choice(GENRES)
    
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
    rarity_multiplier = calculate_rarity_multiplier(years, distance)
    rarity_name = get_rarity_name(rarity_multiplier)
    
    # 基本価値を計算
    base_value = random.uniform(100, 1000)
    base_value *= CONDITIONS[condition]['multiplier']
    base_value *= rarity_multiplier
    
    return {
        'id': int(time.time() * 1000000 + random.randint(0, 999999)),
        'genre': genre,
        'condition': condition,
        'rarity': rarity_name,
        'rarity_multiplier': rarity_multiplier,
        'base_value': base_value,
        'years': years,
        'distance': distance
    }

def calculate_ai_interest(ai_buyer, item, price):
    """AIバイヤーの商品への興味度を計算"""
    # ジャンルマッチング
    if item['genre'] not in ai_buyer['interested_genres']:
        return 0
    
    # 基本興味度
    interest = 1.0
    
    # 状態への評価
    condition_score = CONDITIONS[item['condition']]['multiplier']
    interest *= (condition_score * ai_buyer['condition_preference'])
    
    # 希少性への評価（新しい動的レア度システム）
    rarity_score = item.get('rarity_multiplier', 1.0)
    interest *= (rarity_score * ai_buyer['rarity_preference'])
    
    # 価格評価（高すぎると興味が下がる）
    if price > 0:
        value_ratio = item['base_value'] / price
        price_factor = min(2.0, value_ratio * ai_buyer['price_sensitivity'])
        interest *= price_factor
    
    return interest

@app.route('/')
def index():
    """メインページ"""
    # ゲームオーバー状態を更新
    game_state['game_over'] = check_game_over()
    return render_template('index.html', game_state=game_state)

@app.route('/buy')
def buy_mode():
    """買うモードページ"""
    return render_template('buy.html', game_state=game_state)

@app.route('/sell')
def sell_mode():
    """売るモードページ"""
    return render_template('sell.html', 
                         game_state=game_state, 
                         inventory=game_state['inventory'],
                         auction_items=game_state['auction_items'])

@app.route('/api/buy', methods=['POST'])
def api_buy():
    """商品購入API"""
    try:
        data = request.get_json()
        years = int(data['years'])
        distance = int(data['distance'])
        ufo_size = float(data['ufo_size'])
        
        # コスト計算
        cost = calculate_travel_cost(years, distance, ufo_size)
        
        if cost > game_state['money']:
            return jsonify({'error': 'お金が足りません'}), 400
        
        # UFOサイズに応じて商品数を決定（1.0で1個、2.0で2個など）
        item_count = max(1, int(ufo_size))
        
        # 状態更新（お金を先に支払う）
        game_state['money'] -= cost
        
        # 10%の確率で買い物失敗
        import random
        if random.random() < 0.1:  # 10%の失敗確率
            # 失敗時：お金は支払ったが商品は取得できない
            game_state['game_over'] = check_game_over()
            
            return jsonify({
                'success': True,
                'failed': True,
                'cost': cost,
                'items': [],
                'new_money': game_state['money'],
                'game_over': game_state['game_over']
            })
        
        # 成功時：商品生成
        new_items = []
        for _ in range(item_count):
            item = generate_item(years, distance)
            new_items.append(item)
        
        game_state['inventory'].extend(new_items)
        game_state['game_over'] = check_game_over()
        
        return jsonify({
            'success': True,
            'failed': False,
            'cost': cost,
            'items': new_items,
            'new_money': game_state['money'],
            'game_over': game_state['game_over']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/auction/setup', methods=['POST'])
def api_auction_setup():
    """オークション出品設定API"""
    try:
        data = request.get_json()
        
        # 既存の出品をクリア
        game_state['auction_items'] = []
        
        # 新しい出品を設定
        for item_data in data['items']:
            if item_data['item_id'] and item_data['start_price']:
                # インベントリから商品を探す
                item = None
                for inv_item in game_state['inventory']:
                    if inv_item['id'] == item_data['item_id']:
                        item = inv_item
                        break
                
                if item:
                    auction_item = {
                        'item': item,
                        'start_price': float(item_data['start_price']),
                        'current_price': float(item_data['start_price']),
                        'bid_count': 0,
                        'sold': False
                    }
                    game_state['auction_items'].append(auction_item)
                    game_state['inventory'].remove(item)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/auction/start', methods=['POST'])
def api_auction_start():
    """1分間オークション開始API"""
    try:
        if not AI_BUYERS:
            initialize_ai_buyers()
        
        results = []
        
        for auction_item in game_state['auction_items']:
            item = auction_item['item']
            current_price = auction_item['start_price']
            bid_count = 0
            
            # 1分間のシミュレーション（10回の入札チャンス）
            for _ in range(10):
                best_bidder = None
                best_interest = 0
                
                # 各AIの興味度を計算
                for ai in AI_BUYERS:
                    interest = calculate_ai_interest(ai, item, current_price)
                    if interest > best_interest and interest > 0.8:  # 閾値
                        best_interest = interest
                        best_bidder = ai
                
                # 入札があった場合
                if best_bidder:
                    # 価格上昇（興味度に応じて）
                    price_increase = current_price * random.uniform(0.05, 0.15) * best_interest
                    current_price += price_increase
                    bid_count += 1
            
            # 結果を更新
            auction_item['current_price'] = current_price
            auction_item['bid_count'] = bid_count
            
            # 売却判定（入札があった場合は売却）
            if bid_count > 0:
                auction_item['sold'] = True
                # 手数料10%を引いて収益計算
                profit = current_price * 0.9
                game_state['money'] += profit
                
                results.append({
                    'item_id': item['id'],
                    'sold': True,
                    'final_price': current_price,
                    'profit': profit,
                    'bid_count': bid_count
                })
            else:
                results.append({
                    'item_id': item['id'],
                    'sold': False,
                    'final_price': current_price,
                    'bid_count': bid_count
                })
        
        # 売却済み商品をオークションリストから削除
        game_state['auction_items'] = [
            auction_item for auction_item in game_state['auction_items'] 
            if not auction_item['sold']
        ]
        
        return jsonify({
            'success': True,
            'results': results,
            'new_money': game_state['money']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/auction/cancel', methods=['POST'])
def api_auction_cancel():
    """出品取り消しAPI"""
    try:
        data = request.get_json()
        item_id = data['item_id']
        
        # オークションアイテムを探して削除
        for auction_item in game_state['auction_items']:
            if auction_item['item']['id'] == item_id:
                # インベントリに戻す
                game_state['inventory'].append(auction_item['item'])
                game_state['auction_items'].remove(auction_item)
                break
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/reset')
def api_reset():
    """ゲームリセット"""
    global game_state
    game_state = {
        'money': 1000,
        'inventory': [],
        'auction_items': [],
        'game_over': False
    }
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)