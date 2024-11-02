from dataclasses import dataclass
from typing import Self


class BabaError(Exception):
    """Base class for convenient catching."""


class MiscError(Exception):
    """General information broadcasting in the form of an error."""


class SplittingException(BabaError):
    """Couldn't split `text_a,b,c` ... somehow.

    args: cause
    """


class InvalidFlagError(MiscError):
    """A flag failed to parse.

    args: cause"""

class MacroSyntaxError(MiscError):
    """A macro tree failed to parse.
    
    args: index, source, reason"""
    def __init__(self, index: int, source: str, reason: str) -> None:
        self.index = index
        self.source = source
        self.reason = reason

    def __str__(self):
        source_slice_start = max(self.source[:self.index].rfind("\n"), self.index - 10, 0)
        newline_index = self.source[self.index:].find("\n")
        if newline_index != -1:
            newline_index += self.index
        source_slice_end = min((1 << 30) if newline_index < 0 else newline_index, self.index + 10, len(self.source))
        source_slice = self.source[source_slice_start : source_slice_end]
        return "\n".join((
            f"Syntax error at index {self.index}",
            self.reason,
            source_slice,
            " " * (self.index - source_slice_start) + "^"
        ))

class MacroRuntimeError(MiscError):
    """A macro tree failed to parse.
    
    args: name, tree, reason, [cause]"""
    def __init__(self, name: str, tree, reason: str, cause: Self | None = None) -> None:
        self.name = name
        self.tree = tree
        self.reason = reason
        self.cause = cause

    def __str__(self):
        if hasattr(self, "_builtin"):
            return f"`<builtin error>`: {self.reason}"
        str_tree = str(self.tree)
        if len(str_tree) > 30:
            str_tree = str_tree[:15] + "..." + str_tree[-15:]
        return f"`{self.name}` at `{self.tree}`: {self.reason}"

class BadTileProperty(BabaError):
    """Tried to make a tile a property but it's tooo big.

    args: name, size
    """


class TileNotFound(BabaError):
    """Unknown tile.

    args: tile
    """


class EmptyTile(BabaError):
    """Blank tiles not allowed."""


class EmptyVariant(BabaError):
    """Empty variants not allowed.

    args: tile
    """


# === Variants ===


class VariantError(BabaError):
    """Base class for variants.

    args: tile, variant
    """


class BadMetaVariant(VariantError):
    """Too deep.

    extra args: depth
    """


@dataclass
class FailedBuiltinMacro(BabaError):
    """Builtin macro failed to compute."""
    raw: str
    message: Exception
    custom: bool

class CustomMacroError(BabaError):
    """User-made macro error."""

class BadPaletteIndex(VariantError):
    """Not in the palette."""


# TODO: more specific errors for this


class BadTilingVariant(VariantError):
    """Variant doesn't match tiling.

    extra args: tiling
    """


class OverlayNotFound(Exception):
    """Variant doesn't match tiling.

    extra args: tiling
    """


class TileNotText(VariantError):
    """Can't apply text variants on tiles."""


class BadLetterVariant(VariantError):
    """Text too long to letterify."""


class UnknownVariant(VariantError):
    """Not a valid variant."""


class TooLargeTile(VariantError):
    """Tile exceeds the limit."""


# === Custom text ===


class TextGenerationError(BabaError):
    """Base class for custom text.

    extra args: text
    """


class BadLetterStyle(TextGenerationError):
    """Letter style provided but it's not possible."""


class TooManyLines(TextGenerationError):
    """Max 1 newline."""


class LeadingTrailingLineBreaks(TextGenerationError):
    """Can't start or end with newlines."""


class BadCharacter(TextGenerationError):
    """Invalid character in text.

    Extra args: mode, char
    """


class CustomTextTooLong(TextGenerationError):
    """Can't fit."""


class ScaleError(VariantError):
    """Can't scale below 0."""


class BadVariant(VariantError):
    """Incorrect syntax."""
