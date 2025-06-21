#!/usr/bin/env python3
"""
タイムトラベル仕入れゲーム - CLI版実行スクリプト
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.game_cli import main

if __name__ == "__main__":
    main()