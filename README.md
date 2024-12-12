# Prerequisites

Install python3.12 and poetry

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv
curl -sSL https://install.python-poetry.org | python3.12 -
```

Add
`export PATH="/home/supra/.local/bin:$PATH"`
to your `~/.bashrc` file and execute

`source ~/.bashrc`

# Create environment

```bash
python3.12 -m venv venv
source venv/bin/activate
poetry install
```

# Usage

Instantiate RPCExporter, providing `config_source = "fromEnv"` for reading the configuration variables from the environment or, to read the configuration variables from file, use `config_source = "fromFile"` alongside `config_file = <path to your config>` .

```python


class SolanaExporter(RPCExporter):
    def __init__(
        self,
        config_source: str,
        config_file: Optional[str] = None
    ):
        super().__init__(
            network="solana",
            config_source=config_source,
            config_file=config_file,
        )

...


if __name__ == "__main__":
    configFile: str | None = os.getenv("EXPORTER_ENV")
    print(f"starting solana exporter -- config {configFile}")
    exporter = SolanaExporter(config_source="fromFile", config_file=configFile)
    exporter.start_exporter()


```

For detailed example implementations for Solana and Supra RPCs, please refer to the repositories:
https://github.com/supra-protocol/supra-rpc-exporter
