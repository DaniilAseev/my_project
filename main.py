import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    """Главный класс приложения для обработки изображений.
    
    Предоставляет графический интерфейс для выполнения базовых операций с изображениями:
    загрузка, съемка с камеры, выделение цветовых каналов, изменение размера, яркости,
    рисование кругов и сброс к исходному изображению.
    """
    
    def __init__(self, root):
        """Инициализация приложения.
        
        Args:
            root (tk.Tk): Корневое окно Tkinter.
        """
        self.root = root
        self.root.title("Обработка изображений")
        
        # Максимальные размеры для отображения
        self.max_display_width = 800
        self.max_display_height = 600
        
        self.image = None          # Текущее обработанное изображение
        self.original_image = None # Исходное изображение без изменений
        
        # Создаем фрейм для кнопок в верхней части
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="top", pady=5, fill="x")
        
        # Центрируем кнопки внутри фрейма
        self.center_frame = tk.Frame(self.button_frame)
        self.center_frame.pack()
        
        # Кнопки в один ряд по центру
        buttons = [
            ("Загрузить", self.upload_image),
            ("Камера", self.capture_webcam),
            ("Красный", lambda: self.show_channel("red")),
            ("Зеленый", lambda: self.show_channel("green")),
            ("Синий", lambda: self.show_channel("blue")),
            ("Размер", self.resize_image),
            ("Яркость", self.decrease_brightness),
            ("Круг", self.draw_circle),
            ("Сброс", self.reset_image)
        ]
        
        for text, command in buttons:
            tk.Button(self.center_frame, text=text, command=command, width=10).pack(side="left", padx=2, pady=2)
        
        # Метка для отображения изображения
        self.label = tk.Label(root)
        self.label.pack()

    def upload_image(self):
        """Загружает изображение из файла через диалоговое окно.
        
        Поддерживаемые форматы: JPG, JPEG, PNG.
        В случае ошибки выводит сообщение.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise Exception("Не удалось загрузить изображение")
                self.image = self.original_image.copy()
                self.display_image()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")

    def capture_webcam(self):
        """Захватывает изображение с веб-камеры.
        
        Если камера недоступна или не удалось сделать снимок,
        выводит сообщение об ошибке.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к камере!")
            return
        
        ret, frame = cap.read()
        if ret:
            self.original_image = frame
            self.image = self.original_image.copy()
            self.display_image()
        else:
            messagebox.showerror("Ошибка", "Не удалось сделать фото")
        
        cap.release()

    def display_image(self):
        """Отображает текущее изображение в интерфейсе.
        
        Автоматически масштабирует изображение, если оно превышает
        максимальные размеры для отображения.
        """
        if self.image is not None:
            display_img = self.image.copy()
            height, width = display_img.shape[:2]
            
            if width > self.max_display_width or height > self.max_display_height:
                scale = min(self.max_display_width/width, self.max_display_height/height)
                display_img = cv2.resize(display_img, (0,0), fx=scale, fy=scale)
            
            img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            
            self.label.config(image=img)
            self.label.image = img

    def show_channel(self, channel):
        """Отображает только выбранный цветовой канал изображения.
        
        Args:
            channel (str): Название канала ('red', 'green' или 'blue')
        """
        if self.image is not None:
            b, g, r = cv2.split(self.original_image)
            if channel == "red":
                self.image = cv2.merge((np.zeros_like(b), np.zeros_like(g), r))
            elif channel == "green":
                self.image = cv2.merge((np.zeros_like(b), g, np.zeros_like(r)))
            elif channel == "blue":
                self.image = cv2.merge((b, np.zeros_like(g), np.zeros_like(r)))
            self.display_image()

    def resize_image(self):
        """Изменяет размер изображения через диалоговые окна.
        
        Запрашивает у пользователя новые ширину и высоту,
        затем изменяет размер изображения.
        """
        if self.image is not None:
            try:
                width = simpledialog.askinteger("Изменение размера", "Введите ширину:", minvalue=10, maxvalue=5000)
                if width is None: return
                
                height = simpledialog.askinteger("Изменение размера", "Введите высоту:", minvalue=10, maxvalue=5000)
                if height is None: return
                
                self.image = cv2.resize(self.original_image, (width, height))
                self.display_image()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Неправильные параметры: {str(e)}")

    def decrease_brightness(self):
        """Уменьшает яркость изображения на 50%."""
        if self.image is not None:
            hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
            hsv[:,:,2] = hsv[:,:,2] * 0.5
            self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            self.display_image()

    def draw_circle(self):
        """Рисует круг на изображении по заданным координатам и радиусу.
        
        Запрашивает параметры круга через диалоговые окна.
        """
        if self.image is not None:
            try:
                x = simpledialog.askinteger("Круг", "X координата центра:", minvalue=0, maxvalue=self.image.shape[1])
                if x is None: return
                
                y = simpledialog.askinteger("Круг", "Y координата центра:", minvalue=0, maxvalue=self.image.shape[0])
                if y is None: return
                
                radius = simpledialog.askinteger("Круг", "Радиус круга:", minvalue=1, maxvalue=1000)
                if radius is None: return
                
                self.image = self.original_image.copy()
                cv2.circle(self.image, (x, y), radius, (0, 0, 255), 2)
                self.display_image()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Неправильные параметры: {str(e)}")

    def reset_image(self):
        """Сбрасывает все изменения, возвращая исходное изображение."""
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()