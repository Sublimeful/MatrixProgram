from fractions import Fraction
import string



class Matrix:
    def __init__(self, arr2D):
        self.arr2D = arr2D

    def __str__(self):
        lines = []
        padding = -1
        for row in self:
            for cell in row:
                padding = max(padding, len(str(cell)) + 1 if cell >= 0 else len(str(cell)))
        for idx, row in enumerate(self):
            line = ""
            for cell in row:
                line += f"{' ' if cell >= 0 else ''}{cell}".ljust(padding) + " "
            lines.append("[ " + line + " ]")
        return "\n".join(lines)

    def __mul__(self, o):
        if isinstance(o, self.__class__):
            if len(self[0]) != len(o):
                raise Exception("Columns in matrix A not equal to rows in matrix B")

            ROWS = len(self)
            COLS = len(o[0])

            res = Matrix([[0 for _ in range(COLS)] for _ in range(ROWS)])

            for r in range(ROWS):
                for c in range(COLS):
                    for i in range(len(self[r])):
                        res[r][c] += self[r][i] * o[i][c]

            return res
        elif isinstance(o, Fraction):
            ROWS = len(self)
            COLS = len(self[0])
            res = Matrix([[0 for _ in range(COLS)] for _ in range(ROWS)])

            for r in range(ROWS):
                for c in range(COLS):
                    res[r][c] = self[r][c] * o

            return res
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(o))

    def __add__(self, o):
        if not isinstance(o, self.__class__):
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(o))
        if len(self) != len(o) or len(self[0]) != len(o[0]):
            raise Exception("Matrix dimensions are not the same!")

        ROWS = len(self)
        COLS = len(self[0])
        res = Matrix([[0 for _ in range(COLS)] for _ in range(ROWS)])

        for r in range(ROWS):
            for c in range(COLS):
                res[r][c] = self[r][c] + o[r][c]

        return res

    def __sub__(self, o):
        if not isinstance(o, self.__class__):
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(o))
        if len(self) != len(o) or len(self[0]) != len(o[0]):
            raise Exception("Matrix dimensions are not the same!")

        ROWS = len(self)
        COLS = len(self[0])
        res = Matrix([[0 for _ in range(COLS)] for _ in range(ROWS)])

        for r in range(ROWS):
            for c in range(COLS):
                res[r][c] = self[r][c] - o[r][c]

        return res

    def __copy__(self):
        return Matrix([row[:] for row in self])

    def __setitem__(self, idx, row):
        self.arr2D[idx] = row

    def __getitem__(self, idx):
        return self.arr2D[idx]

    def __len__(self):
        return len(self.arr2D)



def prompt_row(prompt):
    res = None
    while res is None:
        try:
            res = list(map(Fraction, [part.strip() for part in input(prompt).split(" ") if part != ""]))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Type numbers please!")
    return res

def prompt_fraction(prompt):
    res = None
    while res is None:
        try:
            res = Fraction(input(prompt))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Type a number please!")
    return res

def prompt_integer(prompt):
    res = None
    while res is None:
        try:
            res = int(input(prompt))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Type an integer please!")
    return res

def prompt_boolean(prompt):
    res = None
    while res is None:
        try:
            res = input(prompt).lower()
            if res == 'y': res = True
            elif res == 'n': res = False
            else: res = None
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Please enter either Y or N!")
    return res

def prompt_string(prompt):
    res = None
    while res is None:
        try:
            res = input(prompt)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Please provide a string!")
    return res

def mat_modify(matrix):
    # Create copy of matrix to prevent side effects
    matrix = matrix.__copy__()
    operation = 0
    while(operation != -1):
        print("Current matrix")
        print(matrix)
        print("What operation would you like to perform? Type -1 to exit")
        print("1. Replacement")
        print("2. Scaling")
        print("3. Interchanging")
        operation = prompt_integer(": ")
        if operation not in (-1, 1, 2, 3):
            print("That is not a valid operation!")
            continue
        if operation == 1:
            row1 = prompt_integer("Row 1 index: ") - 1
            if row1 < 0 or row1 >= len(matrix):
                print("Index out of range!")
                continue
            row2 = prompt_integer("Row 2 index: ") - 1
            if row2 < 0 or row2 >= len(matrix):
                print("Index out of range!")
                continue
            if row1 == row2:
                print("Indices can't be the same!")
                continue
            coeff = prompt_fraction("Row 2 scale: ")
            for c in range(len(matrix[row1])):
                matrix[row1][c] += coeff * matrix[row2][c]
            print("Done!")
        elif operation == 2:
            row = prompt_integer("Row index: ") - 1
            if row < 0 or row >= len(matrix):
                print("Index out of range!")
                continue
            coeff = prompt_fraction("Scale: ")
            if coeff == 0:
                print("You cannot scale by 0!")
                continue
            for c in range(len(matrix[row])):
                matrix[row][c] *= coeff
            print("Done!")
        elif operation == 3:
            row1 = prompt_integer("Row 1 index: ") - 1
            if row1 < 0 or row1 >= len(matrix):
                print("Index out of range!")
                continue
            row2 = prompt_integer("Row 2 index: ") - 1
            if row2 < 0 or row2 >= len(matrix):
                print("Index out of range!")
                continue
            if row1 == row2:
                print("Indices are the same, so nothing happened");
                continue
            matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
            print("Done!")
    return matrix

def mat_create(numRows, numCols):
    res = []
    print("Write each row as space separated list, EX: 1 2 3")
    for r in range(numRows):
        row = None
        while row is None:
            row = prompt_row(f"Row #{r + 1}: ")
            if len(row) != numCols:
                print("Number of cells is not equal to the number of columns specified!")
                row = None
                continue
            res.append(row)
    return Matrix(res)

def calculate_2_mats(mat1, mat2):
    # Create copy of matrices to prevent side effects
    mat1 = mat1.__copy__()
    mat2 = mat2.__copy__()
    print("Current matrices")
    print("Matrix 1")
    print(mat1)
    print("Matrix 2")
    print(mat2)
    print("What operation would you like to perform?")
    print("1. Matrix Multiplication")
    print("2. Matrix Addition")
    print("3. Matrix Subtraction")
    operation = prompt_integer(": ")
    if operation == 1:
        try:
            res_mat = mat1 * mat2
        except Exception as err:
            print(err)
            return None
        print("Result of Matrix 1 * Matrix 2")
        print(res_mat)
        return res_mat
    elif operation == 2:
        try:
            res_mat = mat1 + mat2
        except Exception as err:
            print(err)
            return None
        print("Result of Matrix 1 + Matrix 2")
        print(res_mat)
        return res_mat
    elif operation == 3:
        try:
            res_mat = mat1 - mat2
        except Exception as err:
            print(err)
            return None
        print("Result of Matrix 1 - Matrix 2")
        print(res_mat)
        return res_mat
    else:
        print("This is not a valid operation!")
        return None

def calculate_1_mat(mat):
    # Create copy of matrix to prevent side effects
    mat = mat.__copy__()
    print("Current Matrix")
    print(mat)
    print("What operation would you like to perform?")
    print("1. Scaling")
    operation = prompt_integer(": ")
    if operation == 1:
        coeff = prompt_fraction("Scale: ")
        try:
            res_mat = mat * coeff
        except Exception as err:
            print(err)
            return None
        print(f"Result of Matrix * {coeff}")
        print(res_mat)
        return res_mat
    else:
        print("This is not a valid operation!")
        return None

def add_matrix(matrices, matrix):
    provide_name_bool = prompt_boolean("Would you like to give this matrix a name(Y/N)? ")
    name = None
    if provide_name_bool:
        while name is None:
            name = prompt_string("Name of matrix: ")
            filtered_name = "".join(filter(lambda c: c in string.printable, name))
            if filtered_name != name:
                name = filtered_name
                print("Name was filtered because it contains some unprintable characters")
                print(f"New name: {name}")
                keepname_boolean = prompt_boolean("Would you like to keep this name(Y/N)? ")
                if not keepname_boolean:
                    name = None
                    continue
            if name in matrices:  # Name already in matrices
                overwrite_boolean = prompt_boolean("There is already a matrix named that, would you like to overwrite it(Y/N)? ")
                if not overwrite_boolean:
                    name = None
                    continue
            matrices[name] = matrix
    else:
        name = len(matrices) + 1
        while str(name) in matrices:
            name += 1
        matrices[str(name)] = matrix
    print(f"Done! Matrix added as \"{name}\"!")

def main_loop(matrices):
    print("What do you want to do?")
    print("1. Add matrix")
    print("2. Perform operations on matrix")
    print("3. Delete matrix")
    print("4. Print matrix")
    print("5. List all matrices")
    print("6. Perform calculation of 1 matrix")
    print("7. Perform calculation of 2 matrices")
    print("#. Type any other integer to exit program")
    option = prompt_integer(": ")
    if option == 1:
        numRows = prompt_integer("Number of rows: ")
        if numRows <= 0:
            print("Number of rows cannot be <=0!")
            return
        numCols = prompt_integer("Number of columns: ")
        if numCols <= 0:
            print("Number of columns cannot be <=0!")
            return
        matrix = mat_create(numRows, numCols)
        if matrix is None: return
        add_matrix(matrices, matrix)
    elif option == 2:
        matrixName = prompt_string("Which matrix do you want to modify? Type the name: ")
        if matrixName not in matrices:
            print("There is no matrix with that name!")
            return
        matrix = matrices[matrixName]
        modified_matrix = mat_modify(matrix)
        answer = prompt_boolean("Would you like to save this modified matrix(Y/N)? ")
        if answer: add_matrix(matrices, modified_matrix)
    elif option == 3:
        matrixName = prompt_string("Which matrix do you want to delete? Type the name: ")
        if matrixName not in matrices:
            print("There is no matrix with that name!")
            return
        del matrices[matrixName]
        print(f"Done! Matrix with name \"{matrixName}\" deleted!")
    elif option == 4:
        matrixName = prompt_string("Which matrix do you want to print? Type the name: ")
        if matrixName not in matrices:
            print("There is no matrix with that name!")
            return
        matrix = matrices[matrixName]
        print(matrix)
    elif option == 5:
        for name, matrix in matrices.items():
            print(f"Matrix with name \"{name}\"")
            print(matrix)
        print(f"There are {len(matrices)} matrices")
    elif option == 6:
        matrixName = prompt_string("Matrix name: ")
        if matrixName not in matrices:
            print("There is no matrix with that name!")
            return
        mat = matrices[matrixName]
        res_mat = calculate_1_mat(mat)
        if res_mat is None:
            print("No result matrix was generated")
            return;
        answer = prompt_boolean("Would you like to save this result matrix(Y/N)? ")
        if answer: add_matrix(matrices, res_mat)
    elif option == 7:
        m1Name = prompt_string("Matrix 1 name: ")
        if m1Name not in matrices:
            print(f"No such name \"{m1Name}\" exists!")
            return
        m2Name = prompt_string("Matrix 2 name: ")
        if m2Name not in matrices:
            print(f"No such name \"{m2Name}\" exists!")
            return
        if m1Name == m2Name:
            print("Matrices can't be the same!")
            return
        mat1 = matrices[m1Name]
        mat2 = matrices[m2Name]
        res_mat = calculate_2_mats(mat1, mat2)
        if res_mat is None:
            print("No result matrix was generated")
            return;
        answer = prompt_boolean("Would you like to save this result matrix(Y/N)? ")
        if answer: add_matrix(matrices, res_mat)
    else:
        print("Bye!")
        exit(0)



if __name__ == "__main__":
    matrices = {}
    while True:
        try:
            main_loop(matrices)
        except KeyboardInterrupt:
            continue
