#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ステージモジュール
"""

import pygame
from game.enemy import Enemy

class Block(pygame.sprite.Sprite):
    """ブロッククラス"""
    
    def __init__(self, x, y, width, height):
        """初期化
        
        Args:
            x (int): X座標
            y (int): Y座標
            width (int): 幅
            height (int): 高さ
        """
        super().__init__()
        
        # ブロックの画像を作成
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # グレー
        self.rect = self.image.get_rect()
        
        # 位置を設定
        self.rect.x = x
        self.rect.y = y


class Goal(pygame.sprite.Sprite):
    """ゴールクラス"""
    
    def __init__(self, x, y):
        """初期化
        
        Args:
            x (int): X座標
            y (int): Y座標
        """
        super().__init__()
        
        # ゴールの画像を作成
        self.image = pygame.Surface((50, 80))
        self.image.fill((0, 255, 0))  # 緑色
        self.rect = self.image.get_rect()
        
        # 位置を設定
        self.rect.x = x
        self.rect.y = y


class Stage:
    """ステージクラス"""
    
    def __init__(self, width, height):
        """初期化
        
        Args:
            width (int): ステージの幅
            height (int): ステージの高さ
        """
        self.width = width
        self.height = height
        
        # スプライトグループ
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goal = None
        
        # スタート位置
        self.start_x = 100
        self.start_y = 400
        
        # ステージを作成
        self._create_stage()
        
    def _create_stage(self):
        """ステージを作成"""
        # 地面
        ground_y = 500
        
        # 左端の地面
        for x in range(0, 800, 50):
            self.blocks.add(Block(x, ground_y, 50, 50))
        
        # 穴（幅200px - ダッシュジャンプで渡れる）
        for x in range(800, 1000, 50):
            pass  # 穴なので何も配置しない
        
        # 中央の地面
        for x in range(1000, 1800, 50):
            self.blocks.add(Block(x, ground_y, 50, 50))
        
        # 穴（幅200px - ダッシュジャンプで渡れる）
        for x in range(1800, 2000, 50):
            pass
        
        # 右端の地面
        for x in range(2000, 3000, 50):
            self.blocks.add(Block(x, ground_y, 50, 50))
        
        # 障害物（ブロック）
        self.blocks.add(Block(500, ground_y - 100, 50, 100))
        self.blocks.add(Block(700, ground_y - 150, 50, 150))
        self.blocks.add(Block(1200, ground_y - 100, 50, 100))
        self.blocks.add(Block(1400, ground_y - 150, 50, 150))
        self.blocks.add(Block(1600, ground_y - 100, 50, 100))
        self.blocks.add(Block(2200, ground_y - 100, 50, 100))
        self.blocks.add(Block(2400, ground_y - 150, 50, 150))
        
        # 敵
        self.enemies.add(Enemy(600, ground_y - 30))
        self.enemies.add(Enemy(1300, ground_y - 30))
        self.enemies.add(Enemy(1700, ground_y - 30))
        self.enemies.add(Enemy(2300, ground_y - 30))
        
        # ゴール
        self.goal = Goal(2800, ground_y - 80)
        
    def update(self):
        """ステージの状態を更新"""
        # 敵の更新
        self.enemies.update(self.blocks)
        
    def reset(self):
        """ステージをリセット"""
        # 既存のスプライトをクリア
        self.blocks.empty()
        self.enemies.empty()
        self.goal = None
        
        # ステージを再作成
        self._create_stage()
        
    def get_start_position(self):
        """スタート位置を取得
        
        Returns:
            tuple: (x, y) スタート位置の座標
        """
        return (self.start_x, self.start_y)
