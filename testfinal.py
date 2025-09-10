import pgzrun
from pgzero.rect import Rect 

WIDTH = 1280
HEIGHT = 720

velocity_y = 0
gravity = 1

music_on = True
sounds_on = True
music_started = False

music_rect = Rect((WIDTH//2 - 150 - 140, HEIGHT//2 + 20), (280, 40))
sounds_rect = Rect((WIDTH//2 + 150 - 140, HEIGHT//2 + 20), (280, 40))
play_rect = Rect((WIDTH // 2 - 300, HEIGHT // 2 - 30), (600, 40))
exit_rect = Rect((WIDTH//2 - 140, HEIGHT//2 + 75),(280,40))

status = 'start'
character_data = [
    {
        "idle": "character_beige_idle",
        "walk": ["character_beige_walk_a", "character_beige_walk_b"],
        "jump": "character_beige_jump",
        "hit": "character_beige_hit",
        "pos": (5 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_green_idle",
        "walk": ["character_green_walk_a", "character_green_walk_b"],
        "jump": "character_green_jump",
        "hit": "character_green_hit",
        "pos": (4 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_pink_idle",
        "walk": ["character_pink_walk_a", "character_pink_walk_b"],
        "jump": "character_pink_jump",
        "hit": "character_pink_hit",
        "pos": (3 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_purple_idle",
        "walk": ["character_purple_walk_a", "character_purple_walk_b"],
        "jump": "character_purple_jump",
        "hit": "character_purple_hit",
        "pos": (2 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_yellow_idle",
        "walk": ["character_yellow_walk_a", "character_yellow_walk_b"],
        "jump": "character_yellow_jump",
        "hit": "character_yellow_hit",
        "pos": (WIDTH/6, HEIGHT-128)
    },
]
characters = [Actor(data["idle"], pos=data["pos"]) for data in character_data]

alien = None
alien_idle = None
alien_walk_frames = []
alien_jump = None
alien_hit = None

char_walk_timer = 0.0
char_walk_interval = 0.12 
char_current_frame = 0

frog_walk_timer = 0.0
frog_walk_interval = 0.4 
frog_current_frame = 0

bee_fly_timer = 0.0
bee_fly_interval = 0.2
bee_current_frame = 0

flag_move_timer = 0.0
flag_move_interval = 0.8
flag_current_frame = 0

clouds = []
for x in range(5):
    cloud = Actor('background_clouds')
    cloud.x = x*256 + 128
    cloud.y = 256 + 128 -64 - 32

    clouds.append(cloud)

trees = [] 
for x in range(5):
    tree = Actor('background_color_trees')
    tree.x = x*256 + 128
    tree.y = 256*2 + 128 - 64 - 32
    
    trees.append(tree)
    
solidskyes = [] 
for x in range(5):
    solidsky = Actor('background_solid_sky')
    solidsky.x = x*256 + 128
    solidsky.y = 128 - 32 - 64
    
    solidskyes.append(solidsky)
    
floor = []
lava = []
for x in range(20):
    if 3 <= x <= 7:
        block = Actor('lava_top')
        lava.append(block)
    else:
        block = Actor("terrain_grass_block_top")
        floor.append(block)
    block.x = x*64 + 32
    block.y = 720-32

bottom_grasses = []
for x in range(20):
    bottom_grass = Actor('terrain_grass_block_top')
    bottom_grass.x = x*64 + 32
    bottom_grass.y = 720-32
    
    bottom_grasses.append(bottom_grass)

platforms = [
    Actor('terrain_grass_cloud_left', (32 + 64 * 4, HEIGHT-64*2)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 5, HEIGHT-64*2)),
    Actor('terrain_grass_cloud_right', (32 + 64 * 6, HEIGHT-64*2)),
    Actor('terrain_grass_cloud', (32 + 64 * 17, HEIGHT-64*2)),
    Actor('terrain_grass_cloud', (32 + 64 * 19, HEIGHT-64*4)),
    Actor('terrain_grass_cloud', (32 + 64 * 17, HEIGHT-64*6)),
    Actor('terrain_grass_cloud_left', (32 + 64 * 13, HEIGHT-64*6)),
    Actor('terrain_grass_cloud', (32 + 64 * 8, HEIGHT-64*6)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 5, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_right', (32 + 64 * 6, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_right', (32 + 64 * 15, HEIGHT-64*6)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 4, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 3, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_left', (32 + 64 * 2, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 14, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 12, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 11, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 10, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 9, HEIGHT-64*6)),
    Actor('terrain_grass_cloud', (32, HEIGHT - 64 * 9)),
]

decorations = [
    Actor('grass',(32+64*19, HEIGHT-64-32)),
    Actor('grass',(32+64*2, HEIGHT-64-32)),
    Actor('grass',(32+64*17, HEIGHT-64*3)),
    Actor('grass',(32+64*5, HEIGHT-64*8)),
    Actor('grass',(32+64*4, HEIGHT-64*3)),
    Actor('bush',(32+64,HEIGHT-64-32)),
    Actor('bush',(32+64*10,HEIGHT-64-32)),
    Actor('bush',(32+64*14,HEIGHT-64*7)),
    Actor('bush',(32+64*17,HEIGHT-64-32)),
]

traps = [
    Actor('saw',(32+64* 16, HEIGHT- 64*8)),
    Actor('spikes', (32+64 * 5, HEIGHT-64*3))
]


enemies_data = [{
    'idle_left' : 'frog_idle',
    'movement_1_left' : 'frog_jump',
    'movement_2_left' : 'frog_rest',
    'idle_right' : 'frog_idle_right',
    'movement_1_right' : 'frog_jump_right',
    'movement_2_right': 'frog_rest_right',
    'pos' : (0, HEIGHT - 128 + 32)
},
{
    'idle_left' : 'frog_idle',
    'movement_1_left' : 'frog_jump',
    'movement_2_left' : 'frog_rest',
    'idle_right' : 'frog_idle_right',
    'movement_1_right' : 'frog_jump_right',
    'movement_2_right': 'frog_rest_right',
    'pos' : (32+64*11, HEIGHT - 128 + 32)
},
{
    'idle_left' : 'frog_idle',
    'movement_1_left' : 'frog_jump',
    'movement_2_left' : 'frog_rest',
    'idle_right' : 'frog_idle_right',
    'movement_1_right' : 'frog_jump_right',
    'movement_2_right': 'frog_rest_right',
    'pos' : (32+64*4, HEIGHT - 128 - 64 * 6)
},
{
    'idle_left' : 'bee_rest',
    'movement_1_left' : 'bee_a',
    'movement_2_left' : 'bee_b',
    'idle_right' : 'bee_rest_right',
    'movement_1_right' : 'bee_a_right',
    'movement_2_right': 'bee_b_right',
    'pos' : (32+64*12, HEIGHT - 128 - 64 * 6)
}
    
]

frogs = []
bees = []

for data in enemies_data:
    if 'frog' in data['idle_left']:
        frog = Actor(data['idle_right'], pos=data['pos'])
        frog.speed = 2
        frog.direction = 1
        frog.right_limit = frog.x + 64 * 2
        frog.left_limit = frog.x - 64 * 2
        frog.frames_right = [data['movement_1_right'], data['movement_2_right'], data['idle_right']]
        frog.frames_left = [data['movement_1_left'], data['movement_2_left'], data['idle_left']]
        frogs.append(frog)
    elif 'bee' in data['idle_left']:
        bee = Actor(data['idle_right'], pos=data['pos'])
        bee.speed = 3
        bee.direction = 1
        bee.right_limit = bee.x + 64 * 3
        bee.left_limit = bee.x - 64 * 3
        bee.frames_right = [data['movement_1_right'], data['movement_2_right'], data['idle_right']]
        bee.frames_left = [data['movement_1_left'], data['movement_2_left'], data['idle_left']]
        bees.append(bee)

flag = Actor('flag_green_a', (48,HEIGHT - 64 *10))
flag.frames = ['flag_green_b','flag_green_a']
solids = floor + platforms

saw = traps[0]
saw.speed = 3
saw.direction = 1
saw.top_limit = HEIGHT - 64 * 7
saw.bottom_limit = HEIGHT - 64 * 2

def draw():
    screen.clear()
    if status == 'start':
        draw_start()
    elif status == 'selection':
        draw_selection()
    elif status == 'game':
        draw_game()
    
def draw_start():
    screen.fill((0,0,0))
    
    for cloud in clouds:
        cloud.draw()    
        
    for tree in trees:
        tree.draw()
        
    for solidsky in solidskyes:
        solidsky.draw()
    
    for bottom_grass in bottom_grasses:
        bottom_grass.draw()
    
    screen.draw.text('Nome Incrível', center=(WIDTH//2, HEIGHT//3), fontsize=60, color='darkblue')
    screen.draw.text('Click here or press SPACE to start', center=play_rect.center, fontsize=50, color="blue")
    screen.draw.text('Music ON/OFF', center=music_rect.center, fontsize=50, color='pink')
    screen.draw.text('Sounds ON/Off', center=sounds_rect.center, fontsize=50, color='purple')
    screen.draw.text('Exit game', center=exit_rect.center,fontsize=50, color='red')
    #screen.draw.rect(play_rect, (255,0,0))
    #screen.draw.rect(music_rect, (255,0,0))
    #screen.draw.rect(sounds_rect, (255,0,0))
    #screen.draw.rect(exit_rect, (255,0,0))
    
def draw_game():     
    screen.fill((0,0,0))
    
    for cloud in clouds:
        cloud.draw()    
        
    for tree in trees:
        tree.draw()
        
    for solidsky in solidskyes:
        solidsky.draw()
    
    for block in floor:
        block.draw()
        
    for s in solids:
        s.draw()
    
    for d in decorations:
        d.draw()
            
    alien.draw() 
    #alien_hitbox = Rect((alien.x-20, alien.y-20), (40,50)) 
    #screen.draw.rect(alien_hitbox, (255,0,0))  
      
    for l in lava:
        l.draw()
        #hitbox = Rect((l.x - l.width/2, l.y - l.height/2), (l.width, l.height))
        #screen.draw.rect(hitbox, (255,0,0))
        
    for f in frogs[1:]:
        f.draw()
        #frog_hitbox = Rect((f.x - 32, f.y - 32), (64,64))
        #screen.draw.rect(frog_hitbox, (255,0,0))
        
    for b in bees:
        b.draw()
        #bee_hitbox = Rect((b.x - 32, b.y - 16), (64,32))
        #screen.draw.rect(bee_hitbox, (255,0,0))
        
    for t in traps:
        t.draw()
        #trap_hitbox = Rect((t.x - 16, t.y - 16), (32,32))
        #screen.draw.rect(trap_hitbox, (255,0,0))
    
    flag.draw()
    
def draw_selection():
    screen.fill((0,0,0))
    
    for cloud in clouds:
        cloud.draw()    
        
    for tree in trees:
        tree.draw()
        
    for solidsky in solidskyes:
        solidsky.draw()
    
    for bottom_grass in bottom_grasses:
        bottom_grass.draw()
    
    screen.draw.text("Select your character", center=(WIDTH//2, 50), fontsize=40, color="red")
    for c in characters:
        c.draw()
    
    for frog in frogs[:1]:
        frog.draw()
    
def update(dt):
    global status, velocity_y, char_walk_timer, char_current_frame, frog_walk_timer, frog_current_frame, bee_fly_timer, bee_current_frame, flag_move_timer,flag_current_frame, flag, sounds_on

    # ----- TELA DE SELEÇÃO -----
    if status == 'selection':
        for c in characters:
            c.x += 1
            if c.x > WIDTH:
                c.x = 0

        for frog in frogs:
            frog.x += 1 
            if frog.x > WIDTH:
                frog.x = 0 
                
        char_walk_timer += dt
        frog_walk_timer += dt

        if char_walk_timer >= char_walk_interval:
            char_current_frame = (char_current_frame + 1) % 2
            for c in characters:
                if "beige" in c.image:
                    c.image = ["character_beige_walk_a", "character_beige_walk_b"][char_current_frame]
                elif "green" in c.image:
                    c.image = ["character_green_walk_a", "character_green_walk_b"][char_current_frame]
                elif "pink" in c.image:
                    c.image = ["character_pink_walk_a", "character_pink_walk_b"][char_current_frame]
                elif "purple" in c.image:
                    c.image = ["character_purple_walk_a", "character_purple_walk_b"][char_current_frame]
                elif "yellow" in c.image:
                    c.image = ["character_yellow_walk_a", "character_yellow_walk_b"][char_current_frame]
            
            char_walk_timer = 0.0

        if frog_walk_timer >= frog_walk_interval:
            frog_current_frame = (frog_current_frame + 1) % 3
            for frog in frogs:
                frog.image = ['frog_jump_right','frog_rest_right','frog_idle_right'][frog_current_frame]
            
            frog_walk_timer = 0.0
            
        if bee_fly_timer >= bee_fly_interval:
            bee_current_frame = (bee_current_frame + 1) % 3
            for bee in bees:
                bee.image = ['bee_a_right', 'bee_b_right', 'bee_rest_right'][bee_current_frame]
            bee_fly_timer = 0.0
            
        return

    # ----- JOGO -----
    if status != 'game' or not alien:
        return

    moved = False

    original_x = alien.x
    original_y = alien.y
    prev_bottom = original_y + (alien.height / 2)
    prev_top    = original_y - (alien.height / 2)

    if keyboard.a:
        alien.x -= 5
        moved = True
    if keyboard.d:
        alien.x += 5
        moved = True

    alien.y += velocity_y
    velocity_y += gravity

    on_ground = False
    solids = floor + platforms   
    feet = Rect((alien.x-10, alien.y + alien.height/2 - 5), (20,10))
    head = Rect((alien.x-20, alien.y-20), (40,50))
    
    if feet.colliderect(flag._rect):
        respawn()
        
    for block in solids:
        solids_hitbox = Rect((block.x - 32, block.y - 32), (64,64))
        if feet.colliderect(solids_hitbox):
            if velocity_y >= 0 and prev_bottom <= block.top:
                alien.y = block.top - alien.height / 2
                velocity_y = 0
                on_ground = True
            elif velocity_y < 0 and prev_top >= block.bottom:
                alien.y = block.bottom + alien.height / 2
                velocity_y = 0
            else:
                alien.x = original_x

    for block in lava:
        lava_hitbox = Rect((block.x - 32, block.y - 32), (64,64))
        if feet.colliderect(lava_hitbox):
                alien.image = alien_hit
                if velocity_y < 4:
                    velocity_y = 4
                set_dead()
    
    for t in traps:
        trap_hitbox = Rect((t.x - 16, t.y - 16), (32,32))
        if feet.colliderect(trap_hitbox) or head.colliderect(trap_hitbox):
            alien.image = alien_hit
            set_dead()
            
    for f in frogs[1:]:
        frog_hitbox = Rect((f.x - 32, f.y - 32), (64,32))
        if feet.colliderect(frog_hitbox) or head.colliderect(frog_hitbox):
            alien.image = alien_hit
            set_dead()
            
    for b in bees:
        bee_hitbox = Rect((b.x - 32, b.y - 32), (64,32))
        if feet.colliderect(bee_hitbox) or head.colliderect(bee_hitbox):
            alien.image = alien_hit
            set_dead()

    if alien.x < 0:
        alien.x = 0
    if alien.x > WIDTH:
        alien.x = WIDTH

    if keyboard.space and on_ground:
        velocity_y = -18
        alien.image = alien_jump
        if sounds_on == True:
            sounds.sfx_jump.play()
        

    if on_ground:
        if keyboard.a or keyboard.d:
            char_walk_timer += dt
            if char_walk_timer >= char_walk_interval:
                animate_walk()
                char_walk_timer = 0.0
        else:
            alien.image = alien_idle
            char_walk_timer = 0.0
    else:
        if velocity_y < 0:
            alien.image = alien_jump
            
        else:
            alien.image = alien_idle
            
    saw.y += saw.speed * saw.direction

    if saw.y <= saw.top_limit:
        saw.direction = 1 
    elif saw.y >= saw.bottom_limit:
        saw.direction = -1 

    for frog in frogs[1:]:
        if frog.direction == 1: 
            frog.x += frog.speed
            if frog.x >= frog.right_limit:
                frog.direction = -1 
        elif frog.direction == -1: 
            frog.x -= frog.speed
            if frog.x <= frog.left_limit:
                frog.direction = 1 
                
    for bee in bees:
        if bee.direction == 1:
            bee.x += bee.speed
            if bee.x >= bee.right_limit:
                bee.direction = -1
        elif bee.direction == -1:
            bee.x -= bee.speed
            if bee.x <= bee.left_limit:
                bee.direction = 1

    frog_walk_timer += dt
    if frog_walk_timer >= frog_walk_interval:
        frog_current_frame = (frog_current_frame + 1) % 3
        for frog in frogs:
            if frog.direction == 1:
                frog.image = frog.frames_right[frog_current_frame]
            else:
                frog.image = frog.frames_left[frog_current_frame]
        frog_walk_timer = 0.0

    bee_fly_timer += dt
    if bee_fly_timer >= bee_fly_interval:
        bee_current_frame = (bee_current_frame + 1) % 3
        for bee in bees:
            if bee.direction == 1:
                bee.image = bee.frames_right[bee_current_frame]
            else:
                bee.image = bee.frames_left[bee_current_frame]
        bee_fly_timer = 0.0
        
    flag_move_timer += dt
    if flag_move_timer >= flag_move_interval:
        flag_current_frame = (flag_current_frame +1) % 2
        for flag in platforms[20:21]:
            flag.image = flag.frames[flag_current_frame]
        flag_move_timer = 0.0    
        

def on_key_down(key):
    global status,music_started
    if status == 'start' and key == keys.SPACE:
        sounds.sfx_select.play()
        status = 'selection'
        if not music_started and music_on:
            music.play('energy')
            music_started = True
        
def on_mouse_down(pos):
    global alien, status, alien_idle, alien_walk_frames, alien_jump, alien_hit, music_on, music_started, sounds_on
    if status == 'start':
        
        if play_rect.collidepoint(pos):
            if sounds_on:
                sounds.sfx_select.play()
            status = 'selection'
            if not music_started and music_on:
                music.play('energy')
                music_started = True
                
        if music_rect.collidepoint(pos): 
            if sounds_on:
                sounds.sfx_select.play()
            if music.is_playing('energy'):
                music.stop()
                music_on = False  
            else:
                music.play('energy')
                music_on = True
                
        if sounds_rect.collidepoint(pos):
            sounds_on = not sounds_on
            if sounds_on:
                sounds.sfx_select.play() 
        
        if exit_rect.collidepoint(pos):
            if sounds_on:
                sounds.sfx_select.play()
            exit()
            
    if status == 'selection':
        for i, c in enumerate(characters):
            if c.collidepoint(pos):
                data = character_data[i]
                alien = Actor(data["idle"])
                alien.pos = (128 , HEIGHT-128)
                alien_idle = data["idle"]
                alien_walk_frames = data["walk"]
                alien_jump = data["jump"]
                alien_hit = data["hit"]
                if sounds_on:
                    sounds.sfx_hurt.play()
                else:
                    pass

                clock.schedule_unique(start_game, 1.0)
                
        


def start_game():
    global status
    status ='game'
                     

def set_alien_normal():
    alien.image = alien_idle
    
def animate_walk():
    global char_current_frame
    alien.image = alien_walk_frames[char_current_frame]
    char_current_frame = (char_current_frame + 1) % len(alien_walk_frames)
    
def set_dead():
    global status
    alien.image = alien_hit
    sounds.sfx_hurt.play()
    status = "dead"
    clock.schedule_unique(respawn, 2.0)

def respawn():
    global status
    alien.pos = (100, HEIGHT - 128)
    alien.image = alien_idle
    status = "game"
    
pgzrun.go()