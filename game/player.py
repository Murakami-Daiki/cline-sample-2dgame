#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
プレイヤーモジュール
"""

import pygame

class Player(pygame.sprite.Sprite):
    """プレイヤークラス"""
    
    # プレイヤーの状態
    STANDING = 0  # 地上に立っている
    JUMPING = 1   # ジャンプ中
    FALLING = 2   # 落下中
    DAMAGED = 3   # ダメージを受けて落下中（操作不能）
    
    # 移動速度と物理パラメータ
    MOVE_SPEED = 5       # 通常の横移動速度
    DASH_SPEED = 8       # ダッシュ時の横移動速度
    JUMP_POWER = 15      # ジャンプ力
    GRAVITY = 0.8        # 重力
    
    def __init__(self, x, y):
        """初期化
        
        Args:
            x (int): 初期X座標
            y (int): 初期Y座標
        """
        super().__init__()
        
        # プレイヤーの画像を作成（シンプルな四角形）
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 0, 255))  # 青色
        self.rect = self.image.get_rect()
        
        # 位置を設定
        self.rect.x = x
        self.rect.y = y
        
        # 物理演算用の浮動小数点座標
        self.float_x = float(x)
        self.float_y = float(y)
        
        # 速度
        self.vel_x = 0
        self.vel_y = 0
        
        # 状態
        self.state = self.FALLING
        
    def update(self, blocks):
        """プレイヤーの状態を更新
        
        Args:
            blocks (pygame.sprite.Group): ブロックのグループ
        """
        # ダメージ状態の場合は、ブロックとの衝突判定を行わず落下するだけ
        if self.state == self.DAMAGED:
            self.vel_y += self.GRAVITY  # 重力を適用
            self.float_y += self.vel_y
            self.rect.y = int(self.float_y)
            return
            
        # 横方向の移動
        self.float_x += self.vel_x
        self.rect.x = int(self.float_x)
        
        # ブロックとの衝突判定（横方向）
        block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
        for block in block_hit_list:
            if self.vel_x > 0:  # 右に移動中
                self.rect.right = block.rect.left
            elif self.vel_x < 0:  # 左に移動中
                self.rect.left = block.rect.right
            self.float_x = float(self.rect.x)
        
        # 縦方向の移動
        if self.state == self.JUMPING or self.state == self.FALLING:
            self.vel_y += self.GRAVITY  # 重力を適用
            
        self.float_y += self.vel_y
        self.rect.y = int(self.float_y)
        
        # ブロックとの衝突判定（縦方向）
        block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
        for block in block_hit_list:
            if self.vel_y > 0:  # 下に移動中
                self.rect.bottom = block.rect.top
                self.state = self.STANDING  # 地面に着地
            elif self.vel_y < 0:  # 上に移動中
                self.rect.top = block.rect.bottom
                self.vel_y = 0  # 上昇を止める
            self.float_y = float(self.rect.y)
            
        # 落下中かどうかの判定
        if self.state == self.STANDING:
            # 足元に何もないか確認
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, blocks, False)
            self.rect.y -= 2
            
            if not platform_hit_list:
                self.state = self.FALLING
                
    def jump(self):
        """ジャンプする"""
        if self.state == self.STANDING:
            self.vel_y = -self.JUMP_POWER
            self.state = self.JUMPING
            
    def take_damage(self):
        """ダメージを受ける"""
        self.state = self.DAMAGED
        self.vel_x = 0
        self.vel_y = 5  # 下向きの初速度
            
    def move_left(self, is_dashing=False):
        """左に移動
        
        Args:
            is_dashing (bool): ダッシュするかどうか
        """
        self.vel_x = -self.DASH_SPEED if is_dashing else -self.MOVE_SPEED
        
    def move_right(self, is_dashing=False):
        """右に移動
        
        Args:
            is_dashing (bool): ダッシュするかどうか
        """
        self.vel_x = self.DASH_SPEED if is_dashing else self.MOVE_SPEED
        
    def stop(self):
        """横移動を停止"""
        self.vel_x = 0
        
    def reset_position(self, x, y):
        """位置をリセット
        
        Args:
            x (int): リセット後のX座標
            y (int): リセット後のY座標
        """
        self.rect.x = x
        self.rect.y = y
        self.float_x = float(x)
        self.float_y = float(y)
        self.vel_x = 0
        self.vel_y = 0
        self.state = self.FALLING
