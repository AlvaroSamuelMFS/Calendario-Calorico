from alimentos import calcular_macros

def calcular_dia(dia):
    total_macros = {"tot_calorias":0,"tot_proteinas":0,"tot_hdc":0,"tot_grasas":0}
    for comida in dia:
        for alimento in dia[comida]:
            macro = calcular_macros(alimento,dia[comida][alimento])
            total_macros["tot_calorias"] += macro["calorias"]
            total_macros["tot_proteinas"] += macro["proteinas"]
            total_macros["tot_hdc"] += macro["hdc"]
            total_macros["tot_grasas"] += macro["grasas"]
    return total_macros
