

__all__ = ['MetadataDescriptor']

class MetadataDescriptor:

    _tapName = ''
    _label = ''
    _visible = True
    _type = ''
    _index = 0
    _maxDecimalDigits = 4

    def __init__(self, label, columnType, maxDecimalDigits):
        self._tapName = label
        self._label = label
        self._type = columnType
        if maxDecimalDigits:
            self._maxDecimalDigits = maxDecimalDigits

    def getLabel(self):
        return self._tapName
    
    def getColumnType(self):
        return self._type

    




