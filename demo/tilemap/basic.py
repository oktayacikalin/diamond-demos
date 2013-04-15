#!/usr/bin/env python

import sys
import os

# Make sure that our diamond engine can be found.
sys.path.insert(0, os.path.abspath('../../'))

from diamond.scene import SceneManager, Scene
from diamond.tilemap import TileMap
from diamond.transition import TransitionManager
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.fps import Fps

import basic_tilesheet


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'framerate': 60,
    # 'scaling': 1.5,  # 1.0 is normal; 2.0 would be double window size.
}


class SmallScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.add_to(self.root_node)
        fps = Fps(ticker=self.ticker, details=True)
        fps.set_alpha(75)
        fps.add_to(fps_node)
        fps.set_align_box(DISPLAY_LAYOUT['screen_size'][0], 0, 'right')

    def setup(self):
        super(SmallScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.transition_manager = TransitionManager()
        self.bind(self.ticker, self.transition_manager)
        self.__setup_fps()

        tilemap = TileMap()
        tilemap.load_sheet(basic_tilesheet)
        tilemap.load_map('basic_tilemap.csv')
        tilemap.build_map()
        tilemap.add_to(self.root_node)
        tilemap.set_pos(30, 30)

        self.transition_manager.add_change(self.move_tilemap_left, tilemap)

    def move_tilemap_right(self, tilemap):
        self.transition_manager.add_range(
            callback=tilemap.set_pos,
            args=lambda value: (value, 30),
            range=(-500, 30),
            msecs=5000,
            min_step_msecs=10,
        )
        self.transition_manager.add_change(self.move_tilemap_left, tilemap)

    def move_tilemap_left(self, tilemap):
        self.transition_manager.add_range(
            callback=tilemap.set_pos,
            args=lambda value: (value, 30),
            range=(30, -500),
            msecs=5000,
            min_step_msecs=10,
        )
        self.transition_manager.add_change(self.move_tilemap_right, tilemap)


def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Basic TileMap Example')
    manager.add_scene(SmallScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
