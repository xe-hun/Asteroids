

    
import pygame

from customEnum import ShipActions


class MiscConfig():
    map_button_save_location = 'button_map.json'
    
    default_key_map = {
            ShipActions.Boost: 'DOWN',
            ShipActions.Cannon:'LEFT',
            ShipActions.Rocket: 'RIGHT',
            ShipActions.Steer: 'L CLICK'
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
    