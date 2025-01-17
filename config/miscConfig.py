

    
import pygame

from customEnum import ShipActions


class MiscConfig():
    
    @staticmethod
    def get_game_tips(_key_map:dict):
        return [
            f'Tips!: press {_key_map[ShipActions.Steer]} and move the mouse to steer the Ship.',
            f'Tips!: press {_key_map[ShipActions.Cannon]} to fire a Cannon',
            f'Tips!: press {_key_map[ShipActions.Rocket]} to fire a Missile.',
            f'Tips!: press {_key_map[ShipActions.Boost]} to boost your Ship.',
            'Tips!: Use Missiles to gain Advantage.',
            'Tips!: Beat the Time!!!',
         
        ]
    
    saved_data_location = 'data.bin'
   
    
    map_button_save_location = 'button_map.json'
    default_key_map = {
            ShipActions.Boost: 'S',
            ShipActions.Cannon:'L CLICK',
            ShipActions.Rocket: 'R CLICK',
            ShipActions.Steer: 'A'
        }
    
    button_to_event_map = {
        
            pygame.K_a : 'A' ,
            pygame.K_b : 'B' ,
            pygame.K_c : 'C' ,
            pygame.K_d : 'D' ,
            pygame.K_e : 'E' ,
            pygame.K_f : 'F' ,
            pygame.K_g : 'G' ,
            pygame.K_h : 'H' ,
            pygame.K_i : 'I' ,
            pygame.K_j : 'J' ,
            pygame.K_k : 'K' ,
            pygame.K_l : 'L' ,
            pygame.K_m : 'M' ,
            pygame.K_n : 'N' ,
            pygame.K_o : 'O' ,
            pygame.K_p : 'P' ,
            pygame.K_q : 'Q' ,
            pygame.K_r : 'R' ,
            pygame.K_s : 'S' ,
            pygame.K_t : 'T' ,
            pygame.K_u : 'U' ,
            pygame.K_v : 'V' ,
            pygame.K_w : 'W' ,
            pygame.K_x : 'X' ,
            pygame.K_y : 'Y' ,
            pygame.K_z : 'Z' ,
            'M_1' : 'L CLICK' ,
            'M_3' : 'R CLICK' ,
            pygame.K_UP : 'UP' ,
            pygame.K_DOWN : 'DOWN' ,
            pygame.K_LEFT : 'LEFT' ,
            pygame.K_RIGHT : 'RIGHT' ,
        }
    