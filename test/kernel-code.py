# For OSP's part B (osp-ops tools/validate.sh app --kind web
# --kernel-code test/kernel-code.py): start, the way a notebook would, the
# servers this image's packages can open, so the record lists their listeners
# and says, for each, what it is.
#
# Dask (secured by app-jupyter's 50-dask-tls.sh: the address should be tls://).
from distributed import Client, LocalCluster
cluster = LocalCluster(n_workers=1, threads_per_worker=1)
client = Client(cluster)
print("dask", cluster.scheduler_address, client.submit(lambda: 6 * 7).result())

# What each port is, one line per listener: "listener <host:port> <role>".
# validate.sh matches these to the listeners it finds, by port, and probes each.
from urllib.parse import urlparse
def hostport(addr):
    u = urlparse(addr)
    return f"{u.hostname}:{u.port}"
print("listener", hostport(cluster.scheduler_address), "dask-scheduler")
dash = cluster.scheduler_info.get("services", {}).get("dashboard")
if dash:
    print("listener", f"0.0.0.0:{dash}", "dask-dashboard (NEW-19: no login; shows tasks and logs)")
for waddr, w in client.scheduler_info()["workers"].items():
    print("listener", hostport(waddr), "dask-worker")
    if w.get("nanny"):
        print("listener", hostport(w["nanny"]), "dask-nanny")
    for name, port in (w.get("services") or {}).items():
        print("listener", f"127.0.0.1:{port}", f"dask-worker-{name} (NEW-19: /health, /metrics; no login)")
# The kernel's pipe for output from subprocesses (ipykernel's own; a private
# attribute, so "?" if a future ipykernel moves it).
pipe = getattr(getattr(get_ipython().kernel, "iopub_thread", None), "_pipe_port", None)
print("listener", f"127.0.0.1:{pipe}" if pipe else "?:0", "kernel-subprocess-pipe (signed with the kernel's key)")

# Every package in requirements.txt imports.
import importlib
mods = ["altair", "bs4", "bokeh", "bottleneck", "cloudpickle", "Cython", "dask", "dill",
        "h5py", "ipympl", "ipywidgets", "jupyterlab_git", "matplotlib", "numba", "numexpr",
        "openpyxl", "pandas", "patsy", "google.protobuf", "tables", "skimage", "sklearn",
        "scipy", "seaborn", "sqlalchemy", "statsmodels", "sympy", "xlrd"]
for m in mods:
    importlib.import_module(m)
print("imports ok:", len(mods))
