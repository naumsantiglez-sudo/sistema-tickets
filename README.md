📌Descripción del Sistema

Este proyecto es un Sistema de Gestión de Tickets desarrollado en Python que permite administrar incidencias (soporte técnico, fallas, solicitudes, etc.) utilizando diferentes estructuras de datos.

El sistema implementa:

Pila (Stack)
Cola (Queue)
Lista enlazada
Árbol binario de búsqueda (BST)
Grafo dirigido

Además, incluye funcionalidades como:

Crear, atender y cerrar tickets
Registrar historial de acciones
Manejar dependencias entre tickets
Guardar y cargar datos en archivos JSON
Sistema básico de undo (deshacer)
🧠 Estructuras de Datos Utilizadas
🔹 Stack (Pila)

Se usa para manejar el historial de acciones de cada ticket y el sistema de undo/redo.

Funciona con el principio LIFO (último en entrar, primero en salir)
Métodos principales:
push(): agrega un elemento
pop(): elimina el último elemento
peek(): consulta el último elemento
to_list(): convierte la pila en lista
🔹 Queue (Cola)

Se utiliza para gestionar los tickets en espera.

Funciona con el principio FIFO (primero en entrar, primero en salir)
Métodos:
enqueue(): agrega ticket a la cola
dequeue(): atiende el primer ticket
peek(): muestra el siguiente ticket
🔹 LinkedList (Lista Enlazada)

Se usa para almacenar:

Tickets abiertos
Tickets cerrados

Permite:

Insertar tickets
Buscar por ID
Eliminar tickets
🔹 BST (Árbol Binario de Búsqueda)

Organiza los tickets por prioridad.

Prioridades:
1 → Alta
2 → Media
3 → Baja

Permite:

Insertar tickets según prioridad
Recorrer en orden (inorder) para ver tickets ordenados
🔹 Graph (Grafo Dirigido)

Se usa para manejar dependencias entre tickets.

Ejemplo:

Un ticket no se puede cerrar si depende de otro

Funciones importantes:

add_dependency(): agrega dependencia
has_circular_dependency(): detecta ciclos (muy importante)
get_dependencies(): obtiene dependencias
🎫 Clase Ticket

Representa cada incidencia del sistema.

Atributos:

id: identificador único
descripcion: detalle del problema
area: redes, software o hardware
prioridad: nivel de urgencia
fecha: fecha de creación
estado: abierto o cerrado
historial: pila de acciones

Métodos:

to_dict(): convierte el ticket a formato JSON
from_dict(): reconstruye un ticket desde JSON
⚙️ Clase Principal: TicketSystem

Es el núcleo del sistema, donde se integran todas las estructuras.

Funciones principales:
🟢 Crear Ticket
crear_ticket(descripcion, area, prioridad)
Genera un ticket nuevo
Lo agrega a:
Cola
Lista de abiertos
Árbol de prioridad
Grafo
🟡 Atender Ticket
atender_ticket()
Saca el ticket de la cola (FIFO)
Registra acción en historial
🔴 Cerrar Ticket
cerrar_ticket(ticket_id)
Verifica dependencias
Cambia estado a "cerrado"
Lo mueve a la lista de cerrados
📝 Historial
ver_historial(ticket_id)
Muestra todas las acciones del ticket
🔗 Dependencias
agregar_dependencia(ticket_id, depende_de_id)
Relaciona tickets
Evita ciclos en el grafo
🔍 Búsqueda
buscar_por_id(ticket_id)
buscar_por_prioridad(prioridad)
💾 Persistencia
save_all()
load_all()
Guarda y carga datos en archivos JSON:
cola.json
abiertos.json
cerrados.json
grafo.json
↩️ Undo
undo()
Permite deshacer acciones básicas como:
crear ticket
cerrar ticket
🖥️ Interfaz de Usuario (CLI)

El sistema incluye un menú en consola:

Opciones:

Crear ticket
Ver cola
Atender ticket
Cerrar ticket
Ver historial
Agregar dependencia
Consultar dependencias
Buscar por ID
Mostrar por prioridad
Guardar datos
Cargar datos
Reportes
Undo
Salir
📊 Características Destacadas

✔ Uso de múltiples estructuras de datos reales
✔ Persistencia en archivos JSON
✔ Manejo de dependencias con grafos
✔ Prevención de ciclos
✔ Sistema básico de undo
✔ Organización por prioridad y fecha
