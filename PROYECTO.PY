import json
import os
import datetime
from typing import Optional, Any, List, Dict, Tuple

# Estructuras Lineales: Stack y Queue (definir antes de Ticket para evitar errores)
class StackNode:
    def __init__(self, data: Any, next: Optional['StackNode'] = None):
        self.data = data
        self.next = next

class Stack:
    def __init__(self):
        self.top: Optional[StackNode] = None

    def push(self, data: Any):
        node = StackNode(data, self.top)
        self.top = node

    def pop(self) -> Any:
        if not self.top:
            return None
        data = self.top.data
        self.top = self.top.next
        return data

    def peek(self) -> Any:
        return self.top.data if self.top else None

    def is_empty(self) -> bool:
        return self.top is None

    def to_list(self) -> List[Any]:
        lst = []
        cur = self.top
        while cur:
            lst.append(cur.data)
            cur = cur.next
        return lst[::-1]  # retornar en orden cronológico (más antiguo primero)

    def clear(self):
        self.top = None

class Queue:
    def __init__(self):
        self.items: List['Ticket'] = []

    def enqueue(self, ticket: 'Ticket'):
        self.items.append(ticket)

    def dequeue(self) -> Optional['Ticket']:
        if not self.items:
            return None
        return self.items.pop(0)

    def peek(self) -> Optional['Ticket']:
        return self.items[0] if self.items else None

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

    def to_list(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self.items]

# -----------------------------
# Clase Ticket
# -----------------------------
class Ticket:
    def __init__(self, ticket_id: int, descripcion: str, area: str, prioridad: int, fecha: Optional[str] = None):
        self.id = int(ticket_id)
        self.descripcion = descripcion
        self.area = area
        self.prioridad = int(prioridad)  # 1 = alta, 2 = media, 3 = baja
        self.fecha = fecha if fecha else datetime.datetime.now().isoformat()
        self.historial = Stack()  # pila local para historial de acciones del ticket
        self.estado = 'abierto'  # 'abierto' o 'cerrado'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'area': self.area,
            'prioridad': self.prioridad,
            'fecha': self.fecha,
            'historial': self.historial.to_list(),
            'estado': self.estado
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        t = Ticket(d['id'], d['descripcion'], d['area'], d['prioridad'], d.get('fecha'))
        t.estado = d.get('estado', 'abierto')
        # cargar historial (lista) en la pila (insertar en orden)
        for accion in d.get('historial', []):
            t.historial.push(accion)
        return t

# -----------------------------
# Lista Enlazada simple para tickets abiertos y cerrados
# -----------------------------
class LinkedListNode:
    def __init__(self, ticket: Ticket, next: Optional['LinkedListNode'] = None):
        self.ticket = ticket
        self.next = next

class LinkedList:
    def __init__(self):
        self.head: Optional[LinkedListNode] = None

    def insert(self, ticket: Ticket):
        node = LinkedListNode(ticket, self.head)
        self.head = node

    def remove_by_id(self, ticket_id: int) -> Optional[Ticket]:
        prev = None
        cur = self.head
        while cur:
            if cur.ticket.id == ticket_id:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return cur.ticket
            prev = cur
            cur = cur.next
        return None

    def find_by_id(self, ticket_id: int) -> Optional[Ticket]:
        cur = self.head
        while cur:
            if cur.ticket.id == ticket_id:
                return cur.ticket
            cur = cur.next
        return None

    def to_list(self) -> List[Dict[str, Any]]:
        arr: List[Dict[str, Any]] = []
        cur = self.head
        while cur:
            arr.append(cur.ticket.to_dict())
            cur = cur.next
        return arr

# -----------------------------
# Árbol de búsqueda para clasificar por prioridad (BST por prioridad)
# -----------------------------
class BSTNode:
    def __init__(self, key: int, tickets: Optional[List[Ticket]] = None):
        self.key = key
        self.tickets = tickets if tickets else []
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BST:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, ticket: Ticket):
        def _insert(node: Optional[BSTNode], key: int, ticket: Ticket) -> BSTNode:
            if node is None:
                return BSTNode(key, [ticket])
            if key == node.key:
                node.tickets.append(ticket)
            elif key < node.key:
                node.left = _insert(node.left, key, ticket)
            else:
                node.right = _insert(node.right, key, ticket)
            return node
        self.root = _insert(self.root, ticket.prioridad, ticket)

    def inorder(self) -> List[Ticket]:
        res: List[Ticket] = []
        def _inorder(node: Optional[BSTNode]):
            if not node:
                return
            _inorder(node.left)
            res.extend(node.tickets)
            _inorder(node.right)
        _inorder(self.root)
        return res

    def find_by_priority(self, prioridad: int) -> List[Ticket]:
        node = self.root
        while node:
            if prioridad == node.key:
                return node.tickets
            elif prioridad < node.key:
                node = node.left
            else:
                node = node.right
        return []

# -----------------------------
# Grafo dirigido para dependencias entre tickets
# -----------------------------
class Graph:
    def __init__(self):
        # adjacency list: ticket_id -> set of ticket_ids it depends on
        self.adj: Dict[int, set] = {}

    def add_ticket(self, ticket_id: int):
        if ticket_id not in self.adj:
            self.adj[ticket_id] = set()

    def add_dependency(self, ticket_id: int, depends_on_id: int):
        self.add_ticket(ticket_id)
        self.add_ticket(depends_on_id)
        self.adj[ticket_id].add(depends_on_id)

    def remove_dependency(self, ticket_id: int, depends_on_id: int):
        if ticket_id in self.adj and depends_on_id in self.adj[ticket_id]:
            self.adj[ticket_id].remove(depends_on_id)

    def get_dependencies(self, ticket_id: int) -> List[int]:
        return list(self.adj.get(ticket_id, []))

    def has_circular_dependency(self) -> bool:
        visited = set()
        recstack = set()

        def dfs(v):
            visited.add(v)
            recstack.add(v)
            for nei in self.adj.get(v, []):
                if nei not in visited:
                    if dfs(nei):
                        return True
                elif nei in recstack:
                    return True
            recstack.remove(v)
            return False

        for node in list(self.adj.keys()):
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def to_dict(self) -> Dict[str, List[int]]:
        return {str(k): list(v) for k, v in self.adj.items()}

    @staticmethod
    def from_dict(d: Dict[str, List[int]]):
        g = Graph()
        for k, lst in d.items():
            kid = int(k)
            g.add_ticket(kid)
            for v in lst:
                g.add_dependency(kid, int(v))
        return g

# -----------------------------
# Sistema completo: combina todo
# -----------------------------
class TicketSystem:
    def __init__(self):
        self.next_id = 1
        self.cola = Queue()
        self.abiertos = LinkedList()
        self.cerrados = LinkedList()
        self.arbol_prioridad = BST()
        self.grafo = Graph()
        # para undo/redo global (acciones en la cola o estado)
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        # ruta archivos
        self.dir_data = 'data_tickets'
        try:
            os.makedirs(self.dir_data, exist_ok=True)
        except OSError:
            # si falla crear carpeta, usar carpeta actual
            self.dir_data = '.'

    # ------------------------
    # Crear ticket
    # ------------------------
    def crear_ticket(self, descripcion: str, area: str, prioridad: int) -> Ticket:
        ticket = Ticket(self.next_id, descripcion, area, prioridad)
        self.next_id += 1
        # acciones iniciales
        ticket.historial.push(f'Creado: {ticket.fecha}')
        # guardar en estructuras
        self.cola.enqueue(ticket)
        self.abiertos.insert(ticket)
        self.arbol_prioridad.insert(ticket)
        self.grafo.add_ticket(ticket.id)
        # registrar en undo (acción simple)
        self.undo_stack.push(('crear', ticket.id))
        self.redo_stack.clear()
        return ticket

    # ------------------------
    # Atender ticket (dequeue) y mover a atendidos/cerrados según acción
    # ------------------------
    def atender_ticket(self) -> Optional[Ticket]:
        ticket = self.cola.dequeue()
        if not ticket:
            return None
        ticket.historial.push(f'Atendido: {datetime.datetime.now().isoformat()}')
        self.undo_stack.push(('atender', ticket.id))
        self.redo_stack.clear()
        return ticket

    def cerrar_ticket(self, ticket_id: int) -> bool:
        deps = self.grafo.get_dependencies(ticket_id)
        if deps:
            # no se puede cerrar si tiene dependencias no resueltas
            return False
        ticket = self.abiertos.remove_by_id(ticket_id)
        if not ticket:
            return False
        ticket.estado = 'cerrado'
        ticket.historial.push(f'Cerrado: {datetime.datetime.now().isoformat()}')
        self.cerrados.insert(ticket)
        self.undo_stack.push(('cerrar', ticket_id))
        self.redo_stack.clear()
        return True

    # ------------------------
    # Historial por ticket (usar pilas)
    # ------------------------
    def registrar_accion_ticket(self, ticket_id: int, accion: str):
        ticket = self.abiertos.find_by_id(ticket_id) or self.cerrados.find_by_id(ticket_id)
        if not ticket:
            return False
        ticket.historial.push(f'{datetime.datetime.now().isoformat()} - {accion}')
        self.undo_stack.push(('accion', ticket_id, accion))
        self.redo_stack.clear()
        return True

    def ver_historial(self, ticket_id: int) -> List[str]:
        ticket = self.abiertos.find_by_id(ticket_id) or self.cerrados.find_by_id(ticket_id)
        if not ticket:
            return []
        return ticket.historial.to_list()

    # ------------------------
    # Dependencias (grafo)
    # ------------------------
    def agregar_dependencia(self, ticket_id: int, depende_de_id: int) -> bool:
        t1 = self.abiertos.find_by_id(ticket_id) or self.cerrados.find_by_id(ticket_id)
        t2 = self.abiertos.find_by_id(depende_de_id) or self.cerrados.find_by_id(depende_de_id)
        if not t1 or not t2:
            return False
        self.grafo.add_dependency(ticket_id, depende_de_id)
        if self.grafo.has_circular_dependency():
            self.grafo.remove_dependency(ticket_id, depende_de_id)
            return False
        self.undo_stack.push(('dependencia', ticket_id, depende_de_id))
        self.redo_stack.clear()
        return True

    # ------------------------
    # Búsqueda y ordenamiento
    # ------------------------
    def buscar_por_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.abiertos.find_by_id(ticket_id) or self.cerrados.find_by_id(ticket_id)

    def buscar_por_prioridad(self, prioridad: int) -> List[Ticket]:
        return self.arbol_prioridad.find_by_priority(prioridad)

    def ordenar_tickets_por_fecha(self, lista: List[Ticket]) -> List[Ticket]:
        return sorted(lista, key=lambda t: t.fecha)

    def ordenar_tickets_por_prioridad(self, lista: List[Ticket]) -> List[Ticket]:
        return sorted(lista, key=lambda t: t.prioridad)

    # ------------------------
    # Persistencia: guardar y cargar estructuras en archivos JSON
    # ------------------------
    def save_all(self):
        try:
            # cola
            with open(os.path.join(self.dir_data, 'cola.json'), 'w', encoding='utf-8') as f:
                json.dump(self.cola.to_list(), f, ensure_ascii=False, indent=2)
            # abiertos
            with open(os.path.join(self.dir_data, 'abiertos.json'), 'w', encoding='utf-8') as f:
                json.dump(self.abiertos.to_list(), f, ensure_ascii=False, indent=2)
            # cerrados
            with open(os.path.join(self.dir_data, 'cerrados.json'), 'w', encoding='utf-8') as f:
                json.dump(self.cerrados.to_list(), f, ensure_ascii=False, indent=2)
            # grafo
            with open(os.path.join(self.dir_data, 'grafo.json'), 'w', encoding='utf-8') as f:
                json.dump(self.grafo.to_dict(), f, ensure_ascii=False, indent=2)
            # meta
            with open(os.path.join(self.dir_data, 'meta.json'), 'w', encoding='utf-8') as f:
                json.dump({'next_id': self.next_id}, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print('Error guardando datos:', e)

    def load_all(self):
        try:
            # cola
            cola_path = os.path.join(self.dir_data, 'cola.json')
            if os.path.exists(cola_path):
                with open(cola_path, 'r', encoding='utf-8') as f:
                    arr = json.load(f)
                self.cola.items = [Ticket.from_dict(d) for d in arr]

            # abiertos
            abiertos_path = os.path.join(self.dir_data, 'abiertos.json')
            if os.path.exists(abiertos_path):
                with open(abiertos_path, 'r', encoding='utf-8') as f:
                    arr = json.load(f)
                # cargar en la linkedlist (limpiar antes)
                self.abiertos.head = None
                for d in reversed(arr):  # reversed para mantener orden cronológico al insertar al inicio
                    self.abiertos.insert(Ticket.from_dict(d))

            # cerrados
            cerrados_path = os.path.join(self.dir_data, 'cerrados.json')
            if os.path.exists(cerrados_path):
                with open(cerrados_path, 'r', encoding='utf-8') as f:
                    arr = json.load(f)
                self.cerrados.head = None
                for d in reversed(arr):
                    self.cerrados.insert(Ticket.from_dict(d))

            # grafo
            grafo_path = os.path.join(self.dir_data, 'grafo.json')
            if os.path.exists(grafo_path):
                with open(grafo_path, 'r', encoding='utf-8') as f:
                    gd = json.load(f)
                self.grafo = Graph.from_dict(gd)

            # meta
            meta_path = os.path.join(self.dir_data, 'meta.json')
            if os.path.exists(meta_path):
                with open(meta_path, 'r', encoding='utf-8') as f:
                    md = json.load(f)
                self.next_id = md.get('next_id', self.next_id)

          
            self.arbol_prioridad = BST()
            cur = self.abiertos.head
            while cur:
                self.arbol_prioridad.insert(cur.ticket)
                cur = cur.next
            cur = self.cerrados.head
            while cur:
                self.arbol_prioridad.insert(cur.ticket)
                cur = cur.next

        except (OSError, json.JSONDecodeError) as e:
            print('Error cargando datos:', e)

   
    def reporte_resueltos_por_dia(self, fecha_iso_date: str) -> int:
        count = 0
        cur = self.cerrados.head
        while cur:
            hist = cur.ticket.historial.to_list()
            for h in hist:
                if isinstance(h, str) and 'Cerrado:' in h and fecha_iso_date in h:
                    count += 1
                    break
            cur = cur.next
        return count

    def undo(self) -> Optional[Tuple]:
        action = self.undo_stack.pop()
        if not action:
            return None
        typ = action[0]
        if typ == 'crear':
            tid = action[1]
            _ = self.abiertos.remove_by_id(tid)
            self.cola.items = [t for t in self.cola.items if t.id != tid]
            if tid in self.grafo.adj:
                del self.grafo.adj[tid]
            self.redo_stack.push(action)
            return action
        elif typ == 'atender':
            self.redo_stack.push(action)
            return action
        elif typ == 'cerrar':
            tid = action[1]
            t = self.cerrados.remove_by_id(tid)
            if t:
                t.estado = 'abierto'
                self.abiertos.insert(t)
            self.redo_stack.push(action)
            return action
        else:
            self.redo_stack.push(action)
            return action
        
def imprimir_ticket(t: Ticket):
    print(f"ID: {t.id} | Area: {t.area} | Prioridad: {t.prioridad} | Estado: {t.estado} | Fecha: {t.fecha}")
    print(f"Descripción: {t.descripcion}")

def main_menu():
    sistema = TicketSystem()
    sistema.load_all()

    while True:
        print('\n--- SISTEMA DE TICKETS - MENÚ ---')
        print('1) Crear ticket')
        print('2) Ver cola de espera')
        print('3) Atender ticket (dequeue)')
        print('4) Cerrar ticket (por ID)')
        print('5) Ver historial de un ticket')
        print('6) Agregar dependencia entre tickets')
        print('7) Consultar dependencias de un ticket')
        print('8) Buscar ticket por ID')
        print('9) Clasificar/mostrar tickets por prioridad (inorden)')
        print('10) Guardar datos')
        print('11) Cargar datos')
        print('12) Reporte: cuántos cerrados en una fecha')
        print('13) Undo (última acción simple)')
        print('14) Salir')
        opt = input('Elige una opción: ').strip()

        if opt == '1':
            desc = input('Descripción: ').strip()
            area = input('Área (redes/software/hardware): ').strip()
            try:
                pr = int(input('Prioridad (1 alta, 2 media, 3 baja): ').strip())
            except:
                pr = 3
            ticket = sistema.crear_ticket(desc, area, pr)
            print('Ticket creado:')
            imprimir_ticket(ticket)

        elif opt == '2':
            if sistema.cola.is_empty():
                print('La cola está vacía')
            else:
                print(f'Cola ({len(sistema.cola)} tickets):')
                for t in sistema.cola.items:
                    imprimir_ticket(t)

        elif opt == '3':
            t = sistema.atender_ticket()
            if not t:
                print('No hay tickets para atender')
            else:
                print('Se atendió el ticket:')
                imprimir_ticket(t)

        elif opt == '4':
            try:
                tid = int(input('ID del ticket a cerrar: ').strip())
            except:
                print('ID inválido')
                continue
            ok = sistema.cerrar_ticket(tid)
            if ok:
                print('Ticket cerrado correctamente')
            else:
                print('No se pudo cerrar el ticket (tal vez tiene dependencias o no existe)')

        elif opt == '5':
            try:
                tid = int(input('ID del ticket: ').strip())
            except:
                print('ID inválido')
                continue
            hist = sistema.ver_historial(tid)
            if not hist:
                print('No se encontró ticket o historial vacío')
            else:
                print('Historial (más antiguo → más reciente):')
                for h in hist:
                    print('-', h)

        elif opt == '6':
            try:
                tid = int(input('ID del ticket que depende: ').strip())
                dep = int(input('ID del ticket del que depende: ').strip())
            except:
                print('ID inválido')
                continue
            ok = sistema.agregar_dependencia(tid, dep)
            if ok:
                print('Dependencia agregada')
            else:
                print('No se pudo agregar dependencia (tickets inexistentes o ciclo)')

        elif opt == '7':
            try:
                tid = int(input('ID del ticket: ').strip())
            except:
                print('ID inválido')
                continue
            deps = sistema.grafo.get_dependencies(tid)
            if not deps:
                print('No tiene dependencias')
            else:
                print('Depende de IDs:', deps)

        elif opt == '8':
            try:
                tid = int(input('ID del ticket: ').strip())
            except:
                print('ID inválido')
                continue
            t = sistema.buscar_por_id(tid)
            if not t:
                print('No encontrado')
            else:
                imprimir_ticket(t)

        elif opt == '9':
            ordenados = sistema.arbol_prioridad.inorder()
            if not ordenados:
                print('No hay tickets en el árbol')
            else:
                print('Tickets ordenados por prioridad (inorden):')
                for t in ordenados:
                    imprimir_ticket(t)

        elif opt == '10':
            sistema.save_all()
            print('Datos guardados en folder', sistema.dir_data)

        elif opt == '11':
            sistema.load_all()
            print('Datos cargados')

        elif opt == '12':
            fecha = input('Fecha (YYYY-MM-DD): ').strip()
            c = sistema.reporte_resueltos_por_dia(fecha)
            print(f'Tickets cerrados en {fecha}: {c}')

        elif opt == '13':
            act = sistema.undo()
            if not act:
                print('Nada que deshacer')
            else:
                print('Deshecho:', act)

        elif opt == '14':
            sistema.save_all()
            print('Guardado automático. Saliendo...')
            break

        else:
            print('Opción no válida')

if __name__ == '__main__':
    main_menu()
