# Design Patterns Adventure Game

![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-success)
![First Timer Friendly](https://img.shields.io/badge/First%20Timer-friendly-informational)
![License MIT](https://img.shields.io/badge/license-MIT-success)

## Installation

### Graphviz

Make sure to [install graphviz from the official website](https://www.graphviz.org/download/)

For Mac users, this might be `brew install graphviz`, while Windows may need to download the latest `.exe` installer from the site or [use chocolatey](https://community.chocolatey.org/packages/graphviz)

### Python and Poetry

If you already have a compatible version of Python and poetry installed, you can get started right away and skip to "Game Play" below.

The recommended installation is with `asdf` on Linux, Mac, and Windows (through WSL). For Windows native, see the recommended solutions further below

#### Mac, Linux, and Windows Subsystem for Linux (WSL)

`asdf` is a general purpose version manager and we use it to ensure consistency between setups. To install `asdf`, follow the [installation guide](https://asdf-vm.com/guide/getting-started.html)

Once you have installed `asdf`, there are a few additional steps

```sh
asdf plugin-add python https://github.com/asdf-community/asdf-python.git
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

# Make sure you are within the project directory and then run:
cd community-rpg
asdf install

# Then install the project to check that setup worked
poetry install
```

#### Windows Native

1. There are multiple ways to install Python on Windows if you don't have it already. Our recommend approach is to install Chocolatey and run `choco install python` ([link](https://community.chocolatey.org/packages/python)). See the [guide for installing and configuring chocolatey here](https://chocolatey.org/install).
1. Next, install `poetry` following the [official poetry installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer). We recommend using `pipx` ([pipx guide](https://pypa.github.io/pipx/installation/)), but installing method with powershell is the fastest way to get started.
1. To test that installation succeeded, run `poetry install` in the game directory before proceeding.

## Game Play

> Make sure you go through the installation steps first!

### Quick Start

Let's launch the game UI and make the first code changes!

```sh
> poetry shell
(shell) doit play
````

This will open the game window where you can walk around using the keys `W`, `A`, `S`, and `D` and pick up items by pressing `E`.

Press an item's inventory number to equip it (tool) or consume it (food). If the item is a tool, left-click to activate it.

To quit the game, click the red "x" icon to close or use the keyboard shortcut `Ctrl C`.

> Note: you may have seen it above, but we will use the convention of `>` to indicate a normal shell prompt and `(shell)` to indicate when the command must be run after running `poetry shell` at least once. Alternatively, you could use `poetry run doit play`, but using `poetry shell` first is more convenient.

## Shortcuts

```sh
# Run all of the default tasks
(shell) doit --continue
(shell) doit list
# Tasks can also be run one-by-one
(shell) doit run format
(shell) doit run test
(shell) doit run check
(shell) doit run build_diagrams
# Or you can use a watcher utility that will re-run tests on changes
(shell) doit watch_changes

# When ready to start the next task, call:
# (FYI: This hasn't been implemented yet!)
(shell) doit next_task
```

## Assets

* [Pipoya Free RPG Tileset 32x32](https://pipoya.itch.io/pipoya-rpg-tileset-32x32)
* [Pipoya Free RPG Character Sprites 32x32](https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32)
* [Kenney Input Prompts Pixel 16x16](https://kenney.nl/assets/input-prompts-pixel-16)
* [Gentle Cat Studios Pixel 16x16](https://gentlecatstudio.itch.io/rpg-items)