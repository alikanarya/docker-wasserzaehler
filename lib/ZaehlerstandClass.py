import configparser
import lib.ReadAnalogNeedleClass
import lib.CutImageClass
import lib.ReadDigitalDigitClass
import math

class Zaehlerstand:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        print('Start Init Zaehlerstand')
        self.readAnalogNeedle = lib.ReadAnalogNeedleClass.ReadAnalogNeedle()
        print('Analog Model Init Done')
        self.readDigitalDigit = lib.ReadDigitalDigitClass.ReadDigitalDigit()
        print('Digital Model Init Done')
        self.CutImage = lib.CutImageClass.CutImage()

#        if config.has_option('Analog_Counter', 'LogImageLocation'):
#            self.log_Image = config['Analog_Counter']['LogImageLocation']
#            if config.has_option('Analog_Counter', 'LogNames'):
#                zw_LogNames = config.get('Analog_Counter', 'LogNames').split(',')
#                self.LogNames = []
#                for nm in zw_LogNames:
#                      self.LogNames.append(nm.strip())
#            else:
#                self.LogNames = ''
#        else:
#            self.log_Image = ''


    def getZaehlerstand(self, img_file, simple = True):
        print('Start CutImage')
        resultcut = self.CutImage.Cut(img_file)
        print('Start DigitalDigit Readout')
        resultdigital = self.readDigitalDigit.Readout(resultcut[1])
        print('Start AnalogNeedle Readout')
        resultanalog = self.readAnalogNeedle.Readout(resultcut[0])
        
        vorkomma = self.DigitalReadoutToValue(resultdigital)
        nachkomma = self.AnalogReadoutToValue(resultanalog)
        zaehlerstand = str(vorkomma.lstrip("0")) + '.' + str(nachkomma)

        print('Start Making Zaehlerstand')

        txt = zaehlerstand + '\t' + vorkomma  + '\t' + nachkomma 

        if not simple:
            txt = txt + '<p>Aligned Image: <p><img src=/image_tmp/alg.jpg></img><p>'
            txt = txt + 'Digital Counter: <p>'
            for i in range(len(resultdigital)):
                if resultdigital[i] == 'NaN':
                    zw = 'NaN'
                else:
                    zw = str(int(resultdigital[i]))
                txt += '<img src=/image_tmp/'+  str(resultcut[1][i][0]) + '.jpg></img>' + zw
            txt = txt + '<p>'
            txt = txt + 'Analog Meter: <p>'
            for i in range(len(resultanalog)):
                txt += '<img src=/image_tmp/'+  str(resultcut[0][i][0]) + '.jpg></img>' + "{:.1f}".format(resultanalog[i])
            txt = txt + '<p>'
        print('Get Zaehlerstand done')
        return txt

    def AnalogReadoutToValue(self, res_analog):
        prev = -1
        erg = ''
#        for item in res_analog[::-1]:
        for item in res_analog:
            prev = self.ZeigerEval(item, prev)
            erg = erg + str(int(prev))
        return erg

    def ZeigerEval(self, zahl, ziffer_vorgaenger):
        ergebnis_nachkomma = math.floor((zahl * 10) % 10)
        ergebnis_vorkomma = math.floor(zahl % 10)

        if ziffer_vorgaenger == -1:
            ergebnis = ergebnis_vorkomma
        else:
            ergebnis_rating = ergebnis_nachkomma - ziffer_vorgaenger
            if ergebnis_nachkomma >= 5:
                ergebnis_rating-=5
            else:
                ergebnis_rating+=5
            ergebnis = round(zahl)
            if ergebnis_rating < 0:
                ergebnis-=1
            if ergebnis == -1:
                ergebnis+=10

        ergebnis = ergebnis  % 10
        return ergebnis


    def DigitalReadoutToValue(self, res_digital):
        erg = ''
#        for item in res_digital[::-1]:
        for item in res_digital:
            if item == 'NaN':
                item = 'N'
            erg = erg + str(item)
        return erg

