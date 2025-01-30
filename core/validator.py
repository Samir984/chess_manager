from django.core.exceptions import ValidationError


def validate_file_size(file:int):
    max_file_size = 4
    if file.size > max_file_size * 1024 * 1024: # type: ignore
        ValidationError(f"file size can't be larger then {max_file_size} MB")
