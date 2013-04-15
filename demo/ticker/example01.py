#!/usr/bin/env python
'''
Demonstrates how to move a sprite using a ticker.
'''

import sys
import os

# Make sure that our diamond engine can be found.
sys.path.insert(0, os.path.abspath('../../'))

from diamond.scene import SceneManager, Scene
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.fps import Fps
from diamond.sprite import Sprite

import basic_spritesheet


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

    def setup(self):
        super(ExampleScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.bind(self.ticker)
        self.__setup_fps()

        sprite = Sprite.make(basic_spritesheet)
        sprite.add_to(self.root_node)

        # FIXME why is the sprite jumping around unregularely?
        self.ticker.add(func=self.add_round, args=(self.ticker, sprite), msecs=0, onetime=True)

    def add_round(self, ticker, sprite):
        print self, 'add round'
        ticker.add(func=sprite.set_pos, args=[300, 300], msecs=1000, onetime=True)
        ticker.add(func=sprite.set_pos, args=[600, 100], msecs=2000, onetime=True)
        ticker.add(func=sprite.set_pos, args=[100, 300], msecs=3000, onetime=True)
        ticker.add(func=self.add_round, args=(ticker, sprite), msecs=3000, onetime=True)


def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Ticker Example 01')
    manager.add_scene(ExampleScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
