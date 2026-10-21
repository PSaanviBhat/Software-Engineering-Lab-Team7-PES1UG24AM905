import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)
        self.player = Puller(90, height // 2, (50, 120, 220), "PLAYER (A/D)")
        self.computer = Puller(width - 90, height // 2, (220, 80, 50), "COMPUTER")

        # Input tracking
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        # AI Dynamic Panic Surge configuration
        self.base_ai_cooldown = 180
        self.min_ai_cooldown = 70  # Fastest cooldown when in max panic
        self.base_ai_strength = 1.0
        self.max_ai_strength = 2.0  # Hardest pull strength when in max panic
        self.current_ai_cooldown = self.base_ai_cooldown
        self.last_computer_pull = pygame.time.get_ticks()

        self.center_start_x = width // 2

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        # Purely edge-triggered logic (KEYDOWN only)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                # If the key is the opposite of the last successful press, pull!
                if event.key != self.last_key:
                    self.rope.pull_left(1.0)
                    self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # Dynamic AI Panic Surge calculation
        total_distance_to_lose = self.center_start_x - self.rope.left_win_x
        current_distance_to_lose = self.rope.marker_x - self.rope.left_win_x

        # Panic factor: 0.0 (center/safe) to 1.0 (at player's winning threshold)
        if total_distance_to_lose > 0:
            panic_factor = 1.0 - (current_distance_to_lose / total_distance_to_lose)
            panic_factor = max(0.0, min(1.0, panic_factor))
        else:
            panic_factor = 0.0

        # Scale cooldown down and strength up as panic increases
        cooldown_range = self.base_ai_cooldown - self.min_ai_cooldown
        self.current_ai_cooldown = self.base_ai_cooldown - (cooldown_range * panic_factor)

        if now - self.last_computer_pull >= self.current_ai_cooldown:
            strength_range = self.max_ai_strength - self.base_ai_strength
            current_strength = self.base_ai_strength + (strength_range * panic_factor)

            computer_variance = random.uniform(current_strength - 0.3, current_strength + 0.2)
            self.rope.pull_right(max(0.1, computer_variance))
            self.last_computer_pull = now

        result = self.rope.check_winner()
        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"
        self.current_ai_cooldown = self.base_ai_cooldown
        self.last_computer_pull = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((30, 32, 36))

        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        self.rope.render(screen)
        self.player.render(screen)
        self.computer.render(screen)

        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!", True, (210, 210, 210)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 40))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50)
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )
