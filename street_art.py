"""
    Purpose: This program renders an ASCII art representation of city street.
        The street consists of buildings, parks, and empty lots specified by
        the user in a single-line input. Each element is drawn to specified
        dimensions and character pattern with recursive functions. The output
        includes a border and proper alignment of all street elements.
"""


class Building:
    """Represents a rectangular building made of a single character.

    The building can render itself at a given height using the brick character.
    Methods include `at_height` to get the line at a certain height.
    """

    def __init__(self, width, height, brick):
        """Initialize a Building object.

        Parameters:
            width (int): Width of the building.
            height (int): Height of the building.
            brick (str): Character used to draw the building.
        """
        self._width = width
        self._height = height
        self._brick = brick

    def width(self):
        return self._width
    
    def brick(self):
        return self._brick
    
    def height(self):
        return self._height
    
    def single_line(self, width, filling):
        """Recursively generate a line of repeated characters.

        Parameters:
            width (int): Number of characters to generate.
            filling (str): Character to use for the line.

        Returns:
            str: A string consisting of 'filling' repeated 'width' times.
        """
        if width == 0:  # base case: no more characters to add
            return ""
        width -= 1
        # prepend character and recurse
        return filling + self.single_line(width, filling)
        
    def at_height(self, height):
        """Return the building's line at the specified height.

        Parameters:
            height (int): The line number from the top (1-indexed).

        Returns:
            str: String representing the building at this height.
        """
        if self.height() < height:  # above the building, return empty space
            return self.single_line(self.width(), " ")
        # within building, return brick line
        return self.single_line(self.width(), self.brick())

class Park:
    """Represents a park with a single centered tree.

    The tree has foliage drawn with the specified character and a trunk made
    of '|'. The park always has a height of 5 lines. The `at_height` method
    returns the line at a specific height.
    """

    def __init__(self, width, fol):
        """Initialize a Park object.

        Parameters:
            width (int): Width of the park (must be odd and >= 5).
            fol (str): Character used for tree foliage.
        """
        self._width = width
        self._fol = fol
        self._height = 5  # park always has fixed height of 5

    def width(self):
        return self._width

    def fol(self):
        return self._fol
    
    def height(self):
        return self._height
    
    def fill_line(self, width, filling):
        """Recursively fill a line with a given character.

        Parameters:
            width (int): Number of characters to generate.
            filling (str): Character to use for the line.

        Returns:
            str: A string of 'filling' repeated 'width' times.
        """
        if width == 0:
            return ''  # Base case: no more characters left
        width -= 1
        # recursively add the filling
        return filling + self.fill_line(width, filling)

    
    def tree_line(self, width, middle, filling):
        """Return a single line of a tree centered in the park.

        Parameters:
            width (int): Total width of the park.
            middle (int): Width of the tree or foliage portion.
            filling (str): Character to fill the tree/trunk/foliage.

        Returns:
            str: A line string with tree/trunk/foliage centered.
        """
        space_width = (width - middle) // 2  # calculate padding on both sides
        space = self.fill_line(space_width, ' ')  # generate padding
        tree_part = self.fill_line(middle, filling)  # generate trunk/foliage
        return space + tree_part + space  # combine padding and tree part
    
    def at_height(self, height):
        """Return the park's line for a given height (tree/trunk/foliage).

        Parameters:
            height (int): Line number from the top (1-indexed).

        Returns:
            str: String representing the park at this height.
        """
        if 5 < height:  # above the park, return empty spaces
            return self.fill_line(self.width(), ' ')
        if 2 >= height:  # trunk at bottom
            return self.tree_line(self.width(), 1, '|')
        if height == 3:  # widest foliage row
            return self.tree_line(self.width(), 5, self.fol())
        if height == 4:  # narrower foliage row
            return self.tree_line(self.width(), 3, self.fol())
        return self.tree_line(self.width(), 1, self.fol())  # top leaf row


class EmptyLot:
    """Represents an empty lot that may contain repeating trash patterns.

    Underscores in the trash string are treated as spaces. The trash pattern
    repeats or is truncated to fit the width of the lot. The lot has a height
    of 1 line. Use `at_height` to get the line at a given height.
    """

    def __init__(self, width, trash):
        """Initialize an EmptyLot object.

        Parameters:
            width (int): Width of the lot.
            trash (str): Pattern of trash in the lot (underscores are spaces).
        """
        self._width = width
        self._trash = trash
        self._height = 1  # empty lots always have height of 1

    def width(self):
        return self._width
    
    def height(self):
        return self._height
    
    def trash(self):
        return self._trash
    
    def empty_line(self, width):
        """Return a blank line of given width using recursion.

        Parameters:
            width (int): Width of the line.

        Returns:
            str: A string of spaces of length 'width'.
        """
        if width == 0:
            return ''  # Base case: no more characters left
        width -= 1
        # recursively add the blank space
        return ' ' + self.empty_line(width)
    
    def change_spaces(self, trash):
        """Replace underscores with spaces recursively in a trash string.

        Parameters:
            trash (str): Original trash string.

        Returns:
            str: Trash string with underscores converted to spaces.
        """
        if len(trash) == 0:  # base case: empty string
            return ''
        if trash[0] == '_':  # underscore -> space
            # add space then recurse the rest of string
            return ' ' + self.change_spaces(trash[1:])
        # keep original character then recurse the rest of string
        return trash[0] + self.change_spaces(trash[1:])
    
    def trash_to_width(self, trash):
        """Adjust trash string to exactly match lot width by repeating
        or trimming.

        Parameters:
            trash (str): Input trash string.

        Returns:
            str: Trash string repeated or trimmed to exactly match lot width.
        """
        if len(trash) >= self.width():  # trim if longer than width
            return trash[0:self.width()]
        times = self.width() // len(trash)  # how many full repeats
        rem = self.width() % len(trash)    # remainder characters
        return trash * times + trash[0:rem]  # combine repeats and remainder
    
    def at_height(self, height):
        """Return the empty lot line for a given height.

        Parameters:
            height (int): Line number from the top (1-indexed).

        Returns:
            str: Line string representing the lot
            (either blank or trash pattern).
        """
        if height > 1:  # above the lot, return blank
            return self.empty_line(self.width())
        # return the trash pattern adjusted to width with underscores converted
        return self.trash_to_width(self.change_spaces(self.trash()))


def create_street(parts, parts_list):
    """Recursively parse the street specification into objects.

    Parameters:
        parts (list): List of street part specifications as strings.
        parts_list (list): Accumulator list of parsed objects.

    Returns:
        list: List of Building, Park, or EmptyLot objects
        representing the street.
    """
    if len(parts) == 0:  # base case: no more parts
        return parts_list
    street_part = parts[0]  # represents characters of a street part
    
    if street_part[0] == 'b':  # parse building 
        parameters = street_part[2:].split(',')  # get parameter parts in list
        # add building object to parts_list
        parts_list.append(
            Building(int(parameters[0]), int(parameters[1]), parameters[2]))


    if street_part[0] == 'p':  # parse park
        parameters = street_part[2:].split(',')  # get parameter parts in list
        # add park object to parts_list
        parts_list.append(Park(int(parameters[0]), parameters[1]))
    
    if street_part[0] == 'e':  # parse empty lot
        parameters = street_part[2:].split(',')  # get parameter parts in list
        # add empty lot object to parts_list
        parts_list.append(EmptyLot(int(parameters[0]), parameters[1]))

    return create_street(parts[1:], parts_list)  # recurse for remaining parts


def max_height(street_parts, max_h):
    """Recursively find the tallest element in the street.

    Parameters:
        street_parts (list): List of street elements.
        max_h (int): Current maximum height.

    Returns:
        int: Maximum height among all street elements.
    """
    if len(street_parts) == 0:  # base case
        return max_h
    if street_parts[0].height() > max_h:  # update max height if needed
        max_h = street_parts[0].height()
    return max_height(street_parts[1:], max_h)  # recurse for remaining parts


def street_line(street_parts, height):
    """Return a single line of the street at the specified height.

    Parameters:
        street_parts (list): List of street elements.
        height (int): Line number from the top (1-indexed).

    Returns:
        str: Combined string of all street elements at this height.
    """
    if len(street_parts) == 0:  # base case
        return ""
    # add line of a part at certain height then recurse for remaining parts
    return (street_parts[0].at_height(height) +
        street_line(street_parts[1:], height))



def print_street(street_parts, height):
    """Recursively print the street line by line from top to bottom.

    Parameters:
        street_parts (list): List of street elements.
        height (int): Maximum height to print.
    """
    if height == 0:  # base case
        return
    print('|' + street_line(street_parts, height) + '|')  # print current line
    print_street(street_parts, height-1)  # recurse for next line


def find_width(street_parts):
    """Recursively compute total width of the street.

    Parameters:
        street_parts (list): List of street elements.

    Returns:
        int: Total width of the street.
    """
    if len(street_parts) == 0:  # base case
        return 0
    # add the width of a part then recurse for remaining parts
    return street_parts[0].width() + find_width(street_parts[1:])


def border_line(width, fill):
    """Recursively generate a line for the street border.

    Parameters:
        width (int): Number of characters.
        fill (str): Character to fill.

    Returns:
        str: Line string filled with the given character.
    """
    if width == 0:  # base case: no more characters left
        return ''
    width -= 1
    # # recursively add the filling
    return fill + border_line(width, fill)


def main():
    """Main function to get input, build street, and print ASCII street."""
    parts = input("Street: ").split()              # split input into parts
    street_parts = create_street(parts, [])       # create objects from input
    max_h = max_height(street_parts, 0)           # find maximum height
    width = find_width(street_parts)              # compute street width

    # print top border
    print('+' + border_line(width, '-') + '+')
    # print top empty padding
    print('|' + border_line(width, ' ') + '|')
    # print street content
    print_street(street_parts, max_h)
    # print bottom border
    print('+' + border_line(width, '-') + '+')

main()
