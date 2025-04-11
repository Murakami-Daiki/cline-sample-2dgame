#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UIモジュール
"""

import pygame

class UI:
    """UIクラス"""
    
    def __init__(self, width, height):
        """初期化
        
        Args:
            width (int): 画面の幅
            height (int): 画面の高さ
        """
        self.width = width
        self.height = height
        
        # フォントの初期化
        pygame.font.init()
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
        
    def draw_start_screen(self, screen):
        """スタート画面を描画
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # 背景を水色で塗りつぶす
        screen.fill((135, 206, 235))  # 空色
        
        # タイトル
        title_text = self.font_large.render("Super Cline Brothers", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # スタート指示
        start_text = self.font_medium.render("Press A to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(start_text, start_rect)
        
    def draw_retry_screen(self, screen, selection):
        """リトライ画面を描画
        
        Args:
            screen (pygame.Surface): 描画対象の画面
            selection (int): 選択中の項目（0: Yes, 1: No）
        """
        # 半透明の黒背景
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # メッセージ
        message_text = self.font_large.render("Continue?", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(message_text, message_rect)
        
        # Yes選択肢
        yes_color = (255, 255, 0) if selection == 0 else (255, 255, 255)  # 選択中は黄色
        yes_text = self.font_medium.render("Yes", True, yes_color)
        yes_rect = yes_text.get_rect(center=(self.width // 2 - 100, self.height // 2 + 50))
        screen.blit(yes_text, yes_rect)
        
        # No選択肢
        no_color = (255, 255, 0) if selection == 1 else (255, 255, 255)  # 選択中は黄色
        no_text = self.font_medium.render("No", True, no_color)
        no_rect = no_text.get_rect(center=(self.width // 2 + 100, self.height // 2 + 50))
        screen.blit(no_text, no_rect)
        
    def draw_result_screen(self, screen, is_cleared):
        """リザルト画面を描画
        
        Args:
            screen (pygame.Surface): 描画対象の画面
            is_cleared (bool): ゲームクリアしたかどうか
        """
        # 背景を黒で塗りつぶす
        screen.fill((0, 0, 0))
        
        # メッセージ
        if is_cleared:
            message_text = self.font_large.render("Congrats!!!", True, (255, 255, 0))
        else:
            message_text = self.font_large.render("Game Over....", True, (255, 0, 0))
        message_rect = message_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(message_text, message_rect)
        
        # リトライ指示
        retry_text = self.font_medium.render("Retry", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(retry_text, retry_rect)
        
    def draw_lives(self, screen, lives):
        """残機を描画
        
        Args:
            screen (pygame.Surface): 描画対象の画面
            lives (int): 残機数
        """
        lives_text = self.font_small.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (self.width - 150, 20))
