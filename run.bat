@echo off
chcp 65001 >nul
echo タイムトラベル仕入れ・オークションゲームを起動しています...

REM 仮想環境の存在チェック
if not exist "venv\" (
    echo 仮想環境が見つかりません。作成します...
    python -m venv venv
    if errorlevel 1 (
        echo 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
)

REM 仮想環境をアクティベート
echo 仮想環境をアクティベートしています...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo 仮想環境のアクティベートに失敗しました。
    pause
    exit /b 1
)

REM 必要なパッケージをインストール
echo 必要なパッケージをチェック・インストールしています...
pip install -r requirements.txt
if errorlevel 1 (
    echo パッケージのインストールに失敗しました。
    pause
    exit /b 1
)

REM ブラウザを起動（バックグラウンド）
echo ブラウザを起動します...
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5000"

REM ゲームサーバーを起動
echo ゲームサーバーを起動します...
echo ============================================
echo   ゲームURL: http://127.0.0.1:5000
echo   終了するには: Ctrl+C を押してください
echo ============================================
python entry.py

REM サーバー終了後の処理
echo.
echo ゲームサーバーが終了しました。
pause