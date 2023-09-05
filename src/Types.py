from enum import Enum

class Type(Enum):
    DATE = "DATE"
    NUMBER = "NUMBER"
    OBSERVATION = "OBSERVATION"
    MEASURER = "MEASURER"
    MEASURED = "MEASURED"
    QUESTIONS = "QUESTIONS"
    HEADER = "HEADER"
    CONTENT = "CONTENT"
    MEASURE = "MEASURE"
    SUBHEADER = "SUBHEADER"

class Style(Enum):
    ID = "id",
    BG_COLOR = "bg-color",
    TEXT_COLOR = "text-color",
    ROW_SPAN = "row-span",
    COL_SPAN = "col-span",
    COL_SPAN_FULL = "full",
    BREAK_LINE = "break-line",
    MAJOR = "major",
    MAJOR_SPAN = "major-span",
    X_ALIGNMENT = "x-alignment",
    Y_ALIGNMENT = "y-alignment",
    BORDER = "border",
    BORDER_COLOR = "border-color",
    LABEL = "label",
    INTERLACED_BG = "interlaced-bg",
    INTERLACED_BG_COLOR = "interlaced-bg-color",

