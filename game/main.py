#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
メインゲームモジュール
"""

import pygame
import sys
import os
from game.game_state import GameState
from game.player import Player
from game.stage import Stage
from game.ui import UI

class Game:
    """ゲームクラス"""
    
    def __init__(self):
        """初期化"""
        # Pygameの初期化
        pygame.init()
        pygame.mixer.init()
        
        # 画面設定
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Super Cline Brothers")
        
        # BGMの読み込みと再生
        self._load_bgm()
        
        # ゲーム状態
        self.game_state = GameState()
        
        # UI
        self.ui = UI(self.screen_width, self.screen_height)
        
        # ステージ
        self.stage = Stage(3000, self.screen_height)
        
        # プレイヤー
        start_pos = self.stage.get_start_position()
        self.player = Player(start_pos[0], start_pos[1])
        
        # カメラオフセット（スクロール用）
        self.camera_offset_x = 0
        
        # クロック
        self.clock = pygame.time.Clock()
        
        # キー入力の状態
        self.keys = {}
        
    def handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
                
                # スタート画面
                if self.game_state.state == GameState.START:
                    if event.key == pygame.K_a:
                        self.game_state.start_game()
                        self._update_bgm()  # BGM状態を更新
                        
                # リトライ画面
                elif self.game_state.state == GameState.RETRY:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        # 選択の切り替え
                        self.game_state.select_retry(1 - self.game_state.retry_selection)
                    elif event.key == pygame.K_RETURN:
                        # 選択の確定
                        self.game_state.confirm_retry()
                        # BGM状態を更新
                        self._update_bgm()
                        if self.game_state.state == GameState.PLAYING:
                            # リトライする場合はプレイヤーの位置をリセットし、敵を復活させる
                            self.stage.reset()
                            start_pos = self.stage.get_start_position()
                            self.player.reset_position(start_pos[0], start_pos[1])
                            self.camera_offset_x = 0
                            
                # リザルト画面
                elif self.game_state.state == GameState.RESULT:
                    if event.key == pygame.K_RETURN:
                        # ゲームを再スタート
                        self.game_state.restart_game()
                        self.stage.reset()
                        start_pos = self.stage.get_start_position()
                        self.player.reset_position(start_pos[0], start_pos[1])
                        self.camera_offset_x = 0
                        # BGM状態を更新
                        self._update_bgm()
                        
            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False
                
    def update(self):
        """ゲーム状態の更新"""
        if self.game_state.state == GameState.PLAYING:
            # プレイヤーの入力処理
            is_dashing = self.keys.get(pygame.K_LSHIFT, False) or self.keys.get(pygame.K_RSHIFT, False)
            
            if self.keys.get(pygame.K_LEFT, False):
                self.player.move_left(is_dashing)
            elif self.keys.get(pygame.K_RIGHT, False):
                self.player.move_right(is_dashing)
            else:
                self.player.stop()
                
            if self.keys.get(pygame.K_SPACE, False):
                self.player.jump()
                
            # プレイヤーの更新
            self.player.update(self.stage.blocks)
            
            # ステージの更新
            self.stage.update()
            
            # カメラのスクロール
            self._update_camera()
            
            # 衝突判定
            self._check_collisions()
            
    def _update_camera(self):
        """カメラ位置の更新"""
        # プレイヤーが画面中央より右にいる場合、カメラを追従させる
        player_screen_x = self.player.rect.x - self.camera_offset_x
        if player_screen_x > self.screen_width // 2:
            self.camera_offset_x = self.player.rect.x - self.screen_width // 2
            
        # カメラが左端より左に行かないようにする
        if self.camera_offset_x < 0:
            self.camera_offset_x = 0
            
        # カメラが右端より右に行かないようにする
        max_offset = self.stage.width - self.screen_width
        if self.camera_offset_x > max_offset:
            self.camera_offset_x = max_offset
            
    def _check_collisions(self):
        """衝突判定"""
        # 敵との衝突判定
        for enemy in self.stage.enemies:
            collision_type = enemy.check_collision_with_player(self.player)
            
            if collision_type == 1:  # 上からの衝突
                enemy.defeat()
                # Shiftキーを押している場合は通常ジャンプと同じ勢いで跳ね返る
                is_dashing = self.keys.get(pygame.K_LSHIFT, False) or self.keys.get(pygame.K_RSHIFT, False)
                if is_dashing:
                    self.player.vel_y = -self.player.JUMP_POWER  # 通常ジャンプと同じ勢い
                else:
                    self.player.vel_y = -10  # 通常の跳ね返り
            elif collision_type == 2:  # その他の衝突（ダメージ）
                # プレイヤーをダメージ状態にする
                self.player.take_damage()
                    
        # 穴に落ちた判定またはダメージ状態で画面外に出た判定
        if self.player.rect.y > self.screen_height:
            self.game_state.lose_life()
            # BGM状態を更新
            self._update_bgm()
            if self.game_state.state == GameState.PLAYING:
                # まだ残機がある場合は位置をリセット
                start_pos = self.stage.get_start_position()
                self.player.reset_position(start_pos[0], start_pos[1])
                self.camera_offset_x = 0
                
        # ゴールとの衝突判定
        if pygame.sprite.collide_rect(self.player, self.stage.goal):
            self.game_state.clear_game()
            self._update_bgm()  # BGM状態を更新
            
    def draw(self):
        """描画処理"""
        if self.game_state.state == GameState.START:
            # スタート画面
            self.ui.draw_start_screen(self.screen)
            
        elif self.game_state.state == GameState.PLAYING:
            # ゲーム画面
            self.screen.fill((135, 206, 235))  # 空色の背景
            
            # ステージの描画（カメラオフセットを適用）
            for block in self.stage.blocks:
                self.screen.blit(block.image, (block.rect.x - self.camera_offset_x, block.rect.y))
                
            for enemy in self.stage.enemies:
                self.screen.blit(enemy.image, (enemy.rect.x - self.camera_offset_x, enemy.rect.y))
                
            # ゴールの描画
            self.screen.blit(self.stage.goal.image, 
                            (self.stage.goal.rect.x - self.camera_offset_x, self.stage.goal.rect.y))
                
            # プレイヤーの描画
            self.screen.blit(self.player.image, 
                            (self.player.rect.x - self.camera_offset_x, self.player.rect.y))
                
            # 残機の描画
            self.ui.draw_lives(self.screen, self.game_state.lives)
            
        elif self.game_state.state == GameState.RETRY:
            # リトライ画面（ゲーム画面の上に重ねて描画）
            self.screen.fill((135, 206, 235))  # 空色の背景
            
            # ステージの描画
            for block in self.stage.blocks:
                self.screen.blit(block.image, (block.rect.x - self.camera_offset_x, block.rect.y))
                
            for enemy in self.stage.enemies:
                self.screen.blit(enemy.image, (enemy.rect.x - self.camera_offset_x, enemy.rect.y))
                
            # ゴールの描画
            self.screen.blit(self.stage.goal.image, 
                            (self.stage.goal.rect.x - self.camera_offset_x, self.stage.goal.rect.y))
                
            # プレイヤーの描画
            self.screen.blit(self.player.image, 
                            (self.player.rect.x - self.camera_offset_x, self.player.rect.y))
                
            # 残機の描画
            self.ui.draw_lives(self.screen, self.game_state.lives)
            
            # リトライ画面のUI
            self.ui.draw_retry_screen(self.screen, self.game_state.retry_selection)
            
        elif self.game_state.state == GameState.RESULT:
            # リザルト画面
            self.ui.draw_result_screen(self.screen, self.game_state.is_cleared)
            
        # 画面の更新
        pygame.display.flip()
        
    def _load_bgm(self):
        """BGMを読み込む"""
        try:
            # BGMファイルのパス
            bgm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    "assets", "music", "157_BPM175.mp3")
            
            # BGMを読み込む
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(0.25)  # 音量を25%に設定（元の半分）
            
            # 初期状態ではBGMを再生しない（ゲーム開始時に再生）
        except Exception as e:
            print(f"BGMの読み込みに失敗しました: {e}")
            
    def _update_bgm(self):
        """ゲーム状態に応じてBGMの再生状態を更新"""
        # プレイ中のみBGMを再生
        if self.game_state.state == GameState.PLAYING:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  # -1を指定すると無限ループ
        else:
            # それ以外の状態ではBGMを停止
            pygame.mixer.music.stop()
    
    def run(self):
        """ゲームループ"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60FPS


if __name__ == "__main__":
    game = Game()
    game.run()
