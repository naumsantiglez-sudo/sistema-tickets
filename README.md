
# Sistema de tickets

<p>
  Algunos temas que vimos
</p>

<ul>
  <li>Estructuras de datos (Stack, Queue, Lista enlazada, Árbol, Grafo)</li>
  <li>Programación orientada a objetos (clases y objetos)</li>
  <li>Manejo de archivos (JSON)</li>
  <li>Manejo de errores (try, except)</li>
  <li>Funciones</li>
  <li>Condicionales</li>
  <li>Ciclos (while)</li>
  <li>Persistencia de datos</li>
  <li>Búsqueda de datos</li>
  <li>Ordenamiento de datos</li>
  <li>Menú interactivo</li>
  <li>Manejo de fechas (datetime)</li>
  <li>Manejo del sistema de archivos (os)</li>
  <li>Tipado de datos (typing)</li>
  <li>Estructuras dinámicas (nodos)</li>
  <li>Algoritmos de recorrido (inorden en árbol)</li>
  <li>Detección de ciclos (grafos)</li>
  <li>Historial de acciones (uso de pila)</li>
  <li>Colas de atención (FIFO)</li>
  <li>Undo/Redo (manejo de estados)</li>
</ul>

<p><strong>Explicacion del codigo</strong></p>
<p>
Este programa es un sistema de gestión de tickets desarrollado en Python. Permite crear, organizar, atender y cerrar tickets utilizando diferentes estructuras de datos, simulando el funcionamiento de un sistema real de soporte técnico.
</p>

<p><strong>Funcionamiento general</strong></p>
<p>
El sistema trabaja mediante un menú interactivo en consola que permite al usuario realizar distintas acciones como crear tickets, atenderlos, cerrarlos, consultar información y guardar datos.
</p>
<p>
Cada ticket contiene información como descripción, área, prioridad, fecha, estado e historial de acciones.
</p>

<p><strong>Estructuras utilizadas</strong></p>
<ul>
  <li>Cola (Queue) para el orden de atención</li>
  <li>Pila (Stack) para historial y undo/redo</li>
  <li>Lista enlazada para tickets abiertos y cerrados</li>
  <li>Árbol binario de búsqueda (BST) para prioridades</li>
  <li>Grafo para dependencias entre tickets</li>
</ul>

<p><strong>Funciones principales</strong></p>
<ul>
  <li>Crear tickets</li>
  <li>Atender tickets</li>
  <li>Cerrar tickets</li>
  <li>Consultar historial</li>
  <li>Buscar tickets por ID</li>
  <li>Clasificar por prioridad</li>
  <li>Agregar dependencias</li>
  <li>Generar reportes</li>
  <li>Deshacer acciones (undo)</li>
</ul>

<p><strong>Manejo de errores</strong></p>
<p>
El programa utiliza manejo de excepciones para evitar fallos durante la ejecución, especialmente al ingresar datos incorrectos o trabajar con archivos.
</p>

<p><strong>Persistencia de datos</strong></p>
<p>
Los datos se guardan en archivos JSON, lo que permite conservar la información incluso después de cerrar el programa. Al iniciar, el sistema puede cargar automáticamente los datos guardados.
</p>

<p><strong>Características adicionales</strong></p>
<ul>
  <li>Control de dependencias entre tickets</li>
  <li>Detección de ciclos</li>
  <li>Registro de historial</li>
  <li>Sistema de undo</li>
  <li>Búsqueda y ordenamiento de datos</li>
</ul>
