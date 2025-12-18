"""
audio/soundeffect.py
音效工具类 - 提供便捷的音效播放接口
"""
import os
import pygame
import random
from typing import List, Optional

from audio_manager import AudioManager
from audio_config import AudioConfig, config


class SoundEffect:
    """
    音效工具类

    提供高级音效播放功能：
    1. 便捷的音效播放方法
    2. 音效组管理
    3. 音效序列播放
    4. 3D音效模拟
    """

    def on_enter(self, **kwards):
        base_path = Path(__file__).parent.parent / 'assets' / 'audio' / 'soundeffect'

    def click_play(volume:float = 0.8):
        try:
            # 查找click.wav文件
            click_path = None
            possible_paths = [
                "assets/audio/soundeffect/click.wav",
                "assets/audio/click.wav",
                "click.wav"
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    click_path = path
                    break

            if not click_path:
                print("警告: 未找到click.wav音效文件")
                return False

            # 加载并播放音效
            sound = pygame.mixer.Sound(click_path)
            sound.set_volume(volume)
            sound.play()
            return True

        except Exception as e:
            print(f"播放点击音效失败: {e}")
            return False

def select_play(volume:float = 0.8):

    try:
        # 查找select.wav文件
        select_path = None
        possible_paths = [
            "assets/audio/soundeffect/select.wav",
            "select.wav"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                select_path = path
                break

        if not select_path:
            print("警告: 未找到select.wav音效文件")
            return False

        # 加载并播放音效
        sound = pygame.mixer.Sound(select_path)
        sound.set_volume(volume)
        sound.play()
        return True

    except Exception as e:
        print(f"播放选择音效失败: {e}")
        return False

