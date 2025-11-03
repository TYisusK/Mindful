# services/offline_queue.py
import json

QUEUE_KEY = "offline_notes_queue"

def _get_storage(page):
    # client_storage está en el cliente. page.session NO sirve offline.
    return page.client_storage

def queue_note(page, note_dict):
    """Guarda una nota en una cola local para sincronizar más tarde."""
    storage = _get_storage(page)
    raw = storage.get(QUEUE_KEY) or "[]"
    lst = json.loads(raw)
    lst.append(note_dict)
    storage.set(QUEUE_KEY, json.dumps(lst))

def pop_all(page):
    storage = _get_storage(page)
    raw = storage.get(QUEUE_KEY) or "[]"
    storage.set(QUEUE_KEY, "[]")
    return json.loads(raw)

def peek_all(page):
    storage = _get_storage(page)
    raw = storage.get(QUEUE_KEY) or "[]"
    return json.loads(raw)

def has_pending(page):
    return len(peek_all(page)) > 0
