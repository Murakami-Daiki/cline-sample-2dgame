#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ゲーム実行スクリプト
"""

import sys
import os

# ゲームディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ゲームを実行
from game.main import Game

if __name__ == "__main__":
    print("忍者の如く、ゲームを起動するでござる！")
    print("操作方法でござる：")
    print("・左右キー：移動")
    print("・Shiftキー + 左右キー：ダッシュ移動")
    print("・スペースキー：ジャンプ")
    print("・Aキー：ゲーム開始")
    print("・Enterキー：決定")
    print("敵は上から踏むと倒せるでござる！穴に落ちないよう気をつけるでござる！")
    print("穴はダッシュジャンプで飛び越えられるでござるぞ！")
    
    game = Game()
    game.run()
