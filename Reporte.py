import tkinter as tk
from tkinter import ttk
from fpdf import FPDF

root = tk.Tk()
root.title("Generador de Reportes Financieros")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

presupuesto_var = tk.DoubleVar()
activos_vars = {}
pasivos_vars = {}
capital_vars = {}

costos_directos_vars = {}
costos_indirectos_vars = {}
gastos_administrativos_vars = {}
gastos_ventas_vars = {}
gastos_financieros_vars = {}
datos_financieros_vars = {}
distribucion_vars = {"Bancos": tk.DoubleVar(), "Caja": tk.DoubleVar()}

def crear_entradas(categorias, frame, variables_dict):
    for categoria in categorias:
        label = tk.Label(frame, text=categoria)
        label.pack(padx=5, pady=5)
        var = tk.DoubleVar()
        entry = tk.Entry(frame, textvariable=var)
        entry.pack(padx=5, pady=5)
        variables_dict[categoria] = var

def obtener_valores(variables_dict):
    return {k: v.get() for k, v in variables_dict.items()}

def crear_seccion_costos_y_gastos(frame, titulo, categorias, variables_dict, row, column):
    section_frame = ttk.LabelFrame(frame, text=titulo)
    section_frame.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")
    crear_entradas(categorias, section_frame, variables_dict)

seccion_presupuesto = ttk.LabelFrame(scrollable_frame, text="Presupuesto Inicial")
seccion_presupuesto.grid(row=0, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
tk.Label(seccion_presupuesto, text="Presupuesto Inicial").pack(padx=5, pady=5)
entry_presupuesto = tk.Entry(seccion_presupuesto, textvariable=presupuesto_var)
entry_presupuesto.pack(padx=5, pady=5)

crear_seccion_costos_y_gastos(scrollable_frame, "Costos Directos", ["Materia Prima", "Mano de Obra Directa"], costos_directos_vars, row=1, column=0)
crear_seccion_costos_y_gastos(scrollable_frame, "Costos Indirectos", ["Servicios", "Renta de Bodega"], costos_indirectos_vars, row=1, column=1)
crear_seccion_costos_y_gastos(scrollable_frame, "Gastos Administrativos", ["Energía eléctrica de Oficina", "Nómina de Oficina", "Papelería"], gastos_administrativos_vars, row=1, column=2)
crear_seccion_costos_y_gastos(scrollable_frame, "Gastos de Ventas", ["Luz de Almacén", "Propaganda", "Viáticos"], gastos_ventas_vars, row=1, column=3)
crear_seccion_costos_y_gastos(scrollable_frame, "Gastos Financieros", ["Agentes", "Préstamo Bancario", "Otros Gastos"], gastos_financieros_vars, row=1, column=4)
crear_seccion_costos_y_gastos(scrollable_frame, "Datos Financieros Adicionales", [
    "Ventas", "Descuento sobre ventas", "Rebaja sobre ventas", "Devoluciones sobre ventas",
    "Inventario inicial", "Gastos sobre la compra", "Devoluciones sobre compras", "Rebajas sobre compras",
    "Descuento sobre compras", "Productos financieros", "Cantidad de venta", "Otros Gastos"
], datos_financieros_vars, row=2, column=0)

crear_seccion_costos_y_gastos(scrollable_frame, "Activos", [
    "Efectivo", "Clientes", "Documentos por cobrar", "Inventario Inicial", "Inventario Final"
], activos_vars, row=2, column=1)
crear_seccion_costos_y_gastos(scrollable_frame, "Pasivos", [
    "Proveedores", "Préstamo Bancario"
], pasivos_vars, row=2, column=2)
crear_seccion_costos_y_gastos(scrollable_frame, "Capital", [
    "Capital Social", "Utilidades Retenidas"
], capital_vars, row=2, column=3)

def crear_seccion_distribucion(frame, row, column):
    section_frame = ttk.LabelFrame(frame, text="Distribución de Utilidades")
    section_frame.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")
    for key, var in distribucion_vars.items():
        label = tk.Label(section_frame, text=key)
        label.pack(padx=5, pady=5)
        entry = tk.Entry(section_frame, textvariable=var)
        entry.pack(padx=5, pady=5)

crear_seccion_distribucion(scrollable_frame, row=3, column=0)

def generar_pdf():
    presupuesto = presupuesto_var.get()
    costos_directos = obtener_valores(costos_directos_vars)
    costos_indirectos = obtener_valores(costos_indirectos_vars)
    gastos_administrativos = obtener_valores(gastos_administrativos_vars)
    gastos_ventas = obtener_valores(gastos_ventas_vars)
    gastos_financieros = obtener_valores(gastos_financieros_vars)
    datos_financieros = obtener_valores(datos_financieros_vars)
    activos = obtener_valores(activos_vars)
    pasivos = obtener_valores(pasivos_vars)
    capital = obtener_valores(capital_vars)
    distribucion_utilidades = obtener_valores(distribucion_vars)
    
    total_costos = sum(costos_directos.values()) + sum(costos_indirectos.values())
    total_gastos = sum(gastos_administrativos.values()) + sum(gastos_ventas.values()) + sum(gastos_financieros.values())
    presupuesto_final = total_costos + total_gastos

    ventas = datos_financieros["Ventas"]
    devoluciones_ventas = datos_financieros["Rebaja sobre ventas"] + datos_financieros["Devoluciones sobre ventas"]
    ventas_netas = ventas - devoluciones_ventas
    
    descuentos_compras = datos_financieros["Devoluciones sobre compras"] + datos_financieros["Rebajas sobre compras"] + datos_financieros["Descuento sobre compras"]
    compras_netas = datos_financieros["Gastos sobre la compra"] - descuentos_compras
    mercaderia_disponible_venta = datos_financieros["Inventario inicial"] + compras_netas
    costo_venta = mercaderia_disponible_venta - datos_financieros["Cantidad de venta"]
    
    utilidad_bruta_venta = ventas_netas - costo_venta
    
    gastos_total_administracion = sum(gastos_administrativos.values()) + sum(gastos_ventas.values())
    utilidad_operacion = utilidad_bruta_venta - gastos_total_administracion
    
    gastos_financieros_resultado = datos_financieros["Productos financieros"] - sum(gastos_financieros.values())
    total_otros_gastos = gastos_financieros_resultado + datos_financieros.get("Otros Gastos", 0)
    
    utilidad_antes_impuestos = utilidad_operacion - total_otros_gastos
    impuestos = utilidad_antes_impuestos * 0.33
    utilidad_neta = utilidad_antes_impuestos - impuestos

    bancos = distribucion_utilidades.get("Bancos", 0)
    caja = distribucion_utilidades.get("Caja", 0)

    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title('Costos Directos')
    for k, v in costos_directos.items():
        pdf.chapter_body(f"{k}: ${v:.2f}")

    pdf.chapter_title('Costos Indirectos')
    for k, v in costos_indirectos.items():
        pdf.chapter_body(f"{k}: ${v:.2f}")

    pdf.chapter_body(f"\nTotal de Costos: ${total_costos:.2f}")

    pdf.add_page()
    pdf.chapter_title('Gastos Administrativos')
    for k, v in gastos_administrativos.items():
        pdf.chapter_body(f"{k}: ${v:.2f}")

    pdf.chapter_title('Gastos de Ventas')
    for k, v in gastos_ventas.items():
        pdf.chapter_body(f"{k}: ${v:.2f}")

    pdf.chapter_title('Gastos Financieros')
    for k, v in gastos_financieros.items():
        pdf.chapter_body(f"{k}: ${v:.2f}")

    pdf.chapter_body(f"\nTotal de Gastos: ${total_gastos:.2f}")

    pdf.add_page()
    pdf.chapter_title('Datos Financieros Adicionales')
    for k, v in datos_financieros.items():
        pdf.chapter_body(f"{k.replace('_', ' ').title()}: ${v:.2f}")

    pdf.add_page()
    pdf.chapter_title('Estado de Resultados')
    
    estado_resultados = [
        ("Ventas", ventas),
        ("Total de devoluciones sobre ventas", devoluciones_ventas),
        ("Ventas netas", ventas_netas),
        ("Descuentos sobre compras", descuentos_compras),
        ("Compras netas", compras_netas),
        ("Mercaderia disponible para la venta", mercaderia_disponible_venta),
        ("Costo venta", costo_venta),
        ("Utilidad bruta en venta", utilidad_bruta_venta),
        ("Gastos total de administración", gastos_total_administracion),
        ("Utilidad de operación", utilidad_operacion),
        ("Gastos financieros", gastos_financieros_resultado),
        ("Total de otros gastos", total_otros_gastos),
        ("Utilidad antes de impuestos", utilidad_antes_impuestos),
        ("Impuestos", impuestos),
        ("Utilidad neta", utilidad_neta),
    ]

    pdf.create_table(estado_resultados)

    pdf.add_page()
    pdf.chapter_title('Balance General')
    
    balance_general = [
        ("Activos", sum(activos.values())),
        ("Pasivos", sum(pasivos.values())),
        ("Capital", sum(capital.values())),
        ("Pasivo + Capital", sum(pasivos.values()) + sum(capital.values()))
    ]

    pdf.create_table(balance_general)

    # Añadir la distribución de utilidades al PDF
    pdf.add_page()
    pdf.chapter_title('Distribución de Utilidades')
    distribucion_utilidades_data = [
        ("Bancos", bancos),
        ("Caja", caja)
    ]
    pdf.create_table(distribucion_utilidades_data)

    ruta_guardado = r'C:\Users\isaac\Desktop\Reporte\reporte_financiero.pdf'
    pdf.output(ruta_guardado)

    print(f"\nReporte financiero guardado en: {ruta_guardado}")

btn_generar = tk.Button(scrollable_frame, text="Generar PDF", command=generar_pdf)
btn_generar.grid(row=4, column=0, columnspan=5, pady=20)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte Financiero', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def create_table(self, data):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Estado de Resultados', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        
        col_width = (self.w - 2 * self.l_margin) / 2  
        row_height = self.font_size + 2  
        spacing = 1.5  
        
        for row in data:
            for item in row:
                self.cell(col_width, row_height * spacing, str(item), border=1)
            self.ln(row_height * spacing)

root.mainloop()
