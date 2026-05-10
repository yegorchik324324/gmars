import pygame
import os
import json

MUSIC_STATE_FILE = "music_state.json"

class MusicManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.current_track = 0
        self.is_playing = False
        self.paused = False
        self.volume = 0.5  # 50% volume

        self.tracks = [
            "whiltswagg_-_Platina_Santa_Klaus_instrumental_(SkySound.cc).mp3",
            "synthwave_goose_-_blade_runner_2049_slowed__reverb_(z3.fm).mp3",
            "Safari_slw_-_Let_Go_slowed_version_(SkySound.cc).mp3",
            "pxlse._hallow_-_numb_(SkySound.cc).mp3"
        ]

        self.available_tracks = []
        for track in self.tracks:
            if os.path.exists(track):
                self.available_tracks.append(track)

        if self.available_tracks:
            self.load_state()
            self.load_track(self.current_track)
            pygame.mixer.music.set_volume(self.volume)
            if self.is_playing:
                pygame.mixer.music.play()
                if self.paused:
                    pygame.mixer.music.pause()

    def load_track(self, index):
        if 0 <= index < len(self.available_tracks):
            self.current_track = index
            pygame.mixer.music.load(self.available_tracks[index])

    def play(self):
        if self.available_tracks:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.play()
            self.is_playing = True
            self.save_state()

    def play_music(self):
        self.play()

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.paused = True
        self.save_state()

    def unpause(self):
        pygame.mixer.music.unpause()
        self.is_playing = True
        self.paused = False
        self.save_state()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.paused = False
        self.save_state()

    def next_track(self):
        if self.available_tracks:
            self.current_track = (self.current_track + 1) % len(self.available_tracks)
            self.load_track(self.current_track)
            if self.is_playing:
                pygame.mixer.music.play()
            self.save_state()

    def prev_track(self):
        if self.available_tracks:
            self.current_track = (self.current_track - 1) % len(self.available_tracks)
            self.load_track(self.current_track)
            if self.is_playing:
                pygame.mixer.music.play()
            self.save_state()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        self.save_state()

    def save_state(self):
        try:
            state = {
                "current_track": self.current_track,
                "is_playing": self.is_playing,
                "paused": self.paused,
                "volume": self.volume,
            }
            with open(MUSIC_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f)
        except Exception:
            pass

    def load_state(self):
        if not os.path.exists(MUSIC_STATE_FILE):
            return
        try:
            with open(MUSIC_STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            if isinstance(state, dict):
                self.current_track = int(state.get("current_track", 0))
                self.volume = float(state.get("volume", self.volume))
                self.is_playing = bool(state.get("is_playing", self.is_playing))
                self.paused = bool(state.get("paused", self.paused))
                if self.current_track >= len(self.available_tracks):
                    self.current_track = 0
        except Exception:
            pass

    # ⭐ ОЦЕ ГОЛОВНЕ — AUTO SWITCH
    def update(self):
        if self.is_playing:
            if not pygame.mixer.music.get_busy():
                self.next_track()

    def toggle_play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            self.unpause()

    def cleanup(self):
        self.save_state()
        self.stop()
        pygame.mixer.quit()


music_manager = MusicManager()