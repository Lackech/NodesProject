
class Bitnator:
    def encrypt(self):
        encriptedMessage = bytearray()

        # Retornamos el mensaje encriptado
        return encriptedMessage






    def encryptIp(self, ip):
        encriptedIp = bytearray()

        ipParts = ip.split('.')
        for s in ipParts:
            encriptedIp += int(s).to_bytes(1, 'big')

        return encriptedIp





    def decrypt(self, packet):
        return (origenIp, origenPort, serverRequest, serverACK, hello, helloACK, update, updateACK, type, message)





    def acomodateIp(self,num4,num3,num2,num1):
        decriptedIp = num1 + '.' + num2 + '.' + num3 + '.' + num4
        return decriptedIp