import z3.z3 as z3
from z3.z3 import Solver, Int, And, Distinct, Or

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
        self.matrix = [
            [z3.Int("x_%s_%s" % (i + 1, j + 1)) for i in range(self.width)]
            for j in range(self.height)
        ]

        # 0 = empty cell
        for i in range(self.width):
            for j in range(self.height):
                self.solver.add(Or(0 == self.matrix[i][j]))

    def placeComponents(self):
        # Place regular components in the matrix (chip platine)
        placements = []
        for id, (reg_width, reg_height) in enumerate(self.regularComponents):
            for i in range(self.height - reg_height + 1):
                for j in range(self.width - reg_width + 1):
                    components_cells = [
                        self.matrix[i + x][j + y] == id + 1
                        for x in range(reg_height)
                        for y in range(reg_width)
                    ]

                    # 90 degree rotation
                    turned_components_cells = [
                        self.matrix[j + y][i + x] == id + 1
                        for x in range(reg_width)
                        for y in range(reg_height)
                    ]
                    placements.append(Or(And(components_cells), And(turned_components_cells)))

        # Only one of these possible placements must be fulfilled 
        self.solver.add(Or(placements))

        # Ensure that the regular components are not placed on top of each other
        unique_placement = [
            Distinct(
                [
                    self.matrix[j][i]
                    for i in range(self.width)
                    for j in range(self.height)
                ]
            )
        ]
        self.solver.add(And(unique_placement))

    def solve(self):
        if self.solver.check() == z3.sat:
            solution = []
            model = self.solver.model()
            for i in range(self.width):
                for j in range(self.height):
                    solution.append(model.evaluate(self.matrix[i][j]))
            print(solution)
        else:
            print("No solution found")


chipdesign = ChipDesign(50, 50, 2, 2, 4)
chipdesign.generateMatrix()
chipdesign.placeComponents()
chipdesign.solve()
