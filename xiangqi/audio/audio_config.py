"""
audio/audio_config.py
音频配置文件 - 定义音频系统的配置和常量
"""
import os
from typing import Dict, List, Tuple
from enum import Enum


class SoundCategory(Enum):
    """音效分类枚举"""
    UI = "ui"
    GAME = "game"
    OTHER = "other"


class AudioConfig:
    """音频配置类"""

    # ========== 路径配置 ==========
    # 基础路径
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
    ASSETS_PATH = os.path.join(BASE_PATH, "assets")

    # 音频文件夹路径
    AUDIO_PATH = os.path.join(ASSETS_PATH, "audio")
    SFX_PATH = os.path.join(AUDIO_PATH, "soundeffect")
    MUSIC_PATH = os.path.join(AUDIO_PATH, "music")  # 如果未来有音乐

    # ========== 音频设置 ==========
    # 混音器设置
    FREQUENCY = 44100
    SIZE = -16  # 16位
    CHANNELS = 8  # 同时播放的音效数量
    BUFFER = 1024

    # 默认音量
    MASTER_VOLUME = 1.0
    SFX_VOLUME = 0.8
    MUSIC_VOLUME = 0.6

    # 音效设置
    MAX_SOUND_INSTANCES = 3  # 同一音效最大同时播放实例数
    MIN_PLAY_DELAY = 0.1  # 相同音效最小播放间隔(秒)

    # ========== 音效文件配置 ==========
    # 支持的音频格式
    SUPPORTED_FORMATS = ('.wav', '.mp3', '.ogg', '.flac')

    # 预定义的音效映射
    SOUND_MAPPINGS = {
        'click': {
            'filename': 'click.wav',
            'category': SoundCategory.UI,
            'volume': 0.7,
            'max_instances': 5,
            'min_delay': 0.05
        },
        'select': {
            'filename': 'select.wav',
            'category': SoundCategory.UI,
            'volume': 0.8,
            'max_instances': 3,
            'min_delay': 0.1
        },

    }

    # 音效组定义
    SOUND_GROUPS = {
        'ui': ['click', 'select', 'hover', 'confirm']
    }

    @classmethod
    def get_sfx_path(cls, sound_name: str) -> str:
        """
        获取音效文件路径

        Args:
            sound_name: 音效名称（配置中的key）

        Returns:
            音效文件完整路径
        """
        if sound_name in cls.SOUND_MAPPINGS:
            filename = cls.SOUND_MAPPINGS[sound_name]['filename']
            return os.path.join(cls.SFX_PATH, filename)

        # 如果没有在配置中，尝试直接查找文件
        for ext in cls.SUPPORTED_FORMATS:
            file_path = os.path.join(cls.SFX_PATH, f"{sound_name}{ext}")
            if os.path.exists(file_path):
                return file_path

        # 如果都没找到，返回默认路径
        return os.path.join(cls.SFX_PATH, f"{sound_name}.wav")

    @classmethod
    def get_all_sfx_files(cls) -> Dict[str, str]:
        """
        获取所有音效文件

        Returns:
            字典：音效名 -> 文件路径
        """
        sfx_files = {}

        # 遍历音效文件夹
        if os.path.exists(cls.SFX_PATH):
            for filename in os.listdir(cls.SFX_PATH):
                if filename.lower().endswith(cls.SUPPORTED_FORMATS):
                    sound_name = os.path.splitext(filename)[0]
                    sfx_files[sound_name] = os.path.join(cls.SFX_PATH, filename)

        return sfx_files

    @classmethod
    def validate_paths(cls) -> Dict[str, bool]:
        """
        验证路径是否存在

        Returns:
            路径验证结果字典
        """
        paths = {
            'base': cls.BASE_PATH,
            'assets': cls.ASSETS_PATH,
            'audio': cls.AUDIO_PATH,
            'sfx': cls.SFX_PATH
        }

        results = {}
        for name, path in paths.items():
            exists = os.path.exists(path)
            results[name] = exists
            if not exists:
                print(f"警告: 路径不存在 - {name}: {path}")

        return results


# 创建全局配置实例
config = AudioConfig()