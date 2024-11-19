# TrackProfit

**TrackProfit** es una herramienta automatizada para monitorear, analizar y predecir el rendimiento de tus inversiones. El proyecto se centra en recolectar datos financieros de diversas plataformas como Orionx, Fintual y MercadoPago, procesarlos, y generar insights a través de gráficos y modelos de predicción basados en IA.

## 🚀 Funcionalidades

- **Recolección automática de datos**: Obtén totales diarios desde tus cuentas en Orionx, Fintual y MercadoPago.
- **Almacenamiento estructurado**: Guarda tus balances en una base de datos o Google Sheets.
- **Análisis de noticias**: Analiza noticias relevantes para identificar posibles impactos en tus inversiones.
- **Gráficos y reportes**: Genera gráficos automáticos para visualizar tendencias y tomar decisiones informadas.
- **Predicción basada en IA**: Conecta noticias y eventos del mercado con el comportamiento de tus inversiones.

---

## 📦 Instalación

### 1. Clona este repositorio
```bash
git clone git@github.com:M4uRoDev/TrackProfit.git
cd TrackProfit
```

### 2. Configuración Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate # En windows: ./venv/Scripts/activate
```

### 3. Instalación Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configuración API Keys
Modifica el archivo .env.example con las credenciales asociadas a tus cuentas.

## 🛠️ Uso 

### 1. Ejecutar Script para Orionx
```bash
python orionx.py
```

### 2. Ejecuta la recolección centralizada
```bash
python trackprofit.py
```

### 3. Automatización diaria
Configuración de un cron job para recolectar datos automáticamente:
```bash
0 9 * * * /path/to/venv/bin/python /path/to/TrackProfit/trackprofit.py
```

## 📚 Documentación Adicional

### Orionx API
Consulta la documentación oficial de Orionx para más detalles sobre su API: [Orionx API Docs](https://docs.orionx.com/docs/)

### Próximas integraciones
- **Fintual API**: Automatización para inversiones en depósitos a plazo y acciones.
- **MercadoPago API**: Recolección de intereses generados en tu cuenta.
