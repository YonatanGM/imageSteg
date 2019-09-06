from os.path import getsize
from binascii import b2a_hex, a2b_hex
from random import choice

START_BUFFER = b'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
END_BUFFER = b'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
TAB = b'\t'

class FILE:
    def __init__(self, file_path):
        self.file_path = file_path
        if self.file_path != None:
            self.file_type = self.file_path.split('.')[-1]
            self.file_size = self.getFilesize()
            print("payload:", self.file_path, self.file_type, self.file_size)
        
    def text_to_binary(self, max_size):
        '''

        '''
        try:
            text_file = open(self.file_path, 'rb')
        except Exception as e:
            raise Exception('[!] Failed to open target file: {}'.format(str(e)))
        try:
            msg = text_file.read()
            msg += START_BUFFER + TAB
            msg += str.encode(self.file_type) + TAB
            msg += END_BUFFER
            text_file.close()
            hex_text = b2a_hex(msg).decode('ascii')
            b = ''
            for ch in hex_text:
                tmp = bin(ord(ch))[2:]
                if len(tmp) < 7:
                    for _ in range(0,(7-len(tmp))):
                        tmp = '0' + tmp
                b += tmp
            for _ in range(0,(max_size - len(b)),7):
                b += str(bin(ord(choice('abcdef')))[2:])
            return b
        except Exception as e:
            raise Exception('[!] Text to binary conversion failed! {}'.format(str(e)))
        
    def set_bit(self, old_byte, new_bit):
        b = list(bin(old_byte))
        b[-1] = new_bit
        return int(''.join(b),2)

    def binary_to_text(self, bits, output_file_name):
        try:
            # break long string into array for bytes
            b = [bits[i:i+7] for i in range(0, len(bits), 7)]
            # convert to string
            c = ''
            for i in b:
                c += chr(int(i,2))
            if len(c) % 2 != 0:
                c += 'A'
            # convert back to ascii
            as_ascii = a2b_hex(c[:-10].encode('ascii'))
            # check to see if the buffer is intact still
            buffer_idx = as_ascii.find(START_BUFFER)
            buffer_idx2 = as_ascii.find(END_BUFFER)
        except Exception as e:
            raise Exception(str(e))

        if buffer_idx != -1:
            fc = as_ascii[:buffer_idx]
        else:
            raise Exception('[!] Failed to find message buffer...')

        if buffer_idx2 != -1:
            payload_file_type = '.' + as_ascii[buffer_idx+49:buffer_idx2-1].decode('ascii')
        else:
            raise Exception('[!] Unknown file type in extracted message')

        if (buffer_idx != -1) and (buffer_idx2 != -1):
            try:
                to_save = open(output_file_name + payload_file_type, 'wb')
                to_save.write(fc)
                to_save.close()
                print('[+] Successfully extracted message: {}{}'.format(output_file_name, payload_file_type))
            except Exception as e:
                raise Exception('[!] Failed to write extracted file: {}'.format(str(e)))
            finally:
                to_save.close()
                return output_file_name + payload_file_type

            
    def getFilesize(self):
        return getsize(self.file_path)*8




    
