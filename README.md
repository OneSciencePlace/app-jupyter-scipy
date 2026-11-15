# app-jupyter-scipy

JupyterLab with the scientific Python packages of the
[Jupyter Docker Stacks](https://github.com/jupyter/docker-stacks)'
`scipy-notebook` -- pandas, NumPy, SciPy, scikit-learn, matplotlib, Dask and
the rest -- adapted for shared research computing systems: one image that
works at many HPC centers, where many people's sessions run side by side on
the same machines and each stays private to the person who started it.

Coming from the Docker Stacks images? On HPC systems this image runs as an
Apptainer (Singularity) image, not a Docker container, and that changes a few
things you'll see:

- **Who you are.** The session runs as the cluster account that started it --
  your own, or the account the portal uses -- not as `jovyan`. `whoami` and
  file owners show that account.
- **Where your files are.** JupyterLab opens in the session's working
  directory (on a cluster, the job's directory), not `/home/jovyan/work`. Your
  home directory depends on how the app is set up: often a fresh, empty one
  for each session, but a class or your own cluster account may give you a
  persistent one. If you are not sure, save your work in the working
  directory.
- **What the session sees.** It starts with a clean environment and only the
  directories it is given: your cluster shell's settings, loaded modules and
  other directories aren't inside it.
- **The image doesn't change while it runs.** Packages and settings are built
  in when the image is made.

The image is designed for this: it works for whichever account starts it,
writes only into the session's own directories, and assumes no fixed user
name or home directory.

It is also **the example to copy**. To make a Jupyter app with your own
packages, you change a list of package names. You do not need the command
line, Docker, or to know how the image is built.

## Make your own

All of this happens in GitHub's web pages.

1. **Copy this repository.** Open
   [OneSciencePlace/app-jupyter-scipy](https://github.com/OneSciencePlace/app-jupyter-scipy)
   and click **Use this template** > **Create a new repository**. Owner:
   `OneSciencePlace` (ask OSP staff if you cannot choose it). Name it
   `app-jupyter-<what it is for>`, lowercase, words joined by hyphens, for
   example `app-jupyter-genomics`.

2. **List your packages.** In your new repository, open `requirements.txt`
   and click the pencil icon to edit it. One package per line, as
   `name==version`, for example `biopython==1.86`. Find the name and the
   newest version on [pypi.org](https://pypi.org). Delete the lines for
   packages you do not need. Click **Commit changes**.

3. **System packages, only if needed.** If a package's instructions say it
   needs a system library or program (for example "requires libgdal"), add
   its Debian package name to `apt.txt` the same way. Most images need
   nothing here.

4. **Wait for the build.** Open the **Actions** tab: committing started a
   build. It takes 10 to 20 minutes. A green check means your image is ready;
   a red cross means it is not, and why is in the last lines of the failed
   step's log. The usual reasons:
   - *pip could not install requirements.txt*: a version that does not exist,
     or two packages that need different versions of a third. The log names
     them; change a version and commit again.
   - *not a Debian package name*: a typo in `apt.txt`.
   - *needs a different version of the Jupyter software*: one of your
     packages wants another JupyterLab. Pick a version of it that accepts this
     one, or ask OSP staff for help.

5. **Make a release.** Click **Releases** > **Draft a new release**. Under
   *Choose a tag*, type `v1.0.0` and pick *Create new tag on publish*. Click
   **Publish release**. This builds the version that goes into use,
   `ghcr.io/onescienceplace/<your repository>-sif:1.0.0`. For later changes,
   release `v1.0.1` for a small fix, `v1.1.0` for added packages, `v2.0.0` if
   notebooks written for the old version may no longer work.

**Help is available at every step.** OSP staff can help you choose packages,
work out why a build failed, test your image, or verify and validate it for
use on a cluster. Send them your repository's name and what you need.

Leave the other files as they are. The `Dockerfile` does not need editing:
everything about the session comes from the base image, `app-jupyter`.

## Rules your image inherits

Some things come with the base image, `app-jupyter`, and stay the same
whatever packages you list. They are what lets many people's sessions share
a machine safely. The build checks them, and stops with a message if one is
broken:

- **Only the person who started the session gets in.** JupyterLab sits
  behind a gate that asks for the session's own token.
- **The Jupyter software stays at the tested versions** (JupyterLab 4.6.3
  and its parts). A package that needs another version stops the build (the
  third reason in step 4).
- **Packages come from the image only.** Kernels ignore packages installed
  in a home directory (with `pip install --user`, or left in `~/.local` from
  earlier work on the cluster), so a notebook finds the same packages in
  every session, for everyone. To add a package, add it to
  `requirements.txt`.
- **No debugger in the kernel.** The JupyterLab debugger panel is not
  available.
- **Programs run with your own rights.** None can gain more, including ones
  installed from `apt.txt`.
- **The base image's own files stay as they are.** If a change replaces one,
  the build stops with "files of app-jupyter were changed".
- **Servers a notebook starts are secured where possible.** Dask's cluster
  is set up for each session (see "What to know when using it").

If one of these gets in the way of what you need, ask OSP staff: there is
often another way to do it.

## What is in it, compared with scipy-notebook

| | |
|---|---|
| Python packages | The same list (`requirements.txt`), pinned to versions that install together. Python 3.14. |
| Command-line tools | git, curl, nano, vim, less, unzip (`apt.txt`), and a terminal in JupyterLab. |
| PDF export | pandoc and TeX Live: **File > Save and Export Notebook As > PDF** works. |
| LaTeX in plots, animations | dvipng and cm-super (matplotlib's `usetex`), ffmpeg. |
| Compilers | build-essential, for Cython. |
| Installing packages | From PyPI with pip, at build time. No conda or mamba, so conda-only packages are not available. |
| Not included | The classic Notebook interface, JupyterHub's single-user server. |

## What to know when using it

- **Save in the working directory** (see above), or in your home directory
  if yours is a persistent one. Anything saved elsewhere is gone when the
  session ends.
- **Add packages to the image, not to a running session.** List them in
  `requirements.txt` and make a new release. The image is read-only while it
  runs, and kernels ignore packages installed into a home directory (see
  "Rules your image inherits").
- **Dask works as usual, and is secured for you.** `Client()` and
  `LocalCluster()` start a cluster as in any tutorial. Behind the scenes the
  base image makes a certificate for each session, so no other session on the
  same machine can connect to your cluster. One exception: Dask's dashboard
  (port 8787) has no login, and anyone who can reach the machine over the
  network can view it. It shows
  your tasks and logs, not your data, and cannot run code. If you do not need
  it, start the cluster with `LocalCluster(dashboard_address=None)`.
- **Saved outputs need a re-run in a new session**: charts and widgets
  reappear when their cells are run again (app-jupyter's README explains why).
- **The session ends** when you choose **File > Shut Down**, or when the
  job's time runs out.

## Run it yourself

Through the portal there is nothing to run. To try it on your own machine
with Docker, or on a cluster with Apptainer, as in app-jupyter's README:

```bash
export OSP_APP_TOKEN=$(openssl rand -hex 32)

# Docker. -e OSP_APP_TOKEN with no "=value" copies it from your environment.
docker run --rm --user "$(id -u):$(id -g)" \
  -p 127.0.0.1:8888:8888 -v "$PWD:/data" \
  -e OSP_APP_PORT=8888 -e OSP_APP_BIND=0.0.0.0 -e OSP_APP_TOKEN \
  ghcr.io/onescienceplace/app-jupyter-scipy:latest

# Apptainer, under the OSP interactive run profile.
apptainer pull oras://ghcr.io/onescienceplace/app-jupyter-scipy-sif:latest   # production pins <version>@sha256:<digest>
mkdir -p tmp
export APPTAINERENV_OSP_APP_TOKEN="$OSP_APP_TOKEN"
apptainer run \
  --contain --pid --ipc --cleanenv --no-mount bind-paths,cwd \
  --pwd "$PWD" --bind "$PWD:$PWD" \
  --env OSP_APP_PORT=8888 --env TMPDIR="$PWD/tmp" \
  app-jupyter-scipy-sif_latest.sif
```

Then open `http://127.0.0.1:8888/?token=<the token>`. The token is never put
on a command line, where other users of the machine could see it. On a Mac
with Apple Silicon a session cannot start (the image is for Intel/AMD
machines; see app-jupyter's README).

## For OSP staff: validating an image

Part B, in `osp-ops`, with the script that starts what this image ships:

```bash
bash tools/validate.sh app --kind web \
  --image ghcr.io/onescienceplace/app-jupyter-scipy-sif:<tag> \
  --kernel-code test/kernel-code.py --by "<your name>"
```

`test/kernel-code.py` starts a Dask cluster, imports every package, and says
which port is which (`listener <host:port> <role>` lines). `validate.sh`
matches those to the listeners it finds and probes each from outside the
session; the record gets a table. Expect: the Dask scheduler, nanny and worker
refusing a client without the session's certificate (app-jupyter's
`50-dask-tls.sh`); the dashboard on `0.0.0.0:8787` and each worker's
`/health` and `/metrics` endpoint answering without a login (WARN; NEW-19,
open); the kernel's own pipe (ZeroMQ, INFO). For an image made from this one,
copy `test/kernel-code.py` and keep what it ships. `test/` is not part of the
image.

## Files

| File | Purpose |
|---|---|
| `requirements.txt` | Python packages. **The file to change.** |
| `apt.txt` | System packages, Debian names. Change only if a package needs one. |
| `Dockerfile` | Three steps on the base image `app-jupyter`, pinned by tag and digest. No need to edit. |
| `test/kernel-code.py` | For OSP staff's validation (above). |
| `OVERVIEW.md` | What the app is, in plain language, for its users. |
| `.github/workflows/build-and-push.yml` | Builds the image and its `.sif` on every commit and release. Do not edit. |

Advanced: an image may also run its own commands at the start of every
session (`session.d/`), and add its own build steps. app-jupyter's README,
"Build your own Jupyter image on this one", and its `osp/session.d/README.md`
explain both; app-object-detection-jupyter uses them.
