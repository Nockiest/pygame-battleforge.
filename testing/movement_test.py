import pygame
import unittest
import math
import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from unit import Unit

class TestUnitMethods(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 500))
        self.unit = Unit(hp=2, attack_range=50, remain_attacks=1, base_movement=100, x=100,
                         y=100, size=20, ammo=50, icon="warrior_img", selected=False, color=(0, 255, 0))
        self.fps = 60
        self.clock = pygame.time.Clock()

    def tearDown(self):
        pygame.quit()

    # def test_move_in_game_field(self):
    # # Simulate a mouse click at position (200, 200)
    #     pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (200, 200)}))

    #     # Run the game loop for 2 seconds to let the unit move
    #     for _ in range(self.fps * 10):
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 return
    #         self.unit.move_in_game_field(pygame.mouse.get_pos())
    #         self.screen.fill((0, 0, 0))
    #         self.unit.render_on_screen(self.screen)
    #         pygame.display.update()
    #         self.clock.tick(self.fps)

    #         # Assert that the unit's position has been updated correctly
    #         # self.assertEqual(self.unit.x, 190)
    #         # self.assertEqual(self.unit.y, 190)

    #         # Assert that the unit stays within the game window boundaries
    #         self.assertTrue(0 <= self.unit.x < 1000, f"Unit's x position is out of bounds: {self.unit.x}")
    #         self.assertTrue(0 <= self.unit.y < 500, f"Unit's y position is out of bounds: {self.unit.y}")

    #         # Calculate the distance between the initial position and the new position
    #         delta_x = self.unit.x + self.unit.size // 2 - self.unit.start_turn_position[0]
    #         delta_y = self.unit.y + self.unit.size // 2 - self.unit.start_turn_position[1]
    #         distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

    #         # Assert that the distance is less than or equal to self.base_movement
    #         print(distance, self.unit.base_movement)
    #         self.assertLessEqual(distance, self.unit.base_movement + 2, msg="Unit moved beyond base_movement")

    # def test_draw_as_active(self):
    #     # Run the game loop for 2 seconds to show the active unit
    #     for _ in range(self.fps * 2):
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 return
    #         self.screen.fill((0, 0, 0))
    #         self.unit.render_on_screen(self.screen)
    #         self.unit.draw_as_active(self.screen)
    #         pygame.display.update()
    #         self.clock.tick(self.fps)

    #     # TODO: Add assertions to check if the outline rectangle and circle are drawn correctly

    # def test_unit_dies(self):
    #     # Create a list of units
    #     units = [self.unit]

    #     # Call the remove_from_game method to remove the unit from the list and set x and y to None
    #     self.unit.remove_from_game(units)

    #     # Assert that the unit has been removed from the units list
    #     self.assertNotIn(self.unit, units, "Unit has not been removed from the units list")
        
    #     # Assert that the unit's x and y coordinates are set to None
    #     self.assertIsNone(self.unit.x, "Unit's x coordinate is not set to None")
    #     self.assertIsNone(self.unit.y, "Unit's y coordinate is not set to None")

    # def test_reset_for_next_turn(self):
    #     # Set specific values for remain_attacks and ammo
    #     self.unit.remain_attacks = 0
    #     self.unit.ammo = 5

    #     # Call reset_for_next_turn method
    #     self.unit.reset_for_next_turn()

    #     # Assert that the remain_attacks and ammo have been updated correctly
    #     self.assertEqual(self.unit.remain_attacks, 1, "remain_attacks not updated correctly")
    #     self.assertEqual(self.unit.ammo, 7, "ammo not updated correctly")

    #     # Assert that ableToMove is True after the reset
    #     self.assertTrue(self.unit.ableToMove, "ableToMove not set to True after reset")
        
    def test_attack(self):
    # Define a list of click positions
        click_positions = [
            (self.unit.x + self.unit.size // 2 + 50, self.unit.y + self.unit.size // 2 + 50),
            (self.unit.x + self.unit.size // 2 + 30, self.unit.y + self.unit.size // 2 + 30)
            # Add more click positions if needed
        ]

        # Loop through each click position and test the attack
        for click_pos in click_positions:
            result, attack_pos = self.unit.attack(click_pos)
            print(result, attack_pos)
            # Assert that the unit remains selected (not ableToMove = False) when attacking is possible
            if result == "UNIT ATTACKS":
                self.assertFalse(self.unit.ableToMove, "Unit should not have any left moves after attacking")
                self.assertEqual(self.unit.remain_attacks, 0, "remain_attacks should be decreased after attacking")
                self.assertEqual(self.unit.ammo, 49, "ammo should be decreased after attacking")
            else:
                # Assert that the result of the attack is correct
                self.assertEqual(result, "Attack not possible", "Attack result should be 'Attack not possible'")
                self.assertEqual(attack_pos, click_pos, "Attack position should be equal to the click position")

                # Assert that the attack-related functions were not called (attack_square is not set)
                self.assertFalse(hasattr(self.unit, 'attack_cross_position'), "attack_square should not be set")




    
if __name__ == '__main__':
    unittest.main()