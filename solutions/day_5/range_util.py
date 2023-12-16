class Range:
    def __init__(self, source_start, source_end, destination_start, destination_end):
        self.source_start = source_start
        self.source_end = source_end
        self.destination_start = destination_start
        self.destination_end = destination_end

    def map_from_source(self, value):
        if self.contains_value(value):
            return self.destination_start + (value - self.source_start)
        else:
            raise RuntimeError("Value is not in range of source")

    def map_from_source_range(self, range):

        target_start = target_end = None
        value_increment = self.destination_start - self.source_start
        if self.contains_value(range.source_start):
            target_start = self.map_from_source(range.source_start)
        if self.contains_value(range.source_end):
            target_end = self.map_from_source(range.source_end)

        if target_start is None and target_end is None:
            return None
        elif target_start is None:
            target_start = self.destination_start
            return Range(target_start - value_increment, range.source_end, target_start, target_end)
        elif target_end is None:
            target_end = self.destination_end
            return Range(range.source_start, target_end - value_increment, target_start, target_end)
        else:
            return Range(range.source_start, range.source_end, target_start, target_end)

    def contains_value(self, value):
        return self.source_start <= value <= self.source_end

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __le__(self, other):
        return self.__cmp__(other) == -1 or self.__cmp__(other) == 0

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __ge__(self, other):
        return self.__cmp__(other) == 1 or self.__cmp__(other) == 0

    def __ne__(self, other):
        return not (self == other)

    def __cmp__(self, other):
        if isinstance(other, int):
            if self == other:
                return 0
            elif self.source_start < other:
                return -1
            else:
                return 1
        elif isinstance(other, Range):
            if self.source_start > other.source_start:
                return 1
            if self.source_start < other.source_start:
                return -1
            return 0
        raise RuntimeError(f"Unsupported comparison between Range and {type(other)}")

    def __eq__(self, other):
        if isinstance(other, int):
            if self.source_start <= other <= self.source_end:
                return True
        elif isinstance(other, Range):
            return self.source_start == other.source_start and self.source_end == other.source_end
        else:
            return False

    def __str__(self):
        return (f"Range(source_start={self.source_start}, source_end={self.source_end}, "
                f"destination_start={self.destination_start}, destination_end={self.destination_end})>")

    def __repr__(self):
        return str(self)