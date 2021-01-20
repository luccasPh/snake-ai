from PyQt5 import QtGui, QtCore, QtWidgets
from .population import Population

from src.snake import Snake


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QWidget { background: #9CCF4A }")
        self.setFixedSize(730, 410)
        self.setWindowTitle("SnakeAI")
        self.population = Population(10, 28, (2, 10), 4)
        self.population.start_population(load=True)
        self.timer = QtCore.QBasicTimer()
        self.next_snake = 0
        self.show()
        self.start()

    def start(self):
        self.timer.start(5, self)
        self.update()

    def new_game(self):
        self.population.new_generations()
        self.next_snake = 0
        self.start()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_wall(qp)
        snake = self.population.snakes[self.next_snake]
        if snake.died:
            snake.calc_fitness()
            if snake.score > self.population.records[1]:
                self.population.records[1] = snake.score

            if snake.life_time > self.population.records[2]:
                self.population.records[2] = snake.life_time
            self.next_snake += 1
        else:
            snake.place_food()
            self.draw_food(snake.food[1], qp)
            snake.brain(self.population.net)
            self.draw_snake(snake, qp)
            snake.move()

        self.draw_text(event, qp)
        qp.end()

    def draw_food(self, food, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 128, 0, 255))
        qp.drawRect(food[0], food[1], 10, 10)

    def draw_snake(self, snake: Snake, qp: QtGui.QPainter):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(230, 0, 0, 230))
        for body in snake.body:
            qp.drawRect(body[0], body[1], 10, 10)

    def draw_wall(self, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(25, 80, 0, 160))
        qp.drawRect(0, 0, 800, 20)
        qp.drawRect(0, 20, 20, 360)
        qp.drawRect(380, 20, 800, 360)
        qp.drawRect(0, 380, 800, 500)

    def draw_text(self, event, qp):
        qp.setPen(QtGui.QColor(204, 0, 0))
        qp.setFont(QtGui.QFont("Serif", 11))
        qp.drawText(20, 400, f"REMAINING: {self.population.size - self.next_snake}")

        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setFont(QtGui.QFont("Serif", 11))
        qp.drawText(400, 30, f"GENERATION: {self.population.generation}")
        qp.drawText(400, 60, f"HIGH SCORE: {self.population.get_high_score()}")
        qp.drawText(400, 90, f"HIGH LIFE TIME: {self.population.get_high_life_time()}")
        qp.drawText(
            400, 120, f"HIGH FITNESS: {round(self.population.get_high_fitness(),2)}"
        )
        qp.drawText(
            400, 180, f"AVERAGE HIGH SCORE: {int(round(self.population.averages[0]))}"
        )
        qp.drawText(
            400,
            210,
            f"AVERAGE HIGH LIFE TIME: {int(round(self.population.averages[1]))}",
        )
        qp.drawText(
            400, 240, f"AVERAGE HIGH FITNESS: {int(round(self.population.averages[2]))}"
        )
        qp.drawText(400, 300, f"BEST GENERATION: {self.population.records[0]}")
        qp.drawText(400, 330, f"BEST HIGH SCORE: {self.population.records[1]}")
        qp.drawText(400, 360, f"BEST HIGH LIFE TIME: {self.population.records[2]}")
        qp.drawText(
            400, 390, f"BEST HIGH FITNESS: {round(self.population.records[3],2)}"
        )

    def timerEvent(self, event):
        if self.next_snake == self.population.size:
            self.timer.stop()
            self.new_game()

        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            self.timer.stop()
            self.population.save()
