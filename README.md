# kefir

**key finnish replace** — a minimal X11-only CLI tool that enables seamless writing of Finnish umlauts (`ä`, `ö`) using a regular ASCII keyboard.

## Installation

```bash
git clone https://github.com/gen2acidking/kefir.git
cd kefir
chmod +x install.sh
./install.sh
```

After installation, the `kefir` command will be available globally.

## Usage

Start the tool with:

```bash
kefir --start
```

- When you type a Finnish root word (e.g. `paiva`), it will be automatically replaced with the correct form (`päivä`) upon pressing space.
- After correction, all typed `a` and `o` characters will be replaced with `ä` and `ö` until you press space again.
- To **reject** the last correction (e.g. when it wrongly replaced a word), hit **three spaces in a row** to undo.

## Dependencies

**System-wide:**
- `xdotool` (required for simulating keystrokes in X11)
- `python3` 

**Python:**
- `pynput` (pulled in with pip at setup) 

All other dependencies are handled automatically by the installer.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
