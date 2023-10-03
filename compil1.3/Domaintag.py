from enum import Enum

class DomainTag(Enum):
    Keyword = 'Keyword'
    Hex_constant = 'Hex_constant'
    Decimal_constant = 'Decimal_constant'
    Identifier = 'Identifier'
    Error = 'Error'