import pygame
from sys import exit


class SpriteBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.direction = pygame.math.Vector2()

    def get_position(self, enemy_group):
        sprite_rect = self.get_group_rect(enemy_group)

        enemy_vec = pygame.math.Vector2(sprite_rect.center)
        vec = pygame.math.Vector2(self.rect.center)
        distance = (enemy_vec - vec).magnitude()

        if distance > 0:
            self.direction = (enemy_vec - vec).normalize()
        else:
            self.direction = pygame.math.Vector2()

    def move(self):
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

    def get_group_rect(self, sprite_group):
        for sprite in sprite_group:
            sprite_rect = sprite.rect
            return sprite_rect
        return self.rect

    @staticmethod
    def check_collision(sprite_group1, sprite_group2):
        collisions = pygame.sprite.groupcollide(sprite_group1, sprite_group2, False, False)

        for sprite in collisions:
            collisions[sprite][0].kill()
            if sprite in collisions:
                sprite_rect = collisions[sprite][0].rect.center
                return sprite_rect


class Scissor(SpriteBase):
    def __init__(self, pos):
        super().__init__()
        image_1 = pygame.image.load('graphics/scissors/scissors_1.png').convert_alpha()
        image_2 = pygame.image.load('graphics/scissors/scissors_2.png').convert_alpha()
        self.frames = [image_1, image_2]

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=pos)

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def transform_enemy(self):
        collision = self.check_collision(scissor_group, paper_group)
        if collision:
            scissor_group.add(Scissor(collision))

    def update(self):
        self.animation_state()
        self.transform_enemy()
        self.get_position(paper_group)
        self.move()


class Rock(SpriteBase):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/rock/rock.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def transform_enemy(self):
        collision = self.check_collision(rock_group, scissor_group)
        if collision:
            rock_group.add(Rock(collision))

    def update(self):
        self.transform_enemy()
        self.get_position(scissor_group)
        self.move()


class Paper(SpriteBase):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/paper/paper.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def transform_enemy(self):
        collision = self.check_collision(paper_group, rock_group)
        if collision:
            paper_group.add(Paper(collision))

    def update(self):
        self.transform_enemy()
        self.get_position(rock_group)
        self.move()


pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dividers')
clock = pygame.time.Clock()
game_active = True

# Groups
scissor_group = pygame.sprite.Group()
scissor_group.add(Scissor((300, 60)))

rock_group = pygame.sprite.Group()
rock_group.add(Rock((80, 500)))

paper_group = pygame.sprite.Group()
paper_group.add(Paper((500, 500)))

entity_choice = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                entity_choice = 1
            elif event.key == pygame.K_2:
                entity_choice = 2
            elif event.key == pygame.K_3:
                entity_choice = 3

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spawn_pos = pygame.mouse.get_pos()
                if entity_choice == 1:
                    rock_group.add(Rock(spawn_pos))
                elif entity_choice == 2:
                    paper_group.add(Paper(spawn_pos))
                else:
                    scissor_group.add(Scissor(spawn_pos))

    if game_active:
        screen.fill('white')

        rock_group.draw(screen)
        rock_group.update()

        paper_group.draw(screen)
        paper_group.update()

        scissor_group.draw(screen)
        scissor_group.update()

    clock.tick(30)
    pygame.display.update()
