import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label, face_dir=-1):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.font = pygame.font.SysFont(None, 24)
        # face_dir: -1 for Player (left side), 1 for Computer (right side)
        self.face_dir = face_dir

    def render(self, surface, lean_intensity=0.0):
        """Draw avatar and label with dynamic leaning."""
        # Create a transparent surface for the character body to allow rotation
        temp_surf = pygame.Surface((80, 120), pygame.SRCALPHA)

        # Body (drawn centered on the temp surface)
        body_rect = pygame.Rect(20, 40, 40, 70)
        pygame.draw.rect(temp_surf, self.color, body_rect, border_radius=6)

        # Head
        pygame.draw.circle(temp_surf, (240, 210, 180), (40, 25), 16)

        # Calculate lean angle based on intensity (max 25 degrees)
        # face_dir ensures they lean backward relative to their side
        angle = 25 * lean_intensity * -self.face_dir

        # Rotate and keep centered
        rotated_surf = pygame.transform.rotate(temp_surf, angle)
        new_rect = rotated_surf.get_rect(center=(self.x, self.y - 5))
        surface.blit(rotated_surf, new_rect)

        # Name / control tag
        label_surf = self.font.render(self.label, True, (240, 240, 240))
        surface.blit(label_surf, (self.x - label_surf.get_width() // 2, self.y + 45))
