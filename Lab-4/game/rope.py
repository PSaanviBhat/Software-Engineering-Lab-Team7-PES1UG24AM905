import random
import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

    def pull_left(self, strength=1.0):
        self.marker_x -= int(self.pull_step * strength)

    def pull_right(self, strength=1.0):
        self.marker_x += int(self.pull_step * strength)

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)

    def render(self, surface, tension=0.0):
        start_pos = (60, self.center_y)
        end_pos = (self.screen_width - 60, self.center_y)

        points = []
        num_segments = 24

        for i in range(num_segments + 1):
            t = i / num_segments
            seg_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            seg_y = float(self.center_y)

            # Parabolic sag (noticeable when tension is low)
            sag_amount = (1.0 - tension) * 28.0
            sag_offset = sag_amount * (4.0 * t * (1.0 - t))
            seg_y += sag_offset

            # High-tension vibration / hum jitter (when tension is high)
            if tension > 0.4:
                vibe_intensity = (tension - 0.4) * 2.5
                seg_y += random.uniform(-3.5, 3.5) * vibe_intensity

            points.append((seg_x, seg_y))

        pygame.draw.lines(surface, (180, 140, 90), False, points, 10)

        # Win boundary lines
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        # Center line indicator
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        # Find flag Y position based on current rope sag/vibration at marker_x
        rope_span = self.screen_width - 120
        t_marker = max(0.0, min(1.0, (self.marker_x - 60) / rope_span))
        flag_y = self.center_y + ((1.0 - tension) * 28.0 * 4.0 * t_marker * (1.0 - t_marker))
        if tension > 0.4:
            flag_y += random.uniform(-2, 2) * (tension - 0.4)

        flag_rect = pygame.Rect(int(self.marker_x) - 12, int(flag_y) - 24, 24, 48)
        pygame.draw.rect(surface, (230, 40, 40), flag_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), flag_rect, width=2, border_radius=4)
