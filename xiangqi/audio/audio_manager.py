"""
audio/audio_manager.py
音频管理器主类 - 统一管理音效播放
"""
import pygame
import os
import time
import json
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass

from audio_config import AudioConfig, SoundCategory, config

@dataclass
class SoundInstance:
    """音效实例信息"""
    sound_name: str
    start_time: float
    channel_id: int

class AudioManager:
    """
    音频管理器

    功能：
    1. 音效的加载和管理
    2. 音效播放控制
    3. 音量管理
    4. 播放统计和限制
    """

    _instance = None  # 单例模式

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._init_audio_system()

    def _init_audio_system(self):
        """初始化音频系统"""
        print("初始化音频系统...")

        # 验证路径
        path_results = AudioConfig.validate_paths()
        if not path_results.get('sfx', False):
            print(f"警告: 音效文件夹不存在，将在 {AudioConfig.SFX_PATH} 创建")
            os.makedirs(AudioConfig.SFX_PATH, exist_ok=True)

        # 初始化混音器
        pygame.mixer.init(
            frequency=AudioConfig.FREQUENCY,
            size=AudioConfig.SIZE,
            channels=AudioConfig.CHANNELS,
            buffer=AudioConfig.BUFFER
        )

        # 音频数据存储
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.sound_configs: Dict[str, dict] = {}

        # 播放状态
        self.playing_instances: List[SoundInstance] = []
        self.last_play_time: Dict[str, float] = {}
        self.play_count: Dict[str, int] = {}

        # 音量设置
        self.master_volume = AudioConfig.MASTER_VOLUME
        self.sfx_volume = AudioConfig.SFX_VOLUME

        # 加载音效
        self.load_configured_sounds()

        print(f"音频系统初始化完成，已加载 {len(self.sounds)} 个音效")

    def load_configured_sounds(self) -> Dict[str, bool]:
        """
        加载配置中定义的音效

        Returns:
            加载结果字典：音效名 -> 是否成功
        """
        results = {}

        for sound_name, sound_config in AudioConfig.SOUND_MAPPINGS.items():
            try:
                # 获取文件路径
                file_path = AudioConfig.get_sfx_path(sound_name)

                if os.path.exists(file_path):
                    # 加载音效
                    sound = pygame.mixer.Sound(file_path)

                    # 设置音量
                    volume = sound_config.get('volume', 1.0)
                    sound.set_volume(volume * self.master_volume * self.sfx_volume)

                    # 存储音效
                    self.sounds[sound_name] = sound
                    self.sound_configs[sound_name] = sound_config
                    self.play_count[sound_name] = 0

                    results[sound_name] = True
                    print(f"✓ 加载音效: {sound_name}")
                else:
                    results[sound_name] = False
                    print(f"✗ 音效文件不存在: {file_path}")

            except Exception as e:
                results[sound_name] = False
                print(f"✗ 加载音效失败 {sound_name}: {e}")

        return results