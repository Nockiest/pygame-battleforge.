import random
import pygame
class BattleGround:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.forrests = []
        self.rivers = []
        self.towns = []
        self.roads = []
        self.supply_depots = []
        
        # Define quantities of each element to generate
        self.num_forrests = 10
        self.num_rivers = 3
        self.num_towns = 4
        self.num_roads = 9
        self.num_supply_depots = 2

    def place_forrests(self):
        for _ in range(self.num_forrests):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.forrests.append((x, y))

    def place_rivers(self):
        for _ in range(self.num_rivers):
            start_x = random.choice([0, self.width])
            start_y = random.randint(0, self.height)
            end_x = self.width - start_x
            end_y = random.randint(0, self.height)

            control_x1 = random.randint(0, self.width)
            control_y1 = random.randint(0, self.height)
            control_x2 = random.randint(0, self.width)
            control_y2 = random.randint(0, self.height)

            self.rivers.append(((start_x, start_y), (end_x, end_y), (control_x1, control_y1), (control_x2, control_y2)))

    def calculate_bezier_curve(self, t, p0, p1, p2, p3):
        u = 1 - t
        uu = u * u
        uuu = uu * u
        tt = t * t
        ttt = tt * t

        p = (
            u * uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0],
            u * uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
        )
        return p

    def place_towns(self):
        for _ in range(self.num_towns):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.towns.append((x, y))

    def place_roads(self):
        for _ in range(self.num_roads):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            self.roads.append(((x1, y1), (x2, y2)))

    def place_supply_depots(self):
    # Place supply depots on the left side
        for _ in range(self.num_supply_depots // 2):
            x_left = random.randint(50, self.width // 2 - 50)  # Ensure at least 50 pixels from the left edge
            y = random.randint(50, self.height - 50)  # Ensure at least 50 pixels from top and bottom edges
            self.supply_depots.append((x_left, y))

        # Place supply depots on the right side
        for _ in range(self.num_supply_depots // 2):
            x_right = random.randint(self.width // 2 + 50, self.width - 50)  # Ensure at least 50 pixels from the right edge
            y = random.randint(50, self.height - 50)  # Ensure at least 50 pixels from top and bottom edges
            self.supply_depots.append((x_right, y))

    def draw_bezier_curve(self, screen, points):
            num_segments = 100
            curve_points = []
            for t in range(num_segments + 1):
                t_normalized = t / num_segments
                x = int((1 - t_normalized)**3 * points[0][0] +
                        3 * (1 - t_normalized)**2 * t_normalized * points[2][0] +
                        3 * (1 - t_normalized) * t_normalized**2 * points[3][0] +
                        t_normalized**3 * points[1][0])
                y = int((1 - t_normalized)**3 * points[0][1] +
                        3 * (1 - t_normalized)**2 * t_normalized * points[2][1] +
                        3 * (1 - t_normalized) * t_normalized**2 * points[3][1] +
                        t_normalized**3 * points[1][1])
                curve_points.append((x, y))
            
            pygame.draw.lines(screen, (128, 128, 128), False, curve_points, 2)

    def draw(self, screen):
        dot_radius = 10

        # Draw forrests
        for x, y in self.forrests:
            pygame.draw.circle(screen, (34, 139, 34), (x, y), dot_radius)  # Dark Green

        # Draw rivers
        for start, end, control1, control2 in self.rivers:
            pygame.draw.circle(screen, (128, 128, 128), start, dot_radius)
            pygame.draw.circle(screen, (128, 128, 128), end, dot_radius)

            num_segments = 100
            points = []
            for i in range(num_segments + 1):
                t = i / num_segments
                point = self.calculate_bezier_curve(t, start, control1, control2, end)
                points.append(point)

            pygame.draw.lines(screen, (128, 128, 128), False, points, 2)
        # Draw towns
        for x, y in self.towns:
            pygame.draw.circle(screen, (255, 0, 0), (x, y), dot_radius)  # Red

        # Draw roads
        # for (x1, y1), (x2, y2) in self.roads:
        #     pygame.draw.circle(screen, (139, 69, 19), (x1, y1), dot_radius)  # Saddle Brown
        #     pygame.draw.circle(screen, (139, 69, 19), (x2, y2), dot_radius)  # Saddle Brown
        #     pygame.draw.line(screen, (139, 69, 19), (x1, y1), (x2, y2), 2)  # Saddle Brown

        # Draw supply depots
        for x, y in self.supply_depots:
            pygame.draw.circle(screen, (255, 255, 0), (x, y), dot_radius)  # Yellow
