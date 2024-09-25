# import pygame
# import Box2D

# # Initialize Pygame
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Box2D Polygon and Triangle")

# # Initialize Box2D
# world = Box2D.b2World(gravity=(0, -10))

# # Create a polygon
# polygon_vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
# polygon_body = world.CreateDynamicBody(position=(4, 3))
# polygon_shape = Box2D.b2PolygonShape(vertices=polygon_vertices)
# polygon_body.CreateFixture(shape=polygon_shape, density=1.0)

# # Create a triangle
# triangle_vertices = [(0, 0), (2, 0), (1, 2)]
# triangle_body = world.CreateDynamicBody(position=(8, 3))
# triangle_shape = Box2D.b2PolygonShape(vertices=triangle_vertices)
# triangle_body.CreateFixture(shape=triangle_shape, density=1.0)

# if __name__ == "__main__":

#     # Simulation loop
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         world.Step(1.0 / 60.0, 6, 2)

#         # Clear the screen
#         screen.fill((255, 255, 255))

#         # Draw the polygon
#         polygon_points = [(polygon_body.transform * v) * 20 for v in polygon_vertices]
#         pygame.draw.polygon(screen, (0, 0, 0), polygon_points)

#         # Draw the triangle
#         triangle_points = [(triangle_body.transform * v) * 20 for v in triangle_vertices]
#         pygame.draw.polygon(screen, (0, 0, 0), triangle_points)

#         pygame.display.flip()

#     pygame.quit()




import pygame
import Box2D

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Box2D Example")

# Set up Box2D world
world = Box2D.b2World(gravity=(0, -10), doSleep=True)

# Create ground body
ground_body_def = Box2D.b2BodyDef()
ground_body_def.position.Set(0, -10)
ground_body = world.CreateBody(ground_body_def)
ground_shape = Box2D.b2PolygonShape()
ground_shape.SetAsBox(50, 10)
ground_body.CreateFixture(ground_shape, 0)

# Create dynamic polygon
polygon_body_def = Box2D.b2BodyDef()
polygon_body_def.type = Box2D.b2_dynamicBody
polygon_body_def.position.Set(0, 10)
polygon_body = world.CreateBody(polygon_body_def)
polygon_shape = Box2D.b2PolygonShape()
polygon_vertices = [
    Box2D.b2Vec2(-1, 1),
    Box2D.b2Vec2(1, 1),
    Box2D.b2Vec2(0, -1)
]
polygon_shape.Set(polygon_vertices)
polygon_body.CreateFixture(polygon_shape, 1)

# Create dynamic triangle
triangle_body_def = Box2D.b2BodyDef()
triangle_body_def.type = Box2D.b2_dynamicBody
triangle_body_def.position.Set(5, 10)
triangle_body = world.CreateBody(triangle_body_def)
triangle_shape = Box2D.b2PolygonShape()
triangle_vertices = [
    Box2D.b2Vec2(-1, -1),
    Box2D.b2Vec2(1, -1),
    Box2D.b2Vec2(0, 1)
]
triangle_shape.Set(triangle_vertices)
triangle_body.CreateFixture(triangle_shape, 1)

# Simulation loop
if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update   
        # Box2D world
        world.Step(1 / 60, 6, 2)

        # Clear screen
        screen.fill((255, 255, 255))

        # Draw shapes
        polygon_x, polygon_y = polygon_body.position.x * 30, polygon_body.position.y * 30
        pygame.draw.polygon(screen, (0, 0, 0), [(polygon_x + x * 30, polygon_y + y * 30) for x, y in polygon_vertices])
        triangle_x, triangle_y = triangle_body.position.x * 30, triangle_body.position.y * 30
        pygame.draw.polygon(screen, (0, 0, 0), [(triangle_x + x * 30, triangle_y + y * 30) for x, y in triangle_vertices])

        # Draw ground
        pygame.draw.rect(screen, (0, 0, 0), (0, 550, 800, 50))

        # Update display
        pygame.display.flip()

    pygame.quit()