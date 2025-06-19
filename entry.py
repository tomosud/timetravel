#!/usr/bin/env python3
"""
タイムトラベル仕入れ・オークションゲーム エントリーポイント
"""

import sys
import os

# 現在のディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("タイムトラベル仕入れ・オークションゲームを開始します...")
    print("ブラウザで http://127.0.0.1:5000 にアクセスしてください")
    app.run(debug=True, host='127.0.0.1', port=5000)