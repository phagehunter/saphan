"""A small JSON Schema checker (draft 2020-12 subset) with no dependencies.

It understands exactly the keywords used in content/schema/phrase.schema.json:
type, required, properties, additionalProperties, enum, pattern, minLength,
maxLength, minimum, items, $ref (local #/$defs only), default. Continuous
integration also runs the full `check-jsonschema` tool; this file exists so
the checks run on a laptop with nothing installed.
"""
from __future__ import annotations

import re
from typing import Any

TYPE_NAMES = {
    "object": dict, "array": list, "string": str, "integer": int,
    "number": (int, float), "boolean": bool, "null": type(None),
}


def _type_ok(value: Any, tname: str) -> bool:
    if tname == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if tname == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if tname == "boolean":
        return isinstance(value, bool)
    return isinstance(value, TYPE_NAMES[tname])


def validate(instance: Any, schema: dict, root: dict | None = None, path: str = "$") -> list[str]:
    root = root if root is not None else schema
    errors: list[str] = []
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return [f"{path}: unsupported $ref {ref}"]
        target: Any = root
        for part in ref[2:].split("/"):
            target = target[part]
        return validate(instance, target, root, path)

    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(instance, t) for t in types):
            return [f"{path}: expected type {'/'.join(types)}, got {type(instance).__name__}"]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not one of {schema['enum']}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match /{schema['pattern']}/")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")

    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required key '{req}'")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{path}: unexpected key '{key}'")
        for key, sub in props.items():
            if key in instance:
                errors.extend(validate(instance[key], sub, root, f"{path}.{key}"))

    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            errors.extend(validate(item, schema["items"], root, f"{path}[{i}]"))

    return errors
