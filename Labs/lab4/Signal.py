class SignalValue:
    def __init__(self, i):
        self.marked = False;
        self.value = i;

    def mark(self):
        self.marked = True;
    
    def unmark(self):
        self.marked = False;

    def is_marked(self):
        return self.marked;

    def __str__(self):
        return str(self.value);
