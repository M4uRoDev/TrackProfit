from src.utils.config_loader import ConfigLoader

config = ConfigLoader()

test_var = config.get_env_var("TEST_VAR")
print(f"TEST_VAR: {test_var}")