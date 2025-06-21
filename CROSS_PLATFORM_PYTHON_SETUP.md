# WSL/Windows両環境対応Python開発環境セットアップ

**更新条件**: 開発環境セットアップ手順・依存関係・プラットフォーム対応の変更時

このドキュメントは、Claude Code使用時にWSL環境とWindows環境の両方でPythonプロジェクトを実行できる環境を構築するための実行手順書です。


## Claude Codeへの指示

まだ後述の仮想環境や関連ファイルが用意されていなければ、このファイルを読んで構築/作成してください。

## 実行手順

### 1. WSL環境での仮想環境作成

Claude CodeがWSL環境で以下を実行：

```bash
python3 -m venv venv
```

### 2. requirements.txt作成

以下の内容でrequirements.txtを作成（**重要**: コメントは英語のみ）：

```txt
# Python dependencies - Add your packages here
# Example packages:
# flask==3.0.0
# requests==2.31.0
# numpy==1.24.3
```

エンコーディング問題回避のため、日本語コメントは使用禁止。

### 3. .gitignore設定

以下の内容で.gitignoreを作成または追記：

```gitignore
# Virtual Environments
venv/
venv_win/
.venv/
.env/
ENV/
env.bak/
venv.bak/
```

### 4. Windows用自動セットアップバッチファイル作成

`run_windows.bat`として以下の内容で作成：

```batch
@echo off
echo Setting up Windows Python environment...

REM Check if venv_win exists, if not create it
if not exist "venv_win" (
    echo Creating virtual environment venv_win...
    python -m venv venv_win
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_win\Scripts\activate.bat

REM Install/update requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run main application (modify entry point as needed)
echo Starting application...
python main.py

REM Keep window open to see output
pause
```

### 5. セットアップ検証用テストファイル作成（オプション）

`main.py`として基本的なテストファイルを作成：

```python
import sys
import platform
from datetime import datetime

def main():
    print("="*50)
    print("Python Environment Test")
    print("="*50)
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()}")
    print(f"Architecture: {platform.architecture()[0]}")
    
    if platform.system() == 'Windows':
        print("Environment: Windows (venv_win)")
    else:
        print("Environment: WSL/Linux (venv)")
    
    print(f"Execution Time: {datetime.now()}")
    print("="*50)
    print("Setup completed successfully!")

if __name__ == "__main__":
    main()
```

## セットアップ完了の確認

### WSL環境での確認
```bash
source venv/bin/activate
python main.py
```

### Windows環境での確認
```cmd
run_windows.bat
```

両環境で実行成功すれば、セットアップ完了です。

## 重要な注意事項

### エンコーディング問題の回避
- **requirements.txt**: 日本語コメント禁止、英語のみ使用
- **バッチファイル**: 英語メッセージ推奨
- **Pythonファイル**: UTF-8エンコーディング使用

### トラブルシューティング

**Windows環境でのエラー例**:
```
UnicodeDecodeError: 'cp932' codec can't decode
```
**解決方法**: requirements.txtから日本語文字を全て削除

**バッチファイル文字化け**:
**解決方法**: バッチファイル内のechoメッセージを英語に変更

## セットアップ後の開発フロー

1. **WSL環境での開発**: Claude Codeで直接編集・実行
2. **Windows環境でのテスト**: `run_windows.bat`でワンクリック実行
3. **依存関係追加**: `requirements.txt`に英語コメントで追記
4. **両環境で検証**: それぞれの環境でテスト実行

## このセットアップの完了基準

以下がすべて達成されればセットアップ完了：

- [ ] WSL環境で`venv/`仮想環境が作成される
- [ ] `requirements.txt`が英語コメントで作成される  
- [ ] `.gitignore`に仮想環境が除外設定される
- [ ] `run_windows.bat`が作成される
- [ ] `main.py`テストファイルが作成される
- [ ] WSL環境で`source venv/bin/activate && python main.py`が実行成功
- [ ] Windows環境で`run_windows.bat`が実行成功（Claude Code実行後に手動確認）

**セットアップはここまでです。この後の具体的な開発内容は別途指示してください。**