from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:

    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map

test:Mapping = {"a":{"b":"value"}}

print(test["a"]["b"])

nested_map = {"a": {"b": {"c": 1}}} 
if __name__ == "__main__":  
    print(access_nested_map(nested_map, ["a", "b", "c"])) 
