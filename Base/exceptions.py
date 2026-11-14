'''Custom exceptions'''


class InvalidDifficultyError(ValueError):
    '''Raised when a requested difficulty is outside the supported range.'''


class InvalidWaveDataError(ValueError):
    '''Raised when a wave entry or path point has an invalid structure.'''


class UnknownDefinitionError(KeyError):
    '''Raised when an enemy or tower ID is not in its dictionary.'''


class InvalidTowerConfigurationError(ValueError):
    '''Raised when a tower definition uses an unsupported or invalid type.'''
