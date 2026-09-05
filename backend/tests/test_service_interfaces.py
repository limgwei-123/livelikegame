import ast
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1] / "app"


def _service_modules() -> list[tuple[Path, Path]]:
    return [
        (interface_path, interface_path.with_name("service.py"))
        for interface_path in APP_ROOT.rglob("interfaces.py")
        if interface_path.with_name("service.py").exists()
    ]


def _public_methods(path: Path) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    methods: dict[str, ast.FunctionDef] = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                methods[item.name] = item

    return methods


def _argument_names(method: ast.FunctionDef) -> list[str]:
    return [arg.arg for arg in method.args.args]


def test_service_interfaces_match_service_method_parameters():
    mismatches: list[str] = []

    for interface_path, service_path in _service_modules():
        interface_methods = _public_methods(interface_path)
        service_methods = _public_methods(service_path)

        for method_name, interface_method in interface_methods.items():
            service_method = service_methods.get(method_name)
            if service_method is None:
                mismatches.append(f"{interface_path}: {method_name} missing in service")
                continue

            interface_args = _argument_names(interface_method)
            service_args = _argument_names(service_method)
            if interface_args != service_args:
                mismatches.append(
                    f"{interface_path}: {method_name} args "
                    f"{interface_args} != {service_args}"
                )

    assert mismatches == []


def test_service_interfaces_have_complete_annotations():
    missing_annotations: list[str] = []

    for interface_path, _service_path in _service_modules():
        interface_methods = _public_methods(interface_path)

        for method_name, method in interface_methods.items():
            for arg in method.args.args:
                if arg.arg == "self":
                    continue
                if arg.annotation is None:
                    missing_annotations.append(
                        f"{interface_path}: {method_name}.{arg.arg} missing type"
                    )

            if method.returns is None:
                missing_annotations.append(
                    f"{interface_path}: {method_name} missing return type"
                )

    assert missing_annotations == []
