import machine
## Simple Free Config Protocol
## SFCP have 2 type header: message_header, data_header
## message:
## [message_header:8][data_header:8][data:8|16|32|64]...[data_header:8][data:8|16|32|64]
# message_header
SFCP_MESSAGE_TYPE_MASK = 0x1F
SFCP_MESSAGE_TYPE_SHIFT = 0x0
SFCP_MESSAGE_IS_COMMAND_MASK = 0x1
SFCP_MESSAGE_IS_COMMAND_SHIFT = 0x6
SFCP_MESSAGE_IS_RESPONSE_MASK = 0x1
SFCP_MESSAGE_IS_RESPONSE_SHIFT = 0x7
# data_header
SFCP_DATA_TYPE_MASK = 0x1F
SFCP_DATA_TYPE_SHIFT = 0x0
SFCP_DATA_IS_LITTLE_ENDIAN_MASK = 0x1
SFCP_DATA_IS_LITTLE_ENDIAN_SHIFT = 0x5
#DATA_SIZE 0 = 1byte 1=2byte 2=4byte 3=8byte 
SFCP_DATA_SIZE_MASK = 0x3
SFCP_DATA_SIZE_SHIFT = 0x6



class sfcp():
    def __init__(self):
        pass

    def init_message(self,type,is_command=0,is_response=0):
        ret = []
        ret.append(((type&SFCP_MESSAGE_TYPE_MASK)<<SFCP_MESSAGE_TYPE_SHIFT)|(is_command&SFCP_MESSAGE_IS_COMMAND_MASK)<<SFCP_MESSAGE_IS_COMMAND_SHIFT|(is_response&SFCP_MESSAGE_IS_RESPONSE_MASK)<<SFCP_MESSAGE_IS_RESPONSE_SHIFT)
        return ret

    #return num add bytes
    def add(self, message,type,data_size,data,is_little=1)-> int:
        
        # message_header = message[0]
        message.append(((type&SFCP_DATA_TYPE_MASK)<<SFCP_DATA_TYPE_SHIFT)|(is_little&SFCP_DATA_IS_LITTLE_ENDIAN_MASK)<<SFCP_DATA_IS_LITTLE_ENDIAN_SHIFT|(data_size&SFCP_DATA_SIZE_MASK)<<SFCP_DATA_SIZE_SHIFT)
        if data_size == 0:
            message.append(data)
            return 2
        elif data_size == 1:
            if is_little == 1:
                # struct.pack_into("<h", message, offset, v1, v2, ...)
                message.append(data&0xFF)
                message.append((data>>8)&0xFF)
                return 3
            else:
                message.append((data>>8)&0xFF)
                message.append(data&0xFF)
                return 3
        elif data_size == 2:
            a = None
            if type(data)=='float':
                
                if is_little == 1:
                    a = struct.pack("<f",data)
                else:
                    a = struct.pack(">f",data)    
                message.extend(a)
                return 5
            else:
                if is_little == 1:
                    a = struct.pack("<i",data)
                else:
                    a = struct.pack(">i",data)
                message.extend(a)
                return 5
        elif data_size == 3:
            a = None
            if type(data)=='double':
                
                if is_little == 1:
                    a = struct.pack("<d",data)
                else:
                    a = struct.pack(">d",data)    
                message.extend(a)
                return 9
            else:
                if is_little == 1:
                    a = struct.pack("<q",data)
                else:
                    a = struct.pack(">q",data)
                message.extend(a)
                return 9