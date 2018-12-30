import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.sprite import Sprite
from GameObjects import GameObject, preload_image, preload_media
from random import randint, choice


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.frame_rate = 1/60.0
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 15
        self.fps_display.label.y = 10

        # self.background_group = pyglet.graphics.OrderedGroup(0)
        # self.forceground_group = pyglet.graphics.OrderedGroup(1)

        # load intro video
        self.intro_video = pyglet.media.Player()
        self.intro_video.queue(preload_media('Intro.mp4'))
        # self.intro_video.group = self.background_group
        self.intro = True

        # load sound effect
        self.player_shot_sound = pyglet.media.load('res/media/laser.wav', streaming=False)
        self.expl_sound = pyglet.media.load('res/media/exp_01.wav', streaming=False)

        # load main soundtrack
        self.theme_music = pyglet.media.Player()
        self.theme_music.queue(preload_media('theme.mp3'))
        # self.theme_music.eos_action = 'loop'
        self.theme_music.EOS_LOOP = 'loop'

        self.main_batch = pyglet.graphics.Batch()

        # Creating a label called "Enemies destroyed"
        self.text1 = pyglet.text.Label("Enemies destroyed:", x=100, y=10,
                                       batch=self.main_batch)
        self.text1.bold = True
        self.text1.font_size = 15

        # creating a label called "Score"
        # self.text2 = pyglet.text.Label("Score", x=1000, y=550,
                                       # batch=self.main_batch)
        # self.text2.bold = True
        # self.text2.font_size = 16

        # creating a label called "Player health"
        self.text3 = pyglet.text.Label("Player health:", x=950, y=10,
                                       batch=self.main_batch)
        self.text3.bold = True
        self.text3.font_size = 15

        # creating a label to display the number of destroyed enemies
        self.num_enemies_destroyed = pyglet.text.Label(str(0), x=350, y=10,
                                                       batch=self.main_batch)
        self.num_enemies_destroyed.color = (120, 200, 150, 255)
        self.num_enemies_destroyed.font_size = 22

        # creating a label to display the score
        # self.num_score = pyglet.text.Label(str(0), x=1100, y=500,
                                           # batch=self.main_batch)
        # self.num_score.color = (220, 100, 150, 255)
        # self.num_score.font_size = 22

        # creating a label to display the player's health
        self.numb_player_health = pyglet.text.Label(str(5), x=1150, y=10,
                                                    batch=self.main_batch)
        self.numb_player_health.color = (0, 100, 50, 255)
        self.numb_player_health.font_size = 22

        self.game_over_text = pyglet.text.Label("GAME OVER", x=640, y=450)
        self.game_over_text.anchor_x = "center"
        self.game_over_text.anchor_y = "center"
        self.game_over_text.bold = True
        self.game_over_text.font_size = 60

        self.reload_text = pyglet.text.Label("Press [R] to reload",
                                             x=640, y=300)
        self.reload_text.anchor_x = "center"
        self.reload_text.anchor_y = "center"
        self.reload_text.bold = True
        self.reload_text.font_size = 40

        # self.intro_text = pyglet.text.Label("Press [SPACE] to start",
        #                                     x=640, y=200)
        # self.intro_text.anchor_x = "center"
        # self.intro_text.anchor_y = "center"
        # self.intro_text.bold = True
        # self.intro_text.font_size = 40
        # self.intro_text.group = self.forceground_group

        self.right = False
        self.left = False
        self.player_speed = 300
        self.fire = False
        self.player_fire_rate = 0
        self.enemy_fire_rate = 0
        self.destroyed_enemies = 0
        self.next_wave = 0
        self.score = 0
        self.alien_spawner = 0
        self.alien_spawner_count = 1
        self.enemy_ship_spawner_count = 5
        self.player_health = 5
        self.player_is_alive = True
        self.explode_time = 2
        self.enemy_explode = False
        self.shake_time = 0
        self.game = False
        self.flash_time = 1
        self.player_flash = False
        self.enemies_list = []
        self.explosion_list = []

        self.start_game = False

        # when creating a new enemy, it will choose a random direction
        # from the list below
        self.directions = [1, -1]

        player_sprite = Sprite(preload_image('rocket1.png'))
        # self.player = GameObject(self.width//2, 50, player_sprite)
        self.player = GameObject(640, 50, player_sprite)
        # self.player.sprite.scale = 0.12

        self.player_laser = preload_image('laser.png')
        self.player_laser_list = []

        self.enemy_laser = preload_image('enemy_laser.png')
        self.enemy_laser_list = []

        self.space_list = []
        self.space_img1 = preload_image('space_1.jpg')
        sprite_space1 = Sprite(self.space_img1)
        space_1_object = GameObject(0, 0, sprite_space1)
        # sprite_space1.scale = 0.5
        self.space_img2 = preload_image('space_2.jpg')
        sprite_space2 = Sprite(self.space_img2)
        space_2_object = GameObject(0, 1080, sprite_space2)
        # sprite_space2.scale = 0.5
        self.space_list.append(space_1_object)
        self.space_list.append(space_2_object)
        self.count = 0

        self.explosion = pyglet.image.load("res/sprites/explosion.png")
        self.explosion_seq = pyglet.image.ImageGrid(self.explosion, 4, 5,
                                                    item_width=96,
                                                    item_height=96)
        self.explosion_animation = pyglet.image.Animation.from_image_sequence(
            self.explosion_seq[0:], 0.1, loop=True)

        # stats_bg_image = Sprite(preload_image('stats_bg_white.png'))
        # self.stats_bg = GameObject(980, 300, stats_bg_image)
        # self.stats_bg.opacity = 10

        for space in self.space_list:
            space.sprite.scale = 2
            space.velocity_y = -50

    def reload(self):
        self.next_wave = 0
        # self.score = 0
        self.player_health = 5
        self.player_fire_rate = 0
        self.enemy_fire_rate = 0
        self.enemy_ship_spawner = 0
        self.enemy_ship_spawner_count = 5
        self.explode_time = 2
        self.enemy_explode = False
        self.shake_time = 0
        self.destroyed_enemies = 0
        self.player_is_alive = True
        self.player.position_x, self.player.position_y = 640, 50
        self.player.batch = self.main_batch

        self.num_enemies_destroyed.text = str(self.destroyed_enemies)
        # self.num_score.text = str(self.score)
        self.numb_player_health.text = str(self.player_health)

        for obj in self.enemies_list:
            obj.batch = None
        for obj in self.enemy_laser_list:
            obj.batch = None
        self.enemies_list.clear()
        self.enemy_laser_list.clear()

        self.game_over_text.batch = None
        self.reload_text.batch = None


    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True
        if symbol == key.SPACE:
            self.fire = True
            self.intro = False
            self.start_game = True
            self.player_shot_sound.play()
            if not self.game:
                self.game = True
                self.fire = False
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol == key.R:
            self.reload()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = False
        if symbol == key.LEFT:
            self.left = False
        if symbol == key.SPACE:
            self.fire = False

    def on_draw(self):
        self.clear()
        if self.intro:
            # self.intro_text.draw()
            # self.intro_video.play()
            #self.intro_text.background_group = pyglet.graphics.OrderedGroup(1)
            # self.intro_text.batch = self.main_batch
            #self.intro_video.background_group = pyglet.graphics.OrderedGroup(0)
            source = pyglet.media.StreamingSource()
            self.intro_video.play()
            # self.main_batch.draw()
            if self.intro_video.source and self.intro_video.source.video_format:
                self.intro_video.get_texture().blit(0, 0)
        else:
            # self.intro_text.draw()
            self.intro_video.pause()
            for space in self.space_list:
                space.draw()
            self.player.draw()
            for enemy in self.enemies_list:
                enemy.draw()
            self.main_batch.draw()
            self.fps_display.draw()

    def update_player(self, dt):
        self.player.update()
        if self.right and self.player.position_x < 1130:
            self.player.position_x += self.player_speed * dt
        if self.left and self.player.position_x > 80:
            self.player.position_x -= self.player_speed * dt

    def update_player_laser(self, dt):
        for laser in self.player_laser_list:
            laser.update()
            laser.position_y += 400 * dt
            if laser.position_y > 1100:
                self.player_laser_list.remove(laser)

    def player_fire(self, dt):
        self.player_fire_rate -= dt
        if self.player_fire_rate <= 0:
            self.player_laser_list.append(GameObject(
                self.player.position_x + 34, self.player.position_y + 105,
                                          Sprite(self.player_laser,
                                                 batch=self.main_batch)))
            self.player_fire_rate += 0.2

    def update_space(self, dt):
        for space in self.space_list:
            space.update()
            space.position_y -= 50 * dt
            if space.position_y <= -1080:
                self.count = self.count + 1
                # space_compare = GameObject(0, 1080, 'space2.jpg')
                # space_compare.sprite.scale = 0.5
                temp_sprite1 = Sprite(self.space_img1)
                # temp_sprite1.scale = 0.5
                space_object1 = GameObject(0, 1080, temp_sprite1)
                temp_sprite2 = Sprite(self.space_img2)
                # temp_sprite2.scale = 0.5
                space_object2 = GameObject(0, 1080, temp_sprite2)
                # space_compare = GameObject(0, 1080, temp_sprite2)
                if self.count % 2 == 0:
                    # temp_space = GameObject(0, 1080, 'space2.jpg')
                    # temp_space = GameObject(0, 1080, temp_sprite2)
                    self.space_list.remove(space)
                    self.space_list.append(space_object2)
                    # print("space 2")
                else:
                    # temp_space = GameObject(0, 1080, 'space.jpg')
                    # temp_space = GameObject(0, 1080, temp_sprite1)
                    self.space_list.remove(space)
                    self.space_list.append(space_object1)

    def enemy_move(self, velocity_y, dt):
        for enemy in self.enemies_list:
            enemy.update()
            if enemy.position_x >= 1000:
                enemy.position_x = 1000
                enemy.velocity_x *= -1
            if enemy.position_x <= 100:
                enemy.position_x = 100
                enemy.velocity_x *= -1
            enemy.position_y -= velocity_y * dt
            enemy.position_x += enemy.velocity_x * dt
            # if (enemy.position_y <= 450 and enemy.position_y >= 449.4
               # and self.player_is_alive):
                # self.score -= 1
                # self.num_score.text = str(self.score)
            if enemy.position_y <= -100:
                self.enemies_list.remove(enemy)

    def enemy_spawn(self, dt):
        self.alien_spawner -= dt
        if self.player_is_alive:
            if self.alien_spawner <= 0:
                alien_sprite = Sprite(preload_image('alien.png'))
                #alien_sprite = Sprite(preload_image('lbaodong.jpg'))
                self.enemies_list.append(GameObject(600, 720, alien_sprite))
                self.enemies_list[-1].velocity_x = (randint(100, 300)
                                                    * choice(self.directions))
                self.enemies_list[-1].hit_count = 0
                self.enemies_list[-1].MAX_HIT = 2
                self.alien_spawner += self.alien_spawner_count
        if self.next_wave >= 20:
            self.alien_spawner_count -= 0.05
            self.enemy_ship_spawner_count -= 0.2
            self.next_wave = 0

    def enemy_shoot(self, dt):
        self.enemy_fire_rate -= dt
        if self.enemy_fire_rate <= 0:
            for enemy in self.enemies_list:
                enemy.update()
                if randint(0, 10) >= 5:
                    self.enemy_laser_list.append(GameObject(
                     enemy.position_x + 50,
                     enemy.position_y,
                     Sprite(self.enemy_laser, batch=self.main_batch)))
            self.enemy_fire_rate += 5

    def update_enemy_shoot(self, dt):
        for lsr in self.enemy_laser_list:
            lsr.update()
            lsr.position_y -= 400 * dt
            if lsr.position_y < -50:
                self.enemy_laser_list.remove(lsr)

    def enemy_hit(self, entity):
        entity.hit_count += 1
        if entity.hit_count >= entity.MAX_HIT and self.player_is_alive:
            self.enemy_explode = True
            self.explosion_list.append(GameObject(
                                       entity.position_x, entity.position_y,
                                       Sprite(self.explosion_animation,
                                              batch=self.main_batch)))
            self.enemies_list.remove(entity)
            entity.delete()
            self.destroyed_enemies += 1
            self.next_wave += 1
            # self.score += 1
            self.num_enemies_destroyed.text = str(self.destroyed_enemies)
            # self.num_score.text = str(self.score)
            self.player_shot_sound.play()

    def player_hit(self):
        self.player_health -= 1
        self.numb_player_health.text = str(self.player_health)
        self.player_flash = True
        if self.player_health <= 0:
            self.player.batch = None
            self.game_over()

    def update_flash(self):
        self.flash_time -= 0.2
        self.player.color = (255, 0, 0)
        if self.flash_time <= 0:
            self.player.color = (255, 255, 255)
            self.flash_time = 1
            self.player_flash = False

    def update_explosion(self):
        self.explode_time -= 0.1
        if self.explode_time <= 0:
            for expl in self.explosion_list:
                self.explosion_list.remove(expl)
                expl.delete()
            self.explode_time += 2

    def game_over(self):
        self.player_is_alive = False
        self.explosion_list.append(GameObject(
                            self.player.position_x, self.player.position_y,
                            Sprite(self.explosion_animation,
                                    batch=self.main_batch)))
        self.game_over_text.batch = self.main_batch
        self.reload_text.batch = self.main_batch


    def bullet_collision(self, entity, bullet_list):
        for lsr in bullet_list:
            if (lsr.position_x < entity.position_x + entity.width and
               lsr.position_x + lsr.width > entity.position_x and
               lsr.position_y < entity.position_y + entity.height and
               lsr.height + lsr.position_y > entity.position_y):
                bullet_list.remove(lsr)
                return True

    def impact(self, entity, enemies_list):
        for ene in enemies_list:
            if (ene.position_x < entity.position_x + entity.width and
               ene.position_x + ene.width > entity.position_x and
               ene.position_y < entity.position_y + entity.height and
               ene.height + ene.position_y > entity.position_y):
                self.enemy_explode = True
                self.explosion_list.append(GameObject(
                                           entity.position_x, entity.position_y,
                                           Sprite(self.explosion_animation,
                                                  batch=self.main_batch)))
                enemies_list.remove(ene)
                self.player_shot_sound.play()
                return True


    def update(self, dt):
        if self.start_game:
            # self.intro_text.batch = None
            self.theme_music.play()
            if self.game:
                self.update_player(dt)
                self.enemy_move(100, dt)
            if self.fire:
                self.player_fire(dt)
            self.update_player_laser(dt)
            self.enemy_shoot(dt)
            self.update_enemy_shoot(dt)
            for entity in self.enemies_list:
                if self.bullet_collision(entity, self.player_laser_list):
                    self.enemy_hit(entity)
            if (self.bullet_collision(self.player, self.enemy_laser_list)
               and self.player_is_alive) \
               or (self.impact(self.player, self.enemies_list)
               and self.player_is_alive):
                self.player_hit()
            if self.player_flash:
                self.update_flash()
            self.update_explosion()
            self.enemy_spawn(dt)
            self.update_space(dt)


if __name__ == "__main__":
    window = GameWindow(1280, 720, "Rocket 1h", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
