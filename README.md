# Super Cline Brothers
※Clineを用いて作ったサンプルになります

忍者の如く作成された2Dプラットフォームゲームでござる！

## Clineで作った事

このゲームは、Claude AIアシスタント「Cline」を使用して作成されました。以下の機能が実装されています：

- Pygameを使用した2Dプラットフォームゲーム
- プレイヤーキャラクターの移動、ジャンプ、ダッシュ機能
- 敵キャラクターの移動と衝突判定
- ステージの自動生成（ブロック、穴、敵の配置）
- スクロール機能付きカメラ
- ゲーム状態管理（タイトル、プレイ中、リトライ、リザルト）
- 残機システム
- BGM再生機能（プレイ中のみ再生、タイトル画面やゲームオーバー時は停止）

## 使用法

### 必要条件

- Python 3.6以上
- Pygame

### インストール方法

```bash
# リポジトリをクローン
git clone https://github.com/Murakami-Daiki/cline-sample-2dgame.git
cd cline-sample-2dgame

# 仮想環境を作成して有効化（オプション）
python -m venv venv
source venv/bin/activate  # Linuxの場合
# または
venv\Scripts\activate  # Windowsの場合

# 必要なパッケージをインストール
pip install pygame
```

### 実行方法

```bash
python run_game.py
```

### 操作方法

- **左右キー**: 移動
- **Shiftキー + 左右キー**: ダッシュ移動
- **スペースキー**: ジャンプ
- **Aキー**: ゲーム開始
- **Enterキー**: 決定

### ゲームの目的
![イメージ](https://github.com/Murakami-Daiki/cline-sample-2dgame/tree/ForImage/2dgame-sample.png)

敵を踏んだり、穴を飛び越えたりしながら、ステージの右端にあるゴールを目指しましょう！

- 敵は上から踏むと倒せます
- 穴に落ちると残機が減ります
- Shiftキーを押しながら敵を踏むと、通常ジャンプと同じ高さまで跳ね返ります
- 穴はダッシュジャンプで飛び越えられます

## 開発者

- Claude AIアシスタント「Cline」
