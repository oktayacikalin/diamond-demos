#!/usr/bin/env python
'''
Demonstrates how to define sprite vaults with images which are build out of
multiple images. Also makes utilizes a tilemap for presentation.
'''

import sys
import os

# Make sure that our diamond engine can be found.
sys.path.insert(0, os.path.abspath('../../'))

from diamond.scene import SceneManager, Scene
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.fps import Fps
from diamond.tilemap import TileMap

import piggyback_tilesheet


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'framerate': 60,
    # 'scaling': 1.5,  # 1.0 is normal; 2.0 would be double window size.
}


class PiggybackSpriteScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.add_to(self.root_node)
        fps_node.set_order_pos(10)
        fps = Fps(ticker=self.ticker, details=True)
        fps.set_alpha(75)
        fps.add_to(fps_node)
        fps.set_align_box(DISPLAY_LAYOUT['screen_size'][0], 0, 'right')

    def setup(self):
        super(PiggybackSpriteScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.bind(self.ticker)
        self.__setup_fps()

        tilemap = TileMap()
        tilemap.load_sheet(piggyback_tilesheet)
        tilemap.load_map('piggyback_tilemap.csv')
        tilemap.build_map()
        map_size = tilemap.get_map_size()
        tilemap.add_to(self.root_node)
        tilemap.set_pos(
            DISPLAY_LAYOUT['screen_size'][0] / 2 - 32 * map_size[0] / 2,
            DISPLAY_LAYOUT['screen_size'][1] / 2 - 32 * map_size[1] / 2,
        )


def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Piggyback Sprite Example')
    manager.add_scene(PiggybackSpriteScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
