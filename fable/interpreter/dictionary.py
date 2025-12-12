"""
Dictionary module for storing Forth word definitions.

The dictionary is the central data structure in Forth, mapping word names
to their implementations. Each entry contains the code, stack effect,
and documentation for a word.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, List
from difflib import get_close_matches


@dataclass
class DictionaryEntry:
    """A single word definition in the dictionary.
    
    Attributes:
        name: Word name (stored uppercase for case-insensitive lookup)
        code: Either a Python callable (primitive) or a list (compiled Forth)
        immediate: If True, execute during compilation instead of compiling
        stack_effect: Stack effect notation, e.g., "( n1 n2 -- sum )"
        docstring: Human-readable description of the word
        source_location: Optional (file, line) where word was defined
    """
    name: str
    code: Callable | List
    immediate: bool = False
    stack_effect: str = ""
    docstring: str = ""
    source_location: tuple[str, int] | None = None
    
    def is_primitive(self) -> bool:
        """Check if this is a primitive (Python function) word."""
        return callable(self.code)
    
    def is_compiled(self) -> bool:
        """Check if this is a compiled (colon definition) word."""
        return isinstance(self.code, list)


class Dictionary:
    """Forth dictionary storing word definitions.
    
    The dictionary is implemented as a dict for O(1) lookup, but maintains
    insertion order for the WORDS command and FORGET operation.
    
    Word names are stored uppercase for case-insensitive matching.
    
    Example:
        >>> d = Dictionary()
        >>> d.define(DictionaryEntry(name="+", code=add_fn, stack_effect="( n1 n2 -- sum )"))
        >>> entry = d.lookup("+")
        >>> entry.name
        '+'
    """
    
    def __init__(self):
        self._entries: dict[str, DictionaryEntry] = {}
        self._order: list[str] = []  # Maintains definition order
    
    def define(self, entry: DictionaryEntry) -> None:
        """Add or redefine a word in the dictionary.
        
        Args:
            entry: The dictionary entry to add
        """
        name_upper = entry.name.upper()
        entry.name = name_upper  # Normalize to uppercase
        
        if name_upper not in self._entries:
            self._order.append(name_upper)
        
        self._entries[name_upper] = entry
    
    def lookup(self, name: str) -> Optional[DictionaryEntry]:
        """Find a word in the dictionary.
        
        Args:
            name: Word name (case-insensitive)
            
        Returns:
            DictionaryEntry if found, None otherwise
        """
        return self._entries.get(name.upper())
    
    def contains(self, name: str) -> bool:
        """Check if a word exists in the dictionary.
        
        Args:
            name: Word name (case-insensitive)
            
        Returns:
            True if word exists
        """
        return name.upper() in self._entries
    
    def forget(self, name: str) -> bool:
        """Remove a word and all words defined after it.
        
        This is the traditional Forth FORGET behavior.
        
        Args:
            name: Word name to forget
            
        Returns:
            True if word was found and removed
        """
        name_upper = name.upper()
        if name_upper not in self._entries:
            return False
        
        # Find position and remove it and everything after
        try:
            idx = self._order.index(name_upper)
            words_to_remove = self._order[idx:]
            self._order = self._order[:idx]
            for word in words_to_remove:
                del self._entries[word]
            return True
        except ValueError:
            return False
    
    def words(self, pattern: str = "") -> List[str]:
        """List all defined words, optionally filtered.
        
        Args:
            pattern: Optional substring to filter by (case-insensitive)
            
        Returns:
            List of word names in definition order
        """
        pattern_upper = pattern.upper()
        if pattern:
            return [w for w in self._order if pattern_upper in w]
        return list(self._order)
    
    def find_similar(self, name: str, n: int = 3) -> List[str]:
        """Find words similar to the given name.
        
        Used for "did you mean?" suggestions.
        
        Args:
            name: Word to find matches for
            n: Maximum number of suggestions
            
        Returns:
            List of similar word names
        """
        name_upper = name.upper()
        return get_close_matches(name_upper, self._order, n=n, cutoff=0.6)
    
    def see(self, name: str) -> Optional[str]:
        """Decompile a word definition.
        
        Args:
            name: Word name
            
        Returns:
            String representation of the word's definition, or None if not found
        """
        entry = self.lookup(name)
        if not entry:
            return None
        
        if entry.is_primitive():
            return f": {entry.name} ( primitive ) ; {entry.stack_effect}"
        
        if entry.is_compiled():
            # Decompile the threaded code
            body = ' '.join(str(item) for item in entry.code)
            return f": {entry.name} {entry.stack_effect}\n  {body} ;"
        
        return f": {entry.name} ( unknown ) ;"
    
    def __len__(self) -> int:
        return len(self._entries)
    
    def __contains__(self, name: str) -> bool:
        return self.contains(name)
