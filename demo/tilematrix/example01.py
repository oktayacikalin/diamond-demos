#!/usr/bin/env python

import sys
import os

# Make sure that our diamond engine can be found.
sys.path.insert(0, os.path.abspath('../../'))

from diamond.scene import SceneManager, Scene
from diamond.tilematrix import TileMatrix
from diamond.transition import TransitionManager
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.fps import Fps

import rpg_tilesheet
import rpg_inventorysheet


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'framerate': 120,
    # 'vsync': False,
    # 'scaling': 1.5,  # 1.0 is normal; 2.0 would be double window size.
}


class ExampleScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.add_to(self.root_node)
        fps = Fps(ticker=self.ticker, details=True)
        fps.set_alpha(75)
        fps.add_to(fps_node)
        fps.set_align_box(DISPLAY_LAYOUT['screen_size'][0], 0, 'right')
        fps_node.set_order_pos(10)

    def setup(self):
        super(ExampleScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.transition_manager = TransitionManager()
        # Keep movement in sync with display vsync.
        self.transition_manager.is_threaded = False
        self.bind(self.ticker, self.transition_manager)
        self.__setup_fps()

        tilematrix = TileMatrix()
        tilematrix.load_sheet(rpg_tilesheet)
        tilematrix.load_sheet(rpg_inventorysheet)
        # tilematrix.load_matrix('matrix5,5')
        tilematrix.load_matrix('matrix10,10')
        tilematrix.pos = 500, 30
        tilematrix.show_sector_coords = True
        tilematrix.add_to(self.root_node)

        self.transition_manager.add_change(self.move_tilematrix_left, tilematrix, stack='movement')
        self.transition_manager.add_change(self.info, tilematrix, delay=500)

        # self.transition_manager.add_change((tilematrix, 'set_pos'), args=(-500, 0), delay=100)
        # self.transition_manager.add_change((tilematrix, 'set_pos'), args=(0, 0), delay=1000)

    def info(self, tilematrix):
        print tilematrix.get_tile_id_at(1, 1)
        print tilematrix.get_tile_at(1, 1)

    def move_tilematrix_right(self, tilematrix):
        self.transition_manager.add_range(
            callback=tilematrix.set_pos,
            args=lambda value: (value, 30),
            range=(-500, 500),
            msecs=10000,
            min_step_msecs=10,
            stack='movement',
        )
        self.transition_manager.add_change(self.move_tilematrix_top, tilematrix, stack='movement')

    def move_tilematrix_left(self, tilematrix):
        self.transition_manager.add_range(
            callback=tilematrix.set_pos,
            args=lambda value: (value, 30),
            range=(500, -500),
            msecs=10000,
            min_step_msecs=10,
            stack='movement',
        )
        self.transition_manager.add_change(self.move_tilematrix_right, tilematrix, stack='movement')

    def move_tilematrix_top(self, tilematrix):
        self.transition_manager.add_range(
            callback=tilematrix.set_pos,
            args=lambda value: (0, value),
            range=(30, -500),
            msecs=10000,
            min_step_msecs=10,
            stack='movement',
        )
        self.transition_manager.add_change(self.move_tilematrix_bottom, tilematrix, stack='movement')

    def move_tilematrix_bottom(self, tilematrix):
        self.transition_manager.add_range(
            callback=tilematrix.set_pos,
            args=lambda value: (0, value),
            range=(-500, 30),
            msecs=10000,
            min_step_msecs=10,
            stack='movement',
        )
        self.transition_manager.add_change(self.move_tilematrix_left, tilematrix, stack='movement')


def main():
    # from diamond.helper import logging
    # logging.LOG_LEVEL_THRESHOLD = logging.LOG_LEVEL_DEBUG

    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('TileMatrix Example 01 (matrix10,10)')
    manager.add_scene(ExampleScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
