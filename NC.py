import itertools
import sys

class NumeralConverter:

    """Class for converting string Roman numerals into the Arabic number system."""

    def __init__(self, s):
        self.s = s
        self.numeral_values = {
            'I':1,
            'V':5,
            'X':10,
            'L':50,
            'C':100,
            'D':500,
            'M':1000
        }
        self.tens_list = ['X','C','M']
        self.next_highest_tens = {
            'I':'X',
            'X':'C',
            'C':'M'
        }
        self.fives_list = ['V','L','D']
        self.next_highest_fives = {
            'I':'V',
            'X':'L',
            'C':'D'
        }
        self.result = 0
        self.split_string = []


    def string_split(self):
        """
        Splits string into component parts.
        :return: List of str
        """
        if self.s == "":
            sys.exit("[ERROR] No input found. Please pass in a correct numeral string.")
        self.split_string = [''.join(g) for k, g in itertools.groupby(self.s)]
        return self.split_string


    def double_five_checker(self, element):
        """
        Checks for double five numerals.
        :param element:
        :return: None
        """
        s = ""
        for ele in element:
            s+=str(ele)
        if "VV" in s:
            sys.exit(f"[ERROR] Malformed element in your input {self.s} @ {element}, You cannot have more than one of "
                     f"a 5 type numeral, yours has at least 2 of the same numeral V in a row.")
        elif "LL" in s:
            sys.exit(f"[ERROR] Malformed element in your input {self.s} @ {element}, You cannot have more than one of "
                     f"a 5 type numeral, yours has at least 2 of the same numeral L in a row.")
        elif "DD" in s:
            sys.exit(f"[ERROR] Malformed element in your input {self.s} @ {element}, You cannot have more than one of "
                     f"a 5 type numeral, yours has at least 2 of the same numeral D in a row.")


    def add_substract_checker(self):
        """
        Checks lists for no add and subtract from same numeral.
        :return:  None
        """
        for i in range(len(self.split_string)-2):
            if len(self.split_string[i]) == 1:
                value = self.numeral_values[self.split_string[i]]
            else:
                value = self.numeral_values[self.split_string[i][0]]
            if len(self.split_string[i+1]) == 1:
                value_plus_1 = self.numeral_values[self.split_string[i+1]]
            else:
                value_plus_1 = self.numeral_values[self.split_string[i+1][0]]
            if value < value_plus_1:
                if self.split_string[i] == self.split_string[i+2]:
                    sys.exit(f"[ERROR] Malformed element in your input {self.s} @ {self.split_string[i]}"
                             f"{self.split_string[i+1]}{self.split_string[i+2]}, You cannot add and subtract from the "
                             f"same numeral, in this case {self.split_string[i+1]}")


    def valid_chars(self):
        """
        Checks for valid numerals used. Only IVXLCDM are valid
        :return: None
        """
        for char in self.s:
            if char not in ['I','V','X','L','C','D','M']:
                sys.exit(f"[ERROR] Malformed element in your input {self.s} @ {char}, {char} is not a roman numeral.")


    def roman_numeral_to_arabic(self):
        """
        Converts list of Roman numerals into Arabic number system
        :return: int
        """
        self.result = 0
        reversed_list = []
        for item in reversed(self.string_split()):
            reversed_list.append(item)
        self.valid_chars()
        self.add_substract_checker()
        i = 0
        for element in reversed_list:
            if len(element) > 1:
                self.double_five_checker(element)
            if len(element) == 1:
                if i == 0:
                    self.result += self.numeral_values[element]
                else:
                    if self.numeral_values[reversed_list[i-1]] > self.numeral_values[element]:
                        if self.next_highest_tens[element] == reversed_list[i-1] or self.next_highest_fives[element] == reversed_list[i-1]:
                            try:
                                if element == reversed_list[i + 1]:
                                    sys.exit(f"[ERROR] Malformed element in your input {element}{reversed_list[i+1]} "
                                             f"cannot be subtracted in unison.")
                                else:
                                    self.result -= self.numeral_values[element]
                            except IndexError:
                                self.result -= self.numeral_values[element]
                        else:
                            sys.exit(f"[ERROR] Malformed element in your input {element} cannot be subtracted from"
                                     f" {reversed_list[i-1]}.")
                    elif self.numeral_values[reversed_list[i-1]] <= self.numeral_values[element]:
                        self.result += self.numeral_values[element]
                i+=1
            elif len(element) > 1 and len(element) < 4:
                j=0
                for ele_part in element:
                    if i == 0:
                        self.result += self.numeral_values[ele_part]
                    else:
                        if self.numeral_values[reversed_list[i-1]] > self.numeral_values[ele_part]:
                            if len(str(self.numeral_values[reversed_list[i-1]])) == len(str(self.numeral_values[ele_part])):
                                if self.next_highest_tens[ele_part] == reversed_list[i-1] or self.next_highest_fives[ele_part] == reversed_list[i-1]:
                                    if ele_part == element[j+1]:
                                        sys.exit(f"[ERROR] Malformed element in your input {ele_part}{element[j+1]} cannot be subtracted in unison.")
                                    else:
                                        self.result -= self.numeral_values[ele_part]
                                else:
                                    sys.exit(
                                        f"[ERROR] Malformed element in your input {ele_part} cannot be subtracted from"
                                        f" {reversed_list[i - 1]}.")
                            else:
                                sys.exit(
                                    f"[ERROR] Malformed element in your input {self.s} @ {ele_part}, "
                                    f"you can only subtract from the next highest five or ten.")
                        elif self.numeral_values[reversed_list[i-1]] <= self.numeral_values[ele_part]:
                            self.result += self.numeral_values[ele_part]
                i+=1
                j+=1
            elif len(element) > 3:
                sys.exit(f"[ERROR] Malformed element in your input {self.s} @ {element}, You cannot have more than 3 of "
                         f"the same numeral, yours has {len(element)} of the same numerals in a row.")
        return self.result

nc = NumeralConverter(s="")
nc.roman_numeral_to_arabic()
print(nc.result)