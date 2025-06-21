"""
ゲーム設定値の統合管理
全てのゲームパラメータを一元管理するための設定ファイル
"""

# ===== 基本ゲーム設定 =====
class GameConfig:
    # 初期設定
    INITIAL_MONEY = 1000  # 初期資金（円）
    
    # タイムトラベル設定
    YEARS_MIN = 1
    YEARS_MAX = 1000000  # 100万年
    DEFAULT_YEARS = 10
    
    DISTANCE_MIN = 0  
    DISTANCE_MAX = 1000000  # 100万km
    DEFAULT_DISTANCE = 100
    
    # ターンシステム設定
    MINOR_TURNS_PER_MAJOR = 8  # 大ターンあたりの子ターン数
    
    # 価格倍率設定
    TARGET_MULTIPLIER_MIN = 1.0
    TARGET_MULTIPLIER_MAX = 10.0
    
    # 固定費設定
    FIXED_COST_RATE = 0.05  # 5%（UFO維持費）
    
    # オークション設定
    AUCTION_FEE_RATE = 0.1  # 手数料10%
    AUCTION_DURATION_ROUNDS = 10
    AUCTION_BID_THRESHOLD = 0.3
    MAX_AUCTION_ITEMS = 8  # 同時出品最大数
    
    # AIバイヤー設定
    AI_BID_INCREASE_MIN = 0.05  # 5%
    AI_BID_INCREASE_MAX = 0.15  # 15%
    
    # タイムトラベル失敗率（現在無効化）
    TRAVEL_FAILURE_RATE = 0.1  # 10%
    
    # 価格曲線生成設定
    RANDOM_MIN = 0.5
    RANDOM_MAX = 1.8
    FIRST_TURN_MIN = 1.0
    TREND_STRENGTH = 0.1
    
    # UI設定（自動投資オプション）
    AUTO_INVEST_OPTIONS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # %

# 設定値の妥当性チェック
def validate_config():
    """設定値の妥当性をチェック"""
    assert GameConfig.YEARS_MIN > 0, "最小年数は正の値である必要があります"
    assert GameConfig.YEARS_MAX > GameConfig.YEARS_MIN, "最大年数は最小年数より大きい必要があります"
    assert GameConfig.DISTANCE_MIN >= 0, "最小距離は非負の値である必要があります"
    assert GameConfig.DISTANCE_MAX > GameConfig.DISTANCE_MIN, "最大距離は最小距離より大きい必要があります"
    assert 0 < GameConfig.TARGET_MULTIPLIER_MIN <= GameConfig.TARGET_MULTIPLIER_MAX, "価格倍率の範囲が無効です"
    assert 0 <= GameConfig.FIXED_COST_RATE <= 1, "固定費率は0-1の範囲である必要があります"
    assert 0 <= GameConfig.AUCTION_FEE_RATE <= 1, "オークション手数料は0-1の範囲である必要があります"
    assert GameConfig.MAX_AUCTION_ITEMS > 0, "最大出品数は正の値である必要があります"

# 初期化時に妥当性チェック実行
validate_config()