import streamlit as st
from prettytable import PrettyTable
import random

# Generador de nombres aleatorios para la empresa
def generar_nombre_empresa():
    adjetivos = ["Innovadora", "Global", "Creativa", "Dinámica", "Futurista"]
    sustantivos = ["Tech", "Industries", "Solutions", "Enterprises", "Corporation"]
    return random.choice(adjetivos) + " " + random.choice(sustantivos)

class Empresa:
    def __init__(self, nombre, industria):
        self.nombre = nombre
        self.industria = industria
        self.capital = 1000
        self.ingresos = 300 if industria == "tecnología" else 200 if industria == "manufactura" else 150
        self.gastos = 100 if industria == "tecnología" else 80 if industria == "manufactura" else 50
        self.deuda = 0
        self.tasa_interes = 0.05
        self.inversion_en_marketing = 0
        self.desarrollo_producto = False
        self.empleados = 10 if industria == "tecnología" else 20 if industria == "manufactura" else 5
        self.historia = ["La empresa fue fundada con la visión de revolucionar su industria."]
        self.balance_historial = []

    def calcular_intereses(self):
        return self.deuda * self.tasa_interes

    def calcular_balance(self):
        intereses = self.calcular_intereses()
        balance = self.capital + self.ingresos - self.gastos - intereses
        return balance

    def tomar_prestamo(self, cantidad):
        self.deuda += cantidad
        self.capital += cantidad
        self.historia.append(f"Se tomó un préstamo de {cantidad}.")
        self.actualizar_historial()

    def pago_deuda(self, cantidad):
        pago = min(self.deuda, cantidad)
        self.deuda -= pago
        self.capital -= pago
        self.historia.append(f"Se pagó una deuda de {cantidad}.")
        self.actualizar_historial()

    def actualizar_finanzas(self, decision, cantidad):
        if decision == "invertir":
            self.capital -= cantidad
            self.gastos += cantidad * 0.05
            self.historia.append(f"Inversión de {cantidad} en infraestructura.")
        elif decision == "marketing":
            self.inversion_en_marketing += cantidad
            self.capital -= cantidad
            self.historia.append(f"Campaña de marketing lanzada con una inversión de {cantidad}.")
        elif decision == "producto":
            if not self.desarrollo_producto:
                self.capital -= cantidad
                self.ingresos += 150 if self.industria == "tecnología" else 100
                self.desarrollo_producto = True
                self.historia.append(f"Desarrollo de un nuevo producto completado con {cantidad}.")
        elif decision == "contratar":
            num = cantidad // 100  # Suponemos que cada empleado cuesta 100
            self.empleados += num
            self.gastos += num * 80
            self.historia.append(f"Contratación de {num} nuevos empleados.")
        self.actualizar_historial()

    def actualizar_historial(self):
        balance = self.calcular_balance()
        self.balance_historial.append({
            "Año": len(self.balance_historial) + 1,
            "Capital": self.capital,
            "Ingresos": self.ingresos,
            "Gastos": self.gastos,
            "Deuda": self.deuda,
            "Intereses": self.calcular_intereses(),
            "Balance": balance,
            "Empleados": self.empleados
        })

    def obtener_balance_tabla(self):
        tabla = PrettyTable()
        columnas = ["Año", "Capital", "Ingresos", "Gastos", "Deuda", "Intereses", "Balance", "Empleados"]
        tabla.field_names = columnas
        for entry in self.balance_historial:
            tabla.add_row([entry[col] for col in columnas])
        return tabla

def main():
    st.set_page_config(layout="wide")
    st.title("Simulador Empresarial")

    if 'empresa' not in st.session_state:
        # Selección de la industria
        st.session_state.industria = st.selectbox("Elige la industria", ["tecnología", "manufactura", "servicios"])
        st.session_state.empresa = Empresa(generar_nombre_empresa(), st.session_state.industria)
        st.experimental_rerun()

    empresa = st.session_state.empresa

    # Barra lateral para la historia
    with st.sidebar:
        st.header("Historia de la Empresa")
        for evento in empresa.historia:
            st.write(evento)

    # Columna principal para el balance y las acciones
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"Estado Financiero de {empresa.nombre}")

        balance_tabla = empresa.obtener_balance_tabla()
        st.text(balance_tabla)

    with col2:
        st.subheader("Realizar una Acción")
        acciones = ["invertir", "marketing", "producto", "contratar", "tomar préstamo", "pagar deuda"]
        accion = st.selectbox("Selecciona una acción", acciones)
        cantidad = st.number_input("Cantidad", min_value=0, step=100)

        if st.button("Realizar Acción"):
            if cantidad > 0:
                if accion in ["invertir", "marketing", "producto", "contratar"]:
                    empresa.actualizar_finanzas(accion, cantidad)
                elif accion == "tomar préstamo":
                    empresa.tomar_prestamo(cantidad)
                elif accion == "pagar deuda":
                    empresa.pago_deuda(cantidad)
                st.success(f"Acción '{accion}' realizada con éxito.")
                st.experimental_rerun()
            else:
                st.error("Introduce una cantidad válida mayor que 0.")

if __name__ == "__main__":
    main()
