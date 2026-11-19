from inicio import Inicio
from database import crear_tabla,crear_tabla_alimentos




crear_tabla()
crear_tabla_alimentos()
app = Inicio()
app.mainloop()
