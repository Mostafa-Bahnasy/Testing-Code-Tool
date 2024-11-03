from cx_Freeze import setup, Executable

setup(
    name="MyApp",
    version="0.1",
    description="My Application",
    executables=[Executable("./Main.py")]
)
