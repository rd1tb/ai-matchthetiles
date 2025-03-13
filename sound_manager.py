import pygame
import os
import threading
import time

class SoundManager:
    """Manages game sounds and music with individual volume controls"""
    
    def __init__(self):
        """Initialize the sound manager"""
        # Ensure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Set default volumes
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        
        # Volume modifiers for individual sound effects (multiplied by sfx_volume)
        self.volume_modifiers = {
            'button': 0.4,    # Lower volume for button clicks (40% of sfx_volume)
            'swish': 0.7,     # Normal volume for swish sounds
            'win': 1.0,       # Normal volume for win sound
            'error': 0.8      # Normal volume for error sound (80% of sfx_volume)
        }
        
        self.original_music_volume = self.music_volume  # Store original volume for restoring
        
        # List of sounds that should trigger ducking
        self.ducking_sounds = ['win', 'error']  # Only duck for win and error sounds
        
        # Define ducking amounts for different sound types
        self.ducking_amounts = {
            'win': 0.1,       # Reduce to 10% for win sounds
            'error': 0.05      # Reduce to 10% for error sounds
        }
        self.default_ducking_amount = 0.1  # Default ducking amount for unlisted ducking sounds
        
        # Define ducking duration for each sound type
        self.ducking_durations = {
            'win': 0.8,       # 0.8 seconds for win sounds
            'error': 1.2      # 1.2 seconds for error sounds
        }
        self.default_ducking_duration = 0.4  # Default ducking duration
        
        # Dictionary to store sound effects
        self.sounds = {}
        
        # Load sounds
        self._load_sounds()
        
        # Flag to track if volume is currently ducked
        self.is_ducked = False
        self.current_duck_thread = None
        
        # Lock for thread safety
        self.volume_lock = threading.Lock()
        
        # Sound cooldown system to prevent double-playing
        self.sound_last_played = {}
        self.sound_cooldown = {
            'button': 150,  # 150ms cooldown for button sounds
            'win': 500,     # 500ms cooldown for win sounds
            'error': 300    # 300ms cooldown for error sounds
        }
    
    def _load_sounds(self):
        """Load all sound files into memory"""
        try:
            self.sounds = {
                'button': pygame.mixer.Sound(os.path.join("./sounds", 'button_click.mp3')),
                'swish': pygame.mixer.Sound(os.path.join("./sounds", 'swish.mp3')),
                'win': pygame.mixer.Sound(os.path.join("./sounds", 'win.mp3')),
                'error': pygame.mixer.Sound(os.path.join("./sounds", 'error.mp3')),
                'background': os.path.join("./sounds", 'background_music.mp3')
            }
            
            # Set specific volumes for each sound effect
            self._update_sound_volumes()
            
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def _update_sound_volumes(self):
        """Update volumes for all sound effects using their individual modifiers"""
        for sound_name, sound in self.sounds.items():
            if isinstance(sound, pygame.mixer.Sound):
                # Get the volume modifier for this sound (default to 1.0 if not found)
                modifier = self.volume_modifiers.get(sound_name, 1.0)
                # Apply the modifier to the base sfx_volume
                adjusted_volume = self.sfx_volume * modifier
                sound.set_volume(adjusted_volume)
    
    def _duck_volume(self, sound_name):
        """Temporarily lower the music volume
        
        Args:
            sound_name: Name of the sound that triggered ducking
        """
        # Only duck for sounds in the ducking_sounds list
        if sound_name not in self.ducking_sounds:
            return
            
        with self.volume_lock:
            # If a ducking is already in progress, terminate it by setting is_ducked to False
            # This will prevent the old thread from restoring the volume
            if self.is_ducked and self.current_duck_thread and self.current_duck_thread.is_alive():
                self.is_ducked = False
                # Allow a small amount of time for any running thread to exit
                time.sleep(0.02)
                
            # Start a new ducking
            self.is_ducked = True
            self.original_music_volume = pygame.mixer.music.get_volume()
            
            # Get ducking amount for this sound type
            ducking_amount = self.ducking_amounts.get(sound_name, self.default_ducking_amount)
            
            # Reduce the volume
            new_volume = max(0.1, self.original_music_volume * ducking_amount)
            pygame.mixer.music.set_volume(new_volume)
            
            # Get ducking duration for this sound type
            ducking_duration = self.ducking_durations.get(sound_name, self.default_ducking_duration)
            
            # Start a thread to restore volume after a delay
            self.current_duck_thread = threading.Thread(
                target=self._restore_volume_after_delay, 
                args=(ducking_duration,),
                daemon=True
            )
            self.current_duck_thread.start()
    
    def _restore_volume_after_delay(self, delay=0.4):
        """Restore the original music volume after a delay
        
        Args:
            delay: Time in seconds to wait before restoring the volume
        """
        # Store the current is_ducked state to check if it changes while we're waiting
        initial_duck_state = self.is_ducked
        
        # Wait for the sound effect to play
        time.sleep(delay)
        
        with self.volume_lock:
            # Only restore if we're still in the same ducking operation
            if self.is_ducked and initial_duck_state == self.is_ducked:
                # Gradually restore volume for smoother transition
                current = pygame.mixer.music.get_volume()
                target = self.original_music_volume
                steps = 10
                step_size = (target - current) / steps
                
                for _ in range(steps):
                    current += step_size
                    pygame.mixer.music.set_volume(current)
                    time.sleep(0.02)
                
                # Ensure we hit the exact target volume
                pygame.mixer.music.set_volume(target)
                self.is_ducked = False
    
    def play_sound(self, sound_name):
        """Play a sound effect with volume ducking and cooldown protection
        
        Args:
            sound_name: Name of the sound to play
        """
        # Check if sound exists
        if sound_name not in self.sounds or not isinstance(self.sounds[sound_name], pygame.mixer.Sound):
            print(f"Warning: Sound '{sound_name}' not available")
            return
            
        # Check if sound is on cooldown
        current_time = pygame.time.get_ticks()
        last_played = self.sound_last_played.get(sound_name, 0)
        cooldown = self.sound_cooldown.get(sound_name, 0)
        
        if current_time - last_played < cooldown:
            return
        
        # Duck the music volume based on the sound type (only if in ducking_sounds list)
        if pygame.mixer.music.get_busy() and sound_name in self.ducking_sounds:
            self._duck_volume(sound_name)
            
        # Play the sound and update last played time
        self.sounds[sound_name].play()
        self.sound_last_played[sound_name] = current_time
    
    def play_music(self):
        """Start playing background music in a loop"""
        try:
            if 'background' in self.sounds:
                pygame.mixer.music.load(self.sounds['background'])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop the background music"""
        pygame.mixer.music.stop()
    
    def set_music_volume(self, volume):
        """Set the volume for music
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.is_ducked:  # Only change if not currently ducked
            pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set the overall volume for sound effects
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        # Update all sound volumes with their individual modifiers
        self._update_sound_volumes()
    
    def set_sound_volume(self, sound_name, volume):
        """Set the volume for a specific sound effect
        
        Args:
            sound_name: Name of the sound ('button', 'swish', etc.)
            volume: Volume level (0.0 to 1.0) relative to the sfx_volume
        """
        if sound_name in self.volume_modifiers:
            self.volume_modifiers[sound_name] = max(0.0, min(1.0, volume))
            # Update this specific sound's volume
            if sound_name in self.sounds and isinstance(self.sounds[sound_name], pygame.mixer.Sound):
                self.sounds[sound_name].set_volume(self.sfx_volume * self.volume_modifiers[sound_name])
    
    def set_ducking_amount(self, sound_name, amount):
        """Set how much the music volume should be reduced when a specific sound plays
        
        Args:
            sound_name: Name of the sound ('win', 'error', etc.)
            amount: A value between 0.0 and 1.0, where:
                   1.0 = no reduction (100% of original volume)
                   0.5 = reduce to 50% of original volume
                   0.0 = mute completely
        """
        self.ducking_amounts[sound_name] = max(0.0, min(1.0, amount))
        
    def set_ducking_duration(self, sound_name, duration):
        """Set how long the ducking should last for a specific sound
        
        Args:
            sound_name: Name of the sound ('win', 'error', etc.)
            duration: Time in seconds for ducking effect
        """
        self.ducking_durations[sound_name] = max(0.1, duration)
        
    def add_ducking_sound(self, sound_name):
        """Add a sound to the list of sounds that trigger ducking
        
        Args:
            sound_name: Name of the sound to add to ducking list
        """
        if sound_name not in self.ducking_sounds:
            self.ducking_sounds.append(sound_name)
            
    def remove_ducking_sound(self, sound_name):
        """Remove a sound from the list of sounds that trigger ducking
        
        Args:
            sound_name: Name of the sound to remove from ducking list
        """
        if sound_name in self.ducking_sounds:
            self.ducking_sounds.remove(sound_name)