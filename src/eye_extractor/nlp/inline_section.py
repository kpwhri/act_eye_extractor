import re

from eye_extractor.nlp.character_groups import get_previous_text_to_newline


PERIPHERY_PAT = re.compile(
    r'\b(?:'
    r'peripher(y|al\s+(retina|fundus))'
    r')\b',
    re.I
)


def is_inline_section(match_start: int, text: str, pattern: re.Pattern) -> bool:
    """Determine if a given match start is within a particular in-line section.

    Args:
        match_start: Index of the re.Match start within `text`.
        text: The string to search for an in-line section. Contains the
            given re.Match.
        pattern: A re.Pattern that captures the header of the in-line
            section being searched for.
    Returns:
        A boolean indicating if the given match is within the specified
        in-line section.
    """
    line_text = get_previous_text_to_newline(match_start, text)
    if re.match(pattern, line_text):
        return True
    return False


def is_periphery(match_start: int, text: str) -> bool:
    """Determine if a given match start is within a periphery in-line section.

        Args:
            match_start: Index of the re.Match start within `text`.
            text: The string to search for a periphery section. Contains the
                given re.Match.
        Returns:
            A boolean indicating if the given match is within a periphery
            in-line section.
        """
    return is_inline_section(match_start, text, PERIPHERY_PAT)
