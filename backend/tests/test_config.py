import os
import subprocess
import sys
import textwrap


def test_settings_database_url_uses_data_dir(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    code = textwrap.dedent(
        f"""
        from pathlib import Path

        from app.config import DATA_DIR, settings

        expected_url = "sqlite:///{data_dir}/database.sqlite"
        assert DATA_DIR == Path(r"{data_dir}")
        assert settings.database_url == expected_url
        """
    )

    env = os.environ.copy()
    env["DATA_DIR"] = str(data_dir)
    env["DATABASE_URL"] = "sqlite:///./data/database.sqlite"
    result = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
