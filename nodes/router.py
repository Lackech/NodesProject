class Router:

    def validIP(self, ipAdress):
        valid = True
        ipSection = ipAdress.split('.')

        if ipSection.length() is 4:
            for section in ipSection:
                if section < 0 or section > 255:
                    valid = False
                    break
        else:
            valid = False

        return valid



    def validPort(self, portAddress):
        valid = True

        if portAddress < 1024 or portAddress > 60000:
            valid = False

        return valid



    def validMascar(self, mascara):
        valid = True

        if int(mascara) < 0 or int(mascara) > 31:
            valid = False

        return valid