# Building Permits Server

## Dev Set-Up

From `$SCALE_HOME/packages/dune/product-approvals-ui/`, run the following commands:

```bash
conda create -n product-approvals-ui python=3.9
```

```bash
conda activate product-approvals-ui
```

```bash
pip install -r requirements.txt
```

```bash
pip install -r ../requirements-dev.txt
```

```bash
pip install -e .
```

```bash
pre-commit install
```

## Frontend Set-Up

**Note: Add `INTERNAL_API_KEY=fire_products` to your `.env` file.**

(recommended) For iteration with Docker, run from this directory:
```bash
make build && make run && make logs
```

For local iteration (with theming), run `streamlit run src/app.py --theme.primaryColor="c78bc4" --theme.base="dark"` from this directory


## Deployment

Refer to permits-api README for more information on setup.

Run `make deploy` from this directory.

