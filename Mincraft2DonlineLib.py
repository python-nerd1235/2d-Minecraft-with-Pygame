# Simple 2D Minecraft online game library.
# version 0.1 (game equivalent to 2dMincraft version 0.4, without saveing.)
class cli():
    def __init__(self,sever_ip,sever_port):
        import online_lib
        import time
        self.sever_ip=sever_ip
        self.sever_port=sever_port
        self.runing=True
        self.client=None
    def connect(self):
        try:
            import online_lib
            self.client = online_lib.Client(self.sever_ip, self.sever_port)
            self.client.connect()
            self.client.send_message('CONN')
            if self.client.wait_for_response()!='CONN_ACK':
                raise Exception
        except:
            import time
            import pygame
            pygame.init()
            win = pygame.display.set_mode((500, 500))
            text_font = pygame.font.SysFont('Arial', 20)
            text=text_font.render(f"Error: Could not connect to server: {self.sever_ip}:{self.sever_port}", True, (255, 0, 0))
            win.blit(text, (5, 25))
            pygame.display.update()
            time.sleep(3)
            self.runing=False
            return
    def run_client(self):
        self.connect()
        if not self.runing:
            return
        import pygame
        pygame.init()
        text_font = pygame.font.SysFont('Arial', 20)
        win = pygame.display.set_mode((500, 500))
        self.connect()
        c = self.client
        blocks, blobks_types,types,x,y,hp,direction,typeponter,sever_name=c.wait_for_response().split(chr(1))
        pygame.display.set_caption(f'Connected to {sever_name}')
        blocks=blocks.split(';')[:-1]
        blobks_types=blobks_types.split(';')[:-1]
        types=types.split(';')[:-1]
        while self.runing:
            win.fill((0, 0, 0))
            pygame.draw.rect(win, (255, 255, 0), (x, y, 50, 50))
            pygame.draw.rect(win, (255, 255, 255), (0, 450, 500, 50))
            pygame.draw.rect(win, types[typeponter], (0, 470, 20, 20))
            text=text_font.render(f'HP: {hp}', True, (0, 0, 255))
            win.blit(text, (30, 470))
            if direction == 0:lix,liy=x-50,y
            elif direction == 2:lix,liy=x,y-50
            elif direction == 1:lix,liy=x+50,y
            elif direction == 3:lix,liy=x,y+50
            pygame.draw.line(win, types[typeponter], (x+25, y+25), (lix+25, liy+25), 2)
            p=0
            for block in blocks:
                pygame.draw.rect(win, blobks_types[p], (block[0], block[1], 50, 50))
                p+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    c.send_message('DCM')
                    c.close()
                    self.runing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        c.send_message('ML')
                    elif event.key == pygame.K_RIGHT:
                        c.send_message('MR')
                    elif event.key == pygame.K_UP:
                        c.send_message('MU')
                    elif event.key == pygame.K_DOWN:
                        c.send_message('MD')
                    elif event.key == pygame.K_z:
                        c.send_message('AB')
                    elif event.key == pygame.K_x:
                        c.send_message('RB')
                    elif event.key == pygame.K_c:
                        c.send_message('CD')
                    elif event.key == pygame.K_SPACE:
                        c.send_message('CT')
            pygame.display.update()
class ser():
    def __init__(self,sever_ip,sever_port,sever_name):
        import online_lib
        self.sever_ip=sever_ip
        self.sever_port=sever_port
        self.sever_name=sever_name
        self.runing=True
        self.server=None
    def start_server(self):
        import online_lib
        self.server = online_lib.server(self.sever_ip, self.sever_port)
    def run_server(self):
        print(f"Server starting on {self.sever_ip}:{self.sever_port}.")
        self.start_server()
        msg=[0]*9
        blocks=[]
        types=[(0,255,0)]
        blobks_types=[]
        typeponter=0
        print("Waiting for a connection...")
        self.server.accept_connection()
        c = self.server.wait_for_message()
        print("Client connected. waiting for connection message...")
        if c!='CONN':
            print('Error: Invalid connection message')
            self.server.close()
            return
        self.server.send_message('CONN_ACK')
        print("Connection message received. Starting game loop.")
        while self.runing:
            message=self.server.wait_for_message()
            if message=='DCM':
                print('Client disconnected')
                c.close()
                self.runing=False
            elif message=='ML' and msg[3] > 0 and (msg[3] - 50, msg[4]) not in blocks:             
                msg[3]=int(msg[3])-50                                                              #All of the logic for the game is here.
            elif message=='MR' and msg[3] < 450 and (msg[3] + 50, msg[4]) not in blocks:
                msg[3]=int(msg[3])+50
            elif message=='MU' and msg[4] > 0 and (msg[3], msg[4] - 50) not in blocks:
                msg[4]=int(msg[4])-50
            elif message=='MD' and msg[4] < 450 and (msg[3], msg[4] + 50) not in blocks:
                msg[4]=int(msg[4])+50
            elif message=='AB':
                blocks.append((msg[3] - 50, msg[4]))
                blobks_types.append(types[msg[7]])
            elif message=='RB':
                if msg[6] == 0 and (msg[3] - 50, msg[4]) in blocks:
                    idx = blocks.index((msg[3] - 50, msg[4]))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
                elif msg[6] == 1 and (msg[3] + 50, msg[4]) in blocks:
                    idx = blocks.index((msg[3] + 50, msg[4]))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
                elif msg[6] == 2 and (msg[3], msg[4] - 50) in blocks:
                    idx = blocks.index((msg[3], msg[4] - 50))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
                elif msg[6] == 3 and (msg[3], msg[4] + 50) in blocks:
                    idx = blocks.index((msg[3], msg[4] + 50))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
            elif message=='CD':
                msg[6]=(msg[6]+1)%4
            elif message=='CT':
                msg[7]=(msg[7]+1)%len(types)
            for i in blocks:
                msg[0]+=str(i)+';'
            for i in blobks_types:
                msg[1]+=str(i)+';'
            for i in types:
                msg[2]+=str(i)+';'
            msg[8]=self.sever_name
            c.send_message(chr(1).join(msg))

if __name__ == "__main__":
    print("Mincraft2DonlineLib module run directly. Import this module to use client/server classes.")
    print('Try again!')