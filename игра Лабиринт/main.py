
from pygame import *

# Определяем родительский класс для игровых объектов
class Parents(sprite.Sprite):
  # Конструктор класса
  def __init__(self,image1,x,y,speed):
    # Вызываем конструктор родительского класса
    sprite.Sprite.__init__(self)
     # Загружаем и масштабируем изображение
    self.image = transform.scale(image.load(image1), (100,100))
     # Задаем скорость движения объекта
    self.speed = speed
    # Получаем прямоугольную область для объекта
    self.rect = self.image.get_rect()
    # Устанавливаем начальное горизонтальное положение
    self.rect.x = x
    # Устанавливаем начальное вертикальное положение
    self.rect.y = y
#перерисовка
  # Метод для отображения объекта на экране
  def reset(self):
    # Отображаем объект на игровом окне
    window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрового объекта, управляемого игроком (наследуется от класса Parents)
class Hero(Parents):
  # Метод для обновления состояния объекта
  def update(self):
    # Получаем состояние клавиш управления
    keys = key.get_pressed()
    # Если нажата клавиша влево и объект не выходит за левую границу
    if keys[K_LEFT] and self.rect.x >5 :
      # Двигаем объект влево
      self.rect.x -= self.speed
    # Если нажата клавиша вправо и объект не выходит за правую границу
    if keys[K_RIGHT] and self.rect.x < win_width-80 :
      # Двигаем объект вправо
      self.rect.x += self.speed
    # Если нажата клавиша вверх и объект не выходит за верхнюю границу
    if keys[K_UP] and self.rect.y >5 :
      # Двигаем объект вверх
      self.rect.y -= self.speed
    # Если нажата клавиша вниз и объект не выходит за нижнюю границу
    if keys[K_DOWN] and self.rect.y <win_height-80 :
      # Двигаем объект вниз
      self.rect.y += self.speed
      
# Класс игрового объекта-врага (наследуется от класса Parents)
class EnemyVert(Parents):
  def __init__(self, image1, x, y, speed):
    Parents.__init__(self, image1, x, y, speed)
    self.image = transform.scale(self.image, (160, 160))  # Увеличиваем размер врага до 100x100
  # Начальное направление движения врага
  side = "down"
  # Метод для обновления состояния объекта
  def update(self,y_top, y_bottom):
    # Если объект достиг правой границы
    if self.rect.y <= y_top:
      # Меняем направление движения на правое
      self.side = "down"
    # Если объект достиг левой границы
    if self.rect.y>= y_bottom:
      # Меняем направление движения на левое
      self.side = "up"
    # Если направление движения - влево
    if self.side == "up":
      # Двигаем объект влево
      self.rect.y -=self.speed
    # Если направление движения - вправо
    else:
      # Двигаем объект вправо
      self.rect.y += self.speed


class EnemyHorizont(Parents):
  def __init__(self, image1, x, y, speed):
    Parents.__init__(self, image1, x, y, speed)
    self.image = transform.scale(self.image, (160, 160))  # Увеличиваем размер врага до 100x100
    self.original_image = self.image
    self.image = transform.flip(self.original_image, True, False)
  # Начальное направление движения врага
  side = "left"
  # Метод для обновления состояния объекта
  def update(self,x_right, x_left):
    # Если объект достиг правой границы
    if self.rect.x <= x_right:
      # Меняем направление движения на правое
      self.side = "right"
      self.image = transform.flip(self.original_image, False, False)
    # Если объект достиг левой границы
    if self.rect.x>= x_left:
      # Меняем направление движения на левое
      self.side = "left"
      self.image = transform.flip(self.original_image, True, False)
    # Если направление движения - влево
    if self.side == "left":
      # Двигаем объект влево
      self.rect.x -=self.speed
    # Если направление движения - вправо
    else:
      # Двигаем объект вправо
      self.rect.x += self.speed
      
# Класс игровой стены (наследуется от родительского класса sprite.Sprite)
class Wall(Parents):
  def __init__(self, image, x, y, width, height):
    super().__init__(image, x, y, 0)  # Скорость движения стены равна 0
    # масштабируют изображение стены до заданных размеров и применяют сглаживание изображения
    self.image = transform.scale(self.image, (width, height))
    self.image = transform.smoothscale(self.image, (width, height))
    # создает прямоугольный объект, соответствующий размерам изображения стены
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

  # Метод для отображения объекта на экране
  def draw_wall(self):
    # Отображаем объект на игровом окне
    window.blit(self.image, (self.rect.x, self.rect.y))

#окно
win_width = 900
win_height = 700
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
# Заполняем фон игрового поля
bg_image = image.load("fon.png")
bg_image = transform.scale(bg_image, (win_width, win_height))

#стены
wall_width = 300
wall_height = 300
walls = [Wall("wall1.png", 40, 450, wall_width, wall_height),
         Wall("wall1.png", 40, 300, wall_width, wall_height),
         Wall("wall2.png", -25, 10, wall_width, wall_height),
         Wall("wall1.png", 300, 250, wall_width, wall_height),
         Wall("wall1.png", 300, 100, wall_width, wall_height),
         Wall("wall1.png", 500, 450, wall_width, wall_height),
         Wall("wall1.png", 500, 300, wall_width, wall_height)]

# Создаем управляемый игроком объект
packman = Hero('hero.png',5, win_height-150,5)
# Создаем первый вражеский объект
monster = EnemyHorizont('enemy1.png',win_width-100,200,5)
# Создаем второй вражеский объект
monster2 = EnemyVert('enemy2.png',win_width-650,80,5)
# Создаем финальный игровой объект
final_sprite = Parents('prize.PNG',win_width-130,win_height-130,5)
monster.update(50, win_height - 160)

# Основной игровой цикл

# Флаг окончания игры
finish = False
# Флаг выполнения игрового цикла
run = True
while run:
  # Задержка между кадрами
  time.delay(50)
  # Обработка событий
  for e in event.get():
    # Если пользователь закрыл окно
    if e.type == QUIT:
       # Завершаем игровой цикл
      run = False
  # Отображение фонового изображения
  window.blit(bg_image, (0, 0))
  # Если игра не окончена
  if not finish:
    #отображаем стены
    for wall in walls:
        wall.draw_wall()
    # Обновляем состояние управляемого игроком объекта
    packman.update()
    # Обновляем состояние первого вражеского объекта
    monster.update(410,win_width-85)
    # Обновляем состояние второго вражеского объекта
    monster2.update(10,410-80)
    # Отображаем управляемый игроком объект
    packman.reset()
    # Отображаем первый вражеский объект
    monster.reset()
    # Отображаем второй вражеский объект
    monster2.reset()
    # Отображаем финальный игровой объект
    final_sprite.reset()
    # Если игрок столкнулся с врагом
    if sprite.collide_rect(packman, monster) or sprite.collide_rect(packman,monster2):
      #Устанавливаем флаг окончания игры
      finish = True
      # Загружаем изображение для конечного экрана
      img = transform.scale(image.load('game_over.PNG'), (win_width, win_height))
      # Заполняем игровое окно белым цветом
      window.fill((255,255,255))
      # Отображаем изображение конечного экрана
      window.blit(img,(0,0))
    # Если игрок достиг финального игрового объекта
    if sprite.collide_rect(packman,final_sprite):
      # Устанавливаем флаг окончания игры
      finish = True
      # Загружаем изображение для конечного экрана
      img = transform.scale(image.load('winning.PNG'), (win_width, win_height))
       # Заполняем игровое окно белым цветом
      window.fill((255,255,255))
      # Отображаем изображение конечного экрана
      window.blit(img,(0,0))
    # Обновляем экран игрового окна
    display.update()
      