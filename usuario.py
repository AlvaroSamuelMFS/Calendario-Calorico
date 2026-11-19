from datetime import date, datetime

class Usuario:
    def __init__(self,nombre,peso,altura,nacimiento,sexo,actividad,objetivo):
        self.nombre = nombre
        self.peso = peso
        self.altura = altura
        self.anoNacimiento = nacimiento
        self.sexo = sexo
        self.actividad = actividad
        self.objetivo = objetivo
        self.edad = self.sacarEdad()

    def sacarEdad(self):
        hoy = date.today()
        nac = datetime.strptime(self.anoNacimiento, "%Y-%m-%d").date()
        edad = hoy.year - nac.year
        if (hoy.month, hoy.day) < (nac.month, nac.day):
            edad -= 1
        print(edad)
        return edad


    def calcularCalorias(self):
        if self.sexo == "M":
            BMR = 10*self.peso+6.25*self.altura-5*self.edad+5
        elif self.sexo == "F":
            BMR = 10*self.peso+6.25*self.altura-5*self.edad-161
        multiplicadores ={1:1.2,2:1.375,3:1.55,4:1.725,5:1.9}
        TDEE = BMR*multiplicadores[self.actividad]
        if self.objetivo == "musculo":
            return TDEE +300
        elif self.objetivo == "adelgazar":
            return round(TDEE-400)
        else:
            return round(TDEE)
