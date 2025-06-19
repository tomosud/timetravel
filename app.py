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
    """メインページ"""
    result = game_api.get_game_state()
    return render_template('index.html', game_state=result['data'])

@app.route('/buy')
def buy_mode():
    """買うモードページ"""
    result = game_api.get_game_state()
    return render_template('buy.html', game_state=result['data'])

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
    """商品購入API"""
    try:
        data = request.get_json()
        years = int(data['years'])
        distance = int(data['distance'])
        ufo_size = float(data['ufo_size'])
        
        result = travel_api.execute_travel(years, distance, ufo_size)
        
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

@app.route('/api/reset')
def api_reset():
    """ゲームリセット"""
    try:
        result = game_api.reset_game()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)