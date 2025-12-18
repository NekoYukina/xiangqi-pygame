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

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
        return cls._instance

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

    def load_sound(self, sound_name: str, file_path: str = None, category: SoundCategory = None) -> bool:
        """
        加载单个音效

        Args:
            sound_name: 音效名称
            file_path: 文件路径，如果为None则根据配置查找
            category: 音效分类

        Returns:
            是否加载成功
        """
        if sound_name in self.sounds:
            print(f"音效已加载: {sound_name}")
            return True

        try:
            # 确定文件路径
            if file_path is None:
                file_path = AudioConfig.get_sfx_path(sound_name)

            if not os.path.exists(file_path):
                print(f"错误: 音效文件不存在: {file_path}")
                return False

            # 加载音效
            sound = pygame.mixer.Sound(file_path)

            # 获取配置
            if sound_name in AudioConfig.SOUND_MAPPINGS:
                config = AudioConfig.SOUND_MAPPINGS[sound_name]
            else:
                # 默认配置
                config = {
                    'category': category or SoundCategory.OTHER,
                    'volume': 1.0,
                    'max_instances': AudioConfig.MAX_SOUND_INSTANCES,
                    'min_delay': AudioConfig.MIN_PLAY_DELAY
                }

            # 设置音量
            volume = config.get('volume', 1.0)
            sound.set_volume(volume * self.master_volume * self.sfx_volume)

            # 存储音效
            self.sounds[sound_name] = sound
            self.sound_configs[sound_name] = config
            self.play_count[sound_name] = 0

            print(f"✓ 加载音效: {sound_name}")
            return True

        except Exception as e:
            print(f"✗ 加载音效失败 {sound_name}: {e}")
            return False

    def load_all_sfx(self) -> Dict[str, bool]:
        """
        加载音效文件夹中的所有音效

        Returns:
            加载结果字典
        """
        results = {}
        sfx_files = AudioConfig.get_all_sfx_files()

        for sound_name, file_path in sfx_files.items():
            # 只加载未加载的音效
            if sound_name not in self.sounds:
                success = self.load_sound(sound_name, file_path)
                results[sound_name] = success

        return results

    def play(self, sound_name: str, volume: float = 1.0) -> bool:
        """
        播放音效（主要接口）

        Args:
            sound_name: 音效名称
            volume: 音量乘数 (0.0-1.0)

        Returns:
            是否播放成功
        """
        # 检查音效是否存在
        if sound_name not in self.sounds:
            print(f"警告: 音效不存在，尝试加载: {sound_name}")
            if not self.load_sound(sound_name):
                return False

        # 获取音效和配置
        sound = self.sounds[sound_name]
        config = self.sound_configs.get(sound_name, {})

        # 检查播放限制
        if not self._can_play_sound(sound_name, config):
            return False

        try:
            # 计算最终音量
            base_volume = config.get('volume', 1.0)
            final_volume = base_volume * volume * self.master_volume * self.sfx_volume
            final_volume = max(0.0, min(1.0, final_volume))

            # 设置音量并播放
            sound.set_volume(final_volume)

            # 查找空闲频道
            channel = self._find_available_channel()
            if channel is None:
                print(f"警告: 没有可用音频频道播放 {sound_name}")
                return False

            # 播放音效
            channel.play(sound)

            # 更新状态
            current_time = time.time()
            instance = SoundInstance(
                sound_name=sound_name,
                start_time=current_time,
                channel_id=channel.get_id()
            )
            self.playing_instances.append(instance)
            self.last_play_time[sound_name] = current_time
            self.play_count[sound_name] = self.play_count.get(sound_name, 0) + 1

            # 设置播放完成回调
            channel.set_endevent(pygame.USEREVENT)

            return True

        except Exception as e:
            print(f"播放音效失败 {sound_name}: {e}")
            return False

    def _can_play_sound(self, sound_name: str, config: dict) -> bool:
        """
        检查是否可以播放音效

        Args:
            sound_name: 音效名称
            config: 音效配置

        Returns:
            是否可以播放
        """
        current_time = time.time()

        # 检查最小播放间隔
        if sound_name in self.last_play_time:
            time_since_last = current_time - self.last_play_time[sound_name]
            min_delay = config.get('min_delay', AudioConfig.MIN_PLAY_DELAY)
            if time_since_last < min_delay:
                return False

        # 检查最大实例数
        max_instances = config.get('max_instances', AudioConfig.MAX_SOUND_INSTANCES)
        current_instances = sum(1 for i in self.playing_instances if i.sound_name == sound_name)

        if current_instances >= max_instances:
            return False

        return True

    def _find_available_channel(self) -> Optional[pygame.mixer.Channel]:
        """查找可用的音频频道"""
        # 先检查是否有空闲频道
        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            if not channel.get_busy():
                return channel

        # 如果没有空闲频道，检查是否有可以停止的旧音效
        if self.playing_instances:
            # 找到最旧的音效实例
            oldest_instance = min(self.playing_instances, key=lambda x: x.start_time)
            channel = pygame.mixer.Channel(oldest_instance.channel_id)
            channel.stop()

            # 从列表中移除
            self.playing_instances = [i for i in self.playing_instances if i.channel_id != oldest_instance.channel_id]

            return channel

        return None

    def stop_all(self):
        """停止所有音效"""
        pygame.mixer.stop()
        self.playing_instances.clear()

    def stop_sound(self, sound_name: str) -> int:
        """
        停止指定音效的所有实例

        Returns:
            停止的实例数量
        """
        stopped_count = 0

        for instance in self.playing_instances[:]:
            if instance.sound_name == sound_name:
                channel = pygame.mixer.Channel(instance.channel_id)
                if channel.get_busy():
                    channel.stop()
                    self.playing_instances.remove(instance)
                    stopped_count += 1

        return stopped_count

    def pause_all(self):
        """暂停所有音效"""
        pygame.mixer.pause()

    def unpause_all(self):
        """恢复所有音效"""
        pygame.mixer.unpause()

    def set_master_volume(self, volume: float):
        """
        设置主音量

        Args:
            volume: 音量值 (0.0-1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()

    def set_sfx_volume(self, volume: float):
        """
        设置音效音量

        Args:
            volume: 音量值 (0.0-1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()

    def _update_all_volumes(self):
        """更新所有音效的音量"""
        for sound_name, sound in self.sounds.items():
            config = self.sound_configs.get(sound_name, {})
            base_volume = config.get('volume', 1.0)
            sound.set_volume(base_volume * self.master_volume * self.sfx_volume)

    def update(self):
        """更新音频管理器状态（需要在游戏循环中调用）"""
        # 清理已完成的音效实例
        current_time = time.time()
        max_age = 10.0  # 最大记录时间

        self.playing_instances = [
            i for i in self.playing_instances
            if current_time - i.start_time < max_age
        ]

    def get_sound_info(self, sound_name: str) -> Optional[dict]:
        """获取音效信息"""
        if sound_name in self.sounds:
            info = self.sound_configs.get(sound_name, {}).copy()
            info['play_count'] = self.play_count.get(sound_name, 0)
            info['is_loaded'] = True
            return info
        return None

    def get_playing_sounds(self) -> List[str]:
        """获取当前正在播放的音效列表"""
        playing = []
        for instance in self.playing_instances:
            channel = pygame.mixer.Channel(instance.channel_id)
            if channel.get_busy():
                playing.append(instance.sound_name)
        return list(set(playing))  # 去重

    def cleanup(self):
        """清理资源"""
        self.stop_all()
        self.sounds.clear()
        self.sound_configs.clear()
        self.playing_instances.clear()


# 创建全局音频管理器实例
audio_manager = AudioManager()