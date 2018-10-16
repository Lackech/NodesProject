redA = 0
redLocal = 1
redB = 2
redC = 3


class Router:

    def validIp(self, ip):
        valid = True
        tipoRed = redC
        if ip != 'localhost':
            ipSection = ip.split('.')

            if len(ipSection) is 4:
                try:
                    if int(ipSection[0]) <= 0 or int(ipSection[0])  > 223:
                        valid = False
                    elif int(ipSection[0]) < 127:
                        tipoRed = redA
                    elif int(ipSection[0]) == 127:
                        tipoRed = redLocal
                    elif int(ipSection[0]) < 192:
                        tipoRed = redB


                    if valid:
                        for section in ipSection:
                            if int(section) < 0 or int(section) > 255:
                                valid = False

                        if valid:
                            if ipSection[3] == 0:
                                if tipoRed == redC:
                                    valid = False
                                elif ipSection[2] == 0:
                                    if tipoRed == redB:
                                        valid = False
                                    elif ipSection[1] == 0:
                                        if tipoRed == redA:
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



    def validMascara(self, mascara, tipoRed):
        valid = True
        mascaraInt = 0
        try:
            mascaraInt = int(mascara)
        except:
            valid = False

        if valid:
            if mascara < 8 or mascara > 31:
                valid = False
            elif tipoRed == redB:
                if mascara < 16:
                    valid = False
            elif tipoRed == redC:
                if mascara < 24:
                    valid = False

        return valid