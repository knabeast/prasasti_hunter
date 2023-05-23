import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, current_level):
        super().__init__()
        self.import_character_assets()
        self.current_level = current_level
        self.frame_index = 0
        self.animation_speed = 0.24
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.path = []

        # dust particles
        self.import_dust_run_particles(self.current_level)
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # attack particles
        self.import_attack_particles()
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.15
        self.attacking = False
        self.waiting_left = None
        self.waiting_right = None
        self.attack_duration = 700

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -10

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.can_move = True 

        # audio
        self.run_sound = pygame.mixer.Sound('./audio/effects/run.wav')
        self.run_sound_playing = False
        
    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self, current_level):
        if current_level == 0:
            self.dust_run_particles = import_folder('./graphics/character/dust_particles/run') 
        else:
            self.dust_run_particles = import_folder('./graphics/character/dust_particles/run2') 

    def import_attack_particles(self):
        self.attack_particles = import_folder('./graphics/character/attack')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)

    def run_attack_animation(self):
        if self.on_ground and self.attacking:
            self.attack_frame_index += self.attack_animation_speed
            if self.attack_frame_index >= len(self.attack_particles):
                self.attack_frame_index = 0

            image = self.attack_particles[int(self.attack_frame_index)]
            if self.facing_right:
                self.image = image
            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            # self.run_sound.play(loops= 1)
            self.facing_right = True
        elif keys[pygame.K_a]:
            # self.run_sound.play(loops= 1)
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
            self.run_sound.stop()

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.run_sound.stop()

    def play_run_sound(self):
        if not self.run_sound_playing:
            self.run_sound.play(loops= -1)
            self.run_sound_playing = True

    def is_running(self):
        if self.status == 'run' and self.on_ground and self.direction.x != 0:
            self.play_run_sound()
        else:
            self.run_sound_playing = False


    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            elif self.direction.x == 0:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def attack(self):
        self.attacking = True
        self.direction.x = 0
        self.run_sound.stop()

    def set_movement_enabled(self, enabled):
        self.can_move = enabled

    def check_mouse_left_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.set_movement_enabled(False)
            self.attack()
            self.waiting_left = pygame.time.get_ticks() + self.attack_duration

        if self.waiting_left and pygame.time.get_ticks() >= self.waiting_left:
            self.attacking = False
            self.attack_frame_index = 0
            self.waiting_left = None
            self.set_movement_enabled(True)

    def check_mouse_right_click(self):
        if pygame.mouse.get_pressed()[2]:
            self.set_movement_enabled(False)
            self.attack()
            self.waiting_right = pygame.time.get_ticks() + self.attack_duration

        if self.waiting_right and pygame.time.get_ticks() >= self.waiting_right:
            self.attacking = False
            self.attack_frame_index = 0
            self.waiting_right = None
            self.set_movement_enabled(True)

    def get_coordinate(self):
        col = self.rect.centerx // 48
        row = self.rect.centery // 48
        return col, row
    
    def stop_run_sound(self):
        self.run_sound.stop()

    def update(self):
        if self.can_move:
            self.get_input()
        self.is_running()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.run_attack_animation()
        self.check_mouse_left_click()
        self.check_mouse_right_click()

