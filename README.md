ИНСТРУКЦИЯ ПО СБОРКЕ И ЗАПУСКУ ПРИЛОЖЕНИЯ

1. Подготовка
Зайдите в командную строку и убедитесь, что на вашем компьютере установлен Python (рекомендуемая версия - 3.9 или выше). Проверить можно следующей командой:

    python --version

2. Создание и активация виртуального окружения

В командной строке откройте папку, где находится приложение.

Чтобы перейти в директорию выполните команду:

    cd C:\путь\к\директории

Затем выполните следующую команду:

    python -m venv myenv - команда, которая создаёт виртуальное окружение

    myenv\Scripts\activate (для Windows) - команда, которая активирует виртуальное окружение

    source venv/bin/activate (для Linux/macOS) - команда, которая активирует виртуальное окружение

3. Скачивание нужных библиотек

В командной строке выполните следующие команды:

    pip install torch==1.11.0+cpu torchvision==0.12.0+cpu torchaudio==0.11.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

    pip install opencv-python pillow numpy

4. Запуск приложения

Для того чтобы запустить программу, выполните следующую команду:

    python main.py

Инструкция по использованию приложения

5. Загрузка изображения
Нажмите кнопку "Загрузить"

В открывшемся окне выберите файл изображения (поддерживаются форматы JPG, JPEG, PNG)

Изображение появится в основном окне приложения

6. Съемка с камеры
Нажмите кнопку "Камера"

Разрешите доступ к веб-камере, если потребуется

Приложение сделает снимок и отобразит его в окне

7. Выделение цветовых каналов
Используйте кнопки:

"Красный" - оставляет только красный канал

"Зеленый" - оставляет только зеленый канал

"Синий" - оставляет только синий канал

8. Изменение размера изображения
Нажмите кнопку "Размер"

Введите желаемую ширину (от 10 до 5000 пикселей)

Введите желаемую высоту (от 10 до 5000 пикселей)

Изображение будет масштабировано до указанных размеров

9. Изменение яркости
Нажмите кнопку "Яркость"

Яркость изображения автоматически уменьшится на 50%

10. Рисование круга
Нажмите кнопку "Круг"

Введите координаты центра круга (X и Y)

Введите радиус круга (от 1 до 1000)

На изображении появится красный круг с указанными параметрами

11. Сброс изменений
Нажмите кнопку "Сброс"

Все изменения будут отменены, изображение вернется к исходному виду