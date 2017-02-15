class Mountain:
    lines = None
    points = None
    regions = None

    fill_points = []

    def __init__(self):
        self.lines = []
        self.points = []
        self.regions = []
        self.fill_points = []

    def sort_fill_points(self):
        self.fill_points = sorted(self.fill_points, key=lambda p: p.y)