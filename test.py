import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from drive import guardar_en_google_sheets,agregar_contacto
import datetime
#pip freeze > requirements.txt
#streamlit run test.py

# Configuración de la página para que sea responsiva
st.set_page_config(layout="wide")

# Estilo CSS para mejorar la visualización en móviles y tablets
st.markdown("""
<style>
    .stRadio > label {
        font-size: 1.2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        font-size: 1.3rem;
    }
    .stMarkdown {
        font-size: 1.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Título y descripción
st.title("🧠 Test de Inteligencias Múltiples - El Expreso de Leo 🚂")
st.markdown("""
Este test es una herramienta de observación para familias de niños de 0 a 2 años.
Su propósito es ayudar a reconocer cómo aprende, se expresa y se relaciona su hijo.

En los primeros años de vida, los bebés no se evalúan. Se observan, se escuchan y se acompañan.

Esta guía te ayudará a reconocer las formas naturales en que tu bebé se expresa y aprende.

""")

# Aviso de Habeas Data
st.header("📜 Aviso de Privacidad y Tratamiento de Datos")
acepto = st.checkbox("""
Este formulario tiene como finalidad recolectar sus datos personales para procesar los resultados del **Test de Inteligencias Múltiples** y brindar una orientación personalizada sobre el perfil de aprendizaje de su hijo(a). 

La información recolectada será tratada bajo los principios de confidencialidad y seguridad, conforme a la **Ley 1581 de 2012 de Protección de Datos Personales (Habeas Data)** en Colombia.

El responsable del tratamiento de estos datos es **Editorial Bebe Genial**.

Al registrar sus datos, **usted autoriza a la editorial para**:

1.Gestionar y entregar los resultados del presente test.

2.Enviarle información pedagógica, publicidad de nuestros productos y servicios educativos.

3.Contactarlo para asesoría sobre el material didáctico que mejor se adapte a los resultados obtenidos.

Usted tiene derecho a conocer, actualizar y rectificar sus datos en cualquier momento a través del correo **servicioalcliente@bebegenial.com**.

Puede consultar nuestra Política de Privacidad [aquí](https://www.bebegenial.com/privacy-policy/).

**Al marcar esta casilla, usted acepta el tratamiento de sus datos conforme a lo descrito.**
""")

# Si no acepta, no se muestra el formulario
if not acepto:
    st.stop()

# Diccionario para mapear ID a nombre del comercial
comerciales = {
    "0490": "Paula",
    "8971": "Pilar",
    "8949": "Lorena",
    "8870": "Sebastian",
    "7171": "Angelo",
    "9043": "Martha",
    "0640": "Edgar",
    "0080": "Estefania",
    "7863": "Eliana",
    "7509": "Sandra",
    "0048": "Nataly"
}

# Recolección de datos
st.header("✨ Recolección de datos")
nombre = st.text_input("Nombre del padre o representante legal:")
correo = st.text_input("Correo electrónico:")
telefono = st.text_input("Teléfono:")
nombre_nino = st.text_input("Nombre del niño:")
fecha_nacimiento = st.date_input(
    "Fecha de nacimiento del niño:",
    value=None, # Puedes poner datetime.date(2015, 1, 1) como predeterminado
    #min_value=datetime.date(2006, 1, 1), # Límite inferior
    min_value = datetime.date.today() - datetime.timedelta(days=730),
    #max_value=datetime.date.today(),      # No permite fechas futuras
    format="DD/MM/YYYY"
)
#id_comercial = st.selectbox("ID del comercial:", index=None ,options=list(comerciales.keys()))

# Validación de correo y teléfono
def validar_correo(correo):
    return "@" in correo and "." in correo.split("@")[-1]

def validar_telefono(telefono):
    # Primero verificamos que sean solo números
    if not telefono.isdigit():
        return False
    
    # Si inicia con "3", la longitud debe ser >= 10
    if telefono.startswith("3"):
        return len(telefono) >= 10
    
    # Para cualquier otro caso, mantenemos la regla de longitud >= 7
    return len(telefono) >= 7

# Sección de preguntas
st.header("📝 Test de Expresiones Naturales")
inteligencias = [
    "Cuerpo", "Sonidos", "Observacion", "Vinculo", "Emociones", "Exploracion Sensorial"
]

preguntas = [
    # Cuerpo
    "Necesita moverse constantemente.",
    "Explora todo con manos, pies o boca.",
    "Aprende gateando, caminando, tocando.",
    "Expresa emociones con movimientos.",
    # SONIDOS
    "Reacciona a la música o a tu voz.",
    "Se calma cuando le cantas.",
    "Balbucea, vocaliza o imita sonidos.",
    "Reconoce melodías familiares.",
    # OBSERVACIÓN
    "Observa con atención luces, colores y movimientos.",
    "Sigue objetos con la mirada.",
    "Explora visualmente antes de tocar.",
    "Reconoce espacios conocidos.",
    # VÍNCULO
    "Busca tu mirada y tu cercanía.",
    "Se calma con el contacto.",
    "Disfruta juegos compartidos.",
    "Responde a emociones de los demás.",
    # EMOCIONES
    "Expresa claramente agrado o desagrado.",
    "Busca consuelo cuando lo necesita.",
    "Se siente seguro con rutinas.",
    "Empieza a autorregularse con ayuda.",
    # EXPLORACIÓN SENSORIAL
    "Disfruta tocar distintas texturas.",
    "Observa animales, plantas o agua.",
    "Reacciona a estímulos naturales.",
    "Explora el entorno con curiosidad."
]

# Diccionario para almacenar respuestas
respuestas = {}

# Mostrar preguntas y opciones (sin valores numéricos y sin preselección)
for i, pregunta in enumerate(preguntas):
    respuestas[f"pregunta_{i+1}"] = st.radio(
        f"**{i+1}. {pregunta}**",
        options=["Nunca", "Ocasionalmente", "Frecuentemente", "Siempre"],
        index=None,  # Evita que esté preseleccionado
        key=f"pregunta_{i+1}"
    )

# Botón para procesar resultados
procesado = st.button("Procesar resultados", key="boton_procesar_1")

if procesado:
    # Validar datos
    if not validar_correo(correo):
        st.error("Por favor, ingresa un correo electrónico válido.")
    elif not nombre:
        st.error("Por favor, ingresa el nombre del padre o representante legal.")
    elif not nombre_nino:
        st.error("Por favor, ingresa el nombre del niño.")
    elif not fecha_nacimiento:
        st.error("Por favor, ingresa la fecha de nacimiento del niño.")
    elif not validar_telefono(telefono):
        st.error("Por favor, ingresa un número de teléfono válido.")
    elif any(respuesta is None for respuesta in respuestas.values()):
        st.error("Por favor, responde todas las preguntas.")
    #elif id_comercial is None or id_comercial == "":
    #    st.error("Por favor, selecciona el ID de un comercial.")
    else:
        # Asignar valores numéricos según la respuesta seleccionada
        valores_respuestas = {
            "Nunca": 0,
            "Ocasionalmente": 1,
            "Frecuentemente": 2,
            "Siempre": 3
        }

        # Calcular subtotales
        subtotales = {}
        for idx, inteligencia in enumerate(inteligencias):
            inicio = idx * 4
            fin = inicio + 4
            subtotales[inteligencia] = sum(
                valores_respuestas[respuestas[f"pregunta_{i+1}"]] for i in range(inicio, fin)
            )

        # Obtener el nombre del comercial a partir del ID seleccionado
        #nombre_comercial = comerciales[id_comercial]

        # Mostrar resultados
        resultado_test = ""
        st.header("📊 Resultados")
        st.write("### Subtotales por observacion:")
        for inteligencia, puntaje in subtotales.items():
            st.write(f"- **{inteligencia}**: {puntaje}/12")
            # Creando una variable llamada 'Resultado' que almacena el resultado de los resultados
            resultado_test += f"- {inteligencia}: {puntaje}/12\n"
        
        # Gráfico de barras con etiquetas inclinadas
        fig, ax = plt.subplots(figsize=(10, 6))
        barras = ax.bar(subtotales.keys(), subtotales.values(), color=[
            "#9b59b6", "#3498db", "#2ecc71", "#e74c3c",
            "#f1c40f", "#e67e22", "#1abc9c", "#34495e"
        ])
        ax.set_ylabel("Puntuación")
        ax.set_title("Puntuación por observacion")
        ax.bar_label(barras, labels=[f"{valor}" for valor in subtotales.values()], padding=3)
        plt.xticks(rotation=45, ha='right')  # Inclinar etiquetas a 45 grados
        st.pyplot(fig)

        ###########################################################################################
        # Gráfico general radar chart
        # Gráfico de radar
        fig2 = plt.figure(figsize=(8, 8))
        ax2 = fig2.add_subplot(111, polar=True)

        # Configurar los ángulos para cada inteligencia
        categorias = list(subtotales.keys())
        N = len(categorias)
        angulos = [n / float(N) * 2 * 3.14159 for n in range(N)]
        angulos += angulos[:1]  # Cerrar el gráfico

        # Valores de las puntuaciones
        valores = list(subtotales.values())
        valores += valores[:1]  # Cerrar el gráfico

        # Dibujar el radar chart
        ax2.plot(angulos, valores, color='blue', linewidth=2, linestyle='solid', label='Puntuación')
        ax2.fill(angulos, valores, color='blue', alpha=0.25)

        # Configurar las etiquetas y título
        ax2.set_thetagrids([a * 180/3.14159 for a in angulos[:-1]], categorias)
        ax2.set_title("Perfil de Observación", size=15, y=1.1)
        ax2.grid(True)

        # Establecer el límite del eje radial
        ax2.set_ylim(0, 12)

        st.pyplot(fig2)
        ###########################################################################################

        # Deshabilitar botón
        st.success("Tu bebé no necesita demostrar nada. Necesita ser mirado, comprendido y acompañado.")
        st.success("🚂 El Expreso de Leo diseña experiencias que respetan estas formas de expresión y acompañan el desarrollo integral desde el nacimiento.")
        st.success("Cuando entendemos cómo se expresa un bebé, sabemos cómo acompañarlo mejor.")
        st.button("Procesar resultados", disabled=True, key="boton_procesar_deshabilitado")

        ###########################################################################################
        # Crear el dato en GHL
        #agregar_contacto(nombre, correo, telefono, nombre_comercial, resultado_test)
        # Guardar en Google Sheets
        # Convertimos a minúsculas para que la validación sea insensible a mayúsculas
        if "prueba" in nombre.lower():
            print(f"Registro omitido: El nombre '{nombre}' contiene la palabra de control 'prueba'.")
        else:
            print(f"Validación exitosa. Procediendo a crear cliente: {nombre}")
            # Ejecutamos la función que ya definiste anteriormente
            try:
                guardar_en_google_sheets(nombre, correo, telefono, nombre_nino, str(fecha_nacimiento), "Organico", respuestas, resultado_test) 
            except Exception as e:
                print(f"Error al crear el cliente en Google Sheets: {str(e)}")
                
