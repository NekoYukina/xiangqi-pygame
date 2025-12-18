"""
audio/soundeffect.py
音效工具类 - 提供便捷的音效播放接口
"""
import pygame
import random
from typing import List, Optional

from audio_manager import audio_manager
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

    @staticmethod
    def play_click(volume: float = 1.0, position: tuple = None) -> bool:
        """
        播放点击音效

        Args:
            volume: 音量 (0.0-1.0)
            position: 3D音效位置 (x, y)，用于模拟空间音效

        Returns:
            是否播放成功
        """
        return audio_manager.play('click', volume)

    @staticmethod
    def play_select(volume: float = 1.0) -> bool:
        """播放选择音效"""
        return audio_manager.play('select', volume)

    @staticmethod
    def play_hover(volume: float = 0.7) -> bool:
        """播放悬停音效"""
        return audio_manager.play('hover', volume)

    @staticmethod
    def play_confirm(volume: float = 1.0) -> bool:
        """播放确认音效"""
        return audio_manager.play('confirm', volume)

    @staticmethod
    def play_ui_sound(sound_name: str, volume: float = 1.0) -> bool:
        """
        播放UI音效

        Args:
            sound_name: 音效名称
            volume: 音量

        Returns:
            是否播放成功
        """
        return audio_manager.play(sound_name, volume)

    @staticmethod
    def play_random_from_group(group_name: str, volume: float = 1.0) -> Optional[str]:
        """
        从音效组中随机播放一个音效

        Args:
            group_name: 音效组名称
            volume: 音量

        Returns:
            播放的音效名称，失败返回None
        """
        if group_name not in AudioConfig.SOUND_GROUPS:
            return None

        # 筛选可用的音效
        available_sounds = []
        for sound_name in AudioConfig.SOUND_GROUPS[group_name]:
            if sound_name in audio_manager.sounds:
                available_sounds.append(sound_name)

        if not available_sounds:
            return None

        # 随机选择并播放
        selected = random.choice(available_sounds)
        if audio_manager.play(selected, volume):
            return selected

        return None

    @staticmethod
    def play_sequence(sound_names: List[str], delays: List[float] = None, volume: float = 1.0):
        """
        播放音效序列

        Args:
            sound_names: 音效名称列表
            delays: 延迟时间列表（秒），如果为None则无延迟
            volume: 音量
        """
        if not sound_names:
            return

        # 如果没有提供延迟，创建默认延迟
        if delays is None:
            delays = [0.1] * len(sound_names)

        # 确保延迟列表长度匹配
        if len(delays) < len(sound_names):
            delays = delays + [0.1] * (len(sound_names) - len(delays))

        # 使用pygame定时器播放序列
        current_time = pygame.time.get_ticks()

        for i, sound_name in enumerate(sound_names):
            delay_ms = int(sum(delays[:i]) * 1000)

            # 创建定时器事件
            if delay_ms == 0:
                # 立即播放第一个音效
                audio_manager.play(sound_name, volume)
            else:
                # 设置定时器
                event_time = current_time + delay_ms
                pygame.time.set_timer(
                    pygame.USEREVENT + 100 + i,
                    delay_ms if i == 0 else delays[i - 1] * 1000,
                    loops=1
                )

                # 这里需要在实际游戏循环中处理定时器事件
                # 在main.py中会演示如何处理

    @staticmethod
    def play_spatial_sound(sound_name: str, position: tuple, listener_position: tuple,
                           max_distance: float = 500.0) -> bool:
        """
        播放3D空间音效

        Args:
            sound_name: 音效名称
            position: 音源位置 (x, y)
            listener_position: 听者位置 (x, y)，通常是屏幕中心或玩家位置
            max_distance: 最大可听距离

        Returns:
            是否播放成功
        """
        # 计算距离
        dx = position[0] - listener_position[0]
        dy = position[1] - listener_position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # 计算基于距离的音量衰减
        if distance >= max_distance:
            return False  # 距离太远，不播放

        # 线性衰减
        volume = 1.0 - (distance / max_distance)
        volume = max(0.1, volume)  # 最小音量

        # 计算立体声平衡（左/右声道）
        screen_width = 800  # 假设屏幕宽度
        pan = (position[0] - listener_position[0]) / (screen_width / 2)
        pan = max(-1.0, min(1.0, pan))  # 限制在-1到1之间

        # 播放音效
        success = audio_manager.play(sound_name, volume)

        # 注意：这里需要设置声道平衡，但pygame.mixer.Sound不支持直接设置
        # 实际项目中可能需要使用更高级的音频库或自己实现

        return success

    @staticmethod
    def preload_sounds(sound_names: List[str]):
        """
        预加载音效

        Args:
            sound_names: 需要预加载的音效名称列表
        """
        for sound_name in sound_names:
            if sound_name not in audio_manager.sounds:
                audio_manager.load_sound(sound_name)

    @staticmethod
    def stop_all():
        """停止所有音效"""
        audio_manager.stop_all()

    @staticmethod
    def pause_all():
        """暂停所有音效"""
        audio_manager.pause_all()

    @staticmethod
    def resume_all():
        """恢复所有音效"""
        audio_manager.unpause_all()

    @staticmethod
    def set_volume(master: float = None, sfx: float = None):
        """
        设置音量

        Args:
            master: 主音量
            sfx: 音效音量
        """
        if master is not None:
            audio_manager.set_master_volume(master)
        if sfx is not None:
            audio_manager.set_sfx_volume(sfx)

    @staticmethod
    def get_volume() -> dict:
        """获取当前音量设置"""
        return {
            'master': audio_manager.master_volume,
            'sfx': audio_manager.sfx_volume
        }

    @staticmethod
    def get_status() -> dict:
        """获取音效系统状态"""
        return {
            'loaded_sounds': len(audio_manager.sounds),
            'playing_now': len(audio_manager.get_playing_sounds()),
            'volume': SoundEffect.get_volume(),
            'available_channels': pygame.mixer.get_num_channels() - len(audio_manager.playing_instances)
        }


# 创建便捷的全局函数
def play_click(volume: float = 1.0) -> bool:
    """播放点击音效（便捷函数）"""
    return SoundEffect.play_click(volume)


def play_select(volume: float = 1.0) -> bool:
    """播放选择音效（便捷函数）"""
    return SoundEffect.play_select(volume)
