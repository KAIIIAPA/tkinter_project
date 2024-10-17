import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)


    def setup_ui(self):
        '''
        :return: Отображение панели инструментов (выбор цвета кисти, выбор размера кисти, очистка экрана,
        сохранение рисунка и применение ластика)
        '''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Добавление горячей клавиши Control-S для вызова функции save_image
        self.root.bind('<Control-s>', lambda event: self.save_image())

        # Добавление горячей клавиши Control-C для вызова функции choose_color
        self.root.bind('<Control-c>', lambda event: self.choose_color())

        # Создаем объект OptionMenu и связываем его с переменной self.selected_brush_size
        sizes = [1, 2, 5, 10]
        self.selected_brush_size = tk.StringVar()
        self.selected_brush_size.set(sizes[0])  # Устанавливаем начальное значение
        option_menu = tk.OptionMenu(control_frame, self.selected_brush_size, *sizes)
        option_menu.pack(side=tk.LEFT)

        # Добавляем обработчик события для обновления размера кисти при изменении выбора
        self.color_pen_previous = ''
        self.selected_brush_size.trace('w', self.update_brush_size)
        self.eraser_button = tk.Button(control_frame, text="Ластик", command=lambda: self.set_eraser())
        self.eraser_button.pack(side='left')



    def set_eraser(self):
        '''
        :return: Возвращает ластик или кисть
        '''
        if self.eraser_button['text'] == "Ластик":
            self.color_pen_previous = self.pen_color
            self.pen_color = 'white'
            self.eraser_button['text'] = "Кисть"
        else:
            self.pen_color = self.color_pen_previous
            self.eraser_button['text'] = "Ластик"

    def update_brush_size(self, name, index, mode):
        """
        :return: Возвращает необходимый размер кисти
        """
        try:
            size = int(self.selected_brush_size.get())
            self.selected_brush_size.set(size)
        except ValueError:
            pass

    def paint(self, event):
        """
        :return: Возвращает в выбранном цвете проведенный контур
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.selected_brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=int(self.selected_brush_size.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        :param event:
        :return: Метод, который срабатывает при отпускании кнопки мыши.
        Он обнуляет последние известные координаты (self.last_x, self.last_y),
        предотвращая дальнейшее рисование до следующего щелчка мышью.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        :return: Отчищает рабочую область
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        :return: Возвращает выбранный цвет кисти
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        """
        :return: Сохраняет рисунок
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def pick_color(self, event):
        """Метод выбора цвета пипеткой"""
        x, y = event.x, event.y
        pixel_color = self.image.getpixel((x, y))[:3]  # берем RGB компоненты без альфа-канала
        hex_color = "#{:02X}{:02X}{:02X}".format(*pixel_color)
        self.pen_color = hex_color
        print(f"Выбран цвет: {hex_color}")

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()