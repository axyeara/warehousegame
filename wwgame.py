import sys, pygame, random, time
from threading import Timer
from ww import *
from pygame.locals import *



pygame.init()

ww=Stage(20, 20, 24)

def setup():
    '''
    Initializes the setup of the game, adding your player, monsters, walls,  sticky boxes and normal boxes across the stage.
    '''
    ww.set_player(KeyboardPlayer("icons/playerright.png", ww))
    ww.add_actor(Monster("icons/monster.png", ww, 7, 4, 5))
    ww.add_actor(Monster("icons/monster.png", ww, 4, 10, 3))
    ww.add_actor(Monster("icons/monster.png", ww, 5, 20, 2))

    for monster in range(random.randint(1, 2)):
        x = random.randrange(ww.get_width())
        y = random.randrange(ww.get_height())
        if ww.get_actor(x, y) is None:
            ww.add_actor(FreeMonster("icons/jedi.png", ww, x, y, 5))
    for monster in range(random.randint(1, 2)):
        x = random.randrange(ww.get_width())
        y = random.randrange(ww.get_height())
        if ww.get_actor(x, y) is None:
            ww.add_actor(BoxMonster("icons/skeleton.png", ww, x, y, 5))
    x = random.randrange(ww.get_width())
    y = random.randrange(ww.get_height())
    if ww.get_actor(x, y) is None:
        ww.add_actor(Boss("icons/boss2.png", ww, x, y, 2))

    for ripper in range(3):
        x = random.randrange(ww.get_width())
        y = random.randrange(ww.get_height())
        if ww.get_actor(x, y) is None:
            ww.add_actor(Ripper("icons/reaperr.png", ww, x, y, 8))

    for wall in range(25):
        x = random.randrange(ww.get_width())
        y = random.randrange(ww.get_height())
        if ww.get_actor(x,y) is None:
            ww.add_actor(Wall("icons/Tree.png", ww, x, y))

    for stickybox in range(5):
        x = random.randrange(ww.get_width())
        y = random.randrange(ww.get_height())
        if ww.get_actor(x, y) is None:
            ww.add_actor(StickyBox("icons/application-rpm.png", ww, x, y))

    num_boxes=0
    while num_boxes<100:
        x=random.randrange(ww.get_width())
        y=random.randrange(ww.get_height())
        if ww.get_actor(x,y) is None:
            ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y))
            num_boxes+=1

def main():
    '''
    This is the main game loop. It takes into account the state variables of the game (start, restart, exit and menu).
    '''
    while ww.exit == False:
        if ww.restart == False:
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                        ww.player_event(event.key)
            ww.step()
            for actor in ww._actors:
                if isinstance(actor, BoxMonster):
                    actor.camouflage()  #For BoxMonsters, the camouflage method is ran in conjunction with the pygame time module.
                if isinstance(actor, Boss):
                    actor.animate()  #Runs animation for Boss in the stage in conjunction with the pygame time module.
            ww.draw()
        else:  #After pressing "t", restart is enabled and conditions of the game are restarted.
            ww.restart = False
            ww._monsters.clear()
            ww._actors.clear()

            setup()

def start_game():
    ''' Function that initiates the game by running the setup and main game loop'''
    setup()
    main()

start_game() # Runs the game!!