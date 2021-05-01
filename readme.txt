GAME - Warehouse Game on Steroids

INSTRUCTIONS

The objective of the game is to kill all monsters by surrounding them with boxes (normal/sticky), stage walls, trees
or other monsters. If you die, it will be game over!

CONTROLLERS

The character is moved in all directions (including diagonal movements)

right - right arrow key
left - left arrow key
up - up arrow key
down - down arrow key
top right - right arrow key + up arrow key
top left - left arrow key + up arrow key
bottom right - right arrow key + down arrow key
bottom left - left arrow key + down arrow key

MONSTERS

There are four types of monsters in this game. Each monster has their own class and
Each inherit from one another (refer to code to check the inheritance for monsters class).

normal monsters: this move diagonally at different speeds. If the monster reaches a box, it will bounce to the opposite
direction. If it reaches the walls of the stage, it will bounce as well but it's direction won't be reversed.

free monsters: these monsters can roam at random directions, can bounce when reaches a box or walls of the stage

box monsters: These monsters are very tricky. For approximately 5 seconds, they transform into a box. They only
go back to their normal selves for 1 second. Be careful!

Boss: this monster can also roam at random directions but at much higher speed than the rest of the monster. Note
that this monster is animated in the game with impressive sword swings.

Ripper: These monster are able to move at random directions. One special characteristic is that once they are dead
sticky boxes are removed from the stage, making the game harder!

BOXES

There are two types of boxes in this game. Each type of boxes have their own classes 
And sticky boxes inherits from boxes class (refer to code).

normal boxes: this boxes are pushed on every direction. These are used to kill the monsters.

sticky boxes: this boxes are pushed on every direction as well. However, everytime a monster gets next to these boxes,
the monster is paralyzed and won't be able to move unless the sticky box is moved away from the position next to the monster.
You won't be able to paralyze a monster diagonally (It would make more sense if the higher the surface area, the higher
the "stickiness" :p.

WALLS

Besides the stage walls, the trees in game act like “walls”. They won't move at all and no object can pass through it. It can be used
to surround monsters as well. A class was created for this (refer to code).

ENHANCEMENTS

- Added a main screen for introduction to the game. This includes a caption at top of the window, text and images
of all the characters in the game for decoration.

- Added different icons to all the actors in the game for better looks, as well as animating one of the monsters.

- The player is also “animated”, which shows the direction by which the player is moving (to the right, body faces that way).

- Everytime a monster dies, a text is displayed indicating that you killed it. If all monsters die, another screen
is displayed indicating the you have won the game, and that you may either play again or go back to the main menu.

-If a player dies, a black screen along with some text indicating that you could either try the game again or go back to the
main menu

- I added a "repeat" feature. If a player is stuck or you just want to play again, pressing "T" will reset the stage. Note that
the number of monsters in the stage might change (including their ratio) and the locations of all the other objects
will probably change as well.

- Added an additional monster (refer to MONSTERS section).

- tried to add music but it’s almost impossible. Sorry.

REFERENCES

 http://inventwithpython.com/pygame/chapter2.html
 https://www.pygame.org/docs/ref/key.html
 Open Source Icons, The Open Icon Library
 ** Icons used in this game are mostly acquired from pixilart.com, which are used as templates!




