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
from diamond.sprite import Sprite, SpriteEffects
from diamond.decorators import time

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
        self.transition_manager = SpriteEffects()
        self.bind(self.ticker, self.transition_manager)
        self.__setup_fps()

        # self.transition_manager.drop_outdated_msecs = 500
        # self.transition_manager.handle_limit_per_iteration = 500

        self.sprites = [Sprite.make(basic_spritesheet) for x in range(0, 5)]
        [sprite.set_pos(x * 32, 32) for x, sprite in enumerate(self.sprites)]
        self.root_node.add_children(self.sprites)

        self.transition_manager.add_change((self, 'add_round'))
        # import pdb; pdb.set_trace()

    @time
    def add_round(self):
        # print self, 'add round'
        # for sprite in self.sprites:
        #     self.transition_manager.move_by(sprite, pos=(200, 200), msecs=1000, stack=id(sprite))
        #     self.transition_manager.move_by(sprite, pos=(-400, 0), msecs=1000, stack=id(sprite))
        #     self.transition_manager.move_by(sprite, pos=(200, -200), msecs=1000, stack=id(sprite))
        for x, sprite in enumerate(self.sprites):
            self.transition_manager.move_to(sprite, pos=(200 + x * 32, 200), msecs=10000, stack=id(sprite))
            self.transition_manager.move_to(sprite, pos=(-200 + x * 32, 200), msecs=10000, stack=id(sprite))
            self.transition_manager.move_to(sprite, pos=(0 + x * 32, 32), msecs=10000, stack=id(sprite))
        self.transition_manager.add_change(self.add_round, delay=30000)


def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Ticker Example 05')
    manager.add_scene(ExampleScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
