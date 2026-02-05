import pathlib
import shutil


def remove_path(path: str) -> None:
    if pathlib.Path(path).is_dir():
        shutil.rmtree(path)
    elif pathlib.Path(path).is_file():
        pathlib.Path(path).unlink()


def main() -> None:
    enable_vitest = "{{ cookiecutter.enable_vitest }}".lower() == "yes"
    enable_i18n = "{{ cookiecutter.enable_i18n }}".lower() == "yes"
    license_value = "{{ cookiecutter.license }}"

    if not enable_vitest:
        remove_path("vitest.config.ts")
        remove_path("tests")

    if not enable_i18n:
        remove_path("src/i18n")
        remove_path("locales")

    if license_value == "none":
        remove_path("LICENSE")


if __name__ == "__main__":
    main()
