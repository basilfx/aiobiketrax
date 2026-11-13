# Contributing
To contribute to this repository, use GitHub pull-requests to contribute code
to this repository.

A few things to pay attention to:

- Dependencies are managed using [uv](https://docs.astral.sh/uv/). Run
  `uv sync` to set up a development environment.
- Code is linted and formatted using [Ruff](https://docs.astral.sh/ruff/) (run
  `uv run ruff check` and `uv run ruff format`) and type checked using
  [mypy](https://mypy-lang.org/) (run `uv run mypy`).
- Documentation conforms to the
  [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#doc-function-args).
- Your branch is linear and logical.
- Do not edit [models](aiobiketrax/models.py) directly. They have been
  generated using [quicktype](https://quicktype.io/). See the
  `contrib/generator/` folder for more information.
