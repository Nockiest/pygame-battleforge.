 line_pixel_colors = get_pixel_colors(
                line_points, background_screen)
            prevented = self.prevent_shhooting_through_forrest(
                line_pixel_colors, line_points)
            if not prevented:
                self.create_shoot_animation(line_points)
            # Check if FORREST_GREEN is present in pixel colors
