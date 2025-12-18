import pygame
import sys
import os

from xiangqi.audio.audio_manager import AudioManager

clock = pygame.time.Clock()

class SimpleBGMPlayer:


    def __init__(self):

        # 状态
        self.status_message = ""
        self.status_timer = 0

    def play_bgm(loops: int = -1, fade_ms: int = 2000, volume: float = 0.6):
        """
        播放背景音乐

        Args:
            loops: 循环次数，-1为无限循环
            fade_ms: 淡入时间（毫秒）
            volume: 音量 (0.0-1.0)
        """
        try:
            # 查找BGM文件
            bgm_path = None
            possible_paths = ["assets/audio/BGM/BGM.mp3"]

            for path in possible_paths:
                if os.path.exists(path):
                    bgm_path = path
                    break

            if not bgm_path:
                print("警告: 未找到BGM文件")
                return False

            # 加载并播放音乐
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            print(f"播放BGM: {os.path.basename(bgm_path)}")
            return True

        except Exception as e:
            print(f"播放BGM失败: {e}")
            return False