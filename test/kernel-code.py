# For OSP's part B (osp-ops tools/validate.sh app --kind web
# --kernel-code test/kernel-code.py): start, the way a notebook would, the
# servers this image's packages can open, so the record lists their listeners.
#
# Dask (secured by app-jupyter's 50-dask-tls.sh: the address should be tls://).
from distributed import Client, LocalCluster
cluster = LocalCluster(n_workers=1, threads_per_worker=1)
client = Client(cluster)
print("dask", cluster.scheduler_address, client.submit(lambda: 6 * 7).result())

# Every package in requirements.txt imports.
import importlib
mods = ["altair", "bs4", "bokeh", "bottleneck", "cloudpickle", "Cython", "dask", "dill",
        "h5py", "ipympl", "ipywidgets", "jupyterlab_git", "matplotlib", "numba", "numexpr",
        "openpyxl", "pandas", "patsy", "google.protobuf", "tables", "skimage", "sklearn",
        "scipy", "seaborn", "sqlalchemy", "statsmodels", "sympy", "xlrd"]
for m in mods:
    importlib.import_module(m)
print("imports ok:", len(mods))
