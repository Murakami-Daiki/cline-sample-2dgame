#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ゲーム状態管理モジュール
"""

class GameState:
    """ゲームの状態を管理するクラス"""
    
    # ゲーム状態の定数
    START = 0      # スタート画面
    PLAYING = 1    # ステージ画面（プレイ中）
    RETRY = 2      # リトライ画面
    RESULT = 3     # リザルト画面
    
    def __init__(self):
        """初期化"""
        self.state = self.START  # 初期状態はスタート画面
        self.lives = 2           # 残機の初期値は2
        self.is_cleared = False  # ゲームクリアフラグ
        self.retry_selection = 0  # リトライ画面での選択（0: Yes, 1: No）
    
    def start_game(self):
        """ゲームを開始する"""
        self.state = self.PLAYING
        self.lives = 2
        self.is_cleared = False
    
    def lose_life(self):
        """残機を減らす"""
        self.lives -= 1
        if self.lives < 0:
            # 残機が負の値になったらゲームオーバー
            self.state = self.RESULT
        else:
            # まだ残機があればリトライ画面へ
            self.state = self.RETRY
    
    def clear_game(self):
        """ゲームクリア"""
        self.is_cleared = True
        self.state = self.RESULT
    
    def select_retry(self, selection):
        """リトライ画面での選択"""
        self.retry_selection = selection
    
    def confirm_retry(self):
        """リトライ画面での選択を確定"""
        if self.retry_selection == 0:  # "Yes"を選択
            self.state = self.PLAYING
        else:  # "No"を選択
            self.lives = -1  # 残機を-1に設定
            self.state = self.RESULT
    
    def restart_game(self):
        """ゲームを再スタート"""
        self.state = self.START
