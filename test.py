import z3
from z3 import Solver, Int, And, Distinct

# definining the class:
x = Int("x")
y = Int("y")


class ChipDesign:
    def __init__(self, width, height, pcHeight, pcWidth, powDistance):
        self.width = width
        self.height = height
        self.powHeight = pcHeight
        self.powWidth = pcWidth
        self.powDistance = powDistance
        self.regularComponents = [
            (4, 5),
            (4, 6),
            (5, 20),
            (6, 9),
            (6, 10),
            (6, 11),
            (7, 8),
            (7, 12),
            (10, 10),
            (10, 20),
        ]
        self.solver = Solver()

    def generateMatrix(self):
        # 0 = empty, 1 = regular component, 2 = power component
        self.matrix = [
            [z3.Int("x_%s_%s" % (i + 1, j + 1)) for i in range(self.width)]
            for j in range(self.height)
        ]

    def placeComponents(self):
        # Place regular components in the matrix (chip platine)
        placements = []
        for id, (width, height) in enumerate(self.regularComponents):
            for i in range(self.width - width + 1):
                for j in range(self.height - height + 1):
                    components_cells = [
                        self.matrix[i + x][j + y] == id + 1
                        for x in range(width)
                        for y in range(height)
                    ]
                placements.append(And(*components_cells))

        # Place power components in the matrix (chip platine)Charlie Puth
        # Ensure that the regular components are not placed on top of each other
        unique_placement = [
            Distinct(
                [
                    self.matrix[i][j]
                    for i in range(self.width)
                    for j in range(self.height)
                ]
            )
        ]

        constraints = placements + unique_placement
        self.solver.add(constraints)

    def solve(self):
        if self.solver.check() == z3.sat:
            model = self.solver.model()
            for i in range(self.width):
                for j in range(self.height):
                    print(model[self.matrix[i][j]], end=" ")
        else:
            print("No solution found")


chipdesign = ChipDesign(40, 50, 2, 2, 4)
chipdesign.generateMatrix()
chipdesign.placeComponents()
chipdesign.solve()
