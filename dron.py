
# SIMULACIÓN 3D DE DRÓN — FASE 4
# Librerías: vpython, numpy, matplotlib


from vpython import *
import numpy as np
import matplotlib.pyplot as plt

# DEFINICIÓN DE FUNCIONES MATEMÁTICAS

# Posición/Altitud h(t)
def h(t):
    return -0.1 * t**4 + 1.6 * t**3 - 7.2 * t**2 + 10 * t + 5

# Velocidad instantánea = derivada h'(t)
def h_prime(t):
    return -0.4 * t**3 + 4.8 * t**2 - 14.4 * t + 10

# Temperatura del motor: T'(t) = 0.6t² - 2t + 4, con T(0) = 22.
def temperature_rate(t):
    return 0.6 * t**2 - 2 * t + 4

def temperature(t):
    return 0.2 * t**3 - t**2 + 4 * t + 22

# Consumo de datos D(t) y su integral definida.
def data_rate(t):
    return 3 * t**2 + 2 * t + 5

def integral_h(t1, t2):
    def D(t):
        return t**3 + t**2 + 5 * t
    return D(t2) - D(t1)


# CONFIGURACIÓN DE LA ESCENA 3D

scene = canvas(title="SIMULACIÓN 3D — DRÓN",
               width=900, height=600,
               center=vector(5, 30, 0),
               background=color.cyan)

# Objeto Drón (esfera + estructura)
dron = sphere(pos=vector(0, h(0), 0), radius=0.5,
              color=color.red, make_trail=True, trail_radius=0.1)
prop1 = cylinder(pos=dron.pos + vector(0.6, 0.3, 0), axis=vector(0.4, 0, 0),
                 radius=0.1, color=color.blue)
prop2 = cylinder(pos=dron.pos + vector(-0.6, 0.3, 0), axis=vector(-0.4, 0, 0),
                 radius=0.1, color=color.blue)

# Suelo y referencias
suelo = box(pos=vector(5, -2, 0), size=vector(12, 0.5, 6), color=color.green)


# VARIABLES DE SIMULACIÓN

t_total = 10          # segundos de simulación
dt = 0.02             # paso de tiempo
t = 0.0
t1 = 1.0              # límite inferior integral
t2 = 4.0              # límite superior integral
tiempo_h = []
posicion_h = []
velocidad_v = []
datos_D = []


# BUCLE PRINCIPAL DE SIMULACIÓN

while t <= t_total:
    rate(50)  # 50 fps → animación fluida

    # Cálculos en tiempo real
    altitud = h(t)
    velocidad = h_prime(t)
    datos_acum = integral_h(t1, t) if t >= t1 and t <= t2 else 0

    # Guardar datos para gráficas
    tiempo_h.append(t)
    posicion_h.append(altitud)
    velocidad_v.append(velocidad)
    datos_D.append(datos_acum)

    # Mover drón en 3D (movimiento en X e Y según h(t))
    dron.pos = vector(t, altitud, np.sin(t) * 2)
    prop1.pos = dron.pos + vector(0.6, 0.3, 0)
    prop2.pos = dron.pos + vector(-0.6, 0.3, 0)
    scene.center = dron.pos

    # HUD — Telemetría en pantalla
    telemetria = f"""
    TELEMETRÍA EN TIEMPO REAL
    Tiempo t: {t:.2f} s
    Altitud h(t): {altitud:.2f} m
    Velocidad h'(t): {velocidad:.2f} m/s
    Integral acumulada: {datos_acum:.2f} m·s
    """
    scene.caption = telemetria

    t += dt


# GRÁFICAS DE RESUMEN — MATPLOTLIB (3 subplots)

print("\n📊 Generando gráficas de resumen...")
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 14))
plt.subplots_adjust(hspace=0.4)

# ---------- GRÁFICA 1: Posición / Altitud h(t) ----------
ax1.plot(tiempo_h, posicion_h, 'r-', linewidth=2, label='h(t) - Altitud')
ax1.set_title('Gráfica 1: Posición / Altitud h(t)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Altitud (m)')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.axvline(x=0, color='black', linewidth=0.5)
ax1.axhline(y=0, color='black', linewidth=0.5)

# ---------- GRÁFICA 2: Velocidad v(t) = h'(t) + Recta tangente ----------
ax2.plot(tiempo_h, velocidad_v, 'b-', linewidth=2, label="v(t) = h'(t) - Velocidad")
# Punto máximo de velocidad: t=2.5 → v=13.5
t_max = 2.5
v_max = h_prime(t_max)
# Recta tangente en punto máximo: y = v_max
ax2.axhline(y=v_max, color='green', linestyle='--', linewidth=2,
            label=f'Recta tangente en t={t_max}s → v={v_max:.2f} m/s')
ax2.scatter(t_max, v_max, color='red', s=100, zorder=5, label='Punto máximo')
ax2.set_title('Gráfica 2: Velocidad instantánea h\'(t) + Recta tangente', fontsize=13, fontweight='bold')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Velocidad (m/s)')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.axvline(x=0, color='black', linewidth=0.5)
ax2.axhline(y=0, color='black', linewidth=0.5)

# ---------- GRÁFICA 3: Integral acumulada + Área bajo curva t=1 a t=4 ----------
ax3.plot(tiempo_h, datos_D, 'purple', linewidth=2, label='∫h(t)dt — Integral acumulada')
# Área sombreada entre t=1 y t=4
mask = (np.array(tiempo_h) >= 1) & (np.array(tiempo_h) <= 4)
ax3.fill_between(np.array(tiempo_h)[mask], np.array(datos_D)[mask],
                 alpha=0.4, color='orange', label='Área bajo la curva t=1 a t=4')
ax3.set_title('Gráfica 3: Integral Definida de la Altitud', fontsize=13, fontweight='bold')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Integral de altitud (m·s)')
ax3.grid(True, alpha=0.3)
ax3.legend()
ax3.axvline(x=0, color='black', linewidth=0.5)
ax3.axhline(y=0, color='black', linewidth=0.5)

plt.suptitle('RESUMEN DE TELEMETRÍA — SIMULACIÓN DRÓN 3D', fontsize=16, fontweight='bold', y=0.995)
plt.show()