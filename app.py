from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.game_api import game_api
from api.travel_api import travel_api
from api.auction_api import auction_api

app = Flask(__name__)
app.secret_key = 'timetravel_game_secret_key'

@app.route('/')
def index():
    """メインページ - 買うモードにリダイレクト"""
    return redirect('/buy')

@app.route('/buy')
def buy_mode():
    """買うモードページ（フェーズ2: UFOサイズ廃止）"""
    from core.travel_config import YEARS_MIN, YEARS_MAX, DISTANCE_MIN, DISTANCE_MAX, DEFAULT_YEARS, DEFAULT_DISTANCE
    from core.turn_system import turn_system
    from core.asset_manager import AssetManager
    
    result = game_api.get_game_state()
    game_state = result['data']
    
    # フェーズ2: 目標倍率と資産情報を追加
    target_multiplier = turn_system.get_target_multiplier()
    asset_info = AssetManager.get_asset_info(game_state['money'], game_state['inventory'])
    
    return render_template('buy.html', 
                         game_state=game_state,
                         target_multiplier=target_multiplier,
                         asset_info=asset_info,
                         travel_limits={
                             'years_min': YEARS_MIN,
                             'years_max': YEARS_MAX,
                             'distance_min': DISTANCE_MIN,
                             'distance_max': DISTANCE_MAX,
                             'default_years': DEFAULT_YEARS,
                             'default_distance': DEFAULT_DISTANCE
                         })

@app.route('/sell')
def sell_mode():
    """売るモードページ"""
    game_result = game_api.get_game_state()
    inventory_result = game_api.get_inventory()
    auction_result = game_api.get_auction_items()
    
    return render_template('sell.html', 
                         game_state=game_result['data'],
                         inventory=inventory_result['data']['inventory'],
                         auction_items=auction_result['data']['auction_items'])

@app.route('/api/buy', methods=['POST'])
def api_buy():
    """商品購入API（フェーズ2: UFOサイズ廃止・固定費統合）"""
    try:
        data = request.get_json()
        years = int(data['years'])
        distance = int(data['distance'])
        
        result = travel_api.execute_travel(years, distance)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/auction/setup', methods=['POST'])
def api_auction_setup():
    """オークション出品設定API"""
    try:
        data = request.get_json()
        result = auction_api.setup_auction(data['items'])
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/auction/start', methods=['POST'])
def api_auction_start():
    """1分間オークション開始API"""
    try:
        result = auction_api.start_auction()
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/auction/cancel', methods=['POST'])
def api_auction_cancel():
    """出品取り消しAPI"""
    try:
        data = request.get_json()
        item_id = data['item_id']
        
        result = auction_api.cancel_auction_item(item_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/debug')
def debug_mode():
    """デバッグページ"""
    game_result = game_api.get_game_state()
    inventory_result = game_api.get_inventory()
    
    return render_template('debug.html',
                         game_state=game_result['data'],
                         inventory=inventory_result['data']['inventory'])

@app.route('/api/reset')
def api_reset():
    """ゲームリセット"""
    try:
        result = game_api.reset_game()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/auto_invest', methods=['POST'])
def api_auto_invest():
    """自動投資API（フェーズ2: 指定割合でUFO代金を引いた金額から投資）"""
    try:
        from core.game_engine import game_engine
        from core.asset_manager import AssetManager
        from core.turn_system import turn_system
        import random
        
        data = request.get_json()
        ratio = float(data.get('ratio', 1.0))  # 投資割合（0.1〜1.0）
        
        if ratio < 0.1 or ratio > 1.0:
            return jsonify({
                'success': False,
                'error': f'投資割合は0.1〜1.0の範囲で指定してください。指定値: {ratio}'
            })
        
        # 現在の状態取得
        current_state = game_engine.get_state()
        current_money = current_state['money']
        current_inventory = current_state['inventory']
        
        # 資産・固定費計算
        assets = AssetManager.calculate_assets(current_money, current_inventory)
        fixed_cost = AssetManager.calculate_fixed_cost(assets)
        
        # 投資可能額 = 現金 - 固定費
        available_for_investment = current_money - fixed_cost
        
        if available_for_investment <= 0:
            return jsonify({
                'success': False,
                'error': f'投資可能額がありません。現金: {current_money}円, 固定費: {fixed_cost:.2f}円'
            })
        
        # 指定割合で投資額を計算
        target_investment = available_for_investment * ratio
        
        if target_investment < 1:
            return jsonify({
                'success': False,
                'error': f'投資額が1円未満です。投資可能額: {available_for_investment:.2f}円 × {ratio*100:.0f}% = {target_investment:.2f}円'
            })
        
        # 年数と距離を適当に割り振り（平方根で分配）
        sqrt_investment = target_investment ** 0.5
        base_years = int(sqrt_investment * random.uniform(0.5, 1.5))
        base_distance = int(target_investment / max(base_years, 1))
        
        # 制限内に収める
        years = max(1, min(base_years, 1000000))
        distance = max(1, min(base_distance, 1000000))
        
        # 実際のコストを計算
        actual_investment = years * distance
        total_cost = actual_investment + fixed_cost
        
        print(f"[AutoInvest] {ratio*100:.0f}%投資: 投資可能額{available_for_investment:.2f}円 × {ratio} = 目標{target_investment:.2f}円 → 年数{years}年 × 距離{distance}km = 実際{actual_investment}円")
        
        # タイムトラベル実行
        result = travel_api.execute_travel(years, distance)
        
        if result['success']:
            result['auto_invest_info'] = {
                'ratio': ratio,
                'ratio_percent': ratio * 100,
                'available_for_investment': available_for_investment,
                'target_investment': target_investment,
                'calculated_years': years,
                'calculated_distance': distance,
                'actual_investment': actual_investment,
                'fixed_cost': fixed_cost,
                'total_cost': total_cost
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)