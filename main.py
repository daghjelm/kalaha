import random

#Klass som har ett bräde och håller koll på 
#antalet kulor i varje steg
class Game:
    board = []
    STEPS = 14 #Antal skålar 
    P1_GOAL = 7 #Index för spelare etts hem
    P2_GOAL = 0 #Index för spelare tvås hem
    last_move = 1

    #Konstruktor, initiera brädet med valt antal kulor
    def __init__(self, beads):
        self.board = self.create_board(beads)

    #Lägg till kulor i varje skål som inte är ett hem
    def create_board(self, beads):
        board = []
        for i in range(self.STEPS):
            if not i in [self.P1_GOAL, self.P2_GOAL]:
                board.append(beads)
            else:
                board.append(0)

        return board

    def get_valid_pos(self, player):
        positions = []
        if player == 1:
            for i in range(1, 7):
                if(self.board[i] > 0):
                    positions.append(i)
        else:
            for i in range(8, 14):
                if(self.board[i] > 0):
                    positions.append(i)
        return positions
    
    #Gör ett drag returnera index för sista skålen
    def make_move(self, pos, player): 
        beads = self.board[pos] #Hur många kulor plockar man upp?
        if beads == 0:
            return -1
        self.board[pos] = 0 #Ta bort alla kulor från vald skål
        current = pos
        for i in range(1, beads + 1): #Börja lägga kulor på nästa position
            current = (pos + i) % 14 #Mod 14 på positionen för att forsätta gå runt
            self.board[current] += 1
        
        self.last_move = player
        
        return current
    
    #Kolla om spelaren har kulor kvar
    def has_left(self, player):
        if player == 1:
            for i in range(1, 7):
                if(self.board[i] > 0):
                    return True
        else:
            for i in range(8, 14):
                if(self.board[i] > 0):
                    return True

    #Få input från 'datorn'
    def get_fake_input(self, player):
        print('Spelare %d, vilken skål väljer du (1-6, 1 är närmast ditt bo): ' % player)
        positions = self.get_valid_pos(player)
        value = positions[random.randint(0, len(positions) - 1)]
        fake_input = input_from_val(player, value)
        print('Spelare %d valde skål %d' % (player, fake_input))
        
        return fake_input


    #Skriv ut spelplanen i konsollen
    def print_board(self): 
        board = self.board

        print('Brädet ser nu ut såhär:')
        print("  ", board[6], board[5], board[4], board[3], board[2], board[1])
        print(board[7], "             ", board[0]) 
        print("  ", board[8], board[9], board[10], board[11], board[12], board[13])
    
    def gather_beads(self):
        print('Lägger till kulor i spelare %ds bo' % self.last_move)
        if self.last_move == 1:
            for i in range (0, self.STEPS):
                if not i in [self.P1_GOAL, self.P2_GOAL]:
                    self.board[self.P1_GOAL] += self.board[i]
                    self.board[i] = 0
        else:
            for i in range (0, self.STEPS):
                if not i in [self.P1_GOAL, self.P2_GOAL]:
                    self.board[self.P2_GOAL] += self.board[i]
                    self.board[i] = 0


    #Kolla vem som har flest kulor i sitt hem
    def get_winner(self):
        if(self.board[self.P1_GOAL] > self.board[self.P2_GOAL]):
            return 1
        else:
            return 2


def can_continue(player, pos):
    return (player == 1 and pos == 7) or (player == 2 and pos == 0)

def get_valid_y_n(str):
    while(True):
        x = input(str).lower()
        if not x in ['y', 'n']:
            print('Felaktig karaktär, vänligen skriv igen.')
        else:
            break

    return x == 'y'

#Returera valen som spelaren gör i början som en lista
def get_player_settings():

    while(True):
        try:
            nr_beads = int(input('Hur många kulor i varje skål (3 till 6)? '))
        except ValueError:
            print('Vänligen skriv in en siffra (3-6).')
            continue
        else: 
            if(nr_beads > 2 and nr_beads < 7):
                break
            else:
                print('Vänligen skriv in en siffra (3-6).')
                continue
    
    p1_human = get_valid_y_n('Är spelare 1 en människa (Y/N): ')
    p2_human = get_valid_y_n('Är spelare 2 en människa (Y/N): ')

    return [nr_beads, p1_human, p2_human]

#Få input från spelaren
def get_input(player):
    while(True):
        try:
            user_input = int(input('Spelare %d, vilken skål väljer du (1-6, 1 är närmast ditt bo): ' % player))
        except ValueError:
            print('Vänligen skriv in en siffra (1-6).')
            continue
        else: 
            if(user_input > 0 and user_input < 7):
                break
            else:
                print('Vänligen skriv in en siffra (1-6).')
                continue

    return user_input

def input_from_val(player, value):
    if player == 1:
        return 7 - value
    else:
        return 14 - value


#Starta en runda
def play_round(game, player, human):
    playing = True

    while(playing):
        if not game.has_left(player):
            return False

        if human:
            user_input = get_input(player) 
        else: 
            user_input = game.get_fake_input(player) 

        if player == 1:
            #Value representerar index i listan, eftersom vi väljer från boet
            value = 7 - user_input 
        else:
            value = 14 - user_input

        current_pos = game.make_move(value, player) #Gör ett drag med position som motsvara index i listan 

        if(current_pos < 0):
            print('Välj en skål som inte är tom.')
            continue

        game.print_board()

        if not can_continue(player, current_pos) :
            playing = False
    
    return True

def main():

    #[beads, p1_human, p2_human]
    settings = get_player_settings()

    game = Game(settings[0])
    game.print_board()
    player = 1

    playing = True

    while(playing):
        #Spelet slutar om en spelare inte kan ta några kulor
        playing = play_round(game, player, settings[player])

        if player == 1:
            player = 2
        else:
            player = 1
    
    print('Spelet är över')
    game.gather_beads()
    winner = game.get_winner()
    game.print_board()
    print('Spelare %d vann!' % winner)

if __name__ == "__main__":
    main()