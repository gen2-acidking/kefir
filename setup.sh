#!/bin/bash

##################################################################
# Kefir uninstall Script
# author: gen2acidking 
##################################################################

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' 

INSTALL_DIR="$HOME/.kefir"
VENV_DIR="$INSTALL_DIR/venv"

echo -e "${YELLOW}Setting up Kefir...${NC}"

if ! command -v xdotool &> /dev/null; then
    echo -e "${RED}Error: xdotool is required but not installed.${NC}"
    echo -e "Please install it with: sudo apt-get install xdotool (Debian/Ubuntu)"
    echo -e "or: sudo dnf install xdotool (Fedora)"
    echo -e "or: sudo pacman -S xdotool (Arch)"
    exit 1
fi

mkdir -p "$INSTALL_DIR"
echo -e "${YELLOW}Copying files to $INSTALL_DIR...${NC}"
cp kefir.py "$INSTALL_DIR/"
cp finnish_ascii_map.json "$INSTALL_DIR/" 2>/dev/null || echo -e "${YELLOW}Warning: finnish_ascii_map.json not found, you'll need to provide it later.${NC}"
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv "$VENV_DIR"
# Activate virtual environment and install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
source "$VENV_DIR/bin/activate"
pip install pynput
echo -e "${YELLOW}Creating wrapper script...${NC}"

cat > "$INSTALL_DIR/kefir" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.kefir"
VENV_DIR="$INSTALL_DIR/venv"
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/kefir.py" "$@"
EOF

chmod +x "$INSTALL_DIR/kefir"

if [ -w /usr/local/bin ]; then
    echo -e "${YELLOW}Creating symlink in /usr/local/bin...${NC}"
    sudo ln -sf "$INSTALL_DIR/kefir" /usr/local/bin/kefir
    echo -e "${GREEN}Kefir installed successfully!${NC}"
    echo -e "You can now run it with: ${YELLOW}kefir --start${NC}"
else
    echo -e "${YELLOW}Adding alias to .bashrc...${NC}"
    # Check if the alias already exists
    if grep -q "alias kefir=" "$HOME/.bashrc"; then
        echo -e "${YELLOW}Alias already exists in .bashrc${NC}"
    else
        echo "alias kefir='$INSTALL_DIR/kefir'" >> "$HOME/.bashrc"
        echo -e "${GREEN}Alias added to .bashrc${NC}"
    fi

    if [ -f "$HOME/.zshrc" ]; then
        if grep -q "alias kefir=" "$HOME/.zshrc"; then
            echo -e "${YELLOW}Alias already exists in .zshrc${NC}"
        else
            echo "alias kefir='$INSTALL_DIR/kefir'" >> "$HOME/.zshrc"
            echo -e "${GREEN}Alias added to .zshrc${NC}"
        fi
    fi
    
    echo -e "${GREEN}Kefir installed successfully!${NC}"
    echo -e "Please restart your terminal or run: ${YELLOW}source ~/.bashrc${NC}"
    echo -e "Then you can use: ${YELLOW}kefir --start${NC}"
fi

echo -e "${GREEN}Setup complete!${NC}"
echo -e "Usage:"
echo -e "  ${YELLOW}kefir --start${NC}   - Start Kefir"
echo -e "  ${YELLOW}kefir --stop${NC}    - Stop Kefir"
echo -e "  ${YELLOW}kefir --status${NC}  - Check if Kefir is running"
echo -e "  ${YELLOW}kefir --help${NC}    - Show this help message"
