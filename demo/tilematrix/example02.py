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
from diamond.decorators import time

import rpg_tilesheet


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'framerate': 60,
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
        tilematrix.set_tile_at(1, 1, 5, '1')
        tilematrix.set_tile_at(-1, 1, 3, '1')
        tilematrix.set_default_tile_value({0: '72'})
        tilematrix.show_sector_coords = True
        tilematrix.add_to(self.root_node)
        # tilematrix.set_default_tile_value({0: '72'})

        tilematrix.set_pos(500, 30)

        self.transition_manager.add_change(self.move_tilematrix_bottom, tilematrix, stack='movement')
        self.transition_manager.add_change(self.info, tilematrix, delay=500, stack='info')
        self.transition_manager.add_change(self.disable_default_tile, tilematrix, delay=2000, append=False)

    # @time
    def info(self, tilematrix):
        print 'info(%s, %s)' % (self, tilematrix)
        print
        print 1, (1, 1), tilematrix.get_tile_id_at(1, 1)
        print 2, (1, 1), tilematrix.get_tile_at(1, 1)
        print 3, (2, 1), tilematrix.get_tile_id_at(2, 1)
        print 4, (2, 1), tilematrix.get_tile_at(2, 1)
        print 5, (8, 1), tilematrix.get_tile_id_at(8, 1)
        print 6, (8, 1), tilematrix.get_tile_at(8, 1)
        print 7, (9, 1), tilematrix.get_tile_id_at(9, 1)
        print 8, (9, 1), tilematrix.get_tile_at(9, 1)

        try:
            if tilematrix.get_tile_id_at(8, 1).keys() and tilematrix.get_tile_id_at(8, 1).keys() != tilematrix.get_tile_at(8, 1).keys():
                raise Exception('BOOM')
        except AttributeError:
            pass

        self.transition_manager.add_change(self.info, tilematrix, delay=500, stack='info')

    @time
    def enable_default_tile(self, tilematrix):
        tilematrix.set_default_tile_value({0: '72'})
        tilematrix.set_tile_at(2, 1, 5, '1')
        tilematrix.set_tile_at(-12, 1, 5, '1')
        self.transition_manager.add_change(self.change_tile, tilematrix, delay=2000)

    @time
    def change_tile(self, tilematrix):
        tilematrix.set_tile_at(2, 1, 5, '2')
        tilematrix.set_tile_at(-12, 1, 5, '2')
        self.transition_manager.add_change(self.disable_default_tile, tilematrix, delay=2000)

    @time
    def disable_default_tile(self, tilematrix):
        tilematrix.set_default_tile_value(None)
        tilematrix.set_tile_at(2, 1, 5, None)
        tilematrix.set_tile_at(-12, 1, 5, None)
        self.transition_manager.add_change(self.enable_default_tile, tilematrix, delay=2000)

    # @time
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

    # @time
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

    # @time
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

    # @time
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
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('TileMatrix Example 02 (no matrix, default tile toggling, tile manipulation)')
    manager.add_scene(ExampleScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
