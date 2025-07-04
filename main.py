import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    """Класс для обработки изображений с графическим интерфейсом"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений")
        
        # Настройки отображения
        self.max_display_width = 800
        self.max_display_height = 600
        
        self.image = None          # Текущее изображение
        self.original_image = None # Оригинальное изображение
        
        # Создаем панель кнопок
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="top", pady=5, fill="x")
        
        self.center_frame = tk.Frame(self.button_frame)
        self.center_frame.pack()
        
        # Список кнопок и их функций
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
        
        # Создаем кнопки
        for text, command in buttons:
            btn = tk.Button(self.center_frame, text=text, command=command, width=10)
            btn.pack(side="left", padx=2, pady=2)
            btn.bind("<Enter>", lambda e, t=text: self.show_hint(t))
        
        # Поле для изображения
        self.label = tk.Label(root)
        self.label.pack()
        
        # Подсказки для кнопок
        self.hints = {
            "Загрузить": "Загрузить изображение с компьютера",
            "Камера": "Сделать фото с веб-камеры",
            "Красный": "Показать только красный канал",
            "Зеленый": "Показать только зеленый канал",
            "Синий": "Показать только синий канал",
            "Размер": "Изменить размер изображения",
            "Яркость": "Уменьшить яркость изображения",
            "Круг": "Нарисовать круг на изображении",
            "Сброс": "Вернуть исходное изображение"
        }
        
        # Поле для подсказок
        self.hint_label = tk.Label(root, text="", fg="gray")
        self.hint_label.pack(side="bottom", fill="x")

    def show_hint(self, button_text):
        """Показывает подсказку для кнопки"""
        self.hint_label.config(text=self.hints.get(button_text, ""))

    def upload_image(self):
        """Загрузка изображения из файла"""
        file_types = [("Изображения", "*.jpg *.jpeg *.png"), ("Все файлы", "*.*")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        
        if file_path:
            try:
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise ValueError("Не удалось открыть файл изображения")
                    
                self.image = self.original_image.copy()
                self.display_image()
                messagebox.showinfo("Успех", "Изображение успешно загружено")
                
            except Exception as e:
                error_msg = {
                    "ValueError": "Неподдерживаемый формат изображения",
                    "FileNotFoundError": "Файл не найден",
                    "PermissionError": "Нет доступа к файлу"
                }.get(type(e).__name__, "Ошибка при загрузке изображения")
                
                messagebox.showerror("Ошибка", f"{error_msg}:\n{str(e)}")

    def capture_webcam(self):
        """Захват изображения с камеры"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError("Камера не подключена или нет разрешения")
            
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Не удалось получить изображение с камеры")
                
            self.original_image = frame
            self.image = self.original_image.copy()
            self.display_image()
            messagebox.showinfo("Успех", "Фото с камеры успешно сделано")
            
        except Exception as e:
            error_msg = {
                "RuntimeError": "Проблема с камерой",
                "AttributeError": "Ошибка доступа к камере"
            }.get(type(e).__name__, "Ошибка при работе с камерой")
            
            messagebox.showerror("Ошибка", f"{error_msg}:\n{str(e)}")
            
        finally:
            if 'cap' in locals():
                cap.release()

    def display_image(self):
        """Отображение изображения с масштабированием"""
        if self.image is not None:
            try:
                display_img = self.image.copy()
                h, w = display_img.shape[:2]
                
                # Масштабирование если изображение слишком большое
                if w > self.max_display_width or h > self.max_display_height:
                    scale = min(self.max_display_width/w, self.max_display_height/h)
                    display_img = cv2.resize(display_img, None, fx=scale, fy=scale)
                
                # Конвертация для Tkinter
                img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(img)
                
                self.label.config(image=img)
                self.label.image = img
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось отобразить изображение:\n{str(e)}")

    def show_channel(self, channel):
        """Выделение цветового канала"""
        if self.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
            
        try:
            b, g, r = cv2.split(self.original_image)
            
            if channel == "red":
                self.image = cv2.merge((np.zeros_like(b), np.zeros_like(g), r))
            elif channel == "green":
                self.image = cv2.merge((np.zeros_like(b), g, np.zeros_like(r)))
            elif channel == "blue":
                self.image = cv2.merge((b, np.zeros_like(g), np.zeros_like(r)))
                
            self.display_image()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выделить канал {channel}:\n{str(e)}")

    def resize_image(self):
        """Изменение размера изображения"""
        if self.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
            
        try:
            h, w = self.original_image.shape[:2]
            
            width = simpledialog.askinteger(
                "Ширина", 
                f"Введите новую ширину (10-5000)\nТекущая: {w}",
                minvalue=10, 
                maxvalue=5000,
                parent=self.root
            )
            if width is None: return
            
            height = simpledialog.askinteger(
                "Высота", 
                f"Введите новую высоту (10-5000)\nТекущая: {h}",
                minvalue=10, 
                maxvalue=5000,
                parent=self.root
            )
            if height is None: return
            
            self.image = cv2.resize(self.original_image, (width, height))
            self.display_image()
            messagebox.showinfo("Успех", "Размер изображения изменен")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить размер:\n{str(e)}")

    def decrease_brightness(self):
        """Уменьшение яркости изображения"""
        if self.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
            
        try:
            value = simpledialog.askinteger(
                "Яркость", 
                "На сколько % уменьшить яркость? (1-100)",
                minvalue=1, 
                maxvalue=100,
                parent=self.root
            )
            if value is None: return
            
            hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
            hsv[:,:,2] = np.clip(hsv[:,:,2] * (1 - value/100), 0, 255)
            self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            self.display_image()
            messagebox.showinfo("Успех", f"Яркость уменьшена на {value}%")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить яркость:\n{str(e)}")

    def draw_circle(self):
        """Рисование круга на изображении"""
        if self.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
            
        try:
            h, w = self.original_image.shape[:2]
            
            x = simpledialog.askinteger(
                "Координата X", 
                f"X центра круга (0-{w-1})",
                minvalue=0, 
                maxvalue=w-1,
                parent=self.root
            )
            if x is None: return
            
            y = simpledialog.askinteger(
                "Координата Y", 
                f"Y центра круга (0-{h-1})",
                minvalue=0, 
                maxvalue=h-1,
                parent=self.root
            )
            if y is None: return
            
            max_radius = min(w, h) // 2
            radius = simpledialog.askinteger(
                "Радиус", 
                f"Радиус круга (1-{max_radius})",
                minvalue=1, 
                maxvalue=max_radius,
                parent=self.root
            )
            if radius is None: return
            
            self.image = self.original_image.copy()
            cv2.circle(self.image, (x, y), radius, (0, 0, 255), 2)
            self.display_image()
            messagebox.showinfo("Успех", "Круг успешно нарисован")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось нарисовать круг:\n{str(e)}")

    def reset_image(self):
        """Сброс изменений"""
        if self.original_image is None:
            messagebox.showwarning("Предупреждение", "Нет изображения для сброса")
            return
            
        self.image = self.original_image.copy()
        self.display_image()
        messagebox.showinfo("Сброс", "Изображение восстановлено")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()