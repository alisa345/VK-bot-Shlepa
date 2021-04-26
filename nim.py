class Nim:

    def __init__(self, stones1, stones2, stones3):
        self.stones1 = stones1
        self.stones2 = stones2
        self.stones3 = stones3
        self.end_play = False
        self.whose_move = True
        self.play_move = 0
        self.num_stones = 0

    def get_stones1(self):
        return self.stones1

    def get_stones2(self):
        return self.stones2

    def get_stones3(self):
        return self.stones3

    # Если true - ходит ии, если false - ходит шлёпа
    def play(self, nm_stns=0, play_mv=0):
        if self.whose_move is True:
            if self.stones1 < self.stones2 and self.stones2 > self.stones3 and self.stones1 <= self.stones3:
                self.play_move = self.stones2 - self.stones1
                self.stones2 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из второй кучи'
            elif self.stones1 > self.stones2 and self.stones1 > self.stones3 and self.stones2 <= self.stones3:
                self.play_move = self.stones1 - self.stones2
                self.stones1 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
            elif self.stones1 < self.stones2 and self.stones2 > self.stones3 and self.stones1 >= self.stones3:
                self.play_move = self.stones2 - self.stones3
                self.stones2 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из второй кучи'
            elif self.stones1 > self.stones2 and self.stones1 > self.stones3 and self.stones2 >= self.stones3:
                self.play_move = self.stones1 - self.stones3
                self.stones1 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
            elif self.stones3 > self.stones2 and self.stones3 > self.stones1 and self.stones2 >= self.stones1:
                self.play_move = self.stones3 - self.stones1
                self.stones3 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из третьей кучи'
            elif self.stones3 > self.stones2 and self.stones3 > self.stones1 and self.stones2 <= self.stones1:
                self.play_move = self.stones3 - self.stones2
                self.stones3 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из третьей кучи'
            elif self.stones1 == 0 and self.stones2 == self.stones3:
                self.play_move = 1
                self.stones2 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из второй кучи'
            elif self.stones2 == 0 and self.stones1 == self.stones3:
                self.play_move = 1
                self.stones1 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
            elif self.stones3 == 0 and self.stones1 == self.stones2:
                self.play_move = 1
                self.stones1 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
            elif self.stones1 == self.stones2 and self.stones2 == self.stones3:
                self.play_move = 1
                self.stones1 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
            elif self.stones1 == 0 and self.stones2 == 0:
                self.play_move = self.stones3
                self.stones3 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из третьей кучи'
            elif self.stones2 == 0 and self.stones3 == 0:
                self.play_move = self.stones1
                self.stones1 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
            elif self.stones1 == 0 and self.stones3 == 0:
                self.play_move = self.stones2
                self.stones2 -= self.play_move
                ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из второй кучи'
            else:
                if self.stones1 != 0:
                    self.play_move = 1
                    self.stones1 -= self.play_move
                    ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из первой кучи'
                elif self.stones2 != 0:
                    self.play_move = 1
                    self.stones2 -= self.play_move
                    ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из второй кучи'
                elif self.stones3 != 0:
                    self.play_move = 1
                    self.stones3 -= self.play_move
                    ln1 = 'Шлёпа взял ' + str(self.play_move) + ' камней из третьей кучи'
            ln2 = 'Оставшееся кол-во камней в первой куче: ' + str(self.stones1) + \
                  '\nОставшееся кол-во камней во второй куче: ' + str(self.stones2) + \
                  '\nОставшееся кол-во камней в третьей куче: ' + str(self.stones3)
            if self.stones1 == 0 and self.stones2 == 0 and self.stones3 == 0:
                self.end_play = True
            else:
                self.whose_move = False
            return self.end_play, ln1, ln2
        if self.whose_move is False:
            self.num_stones = nm_stns
            self.play_move = play_mv
            if self.num_stones == 1:
                self.stones1 -= self.play_move
                ln1 = 'Человек взял ' + str(self.play_move) + ' камней из первой кучи'
                self.whose_move = True
            elif self.num_stones == 2:
                self.stones2 -= self.play_move
                ln1 = 'Человек взял ' + str(self.play_move) + ' камней из второй кучи'
                self.whose_move = True
            elif self.num_stones == 3:
                self.stones3 -= self.play_move
                ln1 = 'Человек взял ' + str(self.play_move) + ' камней из третьей кучи'
                self.whose_move = True
            ln2 = 'Оставшееся кол-во камней в первой куче: ' + str(self.stones1) + \
                  '\nОставшееся кол-во камней во второй куче: ' + str(self.stones2) + \
                  '\nОставшееся кол-во камней в третьей куче: ' + str(self.stones3)
            if self.stones1 == 0 and self.stones2 == 0 and self.stones3 == 0:
                self.end_play = True
            else:
                self.whose_move = True
                self.num_stones = 0
            return self.end_play, ln1, ln2
