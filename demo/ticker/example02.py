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
from diamond.transition import TransitionManager

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
        self.transition_manager = TransitionManager()
        self.bind(self.ticker, self.transition_manager)
        self.__setup_fps()

        sprite = Sprite.make(basic_spritesheet)
        sprite.add_to(self.root_node)

        self.transition_manager.add_change((self, 'add_round'), [self.transition_manager, sprite])

    def add_round(self, ticker, sprite):
        print self, 'add round'
        ticker.add_change((sprite, 'set_pos'), [300, 300], delay=1000)
        ticker.add_change((sprite, 'set_pos'), [600, 100], delay=1000)
        ticker.add_change((sprite, 'set_pos'), [100, 300], delay=1000)
        ticker.add_change(self.add_round, (ticker, sprite))


def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Ticker Example 02')
    manager.add_scene(ExampleScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
