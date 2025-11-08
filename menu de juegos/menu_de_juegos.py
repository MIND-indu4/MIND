import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont

class GameMenu:
    def __init__(self, master):
        self.master = master
        self.script_dir = os.path.dirname(os.path.abspath(__file__)) # <--- ¡MUEVE ESTA LÍNEA AQUÍ ARRIBA!
        
        master.title("Seleccione una actividad")
        master.geometry("1000x800")
        master.resizable(False, False)
        master.config(bg="#FFDE59") # Fondo amarillo claro para la ventana principal

        # --- Paleta de colores y rutas de iconos ---
        self.yellow_bg = "#FFDE59" # Fondo amarillo exterior
        self.white_frame_bg = "#FFFFFF" # Fondo blanco interior
        self.text_color = "#333333" # Color del texto principal
        self.red_border = "#FF4B4B" # Original
        self.pink_border = "#FF69B4"
        self.green_border = "#4CAF50"
        self.blue_border = "#00BFFF"

        # Rutas de los iconos (asegúrate de que estas imágenes existan en la misma carpeta)
        self.icon_paths = {
            "simon": "simondice.png",
            "puzzle": "rompecabezas.png",
            "math": "mate.png",
            "tea": "TEAyudo.png",
            "menu": "menu.png",
            "close": "cerrar.png",
        }
        self.icons = {} # Diccionario para almacenar las PhotoImage

        self.load_icons() # Ahora, cuando se llama a load_icons, self.script_dir ya existe
        self.create_widgets()
        
        self.master.after(100, self.position_corner_buttons)

    def load_icons(self):
        """Carga todas las imágenes de iconos necesarias."""
        # --- Configuración del tamaño deseado para los iconos de juego ---
        game_icon_size = (140, 140) # Define aquí el tamaño deseado para tus iconos de juego
        # ---

        # Creación de iconos de placeholder si no existen
        self.create_placeholder_icon("simondice.png", game_icon_size, (255, 0, 0), "S")
        self.create_placeholder_icon("rompecabezas.png", game_icon_size, (255, 105, 180), "P")
        self.create_placeholder_icon("mate.png", game_icon_size, (0, 128, 0), "M")
        self.create_placeholder_icon("TEAyudo.png", game_icon_size, (0, 191, 255), "T")
        # El tamaño para los iconos de menú y cerrar es más pequeño
        self.create_placeholder_icon("menu.png", (40, 40), (0, 0, 0), "☰")
        self.create_placeholder_icon("cerrar.png", (40, 40), (255, 0, 0), "✕") # El nombre del archivo aquí debe coincidir con el path

        for name, path in self.icon_paths.items():
            try:
                img = Image.open(path)
                if name in ["menu", "close"]:
                    img = img.resize((40, 40), Image.LANCZOS) # Tamaño específico para menú y cerrar
                else:
                    img = img.resize(game_icon_size, Image.LANCZOS)
                self.icons[name] = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print(f"Advertencia: Icono no encontrado en {path}. Intentando cargar placeholder.")
                try:
                    # Intentar cargar el placeholder recién creado o uno existente
                    img = Image.open(path)
                    if name in ["menu", "close"]:
                        img = img.resize((40, 40), Image.LANCZOS)
                    else:
                        img = img.resize(game_icon_size, Image.LANCZOS)
                    self.icons[name] = ImageTk.PhotoImage(img)
                except Exception as ex_placeholder:
                    print(f"Error al cargar el icono placeholder {path}: {ex_placeholder}")
                    self.icons[name] = None
            except Exception as e:
                print(f"Error al cargar el icono {path}: {e}")
                self.icons[name] = None

    def create_placeholder_icon(self, filename_relative, size, color, text):
        """Crea un icono de placeholder si el archivo no existe."""
        # También aquí, construimos la ruta completa para el archivo placeholder
        full_path = os.path.join(self.script_dir, filename_relative) # <--- AÑADE ESTA LÍNEA

        if not os.path.exists(full_path): # <--- USA full_path para verificar si existe
            img = Image.new('RGBA', size, (255, 255, 255, 0)) # Fondo transparente
            draw = ImageDraw.Draw(img)
            
            # Intenta cargar una fuente común o usar la fuente por defecto
            try:
                font = ImageFont.truetype("arial.ttf", int(size[0]*0.4))
            except IOError:
                font = ImageFont.load_default()
            
            if text in ["☰", "✕"]:
                 font_size_menu_close = int(size[0]*0.7)
                 try:
                     font = ImageFont.truetype("arial.ttf", font_size_menu_close)
                 except IOError:
                     font = ImageFont.load_default()
                     if font_size_menu_close > 20:
                         font = ImageFont.load_default(size=20)

                 bbox = draw.textbbox((0,0), text, font=font)
                 text_width = bbox[2] - bbox[0]
                 text_height = bbox[3] - bbox[1]
                 draw.text(((size[0] - text_width) / 2, (size[1] - text_height) / 2), text, font=font, fill=color)
            else:
                 draw.rounded_rectangle((0, 0, size[0], size[1]), radius=size[0]//4, fill=color)
                 
                 text_font_size = int(size[0]*0.6)
                 try:
                    font_game = ImageFont.truetype("arial.ttf", text_font_size)
                 except IOError:
                    font_game = ImageFont.load_default()
                    if text_font_size > 20:
                        font_game = ImageFont.load_default(size=20)
                 
                 bbox = draw.textbbox((0,0), text, font=font_game)
                 text_width = bbox[2] - bbox[0]
                 text_height = bbox[3] - bbox[1]
                 draw.text(((size[0] - text_width) / 2, (size[1] - text_height) / 2 - 5), text, font=font_game, fill=(255,255,255))
            img.save(full_path) # <--- USA full_path para guardar el placeholder
            print(f"Placeholder para {full_path} creado.")


    def create_widgets(self):
        self.main_canvas = tk.Canvas(self.master, bg=self.yellow_bg, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True, padx=40, pady=40)

        canvas_width = 1000 - 2 * 40
        canvas_height = 800 - 2 * 40
        self.round_rect_radius = 40

        self.main_canvas.create_rounded_rectangle(0, 0, canvas_width, canvas_height,
                                                  radius=self.round_rect_radius,
                                                  fill=self.white_frame_bg, outline="", width=0)

        title_label = tk.Label(self.main_canvas, text="Seleccione una actividad",
                               font=("Arial", 28, "bold"),
                               fg=self.text_color,
                               bg=self.white_frame_bg)
        self.main_canvas.create_window(canvas_width / 2, 90, window=title_label, anchor="center")

        game_buttons_frame = tk.Frame(self.main_canvas, bg=self.white_frame_bg)
        self.main_canvas.create_window(canvas_width / 2, canvas_height / 2 + 50, window=game_buttons_frame, anchor="center")

        button_dimensions = {"width": 200, "height": 200}

        # Asegúrate de que los nombres de los iconos aquí coinciden con las claves de self.icons
        self.create_game_button(game_buttons_frame, "Simon dice", self.icons.get("simon"), self.run_game1, self.red_border, 0, 0, button_dimensions)
        self.create_game_button(game_buttons_frame, "Rompecabezas", self.icons.get("puzzle"), self.run_game2, self.pink_border, 0, 1, button_dimensions)
        self.create_game_button(game_buttons_frame, "Matematicas", self.icons.get("math"), self.run_game3, self.green_border, 1, 0, button_dimensions)
        self.create_game_button(game_buttons_frame, "TEAayudo", self.icons.get("tea"), self.run_game4, self.blue_border, 1, 1, button_dimensions)

        if self.icons.get("menu"):
            self.menu_btn = tk.Button(self.master, image=self.icons["menu"], command=self.show_menu,
                                      bd=0, bg=self.yellow_bg, activebackground=self.yellow_bg, relief="flat")
            self.menu_btn.place(x=0, y=0) # Posición temporal, se ajustará en position_corner_buttons

        # Usar self.icons.get("close") para el icono de cerrar
        if self.icons.get("close"):
            self.close_btn = tk.Button(self.master, image=self.icons["close"], command=self.exit_application,
                                       bd=0, bg=self.yellow_bg, activebackground=self.yellow_bg, relief="flat")
        else:
            # Fallback si el icono "cerrar.png" no se carga
            self.close_btn = tk.Button(self.master, text="✕", command=self.exit_application,
                                    font=("Arial", 18, "bold"), fg="#D32F2F", bg=self.yellow_bg,
                                    activebackground=self.yellow_bg, bd=0, padx=10, pady=5)
        self.close_btn.place(x=0, y=0) # Posición temporal, se ajustará en position_corner_buttons


    def position_corner_buttons(self):
        """Ajusta la posición de los botones de esquina después de que la ventana se ha renderizado."""
        button_padding = 35 

        if hasattr(self, 'menu_btn'):
            self.menu_btn.place(x=button_padding, y=button_padding)

        if hasattr(self, 'close_btn'):
            self.close_btn.update_idletasks() # Asegurarse de que el botón se ha renderizado
            
            # Obtener el ancho de la ventana principal
            window_width = self.master.winfo_width()
            
            # Calcular la posición x para el botón de cerrar
            # Restar el ancho del botón y el padding del ancho de la ventana
            x_pos = window_width - self.close_btn.winfo_width() - button_padding
            
            self.close_btn.place(x=x_pos, y=button_padding)


    def create_game_button(self, parent, text, icon_image, command, border_color, row, col, dimensions):
        frame_wrapper = tk.Frame(parent, bg=self.white_frame_bg)
        frame_wrapper.grid(row=row, column=col, padx=25, pady=25)

        button_canvas = tk.Canvas(frame_wrapper, width=dimensions["width"], height=dimensions["height"],
                                  bg=self.white_frame_bg, highlightthickness=0)
        button_canvas.pack()

        # Sombra suave - dibujada ANTES del rectángulo principal
        button_canvas.create_rounded_rectangle(8, 8, dimensions["width"]+8, dimensions["height"]+8,
                                            radius=30, fill="#E0E0E0", outline="", width=0) # Aumentar el offset para una sombra más visible

        # Rectángulo principal (blanco)
        button_canvas.create_rounded_rectangle(0, 0, dimensions["width"], dimensions["height"],
                                            radius=30, fill=self.white_frame_bg, outline=border_color, width=4)

        if icon_image:
            icon_label = tk.Label(button_canvas, image=icon_image, bg=self.white_frame_bg)
            button_canvas.create_window(dimensions["width"] / 2, dimensions["height"] / 2 - 25, window=icon_label, anchor="center")
            icon_label.bind("<Button-1>", lambda e: command())
        else:
            placeholder_label = tk.Label(button_canvas, text="[ICON]", font=("Arial", 12, "bold"), bg=self.white_frame_bg, fg=border_color)
            button_canvas.create_window(dimensions["width"] / 2, dimensions["height"] / 2 - 25, window=placeholder_label, anchor="center")
            placeholder_label.bind("<Button-1>", lambda e: command())

        text_label = tk.Label(button_canvas, text=text, font=("Arial", 16, "bold"), fg=self.text_color, bg=self.white_frame_bg)
        button_canvas.create_window(dimensions["width"] / 2, dimensions["height"] / 2 + 65, window=text_label, anchor="center")
        text_label.bind("<Button-1>", lambda e: command())

        button_canvas.bind("<Button-1>", lambda e: command())
        button_canvas.bind("<Enter>", lambda e: self.on_enter(e, button_canvas, border_color))
        button_canvas.bind("<Leave>", lambda e: self.on_leave(e, button_canvas, border_color))

    def on_enter(self, event, widget_canvas, original_border_color):
        widget_canvas.itemconfig(widget_canvas.find_all()[1], outline="black", width=5) # El segundo elemento es el rectángulo principal
        widget_canvas.config(cursor="hand2")

    def on_leave(self, event, widget_canvas, original_border_color):
        widget_canvas.itemconfig(widget_canvas.find_all()[1], outline=original_border_color, width=4) # Volver al grosor original
        widget_canvas.config(cursor="")

    def run_game1(self):
        """Ejecuta el script 'menu_simondice.py' en la carpeta 'simon dice/menu/'."""
        current_script_dir = os.path.dirname(os.path.abspath(__file__)) 
        
        target_folder_path = os.path.join(current_script_dir, "simon dice", "menu")
        target_script_path = os.path.join(target_folder_path, "menu_simondice.py")

        print(f"DEBUG: Directorio actual del script: {current_script_dir}")
        print(f"DEBUG: Ruta esperada a la carpeta del juego Simon dice: {target_folder_path}")
        print(f"DEBUG: Ruta esperada al script de Simon dice: {target_script_path}")
        
        if os.path.exists(target_script_path):
            self.master.withdraw() 
            try:
                subprocess.Popen([sys.executable, target_script_path])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo iniciar el juego Simon dice: {e}")
                self.master.deiconify() 
        else:
            messagebox.showerror("Error", f"El archivo 'menu_simondice.py' no se encontró en la ruta esperada.\nVerificado: {target_script_path}\nAsegúrate de que la carpeta 'simon dice' y 'menu' dentro de ella existan y contengan el archivo.")


    def run_game2(self):
        """Ejecuta el script 'menu_rompecabezas.py' en la carpeta 'rompecabezas/menu/'."""
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # MODIFICADO: Construye la ruta a la carpeta 'rompecabezas/menu/'
        target_folder_path = os.path.join(current_script_dir, "rompecabezas", "menu")
        
        # Construye la ruta completa al archivo 'menu_rompecabezas.py'
        target_script_path = os.path.join(target_folder_path, "menu_rompecabezas.py")

        print(f"DEBUG: Directorio actual del script: {current_script_dir}")
        print(f"DEBUG: Ruta esperada a la carpeta del juego Rompecabezas: {target_folder_path}")
        print(f"DEBUG: Ruta esperada al script de Rompecabezas: {target_script_path}")
        
        if os.path.exists(target_script_path):
            self.master.withdraw() # Oculta la ventana del menú principal
            try:
                # Usa sys.executable para garantizar que se use el mismo intérprete de Python
                subprocess.Popen([sys.executable, target_script_path])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo iniciar el juego Rompecabezas: {e}")
                self.master.deiconify() # Si hay un error, vuelve a mostrar el menú
        else:
            messagebox.showerror("Error", f"El archivo 'menu_rompecabezas.py' no se encontró en la ruta esperada.\nVerificado: {target_script_path}\nAsegúrate de que la carpeta 'rompecabezas' y 'menu' dentro de ella existan y contengan el archivo.")

    def run_game3(self):
        messagebox.showinfo("Juego", "Iniciando Matematicas...")

    def run_game4(self):
        messagebox.showinfo("Juego", "Iniciando TEAayuda...")

    def show_menu(self):
        messagebox.showinfo("Menú", "Abrir menú de opciones (ej. Ajustes, Acerca de...)")

    def exit_application(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            self.master.destroy()
            sys.exit()

# --- Extensión de Canvas para dibujar rectángulos redondeados ---
def _round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1]
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_rounded_rectangle = _round_rectangle

if __name__ == "__main__":
    root = tk.Tk()
    menu = GameMenu(root)
    root.mainloop()