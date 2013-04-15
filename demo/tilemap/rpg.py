#!/usr/bin/env python

import sys
import os

# Make sure that our diamond engine can be found.
sys.path.insert(0, os.path.abspath('../../'))

from pygame.locals import KEYDOWN, KEYUP, K_UP, K_DOWN, K_LEFT, K_RIGHT

from diamond.scene import SceneManager, Scene
from diamond.tilemap import LayeredTileMap
from diamond.transition import TransitionManager
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.sprite import Sprite
from diamond.fps import Fps
from diamond import event

import rpg_tilemap_layers
import rpg_chars


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'framerate': 60,
    # 'scaling': 1.5,  # 1.0 is normal; 2.0 would be double window size.
}


class Player(Sprite):

    def __init__(self, *args, **kwargs):
        self.__listeners = []
        super(Player, self).__init__(*args, **kwargs)

    def set_controls(self, scene, move_up, move_down, move_left, move_right):
        self.move_up = move_up
        self.move_down = move_down
        self.move_left = move_left
        self.move_right = move_right
        event.remove_listeners(self.__listeners)
        self.__listeners = [
            event.add_listener(self.__on_move_up_event, 'scene.event.system',
                               context__scene__is=scene,
                               context__event__type__eq=KEYDOWN,
                               context__event__key__eq=K_UP),
            event.add_listener(self.__on_move_down_event, 'scene.event.system',
                               context__scene__is=scene,
                               context__event__type__eq=KEYDOWN,
                               context__event__key__eq=K_DOWN),
            event.add_listener(self.__on_move_left_event, 'scene.event.system',
                               context__scene__is=scene,
                               context__event__type__eq=KEYDOWN,
                               context__event__key__eq=K_LEFT),
            event.add_listener(self.__on_move_right_event, 'scene.event.system',
                               context__scene__is=scene,
                               context__event__type__eq=KEYDOWN,
                               context__event__key__eq=K_RIGHT),

            event.add_listener(self.__on_move_stopped_event, 'scene.event.system',
                               context__scene__is=scene,
                               context__event__type__eq=KEYUP),
        ]

    def __del__(self):
        event.remove_listeners(self.__listeners)
        super(Player, self).__del__()

    def __on_move_up_event(self, context):
        if self.action == 'none':
            self.set_action('move_up')

    def __on_move_down_event(self, context):
        if self.action == 'none':
            self.set_action('move_down')

    def __on_move_left_event(self, context):
        if self.action == 'none':
            self.set_action('move_left')

    def __on_move_right_event(self, context):
        if self.action == 'none':
            self.set_action('move_right')

    def __on_move_stopped_event(self, context):
        self.set_action('none')

    def tick(self):
        if self.action == 'move_up':
            self.set_pos_rel(0, -2)
        elif self.action == 'move_down':
            self.set_pos_rel(0, 2)
        elif self.action == 'move_left':
            self.set_pos_rel(-2, 0)
        elif self.action == 'move_right':
            self.set_pos_rel(2, 0)


class RpgScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.add_to(self.root_node)
        fps = Fps(ticker=self.ticker, details=True)
        fps.set_alpha(75)
        fps.add_to(fps_node)
        fps.set_align_box(DISPLAY_LAYOUT['screen_size'][0], 0, 'right')
        fps_node.set_order_pos(10)

    def setup(self):
        super(RpgScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.transition_manager = TransitionManager()
        self.bind(self.ticker, self.transition_manager)
        self.__setup_fps()

        layered_map = LayeredTileMap()
        layered_map.load_layers(rpg_tilemap_layers.layers)
        layered_map.build_maps()
        layered_map.add_to(self.root_node)

        # Get empty layer for player character.
        layer = layered_map.get_layer(-2)

        char_node = Node('chars')
        char_node.add_to(layered_map)
        player = Player.make(rpg_chars, 'minotaur')
        player.pos = 7 * 32, 8 * 32
        player.add_to(layer)
        player.set_controls(self, **dict(
            move_up=K_UP,
            move_down=K_DOWN,
            move_left=K_LEFT,
            move_right=K_RIGHT,
        ))
        self.ticker.add(player.tick, 10)

def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('RPG TileMap Example')
    manager.add_scene(RpgScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
