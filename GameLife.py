import sys, pygame, time, sys, os

class Screen:
        def __init__(self, x, y) -> None:
                self.info = pygame.display.Info()
                self.dict_color = {"white": (255,255,255), "black": (0,0,0), "red": (255,0,0)}
                self.x = x
                self.y = y

                for i in range(self.info.current_w - 100, 0, -1):
                        if i % self.x == 0:
                                self.width = i
                                break
                for i in range(self.info.current_h - 100, 0, -1):
                        if i % self.y == 0:
                                self.height = i
                                break
                self.size = self.width + 100, self.height
                self.screen = pygame.display.set_mode(self.size)
        
        def print_map(self, map):
                size_line = 2
                step_x = (self.width // self.x) - size_line
                step_y = (self.height // self.y) - size_line
                width_case = (self.width // self.x) - (size_line)
                heigtht_case = (self.height // self.y) - (size_line)
                        
                self.screen.fill(self.dict_color["white"])
                for i in range(step_y, self.height, step_y + size_line):
                        pygame.draw.rect(self.screen, self.dict_color["black"], pygame.Rect(0 ,i , self.width, size_line))
                for i in range(step_x, self.width, step_x + size_line):
                        pygame.draw.rect(self.screen, self.dict_color["black"], pygame.Rect(i ,0 , size_line, self.height))
                for i in range(len(map)):
                        for j in range(len(map[i])):
                                if map[i][j] == 1:
                                        pygame.draw.rect(self.screen, self.dict_color["red"], pygame.Rect((step_x * j) + (size_line * j), (step_y * i) + (size_line * i) , width_case, heigtht_case))
                less = pygame.image.load("minus.png")
                plus = pygame.image.load("plus.png")
                self.less_rect = less.get_rect()
                self.less_rect.x = self.width + 25
                self.less_rect.y = self.height/2
                self.screen.blit(less, self.less_rect)
                self.plus_rect = plus.get_rect()
                self.plus_rect.x = self.width + 50
                self.plus_rect.y = self.height / 2
                self.screen.blit(plus, self.plus_rect)
                pygame.display.flip()

def count(map, pos_x, pos_y):
        offset = [(1,0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        count = 0
        for off in offset:
                new_pos_x = pos_x + off[0]
                new_pos_y = pos_y + off[1]
                if new_pos_x < len(map[pos_y]) and new_pos_x >= 0 and new_pos_y < len(map) and new_pos_y >= 0 and map[new_pos_y][new_pos_x] == 1:
                        count += 1
        return count

def update_map(map):
        copy_map = []
        for i in range(len(map)):
                copy_map.append([])
                for j in range(len(map[i])):
                        n = count(map, j, i)
                        if map[i][j] == 0 and n == 3:
                                copy_map[i].append(1)
                        elif map[i][j] == 1 and (n < 2 or n > 3):
                                copy_map[i].append(0)
                        elif map[i][j] == 1 and n >= 2 and n <= 3:
                                copy_map[i].append(1)
                        else:
                                copy_map[i].append(map[i][j])
        # print(copy_map)
        return copy_map

def get_arg():
        map = [[]]
        j = 0
        arguments = sys.argv
        if len(arguments) == 2 and os.path.exists(arguments[1]) and os.access(arguments[1], os.R_OK):
                with open(arguments[1], 'r') as f:
                        contenu = f.read()
                        for i in range(len(contenu)):
                                if contenu[i] == "\n":
                                        map.append([])
                                        j += 1
                                if contenu[i] == "0":
                                        map[j].append(0)
                                if contenu[i] == "1":
                                        map[j].append(1)
                if len(map) != len(map[0]):
                        print("Error")
                        exit()
                for raw in map:
                        if len(raw) != len(map[0]):
                                print("Error")
                                exit()
                return (map)
        else:
                print("Error")
                exit()
                
        
def main():
        pygame.init()
        map = get_arg()
        t = 2
        screen = Screen(len(map[0]), len(map))
        while 1:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT: sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                        if screen.less_rect.collidepoint(event.pos):
                                                t = t * 2
                                        if screen.plus_rect.collidepoint(event.pos):
                                                t = t / 2
                screen.print_map(map)
                map = update_map(map)
                time.sleep(t)
                
if __name__ == "__main__":
        main()