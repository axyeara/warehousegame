import pygame, time, random
from threading import Timer

class Actor:
    '''
    Represents an Actor in the game. Can be the Player, a Monster, boxes, wall.
    Any object in the game's grid that appears on the stage, and has an
    x- and y-coordinate.
    '''
    
    def __init__(self, icon_file, stage, x, y, delay=5):
        '''
        (Actor, str, Stage, int, int, int) -> None
        Given the name of an icon file (with the image for this Actor),
        the stage on which this Actor should appear, the x- and y-coordinates
        that it should appear on, and the speed with which it should
        update, construct an Actor object.
        '''
        
        self._icon = pygame.image.load(icon_file) # the image image to display of self
        self.set_position(x, y) # self's location on the stage
        self._stage = stage # the stage that self is on

        # the following can be used to change this Actors 'speed' relative to other
        # actors speed. See the delay method.
        self._delay = delay
        self._delay_count = 0
    
    def set_position(self, x, y):
        '''
        (Actor, int, int) -> None
        Set the position of this Actor to the given x- and y-coordinates.
        '''
        
        (self._x, self._y) = (x, y)

    def get_position(self):
        '''
        (Actor) -> tuple of two ints
        Return this Actor's x and y coordinates as a tuple.
        '''
        
        return (self._x, self._y)

    def get_icon(self):
        '''
        (Actor) -> pygame.Surface
        Return the image associated with this Actor.
        '''
        
        return self._icon

    def is_dead(self):
        '''
        (Actor) -> bool
        Return True iff this Actor is not alive.
        '''
        
        return False

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool

        Other is an Actor telling us to move in direction (dx, dy). In this case, we just move.
        (dx,dy) is in {(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,1), (-1,0), (-1,-1)}
    
        In the more general case, in subclasses, self will determine 
        if they will listen to other, and if so, will try to move in
        the specified direction. If the target space is occupied, then we 
        may have to ask the occupier to move.
        '''

        self.set_position(self._x + dx, self._y + dy)
        return True

    def delay(self):
        '''
        (Actor) -> bool
        Manage self's speed relative to other Actors. 
        Each time we get a chance to take a step, we delay. If our count wraps around to 0
        then we actually do something. Otherwise, we simply return from the step method.
        '''

        self._delay_count = (self._delay_count+1) % self._delay
        return self._delay_count == 0

    def step(self):
        '''
        (Actor) -> None
        Make the Actor take a single step in the animation of the game.
        self can ask the stage to help as well as ask other Actors
        to help us get our job done.
        '''

        pass

class Player(Actor):
    '''
    A Player is an Actor that can handle events. These typically come
    from the user, for example, key presses etc.
    '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Player, str, Stage, int, int) -> None
        Construct a Player with given image, on the given stage, at
        x- and y- position.
        '''
        
        Actor.__init__(self, icon_file, stage, x, y)
    
    def handle_event(self, event):
        '''
        Used to register the occurrence of an event with self.
        '''
        
        pass

class KeyboardPlayer(Player):
    '''
    A KeyboardPlayer is a Player that can handle keypress events.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        Construct a KeyboardPlayer. Other than the given Player information,
        a KeyboardPlayer also keeps track of the last key event that took place.
        '''
        
        Player.__init__(self, icon_file, stage, x, y)

        self._last_event = None # we are only interested in the last event
        self.dead = False

    
    def handle_event(self, event):
        '''
        (KeyboardPlayer, int) -> None
        Record the last event directed at this KeyboardPlayer.
        All previous events are ignored.
        '''

        self._last_event = event

    def step(self):
        '''
        (KeyboardPlayer) -> None
        Take a single step in the animation. 
        For example: if the user asked us to move right, then we do that.
        This also includes diagonal movement and the start, restart, exit and main menu inputs.
        '''
        keys = pygame.key.get_pressed()
        if self._last_event is not None:
            dx, dy = None, None
            if self._last_event == pygame.K_RIGHT:
                dx, dy = 1, 0
                self._icon = pygame.image.load("icons/playerright.png")
            if self._last_event == pygame.K_DOWN:
                dx, dy = 0, 1
            if self._last_event == pygame.K_UP:
                dx, dy = 0, -1
            if self._last_event == pygame.K_LEFT:
                dx, dy = -1, 0
                self._icon = pygame.image.load("icons/playerleft.png")
            if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:  #this allows player to input two keys at the same time
                dx, dy = 1,1
                self._icon = pygame.image.load("icons/playerright.png")
            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                dx, dy = 1, -1
                self._icon = pygame.image.load("icons/playerright.png")
            if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                dx, dy = -1, 1
                self._icon = pygame.image.load("icons/playerleft.png")
            if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                dx, dy = -1,-1
                self._icon = pygame.image.load("icons/playerleft.png")
            if self._last_event == pygame.K_t:          #this allows the player to start, restart, exit and access main menu of the game
                self._stage.restart = True              #by pressing s, t, x, m, respectively.
            if self._last_event == pygame.K_x:
                self._stage.exit = True
            if self._last_event == pygame.K_s:
                self._stage.start = True
            if self._last_event == pygame.K_m:
                self._stage.start = False
                self._stage.restart = True
            if dx is not None and dy is not None:
                self.move(self, dx, dy) # we are asking ourself to move





            self._last_event = None

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        # Where we are supposed to move. 
        new_x = self._x + dx
        new_y = self._y + dy

        if self._stage.is_in_bounds(new_x, new_y):
            if not self._stage.get_actor(new_x, new_y):
                Actor.move(self, other, dx, dy)
                return True
            if self._stage.get_actor(new_x, new_y) and not isinstance(self._stage.get_actor(new_x, new_y), Wall):
                self._stage.get_actor(new_x, new_y).move(self,dx,dy)
                if not self._stage.get_actor(new_x, new_y):
                    Actor.move(self,other,dx,dy)
                    return True
            if self._stage.get_actor(new_x, new_y) and isinstance(self._stage.get_actor(new_x, new_y), Monster):
                self.dead = True      # This assignment "kills" the player, whose values is later used to display the game_over text.
                return True

        return False

class Box(Actor):
    '''
    A Box Actor. This can be used to surround monsters to kill them. Can be pushed by a Player and other Box objects.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        '''
        
        Actor.__init__(self, icon_file, stage, x, y)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        new_x = self._x + dx
        new_y = self._y + dy

        if self._stage.is_in_bounds(new_x, new_y):
            if not self._stage.get_actor(new_x, new_y):
                Actor.move(self,other, dx, dy)
                return True
            elif self._stage.get_actor(new_x, new_y) and not isinstance(self._stage.get_actor(new_x, new_y), Wall):
                self._stage.get_actor(new_x, new_y).move(self,dx,dy) # when actor is moved, it checks again if there is another actor.
                if not self._stage.get_actor(new_x, new_y):          #if there is no actor, it moves to it's position.
                    Actor.move(self, other, dx, dy)                  #this avoids stacking of items onto one position
        return False                                                 #and allows movement of objects using other objects.

class StickyBox(Box):
    '''
    A StickyBox Actor. Can be used to surround monster to kill them. It can also "paralyze" monsters that are next to this box.
    Can be pushed by a Player and other Box objects.
    '''
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Constructs a StickyBox on the given stage, at given positions
        '''
        Box.__init__(self, icon_file, stage, x, y)

class Wall(Actor):
    '''
    A Wall actor. This object has no movement in the game. You can surround monsters with these objects to kill them.
    '''
    def __init__(self, icon_file, stage, x, y):
        '''
        (Player, str, Stage, int, int) -> None
        Construct a wall with given image, on the given stage, at
        x- and y- position.
        '''

        Actor.__init__(self, icon_file, stage, x, y)
    
class Stage:
    '''
    A Stage that holds all the game's Actors (Player, monsters, boxes, etc.).
    '''
    
    def __init__(self, width, height, icon_dimension):
        '''Construct a Stage with the given dimensions.'''
        
        self._actors = [] # all actors on this stage (monsters, player, boxes, ...)
        self._player = None # a special actor, the player
        self._monsters = []  #new variable that stores all the monsters in the Stage.

        # the logical width and height of the stage
        self._width, self._height = width, height

        self._icon_dimension=icon_dimension # the pixel dimension of all actors
        # the pixel dimensions of the whole stage
        self._pixel_width = self._icon_dimension * self._width
        self._pixel_height = self._icon_dimension * self._height
        self._pixel_size = self._pixel_width, self._pixel_height

        # get a screen of the appropriate dimension to draw on
        self._screen = pygame.display.set_mode(self._pixel_size)

       # variables that assign the state of the game (whether it has exited, restarted or started.
        self.exit = False
        self.restart = False
        self.start = False




    def is_in_bounds(self, x, y):
        '''
        (Stage, int, int) -> bool
        Return True iff the position (x, y) falls within the dimensions of this Stage.'''
        
        return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

    def is_in_bounds_x(self, x):
        '''
        (Stage, int) -> bool
        Return True iff the x-coordinate given falls within the width of this Stage.
        '''
        
        return 0 <= x and x < self._width

    def is_in_bounds_y(self, y):
        '''
        (Stage, int) -> bool
        Return True iff the y-coordinate given falls within the height of this Stage.
        '''

        return 0 <= y and y < self._height

    def get_width(self):
        '''
        (Stage) -> int
        Return width of Stage.
        '''

        return self._width

    def get_height(self):
        '''
        (Stage) -> int
        Return height of Stage.
        '''
        
        return self._height

    def set_player(self, player):
        '''
        (Stage, Player) -> None
        A Player is a special actor, store a reference to this Player in the attribute
        self._player, and add the Player to the list of Actors.
        '''

        self._player=player
        self.add_actor(self._player)

    def remove_player(self):
        '''
        (Stage) -> None
        Remove the Player from the Stage.
        '''
        
        self.remove_actor(self._player)
        self._player=None

    def player_event(self, event):
        '''
        (Stage, int) -> None
        Send a user event to the player (this is a special Actor).
        '''
        
        self._player.handle_event(event)



    def add_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Add the given actor to the Stage.
        '''
        if isinstance(actor, Monster):
            self._monsters.append(actor)
            self._actors.append(actor)
        else:
            self._actors.append(actor)

    def remove_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Remove the given actor from the Stage.
        '''
        if isinstance(actor, Monster):
            self._monsters.remove(actor)
            self._actors.remove(actor)
        else:
            self._actors.remove(actor)

    def step(self):
        '''
        (Stage) -> None
        Take one step in the animation of the game. 
        Do this by asking each of the actors on this Stage to take a single step.
        '''

        for a in self._actors:
            a.step()

    def get_actors(self):
        '''
        (Stage) -> None
        Return the list of Actors on this Stage.
        '''
        
        return self._actors

    def get_actor(self, x, y):
        '''
        (Stage, int, int) -> Actor or None
        Return the first actor at coordinates (x,y).
        Or, return None if there is no Actor in that position.
        '''
        
        for a in self._actors:
            if a.get_position() == (x,y):
                return a
        return None

    def draw(self):
        '''
        (Stage) -> None
        Draw all Actors that are part of this Stage to the screen.
        '''



        self._screen.fill((255,255,255)) # (0,0,0)=(r,g,b)=black
        for a in self._actors:
            icon = a.get_icon()
            (x,y) = a.get_position()
            d = self._icon_dimension
            rect = pygame.Rect(x*d, y*d, d, d)
            self._screen.blit(icon, rect)

        # Displays the game over screen is player is dead.

        if self._player.dead == True:
            self._actors = [self._player]
            self._screen.fill((0,0,0))
            self.game_over_text()

        # Displays the winning screen if all monsters are dead.

        if len(self._monsters) == 0:
            self._actors = [self._player]
            self._player._icon = pygame.image.load("icons/playerwon.png")
            self.you_won_text()

        # Displays main menu if game has not started.

        if self.start == False:
            player_img = pygame.image.load("icons/mainmenu/walkman2.png")
            monster1_img = pygame.image.load("icons/mainmenu/skeleton.png")
            monster2_img = pygame.image.load("icons/mainmenu/boss1.png")
            monster3_img = pygame.image.load("icons/mainmenu/jedi.png")
            monster4_img = pygame.image.load("icons/mainmenu/monster.png")
            tree_img = pygame.image.load("icons/mainmenu/tree.png")
            box_img = pygame.image.load("icons/mainmenu/emblem-package-2-24.png")
            stickybox_img = pygame.image.load("icons/mainmenu/application-rpm.png")
            self._screen.fill((255, 255, 255))
            self._screen.blit(monster1_img, (250, 350))
            self._screen.blit(monster2_img, (40, 350))
            self._screen.blit(monster3_img, (135, 350))
            self._screen.blit(monster4_img, (350, 350))
            self._screen.blit(player_img, (200, 40))
            self._screen.blit(tree_img, (40,40))
            self._screen.blit(tree_img, (350, 40))
            self._screen.blit(box_img, (10, 180))
            self._screen.blit(stickybox_img, (365, 180))
            self.game_start_text()

        # Displays title of game at top of the window

        pygame.display.set_caption("Game - Warehouse Game on Steroids")
        pygame.display.flip()

    def monster_died(self):
        '''
        (Stage) -> None
        Displays text when a monster is killed
        '''

        text_font = pygame.font.Font("freesansbold.ttf", 20)
        text_surface = text_font.render("You killed a monster!", True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (self._pixel_width // 2, self._pixel_height // 2 - 100 )
        self._screen.blit(text_surface, text_rect)
        pygame.display.flip()
        time.sleep(1)

    def game_over_text(self):

        '''
        (Stage) -> None
        Displays text when the player dies (game over).
        '''

        text = ["Game Over!", "Press T to try again", "Press X to quit the game", "Press M for the main menu"]
        centerw = self._pixel_width // 2
        centery = self._pixel_height // 2

        for line in text:   #loop to iterate over all lines of the list in variable text for individual display.
            text_font = pygame.font.Font("freesansbold.ttf", 20)
            text_surface = text_font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (centerw, centery - 50)
            self._screen.blit(text_surface, text_rect)
            centery += 50  #at each iteration, each line of text occurs at 50 units lower than the previous.

    def you_won_text(self):
        '''
        (Stage) -> None
        Displays the winning text after killing all monsters.
        '''

        text = ["You won!", "Press T to play again", "Press X to quit the game"]
        centerw = self._pixel_width // 2
        centery = self._pixel_height // 2

        for line in text:
            text_font = pygame.font.Font("freesansbold.ttf", 20)
            text_surface = text_font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (centerw, centery - 50)
            self._screen.blit(text_surface, text_rect)
            centery += 50

    def clear(self):
        '''
        (Stage) -> None
        Deletes all the actors in the stage.
        '''
        self._actors.clear()

    def game_start_text(self):
        '''
        (Stage) -> None
        Displays text in the main menu of the game.
        '''

        text = ["Welcome to my game!", "Press S to start the game!", " ", "Please read the readme.txt file for instructions!"]

        centerw = self._pixel_width // 2
        centery = self._pixel_height // 2

        for line in text:
            text_font = pygame.font.Font("freesansbold.ttf", 15)
            text_surface = text_font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (centerw, centery - 80)
            self._screen.blit(text_surface, text_rect)
            centery += 50

class Monster(Actor):
    '''A Monster class.'''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster on a given stage, at given position.
        '''
        Actor.__init__(self, icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def step(self):
        '''
        (Actor) -> Bool
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        if not self.is_dead() and not self.is_stuck():
            if not self.delay(): return
            self.move(self, self._dx, self._dy)
            return True

        if self.is_stuck() and not self.is_dead():
            return True


        else:
            self._stage.remove_actor(self)
            time.sleep(0.01)
            self._stage.monster_died()
            return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy
        actor = self._stage.get_actor(new_x, new_y)


        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True
        if actor and not isinstance(actor, KeyboardPlayer ):
            self._dx = - self._dx
            self._dy =  - self._dy
            return True
        if actor and isinstance(actor, KeyboardPlayer):
            self._dx = - self._dx
            self._dy = - self._dy
            actor.dead = True
            return True




        if bounce_off_edge:
            return False

        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: Use actor = self._stage.get_actor(new_x,new_y)
        # YOUR CODE HERE




        return Actor.move(self,other, dx, dy)

    def is_dead(self):
        '''
        (Actor) -> Bool
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''

        # This method is done using a fairly simple algorithm. A list is made of all the positions that surround
        # a Monster by adding the current position to all the possible moves that Monster can take, given 8 possible
        # positions.

        value = True
        moves = [(1,0),(-1,0),(0,1),(0,-1), (1,1),(-1,1),(1,-1),(-1,-1)]
        surrounding_pos = [(self.get_position()[0] + x, self.get_position()[1] + y) for x, y in moves]
        for position in surrounding_pos:
            if (self._stage.get_actor(position[0], position[1]) == None or isinstance(self._stage.get_actor(position[0], position[1]), KeyboardPlayer)) and self._stage.is_in_bounds(position[0],position[1]):
                return False
            else:
                value = True
        return value

    def is_stuck(self):
        '''
        (Actor) -> Bool
        Returns whether this Monster is stuck. That is, if the Monster is next to a StickyBox in atleast one of
        the four possible positions.
        '''

        # This method is similar to the is_dead method. This case, if in one of the four non-diagonal positions
        #there lies a StickyBox, then the returns True.

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        surrounding_pos = [(self.get_position()[0] + x, self.get_position()[1] + y) for x, y in moves]
        for position in surrounding_pos:
            if isinstance(self._stage.get_actor(position[0], position[1]), StickyBox) and not isinstance(self, Boss):
                return True
        return False

class FreeMonster(Monster):

    '''
    A Monster that is able to move at random directions.
    '''
    def __init__(self, icon_file, stage, x = 0, y = 0 , delay = 5):
        '''
        Constructs a FreeMonster on a given stage, at given position.
        '''
        Monster.__init__(self, icon_file, stage, x, y, delay)

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        if not self.is_dead() and not self.is_stuck():
            if not self.delay(): return
            self.move(self, random.choice([-1,0,1]), random.choice([-1,0,1])) #Selects random dx, dy values for random movement.
            return True
        if self.is_stuck() and not self.is_dead():
            return True
        else:
            self._stage.remove_actor(self)
            time.sleep(0.01)
            self._stage.monster_died()

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        new_x = self._x + dx
        new_y = self._y + dy
        actor = self._stage.get_actor(new_x, new_y)

        if not self._stage.is_in_bounds(new_x, new_y):
            self.step()
            return True
        if actor and not isinstance(actor, KeyboardPlayer):
            self.step()
            return True
        if actor and isinstance(actor, KeyboardPlayer):
            actor.dead = True
            return True

        return Actor.move(self, other, dx, dy)

class BoxMonster(FreeMonster):

    '''
    A BoxMonster Class. Type of Monster that is able to transform into a box for 5 seconds.
    '''

    def __init__(self, icon_file, stage, x = 0, y = 0, delay = 5):
        '''
        Constructs a BoxMonster on a given stage, at given position.
        '''

        Monster.__init__(self, icon_file, stage, x, y, delay)
        self.camouflage()


    def camouflage(self):
        '''
        (Actor) -> None
        This method changes the icon of BoxMonster every second for 5 seconds.
        '''

        # This is done using time module in pygame. The get_ticks() function keeps track of the seconds during the main
        #game loop.

        if (round(pygame.time.get_ticks() / 1000)) % 5 == 0:
            self.icon = pygame.image.load("icons/skeleton.png")

        else:
            self.icon = pygame.image.load("icons/emblem-package-2-24.png")

    def get_icon(self):
        '''
        (Actor) -> Img
        returns the icon of the BoxMonster object.
        '''
        return self.icon

class Boss(BoxMonster):
    '''
    Boss class. Stronger Monster that moves faster than other monsters and is not "paralyzed" by StickyBox
    '''
    def __init__(self, icon_file, stage, x = 0, y = 0, delay = 1):
        '''
        Constructs a Boss object on a given stage, at given position.
        '''

        Monster.__init__(self, icon_file, stage, x, y, delay)
        self.camouflage()


    def animate(self):
        '''
        (Actor) -> None
        Changes the icon of a Boss every second.
        '''
        if (round(pygame.time.get_ticks() / 1000)) % 2 == 0:
            self.icon = pygame.image.load("icons/boss1.png")

        else:
            self.icon = pygame.image.load("icons/boss2.png")

class Ripper(FreeMonster):
    '''
        A Monster that is able to move at random directions. It destroys some StickyBoxes once dead.
        '''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''
        Constructs a Ripper on a given stage, at given position.
        '''
        FreeMonster.__init__(self, icon_file, stage, x, y, delay)

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        if not self.is_dead() and not self.is_stuck():
            if not self.delay(): return
            self.move(self, random.choice([-1, 0, 1]),
                      random.choice([-1, 0, 1]))  # Selects random dx, dy values for random movement.
            return True
        if self.is_stuck() and not self.is_dead():
            return True
        else:
            self._stage.remove_actor(self)
            time.sleep(0.01)
            self._stage.monster_died()
            for actor in self._stage._actors:
                if isinstance(actor, StickyBox):
                    self._stage.remove_actor(actor)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        new_x = self._x + dx
        new_y = self._y + dy
        actor = self._stage.get_actor(new_x, new_y)

        if not self._stage.is_in_bounds(new_x, new_y):
            self.step()
            return True
        if actor and not isinstance(actor, KeyboardPlayer):
            self.step()
            return True
        if actor and isinstance(actor, KeyboardPlayer):
            actor.dead = True
            return True

        return Actor.move(self, other, dx, dy)




