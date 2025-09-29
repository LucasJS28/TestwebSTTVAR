import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QStackedWidget, 
                             QColorDialog, QSlider, QFontComboBox, QFrame, QGraphicsDropShadowEffect,
                             QGridLayout) # Se añade QGridLayout
from PyQt5.QtGui import QIcon, QColor, QFont, QPainter, QBrush, QPen, QPainterPath, QPixmap, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QRect, QByteArray, QSize

# --- INICIO DE LA IMPORTACIÓN DE ICONOS (RECURSOS) ---
def create_icon_from_svg(svg_data_str: str, color: str) -> QIcon:
    """Crea un QIcon a partir de datos SVG, reemplazando el color de relleno."""
    final_svg = svg_data_str.replace('fill="white"', f'fill="{color}"')
    byte_array = QByteArray(final_svg.encode('utf-8'))
    pixmap = QPixmap()
    pixmap.loadFromData(byte_array)
    return QIcon(pixmap)

# Datos SVG de los iconos (color blanco por defecto)
icon_data = {
    "mic": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.49 6-3.31 6-6.72h-1.7z"/></svg>',
    "mic_off": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 11h-1.7c0 .58-.1 1.13-.27 1.64l1.27 1.27c.44-.88.7-1.87.7-2.91zm-6 5.1c1.13 0 2.16-.39 3-1.02l-1.46-1.46c-.47.29-1.02.48-1.54.48V14c1.66 0 3-1.34 3-3V5c0-1.06-.55-2-1.33-2.54l-2.09 2.09c.27.16.52.36.72.6V11c0 .19-.03.37-.08.54l-1.41-1.41C11.89 9.58 12 8.8 12 8V7h-1.7l-2-2H12c1.66 0 3 1.34 3 3v.18l-3-3V5c0-1.66-1.34-3-3-3s-3 1.34-3 3v1.18l-1.4-1.4C5.55 5 6.7 4 8 4c.48 0 .93.11 1.33.3L1.39 4.22 2.8 5.63 9 11.83V14c0 1.66 1.34 3 3 3v2.28c-3.28-.49-6-3.31-6-6.72H5c0 3.41 2.72 6.23 6 6.72V22h2v-1.28c.45-.07.88-.2 1.3-.38l.64.64 1.41-1.41-11.7-11.7z"/></svg>',
    "play": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>',
    "settings": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65C14.46 2.18 14.25 2 14 2h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24-.42-.12-.64l2 3.46c.12.22.39.3.61.22l2.49 1c.52.4 1.08.73 1.69.98l.38 2.65c.03.24.24.42.49.42h4c.25 0 .46-.18.49.42l.38-2.65c.61-.25 1.17-.59-1.69.98l2.49 1c.23.09.49 0 .61.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/></svg>',
    "unlock": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 17c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm6-9h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6h1.9c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm0 12H6V10h12v10z"/></svg>',
    "lock": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>',
    "record_active": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/></svg>',
    "stop": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M6 6h12v12H6z"/></svg>',
    "palette": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9c.83 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.01-.23-.26-.38-.61-.38-.99 0-.83.67-1.5 1.5-1.5H16c2.76 0 5-2.24 5-5 0-4.42-4.03-8-9-8zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 9 6.5 9 8 9.67 8 10.5 7.33 12 6.5 12zm3-4C8.67 8 8 7.33 8 6.5S8.67 5 9.5 5s1.5.67 1.5 1.5S10.33 8 9.5 8zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 5 14.5 5s1.5.67 1.5 1.5S15.33 8 14.5 8zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 9 17.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>',
    "font_color": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M9.93 13.5h4.14L12 7.98zM20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-4.05 16.5-1.14-3H9.17l-1.12 3H5.96l5.11-13h1.86l5.11 13h-2.09z"/></svg>',
    "transparency": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6v12z"/></svg>',
    "minus": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M5 11h14v2H5z"/></svg>',
    "plus": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"/></svg>',
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 96 960 960" width="24" fill="white"><path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/></svg>',
    "font_family": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M5 4v3h5.5v12h3V7H19V4z"/></svg>',
    "language": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>',
}
# --- FIN DE LA IMPORTACIÓN DE ICONOS ---

class OptionsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(6)
        self.background_widget = QFrame(self)
        self.background_widget.setObjectName("optionsMenuBackground")
        layout_container = QHBoxLayout(self.background_widget)
        layout_container.setContentsMargins(4, 4, 4, 4)
        layout_container.setSpacing(6)
        self.main_layout.addWidget(self.background_widget)
        self.lock_btn = self._create_menu_button(icon_data["unlock"], "Bloquear posición")
        self.lock_btn.setCheckable(True)
        self.rec_btn = self._create_menu_button(icon_data["stop"], "Detener grabación")
        self.rec_btn.setObjectName("rec_btn")
        self.rec_btn.setCheckable(True)
        self.rec_btn.setChecked(True)
        self.mute_btn = self._create_menu_button(icon_data["mic"], "Silenciar micrófono")
        self.mute_btn.setCheckable(True)
        self.bg_color_btn = self._create_menu_button(icon_data["palette"], "Color de fondo")
        self.font_color_btn = self._create_menu_button(icon_data["font_color"], "Color de fuente")
        self.language_selector_wrapper = QWidget()
        self.language_selector_wrapper.setObjectName("menuItemContainer")
        lang_layout = QHBoxLayout(self.language_selector_wrapper)
        lang_layout.setContentsMargins(4, 0, 4, 0)
        lang_layout.setSpacing(4)
        lang_icon = QLabel()
        lang_icon.setPixmap(create_icon_from_svg(icon_data["language"], "white").pixmap(16, 16))
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Español", "English", "Français"])
        self.language_selector.setCurrentText("Español")
        self.language_selector.setFixedWidth(80)
        lang_layout.addWidget(lang_icon)
        lang_layout.addWidget(self.language_selector)
        opacity_widget = QWidget()
        opacity_widget.setObjectName("menuItemContainer")
        opacity_layout = QHBoxLayout(opacity_widget)
        opacity_layout.setContentsMargins(4, 0, 4, 0)
        opacity_layout.setSpacing(4)
        opacity_icon = QLabel()
        opacity_icon.setPixmap(create_icon_from_svg(icon_data["transparency"], "white").pixmap(16, 16))
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(85)
        self.opacity_slider.setFixedWidth(50)
        opacity_layout.addWidget(opacity_icon)
        opacity_layout.addWidget(self.opacity_slider)
        self.font_selector_wrapper = QWidget()
        self.font_selector_wrapper.setObjectName("menuItemContainer")
        font_layout = QHBoxLayout(self.font_selector_wrapper)
        font_layout.setContentsMargins(4, 0, 4, 0)
        font_layout.setSpacing(4)
        font_icon = QLabel()
        font_icon.setPixmap(create_icon_from_svg(icon_data["font_family"], "white").pixmap(16, 16))
        self.font_selector = QFontComboBox()
        self.font_selector.setEditable(False)
        self.font_selector.setFixedWidth(120)
        font_layout.addWidget(font_icon)
        font_layout.addWidget(self.font_selector)
        self.decrease_font_btn = self._create_menu_button(icon_data["minus"], "Disminuir fuente")
        self.increase_font_btn = self._create_menu_button(icon_data["plus"], "Aumentar fuente")
        layout_container.addWidget(self.lock_btn)
        layout_container.addWidget(self._create_divider())
        layout_container.addWidget(self.rec_btn)
        layout_container.addWidget(self.mute_btn)
        layout_container.addWidget(self._create_divider())
        layout_container.addWidget(self.bg_color_btn)
        layout_container.addWidget(self.font_color_btn)
        layout_container.addWidget(self.language_selector_wrapper)
        layout_container.addWidget(opacity_widget)
        layout_container.addWidget(self.font_selector_wrapper)
        layout_container.addWidget(self.decrease_font_btn)
        layout_container.addWidget(self.increase_font_btn)
        self.setLayout(self.main_layout)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def _create_menu_button(self, svg_data, tooltip):
        btn = QPushButton()
        btn.setIcon(create_icon_from_svg(svg_data, "white"))
        btn.setIconSize(QSize(16, 16))
        btn.setToolTip(tooltip)
        btn.setFixedSize(30, 30)
        btn.setObjectName("menuButton")
        return btn

    def _create_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setObjectName("divider")
        divider.setFixedWidth(1)
        return divider
        
    def show_menu(self):
        self.setWindowOpacity(0.0)
        self.show()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def hide_menu(self):
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.hide_after_animation)
        self.animation.start()
    
    def hide_after_animation(self):
        self.hide()
        try:
            self.animation.finished.disconnect(self.hide_after_animation)
        except TypeError:
            pass

class SubtitleCapsule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 0)  # Altura inicial 0, se ajustará dinámicamente

        self._is_locked = False
        self.bg_color = QColor(25, 25, 25, int(0.85 * 255))
        self.font_color = QColor("#f5f5f5")
        self.current_font = QFont("Segoe UI", 16)
        self.current_language = "Español"
        
        self.offset = QPoint()
        self._resizing = False
        self._edge = 0
        self.initial_pos = QPoint()
        self.initial_geom = QRect()
        self.setMouseTracking(True)

        self.options_menu = OptionsMenu(self)
        # Establecer la fuente inicial en el combo box para que muestre todas las fuentes disponibles correctamente
        self.options_menu.font_selector.setCurrentFont(self.current_font)

        main_layout = QVBoxLayout(self)
        # --- (MODIFICADO) Reducir el margen exterior para la sombra ---
        main_layout.setContentsMargins(10, 10, 10, 10) 

        self.content_frame = QFrame(self)
        self.content_frame.setObjectName("contentFrame")
        self.content_frame.setMouseTracking(True)
        
        shadow = QGraphicsDropShadowEffect(self)
        # --- (MODIFICADO) Reducir el tamaño y la distancia de la sombra ---
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 140))
        self.content_frame.setGraphicsEffect(shadow)

        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setMouseTracking(True)
        self.initial_screen = self._create_initial_screen()
        self.countdown_screen = self._create_countdown_screen()
        self.main_screen = self._create_main_screen()

        self.stacked_widget.addWidget(self.initial_screen)
        self.stacked_widget.addWidget(self.countdown_screen)
        self.stacked_widget.addWidget(self.main_screen)
        
        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.content_frame)
        
        self._load_styles()
        self._connect_signals()

        self.stacked_widget.setCurrentWidget(self.initial_screen)
        self.update_background_color()
        # Ajustar altura dinámicamente al contenido del menú inicial
        self.resize(800, self.sizeHint().height())

    def _create_initial_screen(self):
        widget = QWidget()
        widget.setMouseTracking(True)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(25)
        
        # Contenedor para el título con icono de micrófono
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        mic_icon = QLabel()
        mic_icon.setPixmap(create_icon_from_svg(icon_data["mic"], "#0077b6").pixmap(28, 28))
        sttvar_label = QLabel("STTVAR")
        sttvar_label.setObjectName("welcomeTitle")
        title_layout.addWidget(mic_icon)
        title_layout.addWidget(sttvar_label)
        layout.addWidget(title_container)
        
        self.mic_selector = QComboBox()
        self.mic_selector.addItem("Micrófono Predeterminado")
        self.mic_selector.setItemIcon(0, create_icon_from_svg(icon_data["mic"], "#0077b6"))
        layout.addWidget(self.mic_selector)
        
        layout.addStretch(1)  # Push buttons to the right
        
        self.start_btn = QPushButton("Iniciar")
        self.start_btn.setIcon(create_icon_from_svg(icon_data["play"], "white"))
        self.start_btn.setObjectName("startButton")
        layout.addWidget(self.start_btn)
        
        self.initial_options_btn = QPushButton()
        self.initial_options_btn.setIcon(create_icon_from_svg(icon_data["menu"], "white"))
        self.initial_options_btn.setObjectName("optionsToggleBtn")
        layout.addWidget(self.initial_options_btn)
        
        self.close_btn = QPushButton()
        self.close_btn.setIcon(create_icon_from_svg(icon_data["close"], "#a0a0a0"))
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setToolTip("Cerrar aplicación")
        layout.addWidget(self.close_btn)
        
        return widget

    def _create_countdown_screen(self):
        widget = QWidget()
        widget.setMouseTracking(True)
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        self.countdown_label = QLabel("3")
        self.countdown_label.setObjectName("countdownTimer")
        layout.addWidget(self.countdown_label)
        return widget

    def _create_main_screen(self):
        # Widget principal de esta pantalla
        widget = QWidget()
        widget.setMouseTracking(True)
        
        # Usar un QGridLayout para posicionar el texto en el centro y el botón en una esquina
        grid_layout = QGridLayout(widget)
        grid_layout.setContentsMargins(20, 10, 10, 10) # Márgenes para padding
        
        # --- Crear los widgets que irán en la pantalla ---
        self.transcript_text = QLabel("Ahora puedes ajustar el tamaño como quieras. ¡Poder total!")
        self.transcript_text.setWordWrap(True)
        self.transcript_text.setAlignment(Qt.AlignCenter)
        self.transcript_text.setMouseTracking(True)
        
        self.options_btn = QPushButton()
        self.options_btn.setIcon(create_icon_from_svg(icon_data["menu"], "white"))
        self.options_btn.setObjectName("optionsToggleBtn")
        
        # --- Configurar la cuadrícula para centrar el texto ---
        # Añadir espacio elástico (stretch) en las filas superior e inferior para empujar el contenido a la fila central
        grid_layout.setRowStretch(0, 1) # Fila superior elástica
        grid_layout.setRowStretch(2, 1) # Fila inferior elástica
        # Permitir que la columna del texto se expanda horizontalmente
        grid_layout.setColumnStretch(0, 1)
        
        # --- Añadir los widgets a la cuadrícula ---
        # Colocar el botón en la celda superior derecha (fila 0, columna 1)
        grid_layout.addWidget(self.options_btn, 0, 1, Qt.AlignTop | Qt.AlignRight)
        # Colocar el texto en la celda del medio (fila 1, columna 0)
        grid_layout.addWidget(self.transcript_text, 1, 0, 1, 2) # El texto ocupa 2 columnas para un mejor ajuste
        
        return widget

    def _connect_signals(self):
        self.start_btn.clicked.connect(self.start_countdown)
        self.close_btn.clicked.connect(QApplication.instance().quit)
        self.initial_options_btn.clicked.connect(self.toggle_options_menu)
        self.options_btn.clicked.connect(self.toggle_options_menu)
        menu = self.options_menu
        menu.lock_btn.toggled.connect(self.toggle_lock)
        menu.rec_btn.toggled.connect(self.toggle_recording)
        menu.bg_color_btn.clicked.connect(self.open_bg_color_picker)
        menu.font_color_btn.clicked.connect(self.open_font_color_picker)
        menu.opacity_slider.valueChanged.connect(self.change_opacity)
        menu.font_selector.currentFontChanged.connect(self.change_font_family)
        menu.language_selector.currentTextChanged.connect(self.change_language)
        menu.increase_font_btn.clicked.connect(lambda: self.change_font_size(1.1))
        menu.decrease_font_btn.clicked.connect(lambda: self.change_font_size(1/1.1))

    def change_language(self, lang):
        self.current_language = lang

    def start_countdown(self):
        self.stacked_widget.setCurrentWidget(self.countdown_screen)
        self.count = 3
        self.countdown_label.setText(str(self.count))
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.count -= 1
        self.countdown_label.setText(str(self.count))
        if self.count <= 0:
            self.countdown_timer.stop()
            self.show_main_screen()

    def show_main_screen(self):
        # --- (MODIFICADO) Calcular la altura deseada: min(40, 10% del alto de la pantalla) ---
        screen_height = QApplication.instance().desktop().screenGeometry().height()
        desired_height = min(40, int(screen_height * 0.1))
        self.resize(self.width(), desired_height)
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def go_to_initial_screen(self):
        self.setMinimumSize(0,0) # Permitir que la pantalla inicial sea de cualquier tamaño
        self.stacked_widget.setCurrentWidget(self.initial_screen)
        # Ajustar altura dinámicamente al contenido del menú inicial
        self.resize(800, self.sizeHint().height())
        self.options_menu.hide_menu()
        
    def toggle_options_menu(self):
        if self.options_menu.isVisible():
            self.options_menu.hide_menu()
        else:
            frame_global_pos = self.content_frame.mapToGlobal(QPoint(0, 0))
            frame_width = self.content_frame.width()
            menu_size = self.options_menu.sizeHint()
            menu_width = menu_size.width()
            menu_height = menu_size.height()
            x = frame_global_pos.x() + (frame_width - menu_width) / 2
            y = frame_global_pos.y() - menu_height - 10
            self.options_menu.move(int(x), int(y))
            self.options_menu.show_menu()

    def toggle_lock(self, locked):
        # --- (MODIFICADO) Se quita la llamada a la función eliminada ---
        self._is_locked = locked
        if locked:
            self.options_menu.lock_btn.setIcon(create_icon_from_svg(icon_data["lock"], "white"))
            self.setFixedSize(self.size())
        else:
            self.options_menu.lock_btn.setIcon(create_icon_from_svg(icon_data["unlock"], "white"))
            self.setMinimumSize(0, 0) # La forma más simple de quitar el límite
            self.setMaximumSize(16777215, 16777215)

    def toggle_recording(self, recording):
        if recording:
            self.options_menu.rec_btn.setIcon(create_icon_from_svg(icon_data["stop"], "white"))
            self.transcript_text.setText("Grabación iniciada...")
        else:
            self.options_menu.rec_btn.setIcon(create_icon_from_svg(icon_data["record_active"], "white"))
            self.transcript_text.setText("Grabación detenida.")
            QTimer.singleShot(1000, self.go_to_initial_screen)

    def open_bg_color_picker(self):
        color = QColorDialog.getColor(self.bg_color, self, "Seleccionar color de fondo")
        if color.isValid():
            self.bg_color.setRgb(color.red(), color.green(), color.blue(), self.bg_color.alpha())
            self.update_background_color()

    def open_font_color_picker(self):
        color = QColorDialog.getColor(self.font_color, self, "Seleccionar color de fuente")
        if color.isValid():
            self.font_color = color
            self.update_transcript_style()
    
    def change_opacity(self, value):
        self.bg_color.setAlpha(int(value * 2.55))
        self.update_background_color()

    def update_background_color(self):
        self.content_frame.setStyleSheet(f"""
            #contentFrame {{
                background-color: {self.bg_color.name(QColor.HexArgb)};
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 28px;
            }}
        """)

    def change_font_family(self, font):
        self.current_font.setFamily(font.family())
        self.update_transcript_style()

    def change_font_size(self, factor):
        new_size = self.current_font.pointSizeF() * factor
        if new_size < 6: new_size = 6 
        self.current_font.setPointSizeF(new_size)
        self.update_transcript_style()

    def update_transcript_style(self):
        self.transcript_text.setFont(self.current_font)
        self.transcript_text.setStyleSheet(f"color: {self.font_color.name()}; background-color: transparent;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._is_locked:
            self._edge = self._get_edge(event.pos())
            if self._edge != 0:
                self._resizing = True
                self.initial_pos = event.globalPos()
                self.initial_geom = self.geometry()
            elif self.content_frame.geometry().contains(event.pos()):
                self._resizing = False
                self.offset = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._edge = 0
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if not self._is_locked:
            if self._resizing:
                delta = event.globalPos() - self.initial_pos
                new_rect = QRect(self.initial_geom)
                
                if self._edge in [1, 7, 3]: new_rect.setLeft(self.initial_geom.left() + delta.x())
                if self._edge in [1, 5, 2]: new_rect.setTop(self.initial_geom.top() + delta.y())
                if self._edge in [2, 8, 4]: new_rect.setRight(self.initial_geom.right() + delta.x())
                if self._edge in [3, 6, 4]: new_rect.setBottom(self.initial_geom.bottom() + delta.y())

                self.setGeometry(new_rect)
            elif event.buttons() & Qt.LeftButton and not self._resizing:
                self.move(event.globalPos() - self.offset)
            else:
                current_edge = self._get_edge(event.pos())
                if current_edge != self._edge:
                    self._edge = current_edge
                    self._update_cursor_shape(self._edge)
    
    def _get_edge(self, pos):
        if self._is_locked: return 0
        margin = 15
        rect = self.content_frame.geometry()
        on_left = abs(pos.x() - rect.left()) < margin
        on_right = abs(pos.x() - rect.right()) < margin
        on_top = abs(pos.y() - rect.top()) < margin
        on_bottom = abs(pos.y() - rect.bottom()) < margin
        if on_top and on_left: return 1
        if on_top and on_right: return 2
        if on_bottom and on_left: return 3
        if on_bottom and on_right: return 4
        if on_top: return 5
        if on_bottom: return 6
        if on_left: return 7
        if on_right: return 8
        return 0

    def _update_cursor_shape(self, edge):
        cursors = { 
            0: Qt.ArrowCursor, 1: Qt.SizeFDiagCursor, 2: Qt.SizeBDiagCursor, 
            3: Qt.SizeBDiagCursor, 4: Qt.SizeFDiagCursor, 5: Qt.SizeVerCursor, 
            6: Qt.SizeVerCursor, 7: Qt.SizeHorCursor, 8: Qt.SizeHorCursor 
        }
        self.setCursor(cursors.get(edge, Qt.ArrowCursor))

    def _load_styles(self):
        self.setStyleSheet("""
            #optionsMenuBackground { 
                background-color: rgba(40, 40, 40, 0.95); 
                border: 1px solid rgba(255, 255, 255, 0.2); 
                border-radius: 20px; 
            }
            #contentFrame, #contentFrame * { 
                color: #f5f5f5; 
                /* REMOVIDO: font-family para no sobrescribir cambios dinámicos */
            }
            #contentFrame { border-radius: 28px; }
            #welcomeTitle { 
                font-size: 24px; 
                font-weight: 700; 
                background-color: transparent; 
                color: #0077b6;
            }
            #countdownTimer { 
                font-size: 90px; 
                font-weight: bold; 
                color: white; 
                background-color: transparent; 
            }
            QComboBox { 
                padding: 8px 20px 8px 8px; 
                border-radius: 10px; 
                border: 1px solid rgba(255, 255, 255, 0.2); 
                background-color: rgba(40, 40, 40, 0.9); 
                font-size: 14px; 
                min-width: 120px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 16px;
                border-left-width: 1px;
                border-left-color: rgba(255,255,255,0.2);
                border-left-style: solid;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: rgba(40,40,40,0.9);
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
                image: none;
            }
            QComboBox::drop-down:hover {
                background-color: rgba(255,255,255,0.1);
            }
            QComboBox::drop-down { border: none; }
            #startButton { 
                padding: 14px 35px; 
                font-size: 16px; 
                font-weight: bold; 
                color: white; 
                background-color: #0077b6; 
                border: none; 
                border-radius: 14px; 
            }
            #startButton:hover { 
                background-color: #023e8a; 
                box-shadow: 0 4px 12px rgba(0, 119, 182, 0.3);
            }
            #closeButton { 
                background: transparent; 
                border: none; 
                padding: 8px; 
                border-radius: 10px; 
            }
            #closeButton:hover { 
                background-color: rgba(255, 255, 255, 0.15); 
            }
            #optionsToggleBtn { 
                background: transparent; 
                border: none; 
                padding: 8px; 
                border-radius: 10px; 
            }
            #optionsToggleBtn:hover { 
                background-color: rgba(255, 255, 255, 0.15); 
            }
            #menuButton { 
                background: rgba(255, 255, 255, 0.15); 
                border: none; 
                border-radius: 10px; 
            }
            #menuButton:hover { 
                background-color: rgba(255, 255, 255, 0.25); 
            }
            #menuButton:checked { 
                background-color: #0077b6; 
            }
            #menuButton:checked:hover { 
                background-color: #023e8a; 
            }
            QPushButton#rec_btn:checked { 
                background-color: #e63946; 
            }
            QPushButton#rec_btn:checked:hover { 
                background-color: #d90429; 
            }
            #divider { 
                background-color: rgba(255, 255, 255, 0.25); 
            }
            #menuItemContainer { 
                background: rgba(255, 255, 255, 0.15); 
                border-radius: 10px; 
            }
            #menuItemContainer:hover { 
                background-color: rgba(255, 255, 255, 0.25); 
            }
            #menuItemContainer QFontComboBox { 
                background: transparent; 
                border: none; 
                color: #f5f5f5; 
                padding-left: 4px; 
            }
            QComboBox QAbstractItemView { 
                background-color: rgba(40, 40, 40, 0.98); 
                border: 1px solid rgba(255, 255, 255, 0.2); 
                border-radius: 8px; 
                color: #f5f5f5; 
                selection-background-color: #0077b6; 
            }
            QComboBox QAbstractItemView::item { 
                padding: 6px; 
            }
            QComboBox QAbstractItemView QScrollBar:vertical { 
                background: rgba(255, 255, 255, 0.15); 
                border-radius: 4px; 
                width: 8px; 
            }
            QComboBox QAbstractItemView QScrollBar::handle:vertical { 
                background: #f5f5f5; 
                border-radius: 4px; 
            }
            QSlider::groove:horizontal { 
                height: 3px; 
                background: rgba(255, 255, 255, 0.4); 
                border-radius: 2px; 
            }
            QSlider::handle:horizontal { 
                width: 14px; 
                height: 14px; 
                background: #f5f5f5; 
                border-radius: 7px; 
                border: 1px solid rgba(0,0,0,0.2); 
                margin: -5px 0; 
            }
        """)
        self.update_transcript_style()  # Asegurar inicialización de fuente
        self.transcript_text.setFont(self.current_font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubtitleCapsule()

    # --- INICIO: Lógica para centrar la ventana ---
    # Obtiene la geometría del marco de la ventana (incluyendo la barra de título).
    frame_geometry = window.frameGeometry()
    # Obtiene el punto central de la pantalla disponible (excluyendo la barra de tareas).
    center_point = QApplication.desktop().availableGeometry().center()
    # Mueve el rectángulo de la geometría del marco para que su centro coincida con el centro de la pantalla.
    frame_geometry.moveCenter(center_point)
    # Mueve la esquina superior izquierda de la ventana a la esquina superior izquierda del rectángulo calculado.
    window.move(frame_geometry.topLeft())
    # --- FIN: Lógica para centrar la ventana ---

    window.show()
    sys.exit(app.exec_())