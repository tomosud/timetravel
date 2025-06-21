# フェーズ2: 戦略性・攻略性導入のための設定

# 目標倍率設定
TARGET_MULTIPLIER_MIN = 1.0    # 最小目標倍率（100% = 損益なし）
TARGET_MULTIPLIER_MAX = 10.0   # 最大目標倍率（1000% = 900%利益）

# 固定費設定
FIXED_COST_RATE = 0.05         # UFO代金率（資産の5%）

# 在庫関連設定
INVENTORY_SELL_RATE = 1.0      # 在庫売却時の価格率（100%）

# ゲームオーバー設定
ENABLE_GAME_OVER = True        # ゲームオーバー機能の有効/無効

# デバッグ設定
SHOW_TARGET_MULTIPLIER = True  # 目標倍率のUI表示
SHOW_ASSETS_INFO = True        # 資産情報のUI表示
SHOW_FIXED_COST_INFO = True    # 固定費情報のUI表示