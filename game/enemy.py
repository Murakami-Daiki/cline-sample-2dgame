#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
敵モジュール
"""

import pygame

class Enemy(pygame.sprite.Sprite):
    """敵クラス"""
    
    # 敵の状態
    ACTIVE = 0    # 通常状態
    DEFEATED = 1  # 倒された状態
    
    # 移動方向
    DIRECTION_LEFT = -1  # 左向き
    DIRECTION_RIGHT = 1  # 右向き
    
    # 移動速度と物理パラメータ
    MOVE_SPEED = 2  # 横移動速度
    FALL_SPEED = 10  # 倒された後の落下速度
    
    def __init__(self, x, y):
        """初期化
        
        Args:
            x (int): 初期X座標
            y (int): 初期Y座標
        """
        super().__init__()
        
        # 敵の画像を作成（シンプルな四角形）
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # 赤色
        self.rect = self.image.get_rect()
        
        # 位置を設定
        self.rect.x = x
        self.rect.y = y
        
        # 物理演算用の浮動小数点座標
        self.float_x = float(x)
        self.float_y = float(y)
        
        # 状態と方向
        self.state = self.ACTIVE
        self.direction = self.DIRECTION_LEFT  # 初期方向は左
        
    def update(self, blocks):
        """敵の状態を更新
        
        Args:
            blocks (pygame.sprite.Group): ブロックのグループ
        """
        if self.state == self.ACTIVE:
            # 通常状態では現在の方向に移動
            self.float_x += self.MOVE_SPEED * self.direction
            self.rect.x = int(self.float_x)
            
            # ブロックとの衝突判定
            block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
            for block in block_hit_list:
                if self.direction == self.DIRECTION_LEFT:  # 左に移動中
                    self.rect.left = block.rect.right
                    self.direction = self.DIRECTION_RIGHT  # 方向転換
                elif self.direction == self.DIRECTION_RIGHT:  # 右に移動中
                    self.rect.right = block.rect.left
                    self.direction = self.DIRECTION_LEFT  # 方向転換
                self.float_x = float(self.rect.x)
                
        elif self.state == self.DEFEATED:
            # 倒された状態では下に落下
            self.float_y += self.FALL_SPEED
            self.rect.y = int(self.float_y)
            
            # 画面外に出たら削除
            if self.rect.y > 1000:  # 十分に大きな値
                self.kill()
                
    def defeat(self):
        """敵を倒す"""
        if self.state == self.ACTIVE:
            self.state = self.DEFEATED
            
    def check_collision_with_player(self, player):
        """プレイヤーとの衝突判定
        
        Args:
            player (Player): プレイヤーオブジェクト
            
        Returns:
            int: 0=衝突なし, 1=上からの衝突（敵を倒せる）, 2=その他の衝突（ダメージ）
        """
        if not pygame.sprite.collide_rect(self, player) or self.state == self.DEFEATED:
            return 0  # 衝突なし
            
        # プレイヤーが上から敵に接触したかどうか
        if player.vel_y > 0 and player.rect.bottom < self.rect.centery:
            return 1  # 上からの衝突
        else:
            return 2  # その他の衝突
