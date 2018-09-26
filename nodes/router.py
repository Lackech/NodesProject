class Router:

    def validIp(self, ipAdress):
        valid = True
        ipSection = ipAdress.split('.')

        if len(ipSection) is 4:
            for section in ipSection:
                if int(section) < 0 or int(section) > 255:
                    valid = False
                    break
        else:
            valid = False

        return valid



    def validPort(self, portAddress):
        valid = True

        if int(portAddress) < 1024 or int(portAddress) > 60000:
            valid = False

        return valid



    def validMascar(self, mascara):
        valid = True

        if int(mascara) < 0 or int(mascara) > 31:
            valid = False

        return valid
