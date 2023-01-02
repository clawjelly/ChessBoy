
class Event:
    def __init__(self):
        self._eventHandlers = []

    def __iadd__(self, eventHandler):
        self._eventHandlers.append(eventHandler)
        return self

    def __isub__(self, eventHandler):
        self._eventHandlers.remove(eventHandler)
        return self

    def __call__(self, *args, **keywargs):
        for eventHandler in self._eventHandlers:
            eventHandler(*args, **keywargs)

class EventManager:
    """ My Chess Event Manager.
    
    Subscribe with

    eventManager.onMove += myMethod

    Unsubscribe with

    eventManager.onMove -= myMethod

    Call event with

    eventManager.onMove(myMove)

    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, name = "Chess Event Manager"):
        self.name = name
        self.newGame = Event()
        self.onPieceLifted = Event()
        self.onMoveTry = Event() # trying a move
        self.onMove = Event()   # move is successful
        self.newPieceOnBoard = Event() # a new piece was created

eventManager = EventManager()

if __name__ == "__main__":
    pass
