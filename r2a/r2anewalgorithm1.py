from player.parser import *
from r2a.ir2a import IR2A
from statistics import mean

import time

class R2ANewAlgorithm1(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []
        self.request_time = 0
        self.measured_throughput = []

    def handle_xml_request(self, msg):

        # Iniciar tempo
        self.request_time = time.perf_counter()
        
        self.send_down(msg)

    def handle_xml_response(self, msg):

        # getting qi list
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        # Calculo da banda do usuário
        self.measured_throughput.append(msg.get_bit_length()/(time.perf_counter() - self.request_time))

        self.send_up(msg)

    def handle_segment_size_request(self, msg):     
        # Iniciar tempo
        self.request_time = time.perf_counter()

        # ALGORITMO BASEADO EM BANDA

        #média das bandas
        media = mean(self.measured_throughput)/2
        media = 0.9*media

        x = 0
        qualidade_banda = 0
        for i in self.qi:
            tam = len(self.qi)-1-x
            if tam < 0:
                tam = 0

            if media > self.qi[tam]:
                qualidade_banda = tam
                break
            x += 1

        #ALGORITMO BASEADO EM BUFFER
        if self.whiteboard.get_amount_video_to_play() < 10:
        	qualidade_buffer = 11
        elif self.whiteboard.get_amount_video_to_play() < 13:
        	qualidade_buffer = 12
        elif self.whiteboard.get_amount_video_to_play() < 16:
        	qualidade_buffer = 13
        elif self.whiteboard.get_amount_video_to_play() < 19:
        	qualidade_buffer = 14
        elif self.whiteboard.get_amount_video_to_play() < 22:
        	qualidade_buffer = 15
        elif self.whiteboard.get_amount_video_to_play() < 25:
        	qualidade_buffer = 16
        elif self.whiteboard.get_amount_video_to_play() < 28:
        	qualidade_buffer = 17
        elif self.whiteboard.get_amount_video_to_play() < 31:
        	qualidade_buffer = 18
        elif self.whiteboard.get_amount_video_to_play() < 34:
        	qualidade_buffer = 19

        #...

        if self.whiteboard.get_amount_video_to_play() <20: 
        	qualidade_selecionada = 5
        else:
        	if qualidade_banda < qualidade_buffer:
	        	qualidade_selecionada = qualidade_buffer
        	else :
        		qualidade_selecionada = qualidade_banda

        


        print('\r\n QUALIDADE SELECIONADA:           ')
        print(qualidade_selecionada)
        print('\r\n QUALIDADE DO ALGORITMO BANDA:    ')
        print(qualidade_banda)
        print('\r\n QUALIDADE DO ALGORITMO BUFFER:   ')
        print(qualidade_buffer)
        print('\r\n Tamanho do Buffer:                        ')
        print(repr(self.whiteboard.get_amount_video_to_play()))
        print('\r\n')
   

        msg.add_quality_id(self.qi[qualidade_selecionada])

        self.send_down(msg)

    def handle_segment_size_response(self, msg):


        # Calculo da banda do usuário
        self.measured_throughput.append(msg.get_bit_length() / (time.perf_counter() - self.request_time))
        self.send_up(msg)

        #Pausas
        print('\r\n Pausas               ' )
        print(repr(self.whiteboard.get_playback_pauses()))
        print('\r\n')

    def initialize(self):
        pass

    def finalization(self):
        pass
