RED_A = 0
RED_LOCAL = 1
RED_B = 2
RED_C = 3

class Router:

    def validIp(self, ip):
        valid = True
        tipoRed = RED_C
        if ip != 'localhost':
            ipSection = ip.split('.')

            if len(ipSection) is 4:
                try:
                    if int(ipSection[0]) <= 0 or int(ipSection[0])  > 223:
                        valid = False
                    elif int(ipSection[0]) < 127:
                        tipoRed = RED_A
                    elif int(ipSection[0]) == 127:
                        tipoRed = RED_LOCAL
                    elif int(ipSection[0]) < 192:
                        tipoRed = RED_B


                    if valid:
                        for section in ipSection:
                            if int(section) < 0 or int(section) > 255:
                                valid = False

                        if valid:
                            if ipSection[3] == 0:
                                if tipoRed == RED_C:
                                    valid = False
                                elif ipSection[2] == 0:
                                    if tipoRed == RED_B:
                                        valid = False
                                    elif ipSection[1] == 0:
                                        if tipoRed == RED_A:
                                            valid = False
                except:
                    valid = False
            else:
                valid = False

        return (valid,tipoRed)



    def validPort(self, port):
        valid = True
        portInt = 0
        try:
            portInt = int(port)
        except:
            valid = False

        if valid:
            if portInt < 1024 or portInt > 49151:
                valid = False

        return valid



    def validMascara(self, mascara, networkType):
        valid = True
        mascaraInt = 0
        try:
            mascaraInt = int(mascara)
        except:
            valid = False

        if valid:
            if mascara < 8 or mascara > 31:
                valid = False
            elif networkType == RED_B:
                if mascara < 16:
                    valid = False
            elif networkType == RED_C:
                if mascara < 24:
                    valid = False

        return valid