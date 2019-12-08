from .action_scheme import ActionScheme
from .pair_criteria_size_actions import PairCriteriaSizeActions


_registry = {
    'pair_criteria_size': PairCriteriaSizeActions,
}


def get(identifier: str) -> ActionScheme:
    """Gets the `ActionScheme` that matches with the identifier.

    Arguments:
        identifier: The identifier for the `ActionScheme`

    Raises:
        KeyError: if identifier is not associated with any `ActionScheme`
    """
    if identifier not in _registry.keys():
        raise KeyError(f'Identifier {identifier} is not associated with any `ActionScheme`.')

    return _registry[identifier]()
