from manim import *
import numpy as np

class ParticleFilterExplanation(Scene):
    def construct(self):
        # =========================================================================
        # 1. TÍTULO E INTRODUCCIÓN
        # =========================================================================
        title = Title("Filtro de Partículas (Sequential Monte Carlo)", font_size=40)
        self.play(Write(title))
        self.wait(1)
        
        # Línea divisoria entre la visualización (arriba) y la matemática (abajo)
        divider = Line(LEFT * 7, RIGHT * 7).shift(DOWN * 0.5)
        self.play(Create(divider))

        # =========================================================================
        # 2. DEFINICIÓN DEL ENTORNO (ZONA SUPERIOR)
        # =========================================================================
        # Landmark (Punto de referencia / Faro)
        landmark = Star(n=5, outer_radius=0.3, inner_radius=0.15, color=YELLOW, fill_opacity=1)
        landmark.move_to(RIGHT * 4 + UP * 1.5)
        landmark_label = Text("Landmark (Faro)", font_size=16, color=YELLOW).next_to(landmark, UP)
        
        # Robot Real (Ground Truth) - Empezará en la izquierda
        robot_true = Dot(LEFT * 4 + UP * 1.5, color=GREEN, radius=0.15)
        robot_label = Text("Robot (Real)", font_size=16, color=GREEN).next_to(robot_true, DOWN)
        
        # Inicialización de la Nube de Partículas (Dispersas al inicio)
        np.random.seed(42) # Para reproducibilidad
        num_particles = 40
        particle_positions = np.random.normal(loc=[-3.5, 1.5, 0], scale=[1.0, 0.6, 0], size=(num_particles, 3))
        # Forzar Z coordenada a cero por seguridad en Manim 2D
        particle_positions[:, 2] = 0
        
        particles = VGroup(*[Dot(pos, color=RED, radius=0.05) for pos in particle_positions])
        particles_label = Text("Nube de Partículas", font_size=16, color=RED).move_to(LEFT * 4 + UP * 2.8)

        # Añadir elementos iniciales a la pantalla
        self.play(
            FadeIn(landmark, landmark_label),
            FadeIn(robot_true, robot_label),
            FadeIn(particles, particles_label)
        )
        self.wait(1.5)

        # =========================================================================
        # 3. CICLO DEL ALGORITMO (PASO A PASO)
        # =========================================================================
        
        # --- FASE 1: PREDICCIÓN ---
        phase_1_title = Text("Fase 1: Predicción (Modelo de Movimiento)", font_size=28, color=BLUE).move_to(DOWN * 1.2)
        eq_pred = MathTex(
            "x_t^{[i]} \\sim p(x_t \\mid x_{t-1}^{[i]}, u_t)", 
            font_size=36
        ).move_to(DOWN * 2.2)
        desc_pred = Text("Cada partícula se mueve como el robot, sumando ruido por incertidumbre.", font_size=18).move_to(DOWN * 3.2)
        
        self.play(Write(phase_1_title), Write(eq_pred), Write(desc_pred))
        self.wait(1)
        
        # Animación del movimiento físico con dispersión (Incertidumbre crece)
        # Robot real avanza limpiamente a la derecha
        new_robot_pos = LEFT * 1 + UP * 1.5
        
        # Partículas avanzan a la derecha pero añaden ruido gaussiano extra (se dispersan más)
        moved_animations = []
        for p in particles:
            noise = np.random.normal(loc=[3.0, 0.0, 0], scale=[0.5, 0.3, 0])
            target_pos = p.get_center() + noise
            moved_animations.append(p.animate.move_to(target_pos))
            
        self.play(
            robot_true.animate.move_to(new_robot_pos),
            robot_label.animate.next_to(new_robot_pos, DOWN),
            *moved_animations,
            run_time=2
        )
        self.wait(2)
        
        # Limpieza de textos matemáticos inferiores para la siguiente fase
        self.play(FadeOut(phase_1_title), FadeOut(eq_pred), FadeOut(desc_pred))

        # --- FASE 2: ACTUALIZACIÓN (MEDICIÓN) ---
        phase_2_title = Text("Fase 2: Actualización (Pesado por Medición)", font_size=28, color=ORANGE).move_to(DOWN * 1.2)
        eq_meas = MathTex(
            "w_t^{[i]} = p(z_t \\mid x_t^{[i]})", 
            font_size=36
        ).move_to(DOWN * 2.2)
        desc_meas = Text("Se evalúa el sensor. Partículas más cercanas al valor real ganan peso.", font_size=18).move_to(DOWN * 3.2)
        
        self.play(Write(phase_2_title), Write(eq_meas), Write(desc_meas))
        self.wait(0.5)
        
        # Haz de luz del sensor (Simulación de pulso de medición)
        sensor_beam = Line(new_robot_pos, landmark.get_center(), color=GREEN, stroke_width=2).set_opacity(0.7)
        self.play(Create(sensor_beam))
        self.play(FadeOut(sensor_beam))
        
        # Modificar visualmente el tamaño y opacidad de las partículas según su cercanía al robot real
        scaled_particles = []
        for p in particles:
            dist_to_true = np.linalg.norm(p.get_center() - new_robot_pos)
            # A menor distancia, mayor peso (Gaussiana simple para efectos visuales)
            weight = np.exp(- (dist_to_true ** 2) / 1.2)
            
            # Mapear el peso al tamaño de la partícula en Manim
            new_radius = 0.03 + (weight * 0.12)
            opacity = 0.2 + (weight * 0.8)
            scaled_particles.append(p.animate.set_stroke(width=0).set_fill(color=RED, opacity=opacity).scale(new_radius / 0.05))
            
        self.play(*scaled_particles, run_time=2)
        self.wait(2)
        
        self.play(FadeOut(phase_2_title), FadeOut(eq_meas), FadeOut(desc_meas))

        # --- FASE 3: NORMALIZACIÓN ---
        phase_3_title = Text("Fase 3: Normalización de Pesos", font_size=28, color=PURPLE).move_to(DOWN * 1.2)
        eq_norm = MathTex(
            "\\tilde{w}_t^{[i]} = \\frac{w_t^{[i]}}{\\sum_{j=1}^{N} w_t^{[j]}}", 
            font_size=36
        ).move_to(DOWN * 2.2)
        desc_norm = Text("Se escalan los pesos para asegurar que la suma de todos sea exactamente 1.", font_size=18).move_to(DOWN * 3.2)
        
        self.play(Write(phase_3_title), Write(eq_norm), Write(desc_norm))
        self.wait(2.5)
        
        self.play(FadeOut(phase_3_title), FadeOut(eq_norm), FadeOut(desc_norm))

        # --- FASE 4: RESAMPLEO (REANIMACIÓN DE LA NUBE) ---
        phase_4_title = Text("Fase 4: Resampleo (Muestreo Ruleta)", font_size=28, color=GREEN_A).move_to(DOWN * 1.2)
        eq_resample = Text("Selección Natural: Partículas débiles mueren, las fuertes se duplican.", font_size=20).move_to(DOWN * 2.2)
        desc_resample = Text("La nube colapsa disminuyendo la incertidumbre drásticamente.", font_size=18).move_to(DOWN * 3.2)
        
        self.play(Write(phase_4_title), Write(eq_resample), Write(desc_resample))
        self.wait(1)
        
        # Estimación promedio antes del colapso (Cruz azul)
        estimate_cross = Cross(scale_factor=0.2, stroke_color=BLUE_D, stroke_width=4).move_to(new_robot_pos + np.array([0.2, -0.1, 0]))
        estimate_label = Text("Estimación promedio", font_size=14, color=BLUE_D).next_to(estimate_cross, UP * 0.5)
        
        # Efecto visual de Resampleo:
        # Desaparecer partículas lejanas (bajos pesos) y concentrar la nube densamente sobre el robot real
        resampled_animations = []
        for p in particles:
            dist_to_true = np.linalg.norm(p.get_center() - new_robot_pos)
            
            if dist_to_true > 1.2:
                # Partículas muy lejanas se desvanecen por completo (mueren)
                resampled_animations.append(p.animate.set_opacity(0).scale(0.1))
            else:
                # Partículas con buen peso migran al epicentro real con una desviación muy pequeña
                resample_noise = np.random.normal(loc=[0, 0, 0], scale=[0.18, 0.15, 0])
                final_pos = new_robot_pos + resample_noise
                resampled_animations.append(p.animate.move_to(final_pos).set_opacity(1).set_scale(1.0)) # restaurar tamaño uniforme estándar
                
        self.play(*resampled_animations, Create(estimate_cross), FadeIn(estimate_label), run_time=2.5)
        self.wait(3)
        
        # Cierre suave de la escena
        self.play(
            FadeOut(phase_4_title), FadeOut(eq_resample), FadeOut(desc_resample),
            FadeOut(particles), FadeOut(robot_true), FadeOut(landmark), 
            FadeOut(estimate_cross), FadeOut(divider), FadeOut(title),
            FadeOut(robot_label), FadeOut(landmark_label), FadeOut(particles_label), FadeOut(estimate_label)
        )
        self.wait(1)