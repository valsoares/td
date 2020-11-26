from player.parser import *
from r2a.ir2a import IR2A

import time
from player.player import *

class R2ANewAlgorithm1(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []
        self.request_time = 0
        self.measured_throughput = 0
        self.buffer = 0

    def handle_xml_request(self, msg):
        print("**************** handle_xml_request ****************")
        
        self.send_down(msg)

    def handle_xml_response(self, msg):
        print("************* handle_xml_response ****************")
        # getting qi list
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        self.send_up(msg)

    def handle_segment_size_request(self, msg):

        # debug
        print('\x1b[4;37;42m' + "************* handle_segment_size_request ****************" + '\x1b[0m')
        print('\x1b[6;37;42m' + "**************** BANDAAAA ************* " + '\x1b[0m', end='')
        print(self.measured_throughput)
        print('\x1b[6;37;42m' + "**************** QI ************* " + '\x1b[0m', end='')
        print(self.qi)

        # Iniciar tempo
        self.request_time = time.perf_counter()

        # Monitorar buffer
        # print('\x1b[6;37;42m' + "**************** BUFFER ************* " + '\x1b[0m', end='')
        # print(self.buffer)
        

        # Escolha da banda
        x = 0
        qualidade_selecionada = 0
        for i in self.qi:
            tam = len(self.qi)-1-x
            if tam < 0:
                tam = 0

            # print('\x1b[6;37;42m' + "measured_throughput" + '\x1b[0m', end='')
            # print(self.measured_throughput)
            # print('\x1b[6;37;42m' + "qi[tam]" + '\x1b[0m', end='')
            # print(self.qi[tam])

            if self.measured_throughput > self.qi[tam]:
                print('\x1b[6;37;42m' + "BANDA SELECIONADA" + '\x1b[0m', end='')
                print(self.qi[tam])
                qualidade_selecionada = tam
                break
            x += 1

        print('\x1b[6;37;42m' + "QUALIDADE SELECIONADA" + '\x1b[0m', end='')
        print(qualidade_selecionada)

        # time to define the segment quality choose to make the request
        msg.add_quality_id(self.qi[qualidade_selecionada])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):

        # debug
        print('\x1b[6;37;41m' + "************* handle_segment_size_response ****************" + '\x1b[0m')

        # Calculo da banda do usuário
        self.measured_throughput = msg.get_bit_length() / (time.perf_counter() - self.request_time)

        print('\x1b[6;37;41m' + "**************** BANDAAAA ************* " + '\x1b[0m' , end='') 
        print(self.measured_throughput)
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass
